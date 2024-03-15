import requests

def key_in_dict_and_not_none(d, key):
    return key in d and d[key] is not None


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()