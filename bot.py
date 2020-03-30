from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import csv
import urllib.request
from collections import defaultdict

url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
filename = 'us-states.csv'
urllib.request.urlretrieve(url, filename)

dd = {}
state_list = []

# Build dictionary from url
with open(filename) as csv_file:

    state_tracker = 0
    for row in csv_file:
        my_list = row.split(",")
        if my_list[1] not in dd.keys():
            dd[my_list[1] ] = 5;
        if my_list[1] in dd.keys():
            dd[ my_list[1] ] = my_list[3]


app = Flask(__name__)


@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    if incoming_msg:
        responded = True
        if str(incoming_msg).lower() in str(dd.keys()).lower():
            state = str(incoming_msg).capitalize()
            msg.body(state + " has " + str( dd[state] ) + " cases as of today.")
        else:
            print(str(incoming_msg))
            msg.body("Enter a valid state name.")

    return str(resp)

if __name__ == "__main__":
    app.run()
