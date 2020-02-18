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

    query = body.split()

    r_type = query[0]
    r_loc = query[1]

    print(r_type)
    print(r_loc)

    resp = MessagingResponse()
    message = Message()
    message.body(getReport(r_loc, r_type))
    resp.append(message)

    return str(resp)
    

###########################################################

#QUERY AIRPORT

def getReport(r_loc, r_type):


    print(r_type)
    print(r_loc)

    wx_auth = os.getenv('wx_auth')

    headers = {
        'Authorization': wx_auth
    }

    print(f"https://avwx.rest/api/{r_type.lower()}/{r_loc.upper()}")

    #GET METAR FOR QUERY
    response = requests.get(f"https://avwx.rest/api/{r_type.lower()}/{r_loc.upper()}", headers=headers)

    print(response) 

    parse = response.json()

    print(parse['raw'])
    return(parse['raw'])

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