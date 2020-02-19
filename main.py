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
    #Define Response
    resp = MessagingResponse()
    message = Message()

    #Isolate Query Information
    sender = request.form['From']
    body = request.form['Body']

    query = body.split()

    #Determine Report Type
    r_type = query[0].lower()

    #Determine Station ID
    r_loc = 0

    if len(query) > 1:
        r_loc = query[1].upper()


    #Determine Plaintext
    pt = 0
    if len(query) == 3 and query[2].lower() == 'pt':
        pt = True

    print(r_type)

    #Query for help
    #************************************************************************
    #CURRENT ISSUE: TWILIO API HAS AN OVERRIDING OPT-OUT FUNCTION FOR 'HELP'
    #************************************************************************
    if r_type == 'help':
        body ="Text4Wx\n-------------\n<sample help instructions here"
        message.body(body)
        resp.append(message)
        return str(resp)


    #Query for METAR/TAF
    if r_type == 'metar' or r_type == 'taf' or r_type == 'm' or r_type == 't':
        message.body(getReport(r_loc, r_type, pt))
        resp.append(message)
        return str(resp)


    #Query for Station Info
    if r_type == 'info' or r_type == 'i':
        r_type = 'station'
        message.body(getReport(r_loc, r_type, pt))
        resp.append(message)
        return str(resp)


    #Invalid Query
    message.body("""Sorry, I didn't catch that.\nTry searching again. Type "HELP" for a list of commands.""")
    resp.append(message)
    return str(resp)
    

###########################################################

def getReport(r_loc, r_type, pt):


    #print(r_type)
    #print(r_loc)

    wx_auth = os.getenv('wx_auth')

    headers = {
        'Authorization': wx_auth
    }

    #print(f"https://avwx.rest/api/{r_type.lower()}/{r_loc.upper()}")

    #GET REPORT AS QUERIED
    response = requests.get(f"https://avwx.rest/api/{r_type}/{r_loc}", headers=headers)

    print(response) 

    parse = response.json()

    print(r_type)
    if (r_type == 'station'):
        body = f"Name: {parse['name']}\nLocation: {parse['city']}\nCountry: {parse['country']}\nICAO ID: {parse['icao']}"
        print(body)
        return(body)
    
    else:
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