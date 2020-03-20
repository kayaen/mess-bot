# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 22:03:36 2019

@author: Engin
"""

"""
This bot listens to port 5002 for incoming connections from Facebook. It takes
in any messages that the bot receives and echos it back.
"""

#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot
from pymessenger import Button
from pymessenger import Element
import os
import urllib

app = Flask(__name__)
ACCESS_TOKEN = 'EAADZA3ZB0wzgwBADZBeHCL6ezLFHRcwVSkP5DlxIeHmT8BXqZCmseHpNKW9OaZAZAjeky7cOCMg29tFiDQZCl0sPaxskOic3JnBZBGaiSvMxuvJ5ZAERHkD1qfcSISpBJ1JIc90HmD7zQO5UlZCnyZAR7V2rmaUnAoPjIDbzNc41FIbQgZDZD'
VERIFY_TOKEN = '123qwe'
#ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
#VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot(ACCESS_TOKEN)

def find_songName(keyW):
    # define empty list
    names = []
    # open file and read the content in a list
    data = urllib.request.urlopen("https://raw.githubusercontent.com/kayaen/mess-bot/master/listfile.txt") # it's a file like object and works just like a file
    for line in data: # files are iterable
        names.append(line.title().decode('latin-1'))
    
 #   with open('listfile.txt', 'r') as filehandle:  
 #       names = [current_place.rstrip() for current_place in filehandle.readlines()]
    
    foundedSongs =[]
    indx = 0
    for name in names:
        if does_contain_words(name,keyW):
            #print('Song No: ' + str(indx) + ': '+ name)
            foundedSongs.append('Song No: ' + str(indx) + ': '+ name + '\n')
        indx += 1
    
    return ''.join(foundedSongs)

def does_contain_words(sentence, wordsToCheck):
    if wordsToCheck.lower() in sentence.lower():
        return True
    return False    
    
#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    if 'hi' == message['message']['text'].lower():
                        buttons = []
                        button = Button(title='Arsenal', type='web_url', url='http://arsenal.com')
                        buttons.append(button)
                        button = Button(title='Other', type='postback', payload='other--')
                        buttons.append(button)
                        uu = 'http://capoeiralyrics.info/songs/a-mare-vazou-baixou.html'
                        button = Button(title='Other', type='web_url', url=uu)
                        buttons.append(button)                        
                        text = 'Select'
                        result = bot.send_button_message(recipient_id, text, buttons)
                        assert type(result) is dict
                        assert result.get('message_id') is not None
                        assert result.get('recipient_id') is not None
                    elif 'q' == message['message']['text'].lower():
                        uu = 'http://capoeiralyrics.info/songs/a-mare-vazou-baixou.html'
                        send_message(recipient_id, uu)                                          
                    elif 'w' == message['message']['text'].lower():    
                        imgurl = 'https://lh4.googleusercontent.com/-dZ2LhrpNpxs/AAAAAAAAAAI/AAAAAAAA1os/qrf-VeTVJrg/s0-c-k-no-ns/photo.jpg'
                        elements = []
                        element = Element(title="test", image_url=imgurl, subtitle="subtitle", item_url="http://arsenal.com")
                        elements.append(element)                        
                        bot.send_generic_message(recipient_id, elements)
                    elif 'e' == message['message']['text'].lower():                        
                        response = recipient_id
                        bot.send_action(recipient_id,'typing_on')
                        bot.send_text_message(recipient_id, response)
                    elif 'd' == message['message']['text'].lower():   
                        mm = {
                                'text': 'hello ' + str(recipient_id)
                            }
                        payload = {
                                'message': mm
                            }
                        response = send_info(recipient_id, payload)
                        
#                        bot.send_action(recipient_id,'typing_on')
                        bot.send_text_message(recipient_id, response)     
                    elif 'r' == message['message']['text'].lower():   
                        mm = {
                                "attachment":{
                                  "type":"image", 
                                  "payload":{
                                    "url":"https://lh4.googleusercontent.com/-dZ2LhrpNpxs/AAAAAAAAAAI/AAAAAAAA1os/qrf-VeTVJrg/s0-c-k-no-ns/photo.jpg", 
                                    "is_reusable": True
                                  }
                                }
                            }
                        payload = {
                                'message': mm
                            }
                        response = send_info(recipient_id, payload)
                    elif 't' == message['message']['text'].lower():   
                        # https://developers.facebook.com/docs/messenger-platform/send-messages/quick-replies
                        mm = {
                                "text": "Pick a color:",
                                "quick_replies":[
                                  {
                                    "content_type":"text",
                                    "title":"Red",
                                    "payload":"<POSTBACK_PAYLOAD>",
                                    "image_url":"http://example.com/img/red.png"
                                  },{
                                    "content_type":"text",
                                    "title":"Green",
                                    "payload":"<POSTBACK_PAYLOAD>",
                                    "image_url":"http://example.com/img/green.png"
                                  }
                                ]
                            }
                        payload = {
                                "messaging_type": "RESPONSE",
                                "message": mm
                            }
                        response = send_info(recipient_id, payload)
                    
                    elif 'y' == message['message']['text'].lower():   
                        rr = get_info(recipient_id)
                        print('name',rr['first_name'])
                        print('last name',rr['last_name'])
                        print('user id',rr['id'])
                        print('profile pic',rr['profile_pic'])
                    elif 'who' == message['message']['text'].lower():       
                        rr = get_info(recipient_id)
                        mm = {
                                "attachment":{
                                  "type":"image", 
                                  "payload":{
                                    "url":rr['profile_pic'], 
                                    "is_reusable": True
                                  }
                                }
                            }
                        payload = {
                                'message': mm
                            }
                        response = send_info(recipient_id, payload)
                    else:
                        #response_sent_text = message['message']['text']
                        response_sent_text = find_songName(message['message']['text'])
                        #response_sent_text = get_message()
                        send_message(recipient_id, response_sent_text)
                    
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    user_info = 'no attachment!!!'#bot.get_user_info(recipient_id)
                    send_message(recipient_id, str(user_info))
                    bot.send_action(recipient_id,'typing_on')
                    
                    response_sent_nontext = get_message()
                    send_message(recipient_id, response_sent_nontext)
                    #bot.send_attachment_url(recipient_id, message['message']['attachment']['type'], message['message']['attachment']['payload']['url'])
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


import requests
def get_info(recipient_id):
    params = {}
    params.update(bot.auth_args)
    graph_url = 'https://graph.facebook.com'
    request_endpoint = '{0}/{1}'.format(graph_url, recipient_id)
#    print(request_endpoint)
    response = requests.get(request_endpoint, params = params)
#    print(response)
    if response.status_code == 200:
        return response.json()

def send_info(recipient_id, payload):
    payload['recipient'] = {
            'id': recipient_id
        }
    payload['notification_type'] = "REGULAR"
    result = bot.send_raw(payload)
    print('result', result)
    return result

#chooses a random message to send to the user
def get_message():
    sample_responses = ["You \n\nare  \nstunning", "We're  \n\nproud of you.", "Keep\n on being you!", "We'\nre greatful to know you\n :)"]
    # return selected item to the user
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()