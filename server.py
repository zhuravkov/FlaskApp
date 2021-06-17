import datetime
import time
from flask import abort, jsonify

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import defaultload

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bot.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    text = db.Column(db.String(300), nullable=False)
    time = db.Column(db.Float)
    def __repr__(self):
        return f'({datetime.datetime.fromtimestamp(self.time).strftime("%H:%M:%S")} {self.name} {self.text} )'


@app.route("/")
def hello():
    mess_db=Message.query.all()
    for mes in mess_db:
        print(mes)
    return str(mess_db)  #TODO ВЫДАТЬ обекты из ДБ


@app.route("/status")
def status():
    users = set()

    for message in Message.query.all():
        users.add(message.name)

    return {
        'status': True,
        'time': datetime.datetime.fromtimestamp(time.time()),
        'time2': datetime.datetime.now().strftime('%H:%M:%S'),
        'messages': len(Message.query.all()),
        'users': len(users)

    }


@app.route("/send", methods=['POST'])
def send_message():
    data = request.json  # TODO valid
    if not isinstance(data, dict):
        return abort(400)
    if 'name' not in data or 'text' not in data:
        return abort(400)

    name = data['name']
    text = data['text']

    if not isinstance(name, str) or not isinstance(text, str):
        return abort(400)

    if not (0 < len(name) <= 128):
        return abort(400)
    if not (0 < len(text) <= 128):
        return abort(400)

    # ИДЕМ в БД
    message_base = Message(name=name, text=text, time=float(time.time()))
    try:
        db.session.add(message_base)
        db.session.commit()
        print("Добавлено")
        return {'ok': True}
    except:
        print("Не добавлено")
        return {'ok': False}

@app.route("/messages")
def get_messages():
    try:
        after = float(request.args['after'])  # получает параметр из запроса ../messages?after=0
    except:
        return abort(400)

    messages = []
    for message in Message.query.all():
        if message.time > after:
            messages.append({
                'name': message.name,
                'text': message.text,
                'time': message.time
            })
    return {'messages': messages[:50]} # отдает первых 50 сообщений


app.run()
