#!/usr/bin/python
# encoding=utf-8

import sys

import datetime
import hashlib
import hmac
import time
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import hmac
from new_sample import conf


def send(data, method):
    url = "http://" + conf.host + "/openapi/gettasklist"

    auth = conf.gen_authorization(method, url)
    header = {
        'host': conf.host,
        'Content-Type': 'application/x-www-form-urlencoded',
        'authorization': auth,
        'accept': '*/*'
    }
    request = Request(url, data=data.encode("utf-8"), headers=header)
    response = None
    try:
        response = urlopen(request, timeout=60)
        post_res_str = response.read()
        d_json = json.loads(post_res_str)
        print(d_json, "##########")
        print(d_json['code'])
    except HTTPError as e:
        print("HTTPError")
        print(e.code, e.reason)
        print(e.read())
    except URLError as e:
        print("URLError")
        print(e)


def create_data():
    timestamp = str(int(time.time()))
    token = hmac.new(bytes(conf.api_secret, 'utf-8'), bytes(conf.api_key + timestamp, 'utf-8'),
                     hashlib.sha1).hexdigest()
    data = "user_key=%s&token=%s&timestamp=%s" % (conf.api_key, token, timestamp)
    print(data)
    return data


if __name__ == "__main__":
    data = create_data()
    send(data, "POST")
