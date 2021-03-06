#!/usr/bin/python
import mechanize
import StringIO
import lxml.html
import ConfigParser
import multiprocessing
import json
import sys
import csv

config = ConfigParser.SafeConfigParser()
config.read('admin.cfg')

POOL_SIZE = 15 # High because I'm on a high-latency connection

def get_logged_in_browser():
    # Create Browser object
    b = mechanize.Browser()
    # Log in, at least, we hope
    b.open('https://secure.wikidc.org/wm/reg/user')
    b.select_form(nr=0)
    b['name'] = config.get('auth', 'username')
    b['pass'] = config.get('auth', 'password')
    response = b.submit()
    # Make sure the login worked
    assert 'logout' in response.read()
    return b

def get_email_address(b, user_id):
    url = 'https://secure.wikidc.org/wm/reg/user/%d/edit' % (
        user_id,)
    data = b.open(url).read()
    parsed = lxml.html.parse(StringIO.StringIO(data))
    email = parsed.getroot().cssselect('input[name=mail]')[0].value
    return email

def get_gender(b, user_id):
    url = 'https://secure.wikidc.org/wm/reg/user/%d' % (
        user_id,)
    data = b.open(url).read()
    parsed = lxml.html.parse(StringIO.StringIO(data))
    gender_fields = parsed.getroot().cssselect('dd.profile-profile_gender')
    if gender_fields:
        return gender_fields[0].text
    # Otherwise, no big deal.
    return ''

def log_in_then_consume_list_of_user_ids(user_ids, queue):
    b = get_logged_in_browser()
    ret = {}
    for user_id in user_ids:
        gender = get_gender(b, user_id)
        email = get_email_address(b, user_id)
        ret[user_id] = {'gender': gender, 'email': email}
    queue.put(ret)

def break_list_into_parts(l, parts=POOL_SIZE):
    last_list = 0

    work_lists = []
    for i in range(POOL_SIZE):
        work_lists.append([])

    for user_id in l:
        index = ((last_list + 1) % POOL_SIZE)
        work_lists[index].append(user_id)
        last_list = index

    return work_lists

def get_gender_and_email_in_bulk(list_of_user_ids):
    work_lists = break_list_into_parts(list_of_user_ids)
    processes = []
    queue = multiprocessing.Queue()
    for i in range(POOL_SIZE):
        p = multiprocessing.Process(target=log_in_then_consume_list_of_user_ids,
                                    args=(work_lists[i], queue))
        processes.append(p)
    for p in processes:
        p.start()
    for p in processes:
        p.join()

    # Now, we merge the data
    result = {}
    for i in range(POOL_SIZE):
        result.update(queue.get())

    return result

if __name__ == '__main__':
    # Consume CSV on stdin
    data = []
    in_data = csv.DictReader(sys.stdin)
    for datum in in_data:
        data.append(datum)

    # Grab just the user IDs
    user_ids = [int(thing['Uid']) for thing in data]
    user_ids2extra_data = get_gender_and_email_in_bulk(user_ids)
    for thing in data:
        extra_data = user_ids2extra_data[int(thing['Uid'])]
        thing.update(extra_data)

    out_writer = csv.DictWriter(sys.stdout, fieldnames = thing.keys())

    # Add header
    out_writer.writerow(dict((f,f) for f in out_writer.fieldnames) )

    for datum in data:
        out_writer.writerow(datum)

