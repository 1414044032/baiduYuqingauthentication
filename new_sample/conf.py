from urllib.parse import urlparse, parse_qs
from new_sample import bcesigner
import datetime

host = "yuqing.baidu.com"
access_key = '6ea4fe2eff06446da7daa8c34f19ffac'
secret_key = '64d3181de64a4f8cae786767360bea8f'
api_key = '01bc25ada836c88cd8ae32a8196b3062'
api_secret = 'd00a9516141c863b14e54fa476c82949'



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
