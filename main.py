'''
Выполнить Light со следующим изменением:
реализовать страницу определения основных навыков по определенным вакансиям (взаимодействие с hh api).
Например, на странице представлена форма:
город, название вакансии, кнопка. По нажатию пользователю будет показана
средняя ЗП по данной вакансии в этом городе и список релевантных навыков
'''

from flask import Flask
from flask import render_template, url_for, request
import flask
import datetime
from person import Person
from my_lib import get_week
#from parser import Parser
from parser_price import Parser_price
#import requests

pers = Person()

app = Flask( __name__ )

@app.route("/")
@app.route("/index/")
def main_win():
    today = datetime.datetime.today()
    scw = get_week( int( today.strftime('%w') ) )
    return render_template( 'index.html',  curdate = today.strftime('%d-%m-%Y'), curweek = scw )

@app.route("/personal/")
def pers_win():
    dic={
    'photo' : pers.get_photo(),
    'fio' : pers.get_name() + ' ' + pers.get_otch() + ' ' + pers.get_fam(),
    'birthday' : pers.get_birthday(),
    'attach': pers.get_attach()
    }
    return render_template( 'personal.html', **dic )

@app.route("/parser/" )
def parser():
    return render_template( 'parser_form.html' )

@app.route("/price_apartments/", methods=['POST'] )
def price():
    region = request.form['region']
    parser = Parser_price( region )
    dicMin = parser.cost_min(rej='dic')
    dicMax = parser.cost_max(rej='dic')

    dic={}
    dic['region'] = region
    dic['minprice'] = dicMin['price']
    dic['mincity'] = dicMin['city']
    dic['mincharact'] = dicMin['address']+'; '+dicMin['region']+'; '+dicMin['characteristic']
    dic['maxprice'] = dicMax['price']
    dic['maxcity'] = dicMax['city']
    dic['maxcharact'] = dicMax['address'] + '; ' + dicMax['region'] + '; ' + dicMax['characteristic']

    return render_template( 'price_apartments.html', **dic )

# ********************************************************************
if __name__ == "__main__":
    #print( 'версия:', flask.__version__ )
    app.run( debug=True )