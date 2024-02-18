import argparse
import io
import os
import re
import traceback
import urllib.parse
from datetime import datetime, timedelta

import numpy
import pandas as pd
import requests
import simplekml
from bs4 import BeautifulSoup
from ceotr_file import fsm
from sensor_tracker_client import sensor_tracker_client as stc

HOST = "prod.ceotr.ca"
stc.HOST = "https://{}/sensor_tracker/".format(HOST)
LON_DEG = 'Lon (deg)'
LAT_DEG = 'Lat (deg)'
LATITUDE = 'latitude'
LONGITUDE = 'longitude'
GROUND_SPEED = 'Ground Speed(kt)'
CURRENT_HEADING = 'Current Heading (deg)'
TIMESTAMP = 'timestamp'
TIME = 'time'
POG = 'POG (deg)'
CURRENT_SPEED = 'Current Speed (kt)'
UNIT_METER_PER_SEC = "m/s"
KEEP_DIGIT = 2
NEW_WAVE_URL = "https://data.ceotr.ca/wave_realtime_telemetry_for_kml/"
WAVE_GLIDER_TELEMETRY_PATTERN = 'https://data.ceotr.ca/wave_realtime_telemetry_for_kml/m{}-{}-Telemetry 6 Report.csv'

TELEMETRY_FILE_FORMAT = 'm{}-{}-Telemetry 6 Report.csv'
TELEMETRY_REGEX = r'm\d+_.+-Telemetry 6 Report.csv'
TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
# the frequency to select the show point
SELECT_INTERVAL = 1
KML = "kml"
REGEX_DOMAIN_PATH = r'[^:]*://([^/]*)(.*)'
RES_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/output/wave"
DATA_PATH = "/home/ceotr/resource/wgms_extractor/data2/realtime_telemetry_for_kml"
USER = "ceotr"
CEOTR_PROD_SERVER = "ceotr_prod_server"
fsm.load(HOST, USER, controller_tag=CEOTR_PROD_SERVER)


def covert_kt_to_ms(speed_in_kt):
    return speed_in_kt * 0.51444444444


def friendly_timestamp(raw_timestamp):
    if isinstance(raw_timestamp, str):
        return raw_timestamp
    if isinstance(raw_timestamp, numpy.int64):
        date = datetime.fromtimestamp(raw_timestamp / 1e3)
        return date.strftime(TIME_FORMAT)
    return raw_timestamp


class WaveGliderKml:
    """
    Wave glider kml object is for KML file generation
    """
    LOOK_AT_RANGE = 100000
    ALTITUDE_MODE = simplekml.GxAltitudeMode.relativetoseafloor
    GLIDER_PATH_NAME = "Glider Path"

    def __init__(self, glider_name):
        self.kml = simplekml.Kml()
        self.glider_name = glider_name
        self.kml.document.name = glider_name
        self.start_time = None

    def generate_path_point(self, coords):
        path_points_folder = self.kml.newfolder(name=self.GLIDER_PATH_NAME)
        path_points_folder.newlinestring(name=self.start_time,
                                         coords=coords)

    def generate_current_points(self, currents_point):
        """
        Generate points for currents
        """
        current_points_folder = self.kml.newfolder(name="currents")
        for coord in currents_point:
            speed = "N/A"
            if coord[CURRENT_SPEED]:
                speed = round(covert_kt_to_ms(coord[CURRENT_SPEED]), KEEP_DIGIT)
            pnt = current_points_folder.newpoint(
                name="{} {}".format(speed, UNIT_METER_PER_SEC),
                coords=[(coord[LON_DEG], coord[LAT_DEG])],
                visibility=0)
            # the config of label style
            pnt.style.labelstyle.color = 'aa00ff00'
            pnt.style.labelstyle.scale = 0.6
            # the config of icon style
            pnt.style.iconstyle.heading = coord[CURRENT_HEADING]
            pnt.style.iconstyle.hotspot.x = "32"
            pnt.style.iconstyle.hotspot.xunits = "pixels"
            pnt.style.iconstyle.hotspot.y = "1"
            pnt.style.iconstyle.hotspot.yunits = "pixels"
            pnt.style.iconstyle.scale = 0.4
            pnt.style.iconstyle.color = 'aa00ff00'
            pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/arrow.png'

    def generate_showing_point(self, subset_list):
        show_points_folder = self.kml.newfolder(name="show points")
        l = len(subset_list) - 1

        def is_last_pint(i, length_of_list):
            return i == length_of_list

        for index, subset in enumerate(subset_list):
            gs_str = subset.get(GROUND_SPEED, None) and round(subset[GROUND_SPEED], KEEP_DIGIT) or 'N/A'
            if is_last_pint(index, l):
                pnt = show_points_folder.newpoint(
                    name="Latest Position: {}".format(friendly_timestamp(subset[TIMESTAMP])),
                    coords=[(subset[LON_DEG], subset[LAT_DEG])],
                    visibility=0,
                    description='<![CDATA[<h4>{} UTC</h4><p><b>Speed over groud</b>: '
                                '{} kt<br /><b>Path over ground:  '
                                '</b>{} deg<br /></p>]]>'.format(
                        friendly_timestamp(subset[TIMESTAMP]), gs_str, subset[POG]))
                pnt.iconstyle.scale = 1.2
                pnt.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/paddle/ltblu-diamond.png'
            else:
                pnt = show_points_folder.newpoint(name=friendly_timestamp(subset[TIMESTAMP]),
                                                  coords=[(subset[LON_DEG], subset[LAT_DEG])],
                                                  visibility=0,
                                                  description='<![CDATA[<h4>{} UTC</h4><p><b>Speed over groud</b>: '
                                                              '{} kt<br /><b>Path over ground:  '
                                                              '</b>{} deg<br /></p>]]>'.format(
                                                      friendly_timestamp(subset[TIMESTAMP]), gs_str, subset[POG]))
                pnt.iconstyle.scale = 0.6
                pnt.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/open-diamond.png'
            pnt.lookat.latitude = subset[LAT_DEG]
            pnt.lookat.longitude = subset[LON_DEG]
            pnt.lookat.altitude = 0
            pnt.lookat.heading = 0
            pnt.lookat.tilt = 0
            pnt.lookat.range = self.LOOK_AT_RANGE
            pnt.lookat.altitudemode = simplekml.AltitudeMode.relativetoground
            pnt.lookat.gxaltitudemode = simplekml.GxAltitudeMode.relativetoseafloor
            pnt.style.labelstyle.scale = 0.4
            pnt.balloonstyle.text = "$[description]"

    def save(self, file_path):
        self.kml.save(file_path)


class WaveGliderKmlFactory:
    """
    Factory class for generate a Wave glider kml object
    """

    def __init__(self, io_string, glider_name):
        # an io_string contains csv file or it could be a path of the csv file
        self.io_string = io_string
        self.df = pd.read_csv(io_string)
        self._selected_df = None
        self.glider_name = glider_name
        self.wave_xml_obj = WaveGliderKml(self.glider_name)
        self.lat_key = LAT_DEG in self.df.columns and LAT_DEG or LATITUDE
        self.lon_key = LON_DEG in self.df.columns and LON_DEG or LONGITUDE
        self.time_key = TIMESTAMP in self.df.columns and TIMESTAMP or TIME

    @property
    def select_a_sub_point_set(self, select_interval=SELECT_INTERVAL):
        if self._selected_df is None:
            first_timestamp = None
            next_timestamp = None
            subset_index = []
            length = len(self.df.index)
            is_last = False
            if length > 0:
                for index, row in self.df.iterrows():
                    if isinstance(row[self.time_key], str):
                        current_timestamp = datetime.strptime(row[self.time_key], TIME_FORMAT)
                        if first_timestamp is None:
                            next_timestamp = current_timestamp + timedelta(hours=select_interval)
                            subset_index.append(index)
                            first_timestamp = False
                        else:
                            if current_timestamp >= next_timestamp:
                                subset_index.append(index)
                                next_timestamp = current_timestamp + timedelta(hours=select_interval)
                                if index == length - 1:
                                    is_last = True
                if not is_last:
                    subset_index.append(length - 1)
                if len(subset_index) > 0:
                    try:
                        self._selected_df = self.df.iloc[subset_index]
                    except:
                        print("lol")
        return self._selected_df

    def generate(self):
        """Generate wave xml object, this should be the function called from other obj"""
        self.wave_xml_obj.name = self.glider_name
        if TIMESTAMP in self.df and len(self.df.get(TIMESTAMP)) > 0:
            self.wave_xml_obj.start_time = friendly_timestamp(self.df.get(TIMESTAMP)[0])
        self.generate_glider_path()
        self.generate_showing_points()
        self.generate_glider_current()
        return self.wave_xml_obj

    def generate_glider_path(self):
        self.wave_xml_obj.generate_path_point(self.generate_coords_from_dataframe(self.df))

    def generate_glider_current(self):
        self.wave_xml_obj.generate_current_points(self.generate_subset_list_for_currents(self.select_a_sub_point_set))

    def generate_showing_points(self):
        self.wave_xml_obj.generate_showing_point(
            self.generate_subset_list_for_showing_points(self.select_a_sub_point_set))

    def generate_coords_from_dataframe(self, df):
        coords = []
        for index, row in df.iterrows():
            coords.append((row[self.lon_key], row[self.lat_key]))
        return coords

    def generate_subset_list_for_showing_points(self, df):
        subset = []
        if df is not None:
            for index, row in df.iterrows():
                item = {
                    TIMESTAMP: friendly_timestamp(row[self.time_key]),
                    LON_DEG: row[self.lon_key],
                    LAT_DEG: row[self.lat_key],
                    GROUND_SPEED: row.get(GROUND_SPEED, None),
                    POG: row.get(POG, None)
                }
                subset.append(item)
        return subset

    def generate_subset_list_for_currents(self, df):
        subset = []
        if df is not None:
            for index, row in df.iterrows():
                item = {
                    TIMESTAMP: friendly_timestamp(row[self.time_key]),
                    LON_DEG: row[self.lon_key],
                    LAT_DEG: row[self.lat_key],
                    CURRENT_SPEED: row.get(CURRENT_SPEED, None),
                    CURRENT_HEADING: row.get(CURRENT_HEADING, None)
                }
                subset.append(item)
        return subset


def get_current_wave_glider_deployment():
    """
    Get glider deployment
    :return:
    """
    wave_data = stc.deployment.get({"model": "wave", "how": "contains", "depth": 2}).dict
    wave_mission_data = []
    for item in wave_data:
        wave_deployment_item = dict()
        if item["start_time"] and not item["end_time"]:
            wave_deployment_item["start_time"] = item["start_time"]
            wave_deployment_item["end_time"] = item["end_time"]
            wave_deployment_item["platform_name"] = item["platform"]["name"]
            wave_deployment_item["deployment_number"] = item["deployment_number"]
            wave_deployment_item["model"] = item["platform"]["platform_type"]["model"]
            wave_mission_data.append(wave_deployment_item)
    return wave_mission_data


def generate_kml_for_live_wave_glider_mission():
    """generate kml files for live wave glider mission"""
    current_wave_deployment_dict = get_current_wave_glider_deployment()
    saved_xml_path = []
    for wave_obj in current_wave_deployment_dict:
        platform_name = re.sub(r'\s+', '_', wave_obj["platform_name"])
        file_name = TELEMETRY_FILE_FORMAT.format(wave_obj["deployment_number"], platform_name)
        remote_file_path = os.path.join(DATA_PATH, file_name)
        with open(remote_file_path) as f:
            wave_glider_xml_factory = WaveGliderKmlFactory(f, wave_obj["platform_name"])
        wave_glider_xml_object = wave_glider_xml_factory.generate()
        try:
            os.makedirs(RES_PATH)
        except FileExistsError:
            # not need to raise, if file already exists
            pass
        # output kml path and name
        file_path = os.path.join(RES_PATH,
                                 "m{}_{}_{}.kml".format(wave_obj["deployment_number"], wave_obj["platform_name"],
                                                        wave_obj["start_time"].split()[0]))
        wave_glider_xml_object.save(file_path)
        saved_xml_path.append(file_path)


def generate_temp_kml_for_all_wave_glider_missions():
    """generate historical kml files for track ingestion"""
    folder_url = NEW_WAVE_URL
    domain, path = re.match(REGEX_DOMAIN_PATH, folder_url).group(1, 2)
    page = requests.get(folder_url).content
    soup = BeautifulSoup(page, "html.parser")
    csv_links = []
    saved_xml_path = []

    for link in soup.findAll('a'):
        href = link.get('href')
        if re.match(TELEMETRY_REGEX, href):
            if domain in href:
                csv_links.append(href)
            elif href[0] == '/':
                csv_links.append(urllib.parse.urljoin(domain, href))
            else:
                csv_links.append(urllib.parse.urljoin(folder_url, href))

    for csv_link in csv_links:
        file_name = csv_link.split('/')[-1]
        print("Parsing {}".format(file_name))
        platform_name = file_name.split('_')[1].split('-Telemetry')[0]
        deployment_number = file_name.split('_')[0][1:]
        # output kml path and name
        file_path = os.path.join(RES_PATH, "m{}_{}.telemetry.gps.kml".format(deployment_number, platform_name))

        if not os.path.exists(file_path):
            url = WAVE_GLIDER_TELEMETRY_PATTERN.format(deployment_number, platform_name)
            s = requests.get(url).content
            wave_glider_xml_factory = WaveGliderKmlFactory(io.StringIO(s.decode('utf-8')), platform_name)
            wave_glider_xml_object = wave_glider_xml_factory.generate()

            try:
                os.makedirs(RES_PATH)
            except FileExistsError:
                # not need to raise, if file already exists
                pass

            wave_glider_xml_object.save(file_path)
            saved_xml_path.append(file_path)
            print("Wrote {}".format(file_path))
        else:
            print("Skipping {}, already done".format(file_name))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate simple KMLs from ERDDAP datasets")
    parser.add_argument('--purpose', dest="purpose", default="live_missions",
                        help="determines the format and which ")

    try:
        args = parser.parse_args()
        if args.purpose == "live_missions":
            generate_kml_for_live_wave_glider_mission()
        elif args.purpose == "temp_track":
            generate_temp_kml_for_all_wave_glider_missions()
        else:
            generate_kml_for_live_wave_glider_mission()

    except Exception as e:
        print(traceback.print_exc())
        parser.print_help()
        exit(1)
