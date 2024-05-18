from flask import Flask, request
from json import loads, dumps
import sys, traceback
sys.path.insert(1, 'api/')
import bot


app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()

    if data['type'] == 'confirmation':
        return '5d3d07cf'
    if data['type'] == 'message_new' or data['type'] == 'message_event':
        if data['type'] == 'message_event':
            from_id = data['object']['user_id']
            text = data['object']['payload']['text']
        else:
            from_id = data['object']['message']['from_id']
            text = data['object']['message']['text']
        try:
            from_st, to_st = bot.parseMessage(text)
            trains = bot.getTrains(from_st, to_st)
            bot.send('\n'.join(trains), from_id, dumps({"buttons":[[{"action":{"type":"callback","label":"🔁 Повторить","payload":'"{\"text\": \"' + text + '\"}"'},"color":"secondary"}]],"inline":True}))
        except Exception as e:
            bot.send("К сожалению, я тебя не понимаю. Напиши путь в формате отправление > прибытие", from_id)
            return traceback.format_exc()
        

    return 'ok'
