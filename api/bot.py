import requests
from datetime import datetime, timedelta, timezone

TOKEN = "vk1.a.IxH9tJR6kpx9yd_MtT4n2l2-v4Fdex4CedHpJB25CLRhzmiwrfL06jXaiDXAIBTFJk3gQssiD9Deme4YrhD6pHQyMUrSd5n-oLlfXNRRwpYs7lqjchGR42tnHTZ3yQBbWVYd3SPb4ui7M_M8fnaVQvsZPwS_GvGhX8q6Ymy_Pq-IabyzHaC54BTKJOzEkoGGDUPLrhk9CY03LLEmfAd-Cg"


def getStationId(name):
  return requests.get(f'https://backend.cppktrain.ru/train-schedule/search-station?query={name}&limit=100').json()[0]['id']


def getTrains(from_st, to_st):
  from_id = getStationId(from_st)
  to_id = getStationId(to_st)
  trains = requests.get(f"https://backend.cppktrain.ru/train-schedule/date-travel?date={datetime.now(timezone(timedelta(hours=3))).strftime('%Y-%m-%d')}&fromStationId={from_id}&toStationId={to_id}").json()
  res = []
  for train in trains:
    if datetime.strptime(train["departureTime"], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone(timedelta(hours=3))) >= datetime.now(timezone(timedelta(hours=3))):
      res.append(f"[{train['trainNumber']}] {train['departureTime'].split('T')[1][:-3]}-{train['arrivalTime'].split('T')[1][:-3]} {train['startStationName']} -> {train['finishStationName']}")
      if len(res) == 5:
        return res
  return res


def parseMessage(text):
    splitted = text.split('>')
    return splitted[0].strip(), splitted[1].strip()

def send(message,user_id):
  return requests.get('https://api.vk.com/method/messages.send', params={"message":message,"user_id":user_id,"random_id":0, 'v':"5.131","access_token":TOKEN, "keyboard": {"buttons":[[{"action":{"type":"text","label":"❤️ Добавить в избранные","payload":""},"color":"secondary"}]],"inline":True}}).json()
