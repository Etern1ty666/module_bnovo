from collections import namedtuple

from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm, Form
from wtforms.fields import DateField, EmailField, TelField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields import DateField
from flask_datepicker import datepicker
import requests
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


url_public_api = 'https://public-api.reservationsteps.ru/v1/api/rooms/'
url_nevski = 'https://public-api.reservationsteps.ru/v1/api/rooms/?account_id=2923&dfrom=01-06-2022&dto=03-06-2022'

account_ids = ['2923', '492']

class Api:

    def __init__(self, name):
        self.name = name

    def get_rooms(self, url=url_public_api, account_id='2923', dfrom='01-06-2022', dto='03-06-2022') -> list:
        params = {'account_id': account_id,
                  'dfrom': dfrom,
                  'dto': dto
                  }
        response = requests.get(url, params=params)
        response_data = response.json()
        result = []
        for room in response_data['rooms']:
            result.append(room['name'])
        return response_data

    def get_token(self,
                  username='ivanchetvertkov@gmail.com',
                  password='W56pVfaVlR3q5ofZkXprZjT5jjYNAMqe',
                  url='https://api.reservationsteps.ru/v1/api/auth'
                  ) -> str:
        params = {"username": username,
                  "password": password
                  }
        response = requests.post(url, params=params)
        data = response.json()
        return data['token']

    def get_account_id(self, token, url='https://api.reservationsteps.ru/v1/api/auth'):
        params = {"token": token}
        response = requests.get(url, params=params)
        data = response.json()
        return data['user']['id']

api = Api('api')

Message = namedtuple('Message', 'text tag')
messages = []

@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')


@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html', messages=messages)


@app.route('/search', methods=['POST'])
def add_message():
    messages.clear()
    arrival = request.form['text']
    departure = request.form['tag']
    for account_id in account_ids:
        rooms = api.get_rooms(account_id=account_id, dfrom=arrival, dto=departure)
        for room in rooms['rooms']:
            try:
                for prices in room['plans']['2']['prices']:
                    price = room['plans']['2']['prices'][prices]
                    print(rooms['rooms'][0]['photos'][0]['thumb'])
                messages.append(room['name'] + ' ' + price)
            except:
                for prices in room['plans'][0]['prices']:
                    price = room['plans'][0]['prices'][prices]
                    print(rooms['rooms'][0]['photos'][0]['url'])
                messages.append(room["name"] + ' ' + price)
            #pictures.append(room['url'])
    #messages.append(Message(arrival, departure))
    return redirect(url_for('main'))


class DateForm(FlaskForm):
    entrydate = DateField('entrydate')
    submit = SubmitField('Submit')


@app.route('/2923', methods=['POST', 'GET'])
def nev():
    text = request.form['text']
    tag = request.form['tag']

    messages.append(Message(text, tag))

    return redirect(url_for('main'))

@app.route('/492', methods=['POST', 'GET'])
def lig():
    text = request.form['text']
    tag = request.form['tag']

    messages.append(Message(text, tag))

    return redirect(url_for('main'))

if __name__ == "__main__":
    app.run()