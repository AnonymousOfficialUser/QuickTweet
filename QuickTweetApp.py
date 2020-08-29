from twython import Twython
import tweepy
import pandas as pd
import os
from twilio import twiml
from flask import Flask, request, redirect
from flask_ngrok import run_with_ngrok
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

#import the required keys to tweet from auth.py
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)


#get the hashtags tweets
autho = tweepy.OAuthHandler(consumer_key, consumer_secret)
autho.set_access_token(access_token, access_token_secret)
api = tweepy.API(autho,wait_on_rate_limit=True)


#Sets up the connection between Twitter and your code
twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)


#Twilio account information
account_sid = 'abcdefghijklmnopqrstuvwxyz123456'
auth_token = 'abcdefghijklmnopqrstuvwxyz123456'
client = Client(account_sid, auth_token)


app = Flask(__name__)
run_with_ngrok(app)


#initialize the message body to be sent
message_body = ""


#send, tweet, recieve
@app.route("/sms", methods = ['GET', 'POST'])
def sms_reply():
    global message_body
    
    #get the text sent from users SMS
    message_body = request.form['Body']

    resp = MessagingResponse()
    
    #check if the user wants to tweet or find tweet
    if message_body[0:8] != "~hashtag":
        
        
        #post the tweet 
        twitter.update_status(status=message_body)
        
        
        #confirmation in the editor
        print("Tweeted: " + message_body) 
        
        
        #confirmation of tweet sent back to the users phone via SMS
        message = client.messages.create(to='+321234567890',from_='+210987654321',body="Tweet Sent!")
        
        
    else:
        bodytext = ""
        print("Got request for hashtag")
        
        
        #search and find the top tweets with the requested hashtag and store in variable bodytext
        for tweet in tweepy.Cursor(api.search,q=str(message_body[9::]),count=1, lang="en").items():
            bodytext += str(tweet.text) + "\n" 
        print(bodytext)
         
         
        #connection from Twilio number to users number to send back the hashtag tweets
        message = client.messages.create(to='+321234567890',from_='+210987654321',body=bodytext)
        print(message.sid)

    return "Python Back-end for twitter SMS client."

if __name__ == "__main__":
    app.run()
