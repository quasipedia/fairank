from flask import Flask

import time
import requests
import json
import os

app = Flask(__name__)


def get_data():
    api_url = 'https://adventofcode.com/2021/leaderboard/private/view/1102428.json'
    data_file = 'DATA.json'
    last_update_time = os.path.getmtime(data_file)
    if time.time() - last_update_time > 900:
        with open('SESSION_ID.txt') as f:
            print('DOWNLOAD')
            response = requests.get(api_url, cookies={'session': f.readline().strip()})
            with open(data_file, 'w') as f:
                json.dump(response.json(), f)
            last_update_time = time.time()
            API_DATA = response.json()
    with open(data_file) as f:
        return json.load(f)


def filter_data(data):
    ppl = get_data()['members']



@app.route("/")
def stats():
    return "<p>{}</p>".format(get_data())