from twilio.rest import Client

def NewTwilioConnection():
    account_sid = 'AC61e7581c067d442aba141a1314b2a330'
    auth_token = 'd3bb7adb060259cee3eafd6616c827c9'
    client = Client(account_sid, auth_token)
    return client

class TwilioHandler:
    client = None
    def __init__(self):
        account_sid = 'AC61e7581c067d442aba141a1314b2a330'
        auth_token = 'd3bb7adb060259cee3eafd6616c827c9'
        TwilioHandler.client = Client(account_sid, auth_token)
    
    def sendMsg(self, to, message):
       TwilioHandler.client.messages.create(
        from_='whatsapp:+14155238886',
        body= message,
        to=to
    )