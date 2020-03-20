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
import os
import urllib
import requests

app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot(ACCESS_TOKEN)

def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

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
#    print('result', result)
    return result


def give_randomSong():
    names = []
    links = []
    foundedSongs =[]
    # open file and read the content in a list
    data = urllib.request.urlopen("https://raw.githubusercontent.com/kayaen/mess-bot/master/lyrics_name_link.csv")
    
    for line in data: # files are iterable
        parsedStr = str(line.title().decode('utf-8')).split(',')        
        names.append(parsedStr[0])
        links.append(parsedStr[1][:-2].lower())
        
    indx = random.randint(0,len(names))
    foundedSongs.append('Song No: ' + str(indx) + ': '+ names[indx] + '\n')
    foundedSongs.append(links[indx]+'\n'+ '\n')
        
    return ''.join(foundedSongs)
    
def find_songName(keyW):
    # define empty list
    foundedSongs =[]
    # open file and read the content in a list
    data = urllib.request.urlopen("https://raw.githubusercontent.com/kayaen/mess-bot/master/lyrics_name_link.csv")
    indx = 0    
    for line in data: # files are iterable
        parsedStr = str(line.title().decode('utf-8')).split(',')
        
        if does_contain_words(parsedStr[0], keyW):
            #print('Song No: ' + str(indx) + ': '+ name)
            foundedSongs.append('Song No: ' + str(indx) + ': '+ parsedStr[0] + '\n')
            foundedSongs.append(parsedStr[1][:-2].lower()+'\n'+ '\n')
        indx += 1

    if 0 == len(foundedSongs):
        foundedSongs.append('There is no song includes: '+keyW)
        
    return ''.join(foundedSongs)
    

def does_contain_words(sentence, wordsToCheck):
    wordList = wordsToCheck.split(',')
    for word in wordList:
        if word.lower() not in sentence.lower():
            return False
    return True

def design_welcome_template():
    b1 = {
            "type":"postback",
            "payload":"FIND_SONG_PAYLOAD",
            "title":"Search a song"
        }
    b2 = {
            "type":"postback",
            "payload":"RANDOM_SONG_PAYLOAD",
            "title":"Give me a random song"
        }
    b3 = {
            "type":"web_url",
            "url":"https://kayaen.github.io/",
            "title":"Learn More About Bot"
        }

    templateDesing = {
        "message": {
                "attachment":{
                  "type":"template",
                  "payload":{
                    "template_type":"button",
                    "text":"What do you want to do next?",
                    "buttons":[b1, b2, b3]
                  }
                }
            }
        }
    return templateDesing

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
#       print(output)
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    if 'hi' == message['message']['text'].lower():
                        userInfo = get_info(recipient_id)
                        bot.send_action(recipient_id,'typing_on')
                        welcomeMessage = {
                                'message': {'text': 'Welcome ' + userInfo['first_name'] +' '+ userInfo['last_name']}
                            }
                        send_info(recipient_id, welcomeMessage)
                        bot.send_action(recipient_id,'typing_on')
                        
                        welcomeTemplate = design_welcome_template()
                        send_info(recipient_id, welcomeTemplate)
                        
                    else:
                        #response_sent_text = find_songName(message['message']['text'])
                        infoMessage = {
                                'message': {'text': find_songName(message['message']['text'])}
                            }
                        send_info(recipient_id, infoMessage)                        
                    
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    bot.send_action(recipient_id,'typing_on')
                    infoMessage = {
                                'message': {'text': "Currently, we don't support media, but it will be available soon!"}
                            }
                    send_info(recipient_id, infoMessage)
                    #bot.send_attachment_url(recipient_id, message['message']['attachment']['type'], message['message']['attachment']['payload']['url'])


            elif message.get('postback'):

                recipient_id = message['sender']['id']                
                if 'RANDOM_SONG_PAYLOAD' == message['postback']['payload']:
                    infoMessage = {
                                'message': {'text': give_randomSong()}
                            }
                    send_info(recipient_id, infoMessage)                        
                    
                elif 'FIND_SONG_PAYLOAD' == message['postback']['payload']:
                    infoMessage = {
                                'message': {'text': 'You can write desired keywords as comma seperated'}
                            }
                    send_info(recipient_id, infoMessage)

                    
    return "Message Processed"

if __name__ == "__main__":
    app.run()