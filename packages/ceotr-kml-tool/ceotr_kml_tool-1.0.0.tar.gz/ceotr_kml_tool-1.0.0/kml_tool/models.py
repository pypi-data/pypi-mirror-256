from dateutil.parser import parse
import fastkml.kml
import math
import re

from ceotr_common_utilities import simplified_float
from ceotr_common_utilities.gps_points_tools import gps_point_range_check


class KmlInfo:
    """
    Structured representation of a generic KML file.
    """

    def __init__(self, kml_str=None):
        self.kml = fastkml.kml.KML()
        if kml_str is not None:
            self.kml.from_string(kml_str.encode('utf8'))

            # setup variables from raw kml elements
            document = list(self.kml.features())[0]
            self.features_list = list(document.features())

            self.features = {feature.name: feature.features() for feature in self.features_list}
            self.name = document.name


class CoordinatesKmlInfo(KmlInfo):
    """
    Structured representation of a coordinate only (time optional) KML file. Automatically reduces points set.
    """

    def __init__(self, name, points):
        """
        :param name: Document name
        :param coordinates: coordinates (as list of [lat, lon])
        :param points: time and coordinates (list of [time, lat, lon])
        """
        super().__init__(None)
        self.name = name
        self.points = points
        self.reduced_points = generate_simplified_point_set(points)


class SlocumKmlInfo(KmlInfo):
    """
    Structured representation of a KML file downloaded from SFMC
    """

    def __init__(self, kml_str=None):
        super().__init__(kml_str)
        if kml_str is not None:
            self.surfacings = [Surfacing(x) for x in self.features.get('Surfacings', [])]
            self.surface_movements = [Placemark(x) for x in self.features.get('Surface Movements', [])]
            self.glider_tracks = [Placemark(x) for x in self.features.get('Glider Tracks', [])]
            self.next_waypoints = list(self.features.get('Next Waypoint', []))
            self.glider_latest_location = list(self.features.get('Glider Latest Location', []))
            self.planned_waypoints = list(self.features.get('Planned Waypoints', []))
            self.planned_waypoint_paths = list(self.features.get('Planned Waypoint Paths', []))
            self.depth_averaged_current_vectors = [CurrentVector(x) for x in
                                                   self.features.get('Depth Averaged Current Vectors', [])]

            # statistical data
            try:
                self.first_surfacing = min(self.surfacings, key=lambda x: x.date)
                self.last_surfacing = max(self.surfacings, key=lambda x: x.date)
            except ValueError:
                self.first_surfacing = None
                self.last_surfacing = None


class Placemark:
    """
    A friendlier and more useful version of fastkml's Placemark object.
    It includes the date and more easily-accessible coordinates.
    """

    def __init__(self, obj: fastkml.kml.Placemark):
        self.lng = obj.geometry.coords[0][0]
        self.lat = obj.geometry.coords[0][1]
        self.description = obj.description
        try:
            self.date = parse(re.search(r': ([^<]*)', self.description).group(1))
        except Exception:
            self.date = obj.timeStamp
        self.raw_placemark = obj


class Surfacing(Placemark):
    def __init__(self, obj: fastkml.kml.Placemark):
        super().__init__(obj)
        self.distance = 0
        self.bearing = 0
        self.speed = 0
        self.name = self.date
        self.altitude = 0
        self.heading = 0
        self.tilt = 0
        self.range = 100000
        self.altitude_mode = 'relativeToGround'
        self.gx_altitude_mode = 'relativeToSeaFloor'

    def __str__(self):
        return f"""
            <Placemark>
                <name>{self.name}</name>
                <description>{self.description}</description>
                <LookAt>
                    <longitude>{self.lng}</longitude>
                    <latitude>{self.lat}</latitude>
                    <altitude>{self.altitude}</altitude>
                    <heading>{self.heading}</heading>
                    <tilt>{self.tilt}</tilt>
                    <range>{self.range}</range>
                    <altitudeMode>{self.altitude_mode}</altitudeMode>
                    <gx:altitudeMode>{self.gx_altitude_mode}</gx:altitudeMode>
                </LookAt>
                <Style><BalloonStyle><text>{self.description}</text></BalloonStyle><LabelStyle><scale>0.4</scale></LabelStyle><IconStyle><scale>0.6</scale></IconStyle></Style><styleUrl>#msn_open-diamond</styleUrl>
                <Point>
                    <coordinates>{self.lng},{self.lat},{self.altitude}</coordinates>
                </Point>
            </Placemark>
            """


class CurrentVector(Placemark):
    def __init__(self, obj: fastkml.kml.Placemark):
        super().__init__(obj)
        self.altitude = 0
        self.altitude_mode = 'relativeToGround'
        desc_parse = re.match(r'<b>Speed: (?P<speed>[0-9.]*)m/s @ (?P<heading>[0-9]*)&deg;</b>', self.description)
        self.speed = desc_parse.group('speed')
        self.heading = desc_parse.group('heading')

    def __str__(self):
        return f"""
            <Placemark>
                <visibility>0</visibility>
                <name>{self.speed} m/s</name>
                <Style>
                    <LabelStyle><scale>0.6</scale><color>aa00ff00</color></LabelStyle><IconStyle>
                        <color>aa00ff00</color>
                        <scale>1.28</scale>
                        <heading>{self.heading}</heading>
                    </IconStyle>
                </Style>
                <styleUrl>#msn_arrow</styleUrl>
                <Point>
                    <altitudeMode>{self.altitude_mode}</altitudeMode>
                    <coordinates>{self.lng},{self.lat},{self.altitude}</coordinates>
                </Point>
            </Placemark>
            """


class Folder:
    """
    Allows you to do

    with Folder(f, 'foo', 0):
        f.write('bar')

    and you'll get

    <Folder>
    <name>foo</name>
    <open>0</open>
    bar
    </Folder>

    written to the file
    """

    def __init__(self, file, name='', open=0):
        self.file = file
        self.name = name
        self.open = open

    def __enter__(self):
        self.file.write('\n<Folder>\n')
        self.file.write(f'<name>{self.name}</name>\n')
        self.file.write(f'<open>{self.open}</open>\n')

    def __exit__(self, type, value, traceback):
        self.file.write('\n</Folder>\n')


# TODO: share better
""" Taken (and modified) from glidres_website tractory_point_process.py - Start """

LEAFLET_POINT_ACCURACY = 6
TOLERANT = 0


def point_round(the_float, digit):
    new_float = simplified_float(the_float, digit)
    return new_float


def coordinate_round(point, digit):
    res = [point[0], simplified_float(point[1], digit), simplified_float(point[2], digit)]
    return res


def generate_simplified_point_set(points):
    temp_end_point = None
    previous_point = None
    ref = {
        'line_equation': None
    }
    simp_res = []

    for current_point in points:
        if current_point[1] and current_point[2]:
            latlng = [float(current_point[1]), float(current_point[2])]
            range_check = gps_point_range_check(latlng)
            if range_check and current_point != temp_end_point:
                if check_point_on_line(ref, previous_point, current_point):
                    if temp_end_point:
                        res = temp_end_point
                    else:
                        res = current_point
                    simp_res.append(coordinate_round(res, LEAFLET_POINT_ACCURACY))
                    previous_point = res
                temp_end_point = current_point
    return simp_res


def check_point_on_line(ref, previous_point, current_point):
    """
    return True means can add point to the line.
    """
    if not previous_point:
        return True
    else:
        time1, lat1, lon1 = previous_point
        time2, lat2, lon2 = current_point
        if not ref['line_equation']:
            denominator = (lat2 - lat1)
            if denominator != 0:
                slope = (lon2 - lon1) / denominator
            else:
                slope = 0
            intercept = lon2 - slope * lat2
            ref['line_equation'] = {"slope": slope, "intercept": intercept}
            return False
        else:
            equation_y = ref['line_equation']["slope"] * lat2 + ref['line_equation']["intercept"]
            tolerant = 10 ** (LEAFLET_POINT_ACCURACY - TOLERANT)
            equation_y = math.floor(equation_y * tolerant) / tolerant
            lon2 = math.floor(lon2 * tolerant) / tolerant
            if lon2 == equation_y:
                return False
            else:
                ref['line_equation'] = None
                return True


""" Taken (and modified) from gliders_website trajectory_point_process.py - End """
