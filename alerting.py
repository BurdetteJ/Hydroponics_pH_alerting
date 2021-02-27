import time
import datetime
from twilio.rest import Client
import datetime as dt

# the following line needs your Twilio Account SID and Auth Token
client = Client("some_account_id", "some_auth_token")

    
    def __init__(self):
        self.lastSend = dt.datetime.now()
        # If the alert throttle is large but the pH is outside of desired range early on in the Polling, we should still alert.
        # This keeps track of whether we just started, allowing us to bypass the throttle for the very first alert
        self.justStarted = True
            
    def send_alert(self, lastLine, throttle):
        now = dt.datetime.now()
        if(now - self.lastSend).total_seconds() > throttle or self.justStarted:
            #print("Warning, ph is out of bounds: " + lastLine)
            client.messages.create(to="some_phone_num", 
                           #from_="some_other_phone_num", 
                           #body="pH level outside of accepted boundaries: " + lastLine)
            self.lastSend = now
        # We have alerted once, so now the throttle can kick in
        if self.justStarted:
            self.justStarted = False