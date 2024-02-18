# TODO: use simplekml or other lib
import argparse
import json
import os
import requests
from shutil import copyfile
import traceback
from urllib.parse import urljoin

from kml_tool.models import CoordinatesKmlInfo, Folder

RES_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/output/erddap"


def generate_kml_info(erddap_url, dataset_id):
    url_template = urljoin(erddap_url, "/erddap/tabledap/{0}.json?time%2Clatitude%2Clongitude")
    metadata_url_template = urljoin(erddap_url, "/erddap/info/{0}/index.json")

    print("Generating CoordinatesKmlInfo for " + dataset_id)
    url = url_template.format(dataset_id)
    data = requests.get(url)
    json_data = json.loads(data.text)

    metadata_url = metadata_url_template.format(dataset_id)
    metadata_data = requests.get(metadata_url)
    metadata_json = json.loads(metadata_data.text)
    platform_name = get_platform_from_metadata(metadata_json)
    if platform_name is None:
        platform_name = dataset_id.split("_")[0]

    coord_kml_info = CoordinatesKmlInfo(platform_name, json_data['table']['rows'])
    return coord_kml_info


def get_platform_from_metadata(metadata_json_table):
    rows = metadata_json_table['table']['rows']
    for row_index in range(len(rows)):
        if rows[row_index][0] == "variable" and rows[row_index][1] == "platform":
            row_index += 1
            while rows[row_index][1] == "platform":
                if rows[row_index][2] == "long_name":
                    return rows[row_index][4]
                row_index += 1
    return None


def write_kml_info(kml_file_name, kml_info):
    # create the empty processed file
    f = open(kml_file_name, 'w')
    # write header
    f.write(
        '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<kml xmlns=\"http://www.opengis.net/kml/2.2\" '
        'xmlns:gx=\"http://www.google.com/kml/ext/2.2\" xmlns:kml=\"http://www.opengis.net/kml/2.2\" '
        'xmlns:atom=\"http://www.w3.org/2005/Atom\">\n<Document><name>' + kml_info.name + '</name>\n<open>1</open>')
    # write the style preamble from a reference file
    f.write(open(os.path.join(os.path.dirname(__file__), 'ref/GEstyle.txt')).read())

    # write glider path
    with Folder(f, 'Glider Path', 1):
        coords = '\n'.join(f'{x[2]},{x[1]},0' for x in kml_info.reduced_points)
        path_str = f"""
                    <Placemark>
                        <name>Glider Path</name>
                        <styleUrl>#msn_ylw_pushpin</styleUrl>
                        <LineString>
                            <tessellate>1</tessellate>
                            <coordinates>
                                {coords} 
                            </coordinates>
                        </LineString>
                    </Placemark>
                    """
        f.write(path_str)

    # write points
    with Folder(f, 'Points', 1):
        for point in kml_info.reduced_points:
            time, lat, lng = point
            point_str = f"""
                        <Placemark>
                            <description>{time}</description>
                            <Point>
                                <coordinates>{lng},{lat},0</coordinates>
                            </Point>
                        </Placemark>
                        """
            f.write(point_str)

    # close out file
    f.write('\n</Document>\n</kml>')
    f.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate simple KMLs from ERDDAP datasets")
    parser.add_argument('--url', dest="url", help="Base URL for ERDDAP instance (without /erddap)",
                        default="https://ceotr.ocean.dal.ca")
    parser.add_argument('--dataset_ids', dest="dataset_ids", help="Comma delimited dataset IDs for ERDDAP datasets",
                        required=True)

    try:
        os.makedirs(RES_PATH)
    except FileExistsError:
        # not need to raise, if file already exists
        pass

    try:
        args = parser.parse_args()
        for dataset_id in args.dataset_ids.split(','):
            kml_info = generate_kml_info(args.url, dataset_id)
            temp_file_name = os.path.join(RES_PATH, "temp.kml")
            kml_file_name = os.path.join(RES_PATH, dataset_id + ".erddap.gps.kml")  # TODO: temp name, move file after successful write
            print("Writing " + kml_file_name)
            write_kml_info(temp_file_name, kml_info)
            copyfile(temp_file_name, kml_file_name)
    except Exception as e:
        print(traceback.print_exc())
        parser.print_help()
        exit(1)
