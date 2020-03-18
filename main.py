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

@app.route('/sms/', methods = ['POST'])
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
    try:
        r_loc = query[1].upper()
    except:
        r_loc = False 

    
    #Determine Plaintext
    try:
        if query[-1].lower() == 'pt':
            pt = True
        else:
            pt = False
    except:
        pt = False

    print(r_type)

    #Query for help: Configured with Twilio Advanced Opt-Out --> see Twilio Console
    if r_type == 'help':
        return 0


    #Query for METAR/TAF
    if r_type == 'metar' or r_type == 'taf' or r_type == 'm' or r_type == 't':
        if not r_loc:
            message.body(f"Please enter a Station ID")

        else:
            if r_type == 'm':
                r_type = 'metar'
                
            if r_type == 't':
                r_type = 'taf'
            
            try:
                message.body(getReport(r_loc, r_type, pt))

            except:
                message.body(f"Sorry, no reporting information found for {r_loc}")

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

# NEED TO SET UP PLAINTEXT FUNCTIONALITY
# Get Report from API
def getReport(r_loc, r_type, pt):


    #print(r_type)
    #print(r_loc)
    print(pt)

    wx_auth = os.environ.get('WX_AUTH')

    headers = {
        'Authorization': wx_auth
    }

    #GET REPORT AS QUERIED
    response = requests.get(f"https://avwx.rest/api/{r_type}/{r_loc}", headers=headers)

    print(response) 

    parse = response.json()

    print(r_type)

    if (r_type == 'station'):
        
        
        latitude = '{:4.7}'.format(parse['latitude'])
        longitude = '{:4.7}'.format(parse['longitude'])

        runways = ""
        for runway in parse['runways']:
            if (int(runway['ident1'][:2]) + 18 == int(runway['ident2'][:2]) or int(runway['ident1'][:2]) == int(runway['ident2'][:2]) + 18):
                runways = runways + f"{runway['ident1']}/{runway['ident2']}: {runway['length_ft']} by {runway['width_ft']} ft\n"

        body = f"Name: {parse['name']}\nLocation: {parse['city']}\nCountry: {parse['country']}\n\nICAO ID: {parse['icao']}\nLat/Long: {latitude}, {longitude}\nField Elevation (ft): {parse['elevation_ft']}\n\nRunways:\n{runways}"
        print(body)
        return(body)
    
    elif (r_type == 'metar' and pt):
        clouds = ""

        for layer in parse['clouds']:
            clouds = clouds + layer['repr'] + ', '

        clouds = clouds[:-2]
        
        print(clouds)

        body = f"Station: {r_loc.upper()}\nIssued: {parse['time']['dt']}\nWinds: {parse['wind_speed']['repr']} knots from {parse['wind_direction']['repr']} degrees\nVisibility: {parse['visibility']['repr']} statute miles\nCloud layers: {clouds}\nTemperature: {parse['temperature']['repr']} C\nDewpoint: {parse['dewpoint']['repr']} C\nAltimeter setting: {parse['altimeter']['value']}\n"
        
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


@app.route('/')
def index():
    return "<h1>Welcome to the Text4Wx Page!</h1>"

if __name__ == "__main__":
    app.run(threaded=True, port=5000)