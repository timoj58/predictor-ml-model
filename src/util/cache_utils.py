import requests
from requests.auth import HTTPDigestAuth
import json

from util.config_utils import get_analysis_cfg
from util.config_utils import get_dir_cfg


TYPES_URL = get_analysis_cfg()['types_url']
COUNTRIES_URL = get_analysis_cfg()['countries_url']
COMPETITIONS_BY_COUNTRY_URL = get_analysis_cfg()['comps_by_country_url']


def get_countries(url):

    response = requests.get(url, headers={'groups': 'ROLE_AUTOMATION'})
    values = response.json()

    countries = []

    for value in values:
     countries.append(value['country'])

    return countries

def get_teams(url, country):

    response = requests.get(url+"?country="+country, headers={'groups': 'ROLE_AUTOMATION'})
    values = response.json()

    teams = []

    for value in values:
        label = value['id']
        if label is not None:
            teams.append(label.encode('unicode_escape'))

    return teams


def get_competitions_per_country(url, country):
    response = requests.get(url+"?country="+country, headers={'groups': 'ROLE_AUTOMATION'})
    return response.json()['count']

