import os
from dotenv import load_dotenv
import json
import requests
from datetime import datetime, timezone, date

CONSUMER_KEY = os.environ['CONSUMER_KEY']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']

def main():
    data = retrieve_articles()['list']
    check_all_articles(data)

def retrieve_articles():
    return get({})

def date_expired(time_added, delta):
    today = datetime.now(timezone.utc).astimezone().date()
    return (today - date.fromtimestamp(int(time_added))).days > delta

def check_all_articles(articles):
    ids = []
    for article_id, value in articles.items():
        # 100 days up and not favorite -> delete
        # 30 days up and not read -> delete
        if date_expired(value['time_added'], 30):
            if not int(value['time_read'])  or (date_expired(value['time_added'], 100) and not int(value['favorite'])):
                ids.append(article_id)
    delete_articles(ids)

def delete_articles(item_id_list):
    query = []
    for id in item_id_list:
        query.append({
            "action": "delete",
            "item_id": id
        })
    post('/send', query)


def get(extra_query):
    url = 'https://getpocket.com/v3/get'
    query = {'consumer_key': CONSUMER_KEY,
             'access_token': ACCESS_TOKEN
             }
    get_json = requests.get(url, params=query)
    get_json = json.loads(get_json.text)
    return get_json


def post(endpoint, data):
    url = 'https://getpocket.com/v3' + endpoint

    payload = {
        "consumer_key": CONSUMER_KEY,
        "access_token": ACCESS_TOKEN,
    }
    headers = {'content-type' : 'application/json'}
    
    payload.update({
        'actions': data,
    })

    return requests.post(url, data=json.dumps(payload), headers=headers)


if __name__ == '__main__':
    main()