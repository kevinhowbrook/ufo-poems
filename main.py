import errno
import json
import mimetypes
import random
import socket
import time
import urllib
from multiprocessing import Pool
from socket import error as SocketError
from socket import gaierror
from time import sleep
from urllib import parse

import feedparser
import requests
from bs4 import BeautifulSoup

from database.db import Databse
from database.query import work_out_remaining
from proxy.generate_proxies import gen_proxies


def get_latest_from_feed():
    # Get the latest feed post ID
    url = 'http://feeds.feedburner.com/ufostalker'
    d = feedparser.parse(url)
    latest_link = d['entries'][0]['link'].split('/')
    latest_id = latest_link[-1]
    return int(latest_id)


# Get a proxy value from the generated list
def get_proxy(protocol):
    http = []
    https = []
    lines = open('proxy/proxies.txt').readlines()
    for line in lines:
        if 'https' not in line:
            http.append(line)
        else:
            https.append(line)
    if protocol == 'http':
        ip = str(random.choice(http))
    elif protocol == 'https':
        ip = str(random.choice(https))
    return ip


def get_listing():
    return [
        'http://ufostalker.com:8080/event?id={}'.format(i)
        for i in work_out_remaining()
    ]


# parse a single item to get information
def parse(url):
    print('running')
    observation_id = url.replace('http://ufostalker.com:8080/event?id=', '')
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) \
         AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 \
         Safari/537.36'}

    info = []
    title_text = '-'
    while True:
        try:
            http_proxy = get_proxy('http')
            https_proxy = get_proxy('https')

            proxyDict = {
                "http": "{}".format(http_proxy.rstrip()),
                        # "https" : "{}".format(https_proxy.rstrip())
            }
            print(proxyDict)

            response = requests.get(url, headers=headers, timeout=20,
                                    proxies=proxyDict)

            if response.status_code == 200:
                print('Processing..' + url)
                html = response.text
                parsed_html = BeautifulSoup(html, 'lxml')

                # handle files
                if parsed_html.body.find('urls') is not None:
                    images = parsed_html.body.findAll('urls')
                    counter = 0
                    for image in images:
                        print('Image found...')
                        counter += 1
                        # put the images in var for json
                        try:
                            ip = get_proxy('http')

                            proxy = urllib.request.ProxyHandler(
                                {'http': '{}'.format(ip)})
                            opener = urllib.request.build_opener(proxy)
                            urllib.request.install_opener(opener)
                            image_url = str(image.get_text())
                            print(image_url)
                            response_im = urllib.request.urlopen(image_url)

                        except SocketError as e:
                            print('error with {}'.format(image_url))
                            print(e)
                            continue

                        except urllib.error.HTTPError as e:
                            # Return code error (e.g. 404, 501, ...)
                            # ...
                            print('File HTTPError: {}'.format(e.code))
                            error = e.code
                            # Add data for the missing file
                            db.add_file((
                                observation_id,  # the sighting id
                                response.status_code,
                                '',  # filename
                                '',  # mime
                                '',  # type/type
                                image.get_text()
                            ))
                            continue

                        # save the image
                        with response_im:
                            info = response_im.info()
                            file_type = info.get_content_type()
                            extension = mimetypes.guess_extension(
                                info.get_content_type()
                            )
                            filename = "{}_{}".format(observation_id, counter)
                            print('Retrieving files...')
                            print(image.getText())
                            urllib.request.urlretrieve(
                                image_url, "files/{}_{}{}".format(observation_id, counter, extension))

                            # Add the file
                            db.add_file((
                                observation_id,  # the sighting id
                                response.status_code,
                                filename,  # filename
                                extension,  # mime
                                file_type,  # type/type
                                image.get_text()
                            ))

                db.add_sighting((
                    int(observation_id),
                    parsed_html.body.find('summary').getText() if parsed_html.body.find(
                        'summary') is not None else '',
                    response.status_code,
                    parsed_html.body.find('description').getText() if parsed_html.body.find(
                        'description') is not None else '',
                    parsed_html.body.find('detaileddescription').getText(
                    ) if parsed_html.body.find('detaileddescription') is not None else '',
                    parsed_html.body.find('altitude').getText() if parsed_html.body.find(
                        'altitude') is not None else '',
                    parsed_html.body.find('city').getText() if parsed_html.body.find(
                        'city') is not None else '',
                    parsed_html.body.find('country').getText() if parsed_html.body.find(
                        'country') is not None else '',
                    parsed_html.body.find('region').getText() if parsed_html.body.find(
                        'region') is not None else '',
                    parsed_html.body.find('zipcode').getText() if parsed_html.body.find(
                        'zipcode') is not None else '',
                    parsed_html.body.find('distance').getText() if parsed_html.body.find(
                        'distance') is not None else '',
                    parsed_html.body.find('duration').getText() if parsed_html.body.find(
                        'duration') is not None else '',
                    parsed_html.body.find('entityencountered').getText() if parsed_html.body.find(
                        'entityencountered') is not None else '',
                    parsed_html.body.find('features').getText() if parsed_html.body.find(
                        'features') is not None else '',
                    parsed_html.body.find('flightPath').getText() if parsed_html.body.find(
                        'flightPath') is not None else '',
                    parsed_html.body.find('landingoccurred').getText() if parsed_html.body.find(
                        'landingoccurred') is not None else '',
                    parsed_html.body.find('latitude').getText() if parsed_html.body.find(
                        'latitude') is not None else '',
                    parsed_html.body.find('logNumber').getText() if parsed_html.body.find(
                        'logNumber') is not None else '',
                    parsed_html.body.find('submitted').getText() if parsed_html.body.find(
                        'submitted') is not None else '',
                    parsed_html.body.find('timeZoneName').getText() if parsed_html.body.find(
                        'timeZoneName') is not None else '',
                    parsed_html.body.find('longitude').getText() if parsed_html.body.find(
                        'longitude') is not None else '',
                    parsed_html.body.find('shape').getText() if parsed_html.body.find(
                        'shape') is not None else '',
                    parsed_html.body.find('source').getText() if parsed_html.body.find(
                        'source') is not None else ''
                ))
            else:
                db.add_bad_data(observation_id, 'error')
        except Exception as ex:
            print(str(ex))
            continue
        break


""" Main running """

start = time.time()  # Set a start time for gneral checking
# setup db
db = Databse('database/database.db')
db.setup()
# Get a list of urls to scrape
links = get_listing()
# Run Multithread running
with Pool(10) as p:
    proxies = gen_proxies()  # generate some proxies
    records = p.map(parse, links)
    p.terminate()
    p.join()

end = time.time()
print('Time taken: {}'.format(end - start))
