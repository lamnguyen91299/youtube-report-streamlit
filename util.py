import requests
import streamlit as st
def key_in_dict_and_not_none(d, key):
    return key in d and d[key] is not None


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def convert_image_url_to_data(image_url):
    # image_url = "https://example.com/image.jpg"
    response = requests.get(image_url)
    if response.status_code == 200:
        image_data = response.content  # extract bytes from response content
        return image_data
    else:
        return None
