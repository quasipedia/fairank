from flask import Flask, render_template

import time
import requests
import json
import os
from collections import defaultdict
from itertools import chain
import statistics
import datetime

app = Flask(__name__)

CONFIG = {}
with open('CONFIG.json') as config_file:
    CONFIG = json.load(config_file)

def get_data():
    data_fname = 'DATA.json'
    if time.time() - os.path.getmtime(data_fname) > 900:
        print('DOWNLOAD')
        response = requests.get(CONFIG['api_url'], cookies={'session': CONFIG['session_id']})
        with open(data_fname, 'w') as data_fname:
            json.dump(response.json(), data_fname, indent=2)
    with open(data_fname) as data_file:
        payload = json.load(data_file)
        payload['last_updated'] = os.path.getmtime(data_fname)
        return payload


class User:

    COMPETITION_START = int(
        datetime.datetime.fromisoformat("{}-12-01T00:00:00-05:00".format(CONFIG['year'])).timestamp())
    # 1638334800  # Midnight UTC-5 of 01.12.2021
    POSITIONAL_SUFFIXES = {1: 'st', 2: 'nd', 3: 'rd'}

    def __init__(self, data):
        self.__original_data = data
        self.name = data['name'] or 'User #' + data['id']
        self.stars = data['stars']
        self.timestamps = defaultdict(lambda: {1: None, 2: None})
        self.gold_star_within_day = set()
        self.ranks = defaultdict(lambda : {1: 0, 2: 0})
        self.fair_rank = 0
        self.gold_record = {'day': None, 'rank': None, 'time': None}
        self._process_timestamps(data['completion_day_level'])

    def _process_timestamps(self, original):
        for k, v in original.items():
            for day in '12':
                if day in v:
                    timestamp = v[day]['get_star_ts']
                    self.timestamps[int(k)][int(day)] = timestamp
                    if day == '2' and timestamp < self.COMPETITION_START + int(k) * 86400:
                        self.gold_star_within_day.add(int(k))

    @property
    def gold_sentence(self):
        if self.gold_record['day'] is None:
            return 'n/a'
        rank = self.gold_record['rank']
        position = '{}{}'.format(rank, self.POSITIONAL_SUFFIXES[rank] if rank in self.POSITIONAL_SUFFIXES else 'th')
        formatted_time = time.strftime('%Hh %Mm %Ss', time.gmtime(self.gold_record['time']))
        return '{} on day {} in {}'.format(position, self.gold_record['day'], formatted_time)


def rank_users(users):
    """See README.md for a description for the rationale and algorithm of the ranking system."""
    for day in range(1, 26):
        participants = list(filter(lambda u: day in u.gold_star_within_day, users))
        for star in '12':
            participants.sort(key=lambda u: u.timestamps[day][int(star)])
            for rank, user in enumerate(participants):
                user.ranks[day][int(star)] = 1 - float(rank) / len(participants)
                rank += 1  # Human positional :)
                if star == '1':
                    continue  # The gold record is only calculated for gold stars
                if user.gold_record['rank'] is None or rank <= user.gold_record['rank']:
                    new_time = user.timestamps[day][2] - (user.COMPETITION_START + 86400 * (day - 1))
                    if not (rank == user.gold_record['rank'] and new_time > user.gold_record['time']):
                        user.gold_record = {'day': day, 'rank': rank, 'time': new_time}
    for user in users:
        try:
            speeds = list(chain.from_iterable([r.values() for r in user.ranks.values()]))
            speeds.extend([0] * max(0, 15 - len(speeds)))  # If there are less than 15 data points assume speeds = 0
            avg_rank = statistics.mean(speeds)
        except statistics.StatisticsError:
            avg_rank = 0.0
        user.avg_rank = avg_rank
        user.fair_rank = 1.5 * user.stars + 0.3 * len(user.gold_star_within_day) + 10 * user.avg_rank


@app.route("/")
def stats():
    data = get_data()
    users = [User(u) for u in data['members'].values()]
    rank_users(users)
    users.sort(key=lambda u: u.fair_rank, reverse=True)
    last_updated = datetime.datetime.fromtimestamp(data['last_updated']).strftime("%c")
    return render_template('home.html.jinja', users=users, last_updated=last_updated)