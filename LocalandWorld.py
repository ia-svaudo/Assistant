import logging
import platform
import subprocess
import sys
import time
import aiy.assistant.auth_helpers
from aiy.assistant.library import Assistant
import aiy.audio
import aiy.voicehat
from google.assistant.library.event import EventType
import random
time.sleep(20)
grade = 12
tscount = 0
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)
aiy.audio.set_tts_volume(25)

def power_off_pi():
    aiy.audio.say('Good bye!')
    subprocess.call('sudo shutdown', shell=True)


def reboot_pi():
    aiy.audio.say('See ya later aligata')
    subprocess.call('sudo reboot', shell=True)


def say_ip():
    ip_address = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True)
    aiy.audio.say('My IP address is %s' % ip_address.decode('utf-8'))


def process_event(assistant, event):
    global tscount
    status_ui = aiy.voicehat.get_status_ui()
    global grade 
    
    if event.type == EventType.ON_START_FINISHED:
        status_ui.status('ready')
        if sys.stdout.isatty():
            print('Say "OK, Google" then speak, or press Ctrl+C to quit...')
            aiy.audio.say('Break Time Bro')

    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        status_ui.status('listening')

    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
        print('You said:', event.args['text'])
        text = event.args['text'].lower()
        if "computer" in text:
            assistant.stop_conversation()
            aiy.audio.say('I have never heard of such thing!')
        elif text == 'tell me a quote':
            thing = random.randint(1,3)
            if thing == 1:
                assistant.stop_conversation()
                aiy.audio.say("Sammy was painting")
            elif thing == 2:
                assistant.stop_conversation()
                aiy.audio.say('Mr. Tom? Yes.')
                aiy.audio.say('IM GROWING', volume=70)
            elif thing == 3:
                assistant.stop_conversation()
                aiy.audio.say("Don't you have to go to class")

                
        
            
            
            
        elif text == "lol":
            assistant.stop_conversation()
            aiy.audio.say('Are you shure about that?')
            power_off_pi()
        elif text == 'reboot':
            assistant.stop_conversation()
            aiy.audio.say('Yur making me doing that?')
            reboot_pi()
        elif text == 'ip address':
            assistant.stop_conversation()
            aiy.audio.say('Ok...')
            say_ip()
        elif text == 'sammy':
            assistant.stop_conversation()
            aiy.audio.say('REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')
        
        elif "moonbase alpha" in text:
            assistant.stop_conversation()
            aiy.audio.say('Yoyu want moonbase alpha? OK: nine nine nine, nine nine nine, nine nine nine. question mark exclamation point question mark exclamation point question mark exclamation point uuuuuuuuuuu here comes another chinese earthquake ebrbrbrbrbrbrbrbrbrbrbrbrb', volume=75)
        elif "egg" in text or "yolk" in text:
            assistant.stop_conversation()
            aiy.audio.say("Don't hurt my brain with any more egg puns!")
        elif "caillou" in text:
            assistant.stop_conversation()
            aiy.audio.say("caillou go back to "+ str(grade-1) +"th grade")
            grade -= 1
            print(grade)
        elif "chicken" in text:
            assistant.stop_conversation()
            aiy.audio.say("CHICKEN STRIPS!")
            
            
        else:
            status_ui = aiy.voicehat.get_status_ui()
            if event.type == EventType.ON_START_FINISHED:
                status_ui.status('ready')
            if sys.stdout.isatty():
                print('Say "OK, Google" then speak, or press Ctrl+C to quit...')

            elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
                status_ui.status('listening')

            elif event.type == EventType.ON_END_OF_UTTERANCE:
                status_ui.status('thinking')

            elif (event.type == EventType.ON_CONVERSATION_TURN_FINISHED
                  or event.type == EventType.ON_CONVERSATION_TURN_TIMEOUT
                  or event.type == EventType.ON_NO_RESPONSE):
                status_ui.status('ready')

            elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
                sys.exit(1)
        tscount += 1
        

def main():
    global tscount
    if platform.machine() == 'armv6l':
        print('Cannot run hotword demo on Pi Zero!')
        exit(-1)

    credentials = aiy.assistant.auth_helpers.get_assistant_credentials()
    with Assistant(credentials) as assistant:
        for event in assistant.start():
            process_event(assistant, event)
            time.sleep(0.5)
            print(tscount)
            if tscount >= 20:
                aiy.audio.say("FUN TIME!!")
                tscount -= 1
                thing = random.randint(1,3)
                if thing == 1:
                    assistant.stop_conversation()
                    aiy.audio.say("Sammy was painting")
                elif thing == 2:
                    assistant.stop_conversation()
                    aiy.audio.say('Mr. Tom? Yes.')
                    aiy.audio.say('IM GROWING', volume=70)
                elif thing == 3:
                    assistant.stop_conversation()
                    aiy.audio.say("Don't you have to go to class")

while True:
    main()
    
        

