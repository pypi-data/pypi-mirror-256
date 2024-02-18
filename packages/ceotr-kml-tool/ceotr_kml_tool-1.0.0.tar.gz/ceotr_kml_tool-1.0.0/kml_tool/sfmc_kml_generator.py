from bs4 import BeautifulSoup
from datetime import datetime
from kml_tool.models import SlocumKmlInfo, Folder
from lxml.html import Element
import os
import pykml.parser
import re
import requests as requests
import sys
from typing import List
from urllib3.exceptions import InsecureRequestWarning
from zipfile import ZipFile
import warnings


URL_BASE = 'https://gliderbak.ocean.dal.ca'
URL_LOGIN = URL_BASE + '/sfmc/login'
URL_ACTIVE_DEPLOYMENTS = URL_BASE + '/sfmc/deployment-pages/active-deployments'
URL_ARCHIVED_DEPLOYMENTS = URL_BASE + '/sfmc/deployment-pages/archived-deployments'
ACTIVE_ZIPPED_FOLDER = './active_zipped/'
ACTIVE_UNZIPPED_FOLDER = './active/'
ARCHIVED_ZIPPED_FOLDER = './archived_zipped/'
ARCHIVED_UNZIPPED_FOLDER = './archived/'
CREDENTIALS_FILE = '../credentials.txt'


def load_credentials() -> (str, str):
    """
    Load SFMC credentials from CREDENTIALS_FILE.

    :return: (username, password)
    """
    try:
        with open(CREDENTIALS_FILE) as f:
            username = f.readline().rstrip()
            password = f.readline().rstrip()
    except FileNotFoundError:
        print('Please create a credentials.txt file and enter the SFMC username and password on separate lines',
              sys.stderr)
        sys.exit(1)
    return username, password


def download(username, password, url, destination, destination_zipped):
    """
        Download deployments, save them to disk, and return them.

        Put zipped kmz files in destination_zipped, unzipped kml files in destination,
        and return a list of parsed kml objects.
        """
    # start a session
    session = requests.session()
    # get csrf
    login_page = session.get(URL_LOGIN, verify=False)
    csrf_token = re.search('<input type="hidden" name="_csrf" value="([^"].*)"/>', login_page.text).group(1)
    # login
    params = {
        'username': username,
        'password': password,
        '_csrf': csrf_token
    }
    session.post(URL_LOGIN, params=params, verify=False)
    # get missions list
    params = {
        'page': 0,
        'size': 100000,
    }
    deployments_page = session.get(url, params=params, verify=False)
    deployments_links = re.findall(r'<td>[\n\r\s]*<a href="([^"].*)">', deployments_page.text)

    # make sure directory exists
    try:
        os.mkdir(destination_zipped)
    except FileExistsError:
        pass
    try:
        os.mkdir(destination)
    except FileExistsError:
        pass
    # download kmz files
    for link in deployments_links:
        deployment_page = session.get(URL_BASE + link)
        deployment_id = re.search('sfmcPageDataNs.deploymentId = ([0-9]+);', deployment_page.text).group(1)
        deployment_name = re.search(r'<li class="active">[\n\r\s]*<span>([^<]*)</span>', deployment_page.text).group(1)
        tree = BeautifulSoup(deployment_page.text, features='lxml')
        date_start = tree.body.find('span', attrs={'id': 'deployment-start-date-time'}).text
        # the start date is in format YYYY-MM-DDHHmm (there's a <br> between date and time that .text removes)
        # SFMC wants the format: YYYYMMDDHHmm
        sfmc_date_format = '%Y%m%d%H%M'
        date_start = datetime.strptime(date_start, '%Y-%m-%d%H:%M').strftime(sfmc_date_format)
        date_end = datetime.now().strftime(sfmc_date_format)
        download_url = URL_BASE + '/sfmc/kmz-requests/export-to-kmz-authenticated/{}'.format(deployment_id)
        params = {
            'startDateTime': date_start,
            'endDateTime': date_end,
        }
        kmz_file_path = '{}.kmz'.format(os.path.join(destination_zipped, deployment_name))
        print('Downloading ', download_url, ' to ', kmz_file_path)
        kmz_file_result = session.get(download_url, params=params, verify=False)
        kmz_file_binary = kmz_file_result.content
        with open(kmz_file_path, 'wb') as f:
            f.write(kmz_file_binary)
    # unzip kmz files
    for fname in os.listdir(destination_zipped):
        filepath = os.path.join(destination_zipped, fname)
        destination_path = '{}.kml'.format(os.path.join(destination, os.path.splitext(fname)[0]))
        print('Unzipping ', filepath, ' to ', destination_path)
        kmz = ZipFile(filepath, 'r')
        kml = kmz.open('doc.kml', 'r').read()
        with open(destination_path, 'wb') as f:
            f.write(kml)
    # return parsed kml files
    parsed_kmls = []
    for fname in os.listdir(destination):
        kml_tree = pykml.parser.parse(os.path.join(destination, fname))
        parsed_kmls.append(kml_tree)
    return parsed_kmls


def download_active(username, password, destination=ACTIVE_UNZIPPED_FOLDER, destination_zipped=ACTIVE_ZIPPED_FOLDER) -> \
        List[Element]:
    return download(username,
                    password,
                    url=URL_ACTIVE_DEPLOYMENTS,
                    destination=destination,
                    destination_zipped=destination_zipped)


def download_archived(username, password, destination=ARCHIVED_UNZIPPED_FOLDER,
                      destination_zipped=ARCHIVED_ZIPPED_FOLDER) -> List[Element]:
    return download(username,
                    password,
                    url=URL_ARCHIVED_DEPLOYMENTS,
                    destination=destination,
                    destination_zipped=destination_zipped)


def main():
    with warnings.catch_warnings():
        # our SFMC doesn't have a proper certificate, so we do verify=False and ignore warnings
        warnings.simplefilter("ignore", InsecureRequestWarning)
        username, password = load_credentials()
        kmls = download_active(username, password) + download_archived(username, password)
        return kmls


def process(in_path: str, out_path: str) -> SlocumKmlInfo:
    """
    :param in_path: path to the raw KML file
    :param out_path:  path to save the processed KML file to
    :return: SlocumKmlInfo object for the KML file

    Process a KML file downloaded from SFMC, changing it to match those on http://gliders.oceantrack.org/ge/,
    which are generated by https://gitlab.oceantrack.org/ceotr/gliders/old_glider_tools/blob/master/colton_backup/scripts/python/googleEarthGliders.py

    This function heavily uses code from the above script.
    """

    # load raw kml file
    raw_str = None
    with open(in_path) as f:
        raw_str = f.read()
    kml_info = SlocumKmlInfo(raw_str)

    try:
        start_date = str(kml_info.surface_movements[0].date)
    except IndexError:
        start_date = None

    try:
        end_date = str(kml_info.surface_movements[-1].date)
    except IndexError:
        end_date = None

    # missionId = str(datepair['missionId'])  # not in kml, do we need it?
    kml_file_name = out_path

    try:
        glider_name = os.path.basename(in_path).split('-')[0]
    except IndexError:
        glider_name = 'unknown_glider_name'

    kml_info.name = glider_name

    write_kml_info(kml_file_name, kml_info)

    # return KML info
    return kml_info


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

    # write surfacings
    with Folder(f, f'{kml_info.name} Surfacings', 0):
        for surfacing in kml_info.surfacings:
            f.write(str(surfacing))

    # write glider path
    with Folder(f, 'Glider Path', 1):
        coords = ' '.join(f'{x.lng},{x.lat},0' for x in kml_info.surfacings)
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

    # write currents
    with Folder(f, 'Glider Calculated Currents', 1):
        for vec in kml_info.depth_averaged_current_vectors:
            f.write(str(vec))

    # close out file
    f.write('\n</Document>\n</kml>')
    f.close()


if __name__ == '__main__':
    # main()
    process('/home/peter/code/kml_tool/kml_tool/bad_bond-2019-08-28T11:24.kml',
            '/home/peter/code/kml_tool/kml_tool/test_out.kml')
