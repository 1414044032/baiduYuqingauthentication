#!/usr/bin/python
# encoding=utf8

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import datetime
import hashlib
import hmac
import time
import json
import urllib2
import urllib
import hmac
import conf


def send(data, method):
    url = "http://" + conf.host + "/openapi/updatetask"

    auth = conf.gen_authorization(method, url)
    header = {
        'host': conf.host,
        'Content-Type': 'application/x-www-form-urlencoded',
        'authorization': auth,
        'accept': '*/*'
    }
    request = urllib2.Request(url, data=data, headers=header)
    response = None
    try:
        response = urllib2.urlopen(request, timeout=60)
        post_res_str = response.read()
        print
        post_res_str
    except urllib2.HTTPError, e:
        print
        "HTTPError"
        print
        e.code, e.reason
        print
        e.read()
    except urllib2.URLError, e:
        print
        "URLError"
        print
        e


def create_data():
    api_dict = {
        "realtime_flow": {
            "switch": "1",
            "config": {
                "sentiment_analysis": "1",
                "abstract_extract": "1",
                "geo_extract": "1",
                "similar_merge": "1"
            }
        },
        "event_timeline": {
            "switch": "0"
        },
        "spread_analysis": {
            "switch": "0"
        },
        "opinion_analysis": {
            "switch": "0"
        }
    }

    params_dict = {"media_type": ["search", "news", "weibo", "luntan", "boke", "weixin", "custom", "ps_page"],
                   "history": "1",
                   "required_keywords": ["范冰冰"],
                   "optional_keywords": [],
                   "filter_keywords": [],
                   "data_source": [],
                   "api_dict": api_dict
                   }

    timestamp = str(int(time.time()))
    token = hmac.new(conf.api_secret, conf.api_key + timestamp, hashlib.sha1).hexdigest()
    params_dict_str = urllib.quote(json.dumps(params_dict, ensure_ascii=False))

    task_id = "设置为需要更新的task_id"
    data = "user_key=%s&token=%s&timestamp=%s&params_dict=%s&task_id=%s" % (
        conf.api_key, token, timestamp, params_dict_str, task_id)
    print
    data
    return data;


if __name__ == "__main__":
    data = create_data()
    send(data, "POST")
