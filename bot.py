from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

import csv
import requests

import urllib.request

from collections import defaultdict

#url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=MSFT&apikey=demo&datatype=csv'

url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
filename = 'us-states.csv'
urllib.request.urlretrieve(url, filename)

dd = {}
state_list = []

with open(filename) as csv_file:

    state_tracker = 0
    for row in csv_file:

        my_list = row.split(",")
        print(my_list)
        if my_list[1] not in dd.keys():
            dd[my_list[1] ] = 5;


        if my_list[1] in dd.keys():
            dd[ my_list[1] ] = my_list[3]
        
    print ("Resultant dictionary", str(dd) ) 




app = Flask(__name__)


@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    # if 'quote' in incoming_msg:
    #     # return a quote
    #     r = requests.get('https://api.quotable.io/random')
    #     if r.status_code == 200:
    #         data = r.json()
    #         quote = f'{data["content"]} ({data["author"]})'
    #     else:
    #         quote = 'I could not retrieve a quote at this time, sorry.'
    #     msg.body(quote)
    #     responded = True
    # if 'cat' in incoming_msg:
    #     # return a cat pic
    #     msg.media('https://cataas.com/cat')

    if incoming_msg:
        responded = True
        if str(incoming_msg).lower() in str(dd.keys()).lower():
            state = str(incoming_msg).capitalize()
            msg.body(state + " has " + str( dd[state] ) + " cases as of today.")
        else:
            print(str(incoming_msg))
            msg.body("Enter a valid state name.")


    





    # if 'mudbone' in incoming_msg:
    #     msg.media('https://pbs.twimg.com/profile_images/726295664032772098/fe1hGAKb_400x400.jpg')
    #     responded = True

    # if not responded:
    #     msg.body('I only know about famous quotes and cats, sorry!')

    return str(resp)

if __name__ == "__main__":
    app.run()
