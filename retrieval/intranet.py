"""
Copyright 2017 (or whatever, you care?) Rohit Suratekar
Code is released under MIT license.

TL;DR : use "do_all()" function and retrieve all photo and related info. You can skip reading following.

Retrieves data from intranet about photos and associated meta-data.
Ideally it just typical web crawler which scraps the photography page.
Photography page is written in classic html-css-javascript style with Drupal template.
This script just extracts all the css tags and then extract whichever field is needed.

General workflow should be
1) Retrieve files (get_all_info())
2) Download all photos (retrieve_pics())
3) Save meta-data and related details (save_details())

JSON file created in final step can be used for further process
like uploading photos to server or calculating rating etc.
"""
import csv
import json
import os
import random
import re
import string
import urllib.request as request

from bs4 import BeautifulSoup

from models.photography import PhotoObject as Photo
from user_constants import *


def read_main_page() -> list:
    """
    Read entire page. All currently uploaded photos will be here
    :return: List of Odd and Even elements of HTML for further processing
    """
    page = request.urlopen(base_url + "/photography").read()
    soup = BeautifulSoup(page, 'html.parser')
    # Photos are divided into two alternate rows. Get both
    all_even = soup.findAll("tr", {"class": "even"})
    all_odd = soup.findAll("tr", {"class": "odd"})
    return all_even + all_odd


def get_number(s) -> list:
    """
    Average votes and total votes are in some different format. We need regex power to get what we need!
    :param s: String containing votes details
    :return: list of items after compiling regex. We need first item of this
    """
    return re.findall(r'[-+]?\d*\.\d+|\d+', s)


def get_author_email(u) -> str:
    """
    This takes relative path from hyperlink and goes to that page.
    Then extract email address (or Username) given in author field
    :param u: relative path of photo
    :return: email ID (or Username)
    """
    specific_url = base_url + u
    new_page = request.urlopen(specific_url).read()
    new_soup = BeautifulSoup(new_page, 'html.parser')
    return new_soup.find("a", {"class": "username"}).text.strip()


def get_all_info() -> list:
    """
    Main function to retrieve all the information regarding all the uploaded photos
    :return: List of PhotoObjects
    """
    photos = []
    # iterate over all odd and even category
    for a in read_main_page():
        url = a.find("td", {"class": "views-field views-field-title"}).find("a").get('href')
        title = a.find("td", {"class": "views-field views-field-title"}).find("a").text
        photo_url = a.find("td", {"class": "views-field views-field-field-photo-image"}).find("a").get('href')
        author = a.find("td", {"class": "views-field views-field-field-personal-first-name"}).text.strip()
        # Following items needs to be check if they exists
        # because in early phases of competition, this information will not be available.
        average_votes = None
        creation_date = None
        total_votes = None
        # use "views-field views-field-field-photo-rating active" when voting is still going on
        try:
            creation_date = a.find("td", {"class": "views-field views-field-created active"}).text.strip()
            average_votes = \
                get_number(a.find("td", {"class": "views-field views-field-field-photo-rating"}).find("div", {
                    "class": "fivestar-summary fivestar-summary-average-count"})
                           .find("span", {"class": "average-rating"}).text)[0]
            total_votes = \
                get_number(a.find("td", {"class": "views-field views-field-field-photo-rating"}).find("div", {
                    "class": "fivestar-summary fivestar-summary-average-count"}).find("span",
                                                                                      {"class": "total-votes"}).text)[0]
        except AttributeError:
            print("Skipping data field because it was not available")

        # Create new object
        current_pic = Photo()
        current_pic.author = author
        current_pic.title = title
        current_pic.average_votes = average_votes
        current_pic.creation_date = creation_date
        current_pic.photo_url = photo_url
        current_pic.total_votes = total_votes
        current_pic.url = url
        current_pic.author_email = get_author_email(url)
        # add to list
        photos.append(current_pic)

    return photos


def retrieve_pics(photos: list) -> list:
    """
    Downloads photo from absolute url retrieved from `get_all_info()` function.
    This also added file name details into PhotoObjects and returns same list with updated parameter
    :param photos: List of all PhotoObjects
    :return: Same list with `file_name' field updated
    """
    file_counter = 1  # Counter for files
    if not os.path.exists(photo_store_folder):
        # Make folder if it does not exists
        os.makedirs(photo_store_folder)

    for p2 in photos:
        # Create file name
        # Besides prefix, add little bit of title. Remove all the special characters from title and use string sequence
        filename = photo_prefix + "%d_%s" % (file_counter, re.sub('[^A-Za-z0-9]+', '', p2.title))
        filename = filename[:20] + ".jpg"  # If name if more than 20 characters, strip it and add file extension
        p2.file_name = filename  # Update file_name field in the PhotoObject
        testfile = request.URLopener()  # start downloading
        testfile.retrieve(p2.photo_url, photo_store_folder + filename)  # Save
        file_counter += 1

    return photos


def save_details(photos: list) -> None:
    """
    Saves details into file.
    Important to use encoding as utf-8 because some characters can not be written in regular parser
    :param photos: List of PhotoObjects
    :return: None
    """
    # Writes CSV files for `general public'
    with open(output_file_name + ".csv", "w", encoding="utf-8") as output:
        writer = csv.writer(output, lineterminator='\n')
        for p in photos:
            writer.writerow(p.get_all())

    # Write json file for advance users, if anyone want's to use this information for further process.
    all_info = {}
    for photo in photos:
        key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))  # Create some random key
        # Create json entry
        all_info[key] = {"uid": key,
                         "url": photo.url,
                         "author": photo.author,
                         "title": photo.title,
                         "total_votes": photo.total_votes,
                         "average_votes": photo.average_votes,
                         "creation_date": photo.creation_date,
                         "photo_url": photo.photo_url,
                         "author_email": photo.author_email,
                         "file_name": photo.file_name}
    # Dump to json
    with open(output_file_name + ".json", "w") as f:
        print(json.dumps(all_info), file=f)


def do_all():
    """
    For lazy people. This function does entire process
    :return: Download all photos with thier information and details
    """
    save_details(retrieve_pics(get_all_info()))
