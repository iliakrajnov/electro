from flask import Flask, request
import bot


app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()

    if data['type'] == 'confirmation':
        return '5d3d07cf'
    if data['type'] == 'message_new':
        from_id = data['object']['message']['from_id']
        try:
            from_st, to_st = bot.parseMessage(data['object']['message']['text'])
            trains = bot.getTrains(from_st, to_st)
            bot.send('\n'.join(trains), from_id)
        except Exception as e:
            return str(e)
            bot.send("К сожалению, я тебя не понимаю 2", from_id)

    return 'ok'