#!/usr/bin/python
# encoding=utf-8

import sys

import datetime
import hashlib
import hmac
import time
import json
from urllib.parse import unquote, quote
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import hmac
from new_sample import conf


def send(data, method):
    url = "http://" + conf.host + "/openapi/getresult"

    auth = conf.gen_authorization(method, url)
    header = {
        'host': conf.host,
        'Content-Type': 'application/x-www-form-urlencoded',
        'authorization': auth,
        'accept': '*/*'
    }
    request = Request(url, data=data.encode("utf-8"), headers=header)
    response = None
    print(url, header, data, "##########")
    try:
        response = urlopen(request, timeout=60)
        post_res_str = response.read()
        print(post_res_str)
    except HTTPError as e:
        print("HTTPError")
        print(e.code, e.reason)
        print(e.read())
    except URLError as e:
        print("URLError")
        print(e)


def create_data():
    params_dict = {
        "realtime_flow": {
            "offset": "0",
            "size": "1",
            "time_from": "20161203000000",
            "time_to": "20161205235959",
            "media_type": "news",
            "sentiment_type": "0",
            "search_word": "",
            "relate_type": "0",
            "province": "",
            "city": "",
            "county": ""
        }
    }

    timestamp = str(int(time.time()))
    token = hmac.new(bytes(conf.api_secret, 'utf-8'), bytes(conf.api_key + timestamp, 'utf-8'),
                     hashlib.sha1).hexdigest()
    params_dict_str = quote(json.dumps(params_dict, ensure_ascii=False))

    api_type = "realtime_flow"
    task_id = "210088"
    data = "user_key=%s&token=%s&timestamp=%s&params_dict=%s&api_type=%s&task_id=%s" % (
        conf.api_key, token, timestamp, params_dict_str, api_type, task_id)
    print(data)
    return data


if __name__ == "__main__":
    data = create_data()
    send(data, "POST")
