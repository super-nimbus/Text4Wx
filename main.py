import requests
import json
import os
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse
from twilio import twiml
from flask import Flask, request
load_dotenv()

app = Flask(__name__)

@app.route('/app', methods = ['POST'])
def home():

    sender = request.form['From']
    body = request.form['Body']

    print(body)

    resp = MessagingResponse()
    message = Message()
    message.body(f'{sender} said {body}')
    resp.append(message)

    return str(resp)
    

###########################################################

#QUERY AIRPORT
# s_id = "CYYZ"


# wx_auth = os.getenv('wx_auth')

# headers = {
#     'Authorization': wx_auth
# }

# #GET METAR FOR QUERY
# response = requests.get(f"https://avwx.rest/api/metar/{s_id}", headers=headers)


# parse = json.dumps(response.json(), indent= 4, sort_keys= True)

# print(response.status_code)

###########################################################

#Twilio Set Up
# twil_id = os.getenv('twil_id')
# twil_auth_token = os.getenv('twil_auth_token')
# client = Client(twil_id, twil_auth_token)

# twil_num = os.getenv('twil_num')
# real_num = os.getenv('real_num')


# message = client.messages \
#                 .create(
#                      body="Testing for Outbound SMS from Text4Wx.",
#                      from_=twil_num,
#                      to=real_num
#                  )


if __name__ == "__main__":
    app.run(debug=True)