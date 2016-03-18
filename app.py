__author__ = 'Neal'
import os
from bottle import run, template, get, post, request
from model import City_choices, create_new
from bulk_mail import *

@get('/subscribe')
def form():
    return template('subscription',rows=City_choices.city_states)

@post('/confirm')
def submit2():
    email = request.forms.get('email_input')
    location = request.forms.get('location')
    response = (email,location)
    if response and create_new(response[0],response[1]):
        return template('confirmation')
    else:
        return template('exists')


@get('/emailcmd')
def push_email_cmd():
    return template('emailCmd')


@post('/pushEmailConf')
def push_email_confirmation():
    mail = WeatherEmailCmd()
    mail.prep_and_sendmail()
    return template('emailCmdConf')


if __name__ == '__main__':
    port = int(os.environ.get('PORT',8010))
    run(host='0.0.0.0', port=port, debug=True)