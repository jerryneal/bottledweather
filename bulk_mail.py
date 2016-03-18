__author__ = 'Kanyu'

from model import get_data_in_db
import urllib2, json
from urllib2 import Request
from datetime import datetime
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from smtplib import SMTP

'''
1 . To run this, first include the following delays in the def _init_ section

'''
class WeatherEmailCmd():

    def __init__(self):
        self.sender_email = 'happystpatts@gmail.com'    #e.g mike@klaviyo.com
        self.sender_password =  '########' #'leprecheuens'
        self.sender_smtp_gateway = 'smtp.gmail.com'#e.g smtp.gmail.com -> Gmail user account,
                                                   #    smtp.live.com -> Live user account

    def sending_the_email(self,user_email,subject,city, state, current_temp, weather_description, icon_for):
        """
        :param user_email: User Email
        :param subject: Subject of email
        :param city: City of location
        :param state: State of location in the US
        :param current_temp: Current temperature of location
        :param weather_description: As is
        :param icon_for: Icon going with this
        :return: Email should be sent
        """
        # Send an HTML email with an embedded image and a plain text message for
        # email clients that don't want to display the HTML.


        strFrom = self.sender_email
        strTo = user_email #

        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = subject
        msgRoot['From'] = strFrom
        msgRoot['To'] = strTo
        msgRoot.preamble = 'This is a multi-part message in MIME format.'

        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        msgText = MIMEText('This is the alternative plain text message.')
        msgAlternative.attach(msgText)

        msgText = MIMEText('Current weather in <b> {} <i> {} </i> is {}</b> and temperature '
                           'is {}F!<br><img src="cid:image1"><br> Thanks! With love from Klaviyo! '
                           .format(city,state,weather_description,current_temp), 'html')
        msgAlternative.attach(msgText)


        fp = open('icons/{}.png'.format(icon_for), 'rb') #Place Image here
        msgImage = MIMEImage(fp.read())
        fp.close()


        msgImage.add_header('Content-ID', '<image1>')
        msgRoot.attach(msgImage)


        smp = SMTP('smtp.gmail.com', 587)
        smp.ehlo()
        smp.starttls()
        smp.ehlo()
        smp.login(self.sender_email, self.sender_password)
        smp.sendmail(strFrom, strTo, msgRoot.as_string())
        smp.quit()

    def prep_and_sendmail(self):

        current_time = datetime.now().time().hour in range(8, 20)
        almanac_temp = 'temp_high' if current_time else 'temp_low'

        for i in get_data_in_db():
            user_email = i[0]
            city = i[1]
            state = i[2]

            api_url_name = ("http://api.wunderground.com/api/77f11864d200c21d/conditions/almanac/q/%s/%s.json" % (state, city)).replace(' ', '_')

            try:
                req = Request(api_url_name)
            except IOError as e:
                print(city,state + ' not providing a valid URL, continuing without email')
                continue

            esn = urllib2.urlopen(req)
            weather_dict = json.loads(esn.read().decode('utf-8'))
            if 'error' in weather_dict:
                print(city,state + ' Providing Invalid JSON response')
                continue

            current_temp = float(weather_dict['current_observation']['temp_f'])
            normal_temp = float(weather_dict['almanac'][almanac_temp]['normal']['F'])
            weather_description = weather_dict['current_observation']['weather']
            subject = "Enjoy a discount on us."

            if any(w in weather_description for w in {'Drizzle', 'Rain', 'Snow', 'Ice', 'Hail', 'Mist',
                        'Thunderstorm', 'Squalls', 'Sandstorm' }) or current_temp - normal_temp <= -5.0:
                subject = "Not so nice out? That's okay, e" + subject[1:]
            elif weather_description == 'Clear' or current_temp - normal_temp >= 5.0:
                subject = "It's nice out! " + subject

            icon_for = 0
            if 'Thunderstorm' in weather_description:
                icon_for = 6
            elif 'Rain' in weather_description or 'Drizzle' in weather_description:
                icon_for = 7 if 'Freezing' in weather_description else (5 if current_time else 11)
            elif 'Snow' in weather_description:
                icon_for = 8 if current_time else 12
            elif weather_description == 'Clear':
                icon_for = 1 if current_time else 9
            elif 'Cloud' in weather_description:
                icon_for = 3 if current_time else 10
            elif weather_description == 'Overcast':
                icon_for = 2

            #print user_email,subject,city, state, current_temp, weather_description, icon_for
            self.sending_the_email(user_email,subject,city, state, current_temp, weather_description, icon_for)

