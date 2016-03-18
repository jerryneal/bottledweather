***viyo Weather App by Neal - "bottledweather"

Email application that allows a user to subscribe and then later gets sent emails detailing
weather corresponding to place in point.

1. To run the app use
   First download modules needed for app can be found on requirements.txt

   Admin:Gopher$  pip install bottle
   Admin:Gopher$  pip install sqlalchemy
   Admin:Gopher$  pip install sqlite3


2. Go open the bulk_mail.py file and enter the appropriate senders user_name, password and
   "SMTP" protocal for the email

    Admin:Gopher$ cat bulk_mail.py
    
             self.sender_email =     'happystpatts@gmail.com'#e.g patrick@gmail.com
             self.sender_pass =      '########'       
             self.sender_smtp_gateway = 'smtp.gmail.com' #e.g smtp.gmail.com -> Gmail user account,
                                                          #   smtp.live.com -> Live user account
    Save and continue!
    (To be Improved)

2. Then run python app.py. Should like this below.

    Admin:Gopher$ python app.py

            Bottle v0.12.3 server starting up (using WSGIRefServer())...
            Listening on http://0.0.0.0:8010/
            Hit Ctrl-C to quit.

3.  Then go over to your localwebsite and use the following links to get to your pages

           localhost:8010/subscribe - Enter your valid email and scroll down to select email
                                      Hit "Subscribe" when done and you should get a confirmation page.
           localhost:8010/emailcmd - Push the "Send Email" to send the bulk email and you should
                                     get a confirmation page

4.   Improvements(Future Use)
	            1. Include more buttons to improve moving in between pages.
	            2. Get a reliable source for cities in the US. Best source was 288 but there could be more.
	            3. Make new table in db to include cities, seperate logs for app and db and track userlytics
	            4. Wake up and artist and improve the colors on UI. I know.
	            5. Have user input user_name and password in UI instead of in code.
