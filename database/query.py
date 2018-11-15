import sqlite3
from sqlite3 import Error
import feedparser


def get_latest_from_feed():
    # Get the latest feed post ID
    url = 'http://feeds.feedburner.com/ufostalker'
    d = feedparser.parse(url)
    latest_link = d['entries'][0]['link'].split('/')
    latest_id = latest_link[-1]
    return int(latest_id)


def get_latest_db_entry():
    conn = sqlite3.connect('database/database.db')
    cur = conn.cursor()
    with conn:
        latest = cur.execute(
            'SELECT original_id FROM sightings WHERE original_id = (SELECT \
            MAX(original_id) FROM sightings)')

        if latest.fetchall():
            id = cur.execute(
                'SELECT original_id FROM sightings WHERE original_id = (SELECT\
                 max(original_id) FROM sightings)').fetchall()[0][0]
            return int(id)
        else:
            return 1  # Empty set


def get_all():
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    ids = [original_id[0] for original_id in cursor.execute(
        "SELECT original_id FROM sightings")]
    return ids


def work_out_remaining():
    min = 1
    all_results = sorted(get_all(), key=int)  # List of all the results we have
    # Work out what the list should contain.
    id_list = list(range(min, get_latest_from_feed()))
    left_to_run = list(set(all_results).symmetric_difference(set(id_list)))
    # return a list of ids still to process, includes missing ones
    return left_to_run
