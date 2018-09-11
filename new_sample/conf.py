from urllib.parse import urlparse, parse_qs
from new_sample import bcesigner
import datetime

host = "yuqing.baidu.com"  # 试用地址为这个；  正式的需要参考文档的地址为：trends.baidubce.com
access_key = 'your'
secret_key = 'your'
api_key = 'your'
api_secret = 'your'


def gen_authorization(method, url):
    """
    normal case
    """
    utc_time = datetime.datetime.utcnow()
    utc_time_str = utc_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    url_parse_ret = urlparse(url)
    query = url_parse_ret.query
    request = {
        'method': method,
        'uri': url_parse_ret.path,
        'params': dict([(k, v[0]) for k, v in parse_qs(query).items()]),
        'headers': {
            'Host': url_parse_ret.hostname
        }
    }

    signer = bcesigner.BceSigner(access_key, secret_key)
    auth = signer.gen_authorization(request, timestamp=utc_time_str)
    return auth
