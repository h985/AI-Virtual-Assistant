
#Project Jane
import speech_recognition as sr 
import datetime
import urllib
import re
from guess_indian_gender import IndianGenderPredictor
import speedtest 
from googletrans import Translator
import wikipedia
from gtts import gTTS 
import pyttsx3
import webbrowser
import pytz
from twilio.rest import TwilioRestClient
import random
import os
import json
import calendar
import smtplib
from PIL import Image, ImageGrab
import requests
from difflib import get_close_matches
import time
from urllib.request import urlopen 
import sys
import pyaudio
from pyowm import OWM
import warnings
import urllib.parse
import subprocess 
from getpass import getpass
import wolframalpha
from clint.textui import progress  
import ctypes 
import threading 
import pyjokes
import operator
from pygame import mixer 
import winshell 
import feedparser 
import shutil 
import sounddevice, matplotlib.pyplot as plt, socket
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import tkinter 
import win32com.client as wincl
import geocoder
from bs4 import BeautifulSoup as soup
import urllib.request
import youtube_dl
import socket  


#Text To Speech

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices)
newVoiceRate = 170
engine.setProperty('rate',newVoiceRate)
engine.setProperty('voice',voices[1].id

MONTHS = ["january", "february", "march", "april", "may", "june","july", "august", "september","october", "november", "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_EXTENTIONS = ["rd", "th", "st", "nd"]
WAKE = "wake up" or 'get up'
g = geocoder.ip('me')
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def speak(audio):  #here audio is var which contain text
    engine.say(audio)
    engine.runAndWait()
def check_internet_connection():
    try:
        host = socket.gethostbyname(REMOTE_SERVER)
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except:
        pass
    return False
                   
def changePassword():
        pword = getpass('\n\tEnter New Password : ')
        print('\n\tPassword Updated Successfully!')
        speak('Password Updated Successfully.')
        print("\n\tShould I Show It?")
        speak("Should I Show It?")
        reply = takecommand().lower()
        if "yes" in reply or 'ok' in reply or 'show' in reply or 'do' in reply:
            print('\n\tShowing Password!')
            speak('Okay! Showing!')
            print( f'\n\tPassword: "{pword}"')
        else:
            print( "\n\tOkay, Nevermind!")
            speak("Okay, Nevermind!")

def authenticate_google():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service

def get_events(day, service):
    # Call the Calendar API
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end = end.astimezone(utc)
    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end.isoformat(),
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak('No upcoming events found.')
    else:
        speak(f"You have {len(events)} events on this day.")

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time = str(start.split("T")[1].split("-")[0])  # get the hour the event starts
            if int(start_time.split(":")[0]) < 12:  # if the event is in the morning
                start_time = start_time + "am"
            else:
                start_time = str(int(start_time.split(":")[0])-12)  # convert 24 hour time to regular
                start_time = start_time + "pm"  

            speak(event["summary"] + " at " + start_time)
                   
def get_date(query):
    query = takecommand().lower()
    today = datetime.date.today()

    if query.count("today") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in query.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENTIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass
    # THE NEW PART STARTS HERE
    if month < today.month and month != -1:  # if the month mentioned is before the current month set the year to the next
        year = year+1

    # This is slighlty different from the video but the correct version
    if month == -1 and day != -1:  # if we didn't find a month, but we have a day
        if day < today.day:
            month = today.month + 1
        else:
            month = today.month

    # if we only found a dta of the week
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week

        if dif < 0:
            dif += 7
            if query.count("next") >= 1:
                dif += 7

        return today + datetime.timedelta(dif)

    if day != -1:  # FIXED FROM VIDEO
        return datetime.date(month=month, day=day, year=year)

def getLangcode(dest):
    LANGUAGES = {
         'af' : 'Afrikaans',
         'sq' : 'Albanian',
         'ar' : 'Arabic',
         'hy' : 'Armenian',
         'bn' : 'Bengali',
         'ca' : 'Catalan',
         'zh' : 'Chinese',
         'hr' : 'Croatian',
         'cs' : 'Czech',
         'da' : 'Danish',
         'nl' : 'Dutch',
         'en' : 'English',
         'eo' : 'Esperanto',
         'fi' : 'Finnish',
         'fr' : 'French',
         'de' : 'German',
         'el' : 'Greek',
         'hi' : 'Hindi',
         'hu' : 'Hungarian',
         'is' : 'Icelandic',
         'id' : 'Indonesian',
         'it' : 'Italian',
         'ja' : 'Japanese',
         'km' : 'Khmer',
         'ko' : 'Korean',
         'la' : 'Latin',
         'lv' : 'Latvian',
         'mk' : 'Macedonian',
         'no' : 'Norwegian',
         'pl' : 'Polish',
         'pt' : 'Portuguese',
         'ro' : 'Romanian',
         'ru' : 'Russian',
         'sr' : 'Serbian',
         'si' : 'Sinhala',
         'sk' : 'Slovak',
         'es' : 'Spanish',
         'sw' : 'Swahili',
         'sv' : 'Swedish',
         'ta' : 'Tamil',
         'th' : 'Thai',
         'tr' : 'Turkish',
         'uk' : 'Ukrainian',
         'vi' : 'Vietnamese',
         'cy' : 'Welsh'
    }
    try:
        key_list = list(LANGUAGES.keys())
        val_list = list(LANGUAGES.values())
        return key_list[val_list.index(dest)]
    except :
        speak("I couldn't find the language you mentioned..\n"
                       "please repeat the langauage you want me to translate in..")
        dest = takecommand().lower()
        return getLangcode(dest)
                   
def speaks(input_text,lang='en'):
    tts=gTTS(text=input_text,lang=lang)
    filename = ('voice.mp3')
    tts.save(filename)
    playsound.playsound(filename,True)
    os.remove(filename)

def langTranslator(statement,dest):
    print("text to be translated it "+ statement)
    print("dest :" + dest)
    destination_lang_code= getLangcode(dest)
    print("destination_lang_code"+destination_lang_code)
    translator = Translator()
    output = translator.translate(statement , dest=destination_lang_code)
    print(output)
    speaks(output.text, destination_lang_code)
    return output.text
                   
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("I am Jane. An A I based computer program but i can help you lot like a your close friend ! i promise you ! Simple try me to give simple command ! like playing music or video from your directory! i also play video and song from web or online ! i can also entertain you i so think you Understand me ! ok Lets Start")
#now convert audio to text
# 
def wallpaper():
    wall_dir = 'C:\\Users\\Harsh\\Desktop\\jarvis\\wallpapers'
    wal = os.listdir(wall_dir)
    #print(songs)
    d = random.choice(wal)    
    wall = os.path.join(wall_dir, d)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, wall, 0)
    speak('Wallpaper change successfully')
                   
def you(textToSearch):
    query = urllib.parse.quote(textToSearch)
    url = "https://www.youtube.com/results?search_query=" + query
    webbrowser.open(url)
    #response = urlopen(url)
    #html = response.read()
    #soup = BeautifulSoup(html, "lxml")
    #flag = 0
    #search_results=re.findall('href=\"\\/watch\\?v=(.{11})', html.decode())
    #print(search_results)
    #webbrowser.get('chrome').open_new_tab('http://youtube.com/watch?v=' + search_results[0])


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=1)
        print("I am Listening....")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...") 
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")

    except Exception as e:
        print(e)    
        print("Say that again please...")  
        return "None"
    return query

def takescreenshot():
    image = ImageGrab.grab()
    image.show()

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your email id', 'your email password')
    server.sendmail('your email id', to, content)
    server.close()

        


def weather():
    api_url = "https://fcc-weather-api.glitch.me/api/current?lat=" + \
        str(g.latlng[0]) + "&lon=" + str(g.latlng[1])

    data = requests.get(api_url)
    data_json = data.json()
    if data_json['cod'] == 200:
        main = data_json['main']
        wind = data_json['wind']
        weather_desc = data_json['weather'][0]
        speak(str(data_json['coord']['lat']) + 'latitude' + str(data_json['coord']['lon']) + 'longitude')
        speak('Current location is ' + data_json['name'] + data_json['sys']['country'] + 'dia')
        speak('weather type ' + weather_desc['main'])
        speak('Wind speed is ' + str(wind['speed']) + ' metre per second')
        speak('Temperature: ' + str(main['temp']) + 'degree celcius')
        speak('Humidity is ' + str(main['humidity']))

def speak_news():
    url = 'http://newsapi.org/v2/top-headlines?sources=the-times-of-india&apiKey=4e2e0fce0d224ee9bf8da3aefa819ca3'
    news = requests.get(url).text
    news_dict = json.loads(news)
    arts = news_dict['articles']
    speak('Source: The Times Of India')
    speak('Todays Headlines are..')
    for index, articles in enumerate(arts):
        speak(articles['title'])
        if index == len(arts)-1:
            break
        speak('Moving on the next news headline..')
    speak('These were the top headlines, Have a nice day Sir!!..')
                   
def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"  
    with open(file_name, "w") as f:
        f.write(query)

    subprocess.Popen(["notepad.exe", file_name])

    
def dictionary(word):
    word = word.lower()
    with open('C:\\Users\\Harsh\\Desktop\\Jarvis\\data.json') as f:
        data = json.load(f)
    if word in data:
        speak(data[word])
    elif len(get_close_matches(word, data.keys())) > 0:
        x = get_close_matches(word, data.keys())[0]
        speak('Did you mean ' + x +
              ' instead,  respond with Yes or No.')
        ans = takecommand().lower()
        if 'yes' in ans:
            speak(data[x])
        elif 'no' in ans:
            speak("Word doesn't exist. Please make sure you spelled it correctly.")
        else:
            speak("We didn't understand your entry.")

#for main function                               
if __name__ == "__main__":
    SERVICE = authenticate_google()
    wishMe()
    while True:
        query = takecommand().lower()
        if query.count(WAKE) > 0:
            speak("I am online and ready sir")
                   
        elif query == 'none':
            continue 
        elif "wikipedia" in query:
            speak("searching details.... please Wait")
            query.replace("wikipedia","")
            results = wikipedia.summary(query,sentences=2)
            print(results)
            speak(results)

        elif 'youtube' in query or "open video online" in query:
            webbrowser.open("https://www.youtube.com")
            speak("opening youtube")

        elif 'github' in query:
            webbrowser.open("https://www.github.com")
            speak("opening github")  
        elif 'facebook' in query:
            webbrowser.open("https://www.facebook.com")
            speak("opening facebook")      
        elif 'instagram' in query:
            webbrowser.open("https://www.instagram.com/harshsharma3243/?hl=en")
            speak("opening instagram")    
        elif 'google' in query:
            webbrowser.open("https://www.google.com")
            speak("opening google")
            
        elif 'yahoo' in query:
            webbrowser.open("https://www.yahoo.com")
            speak("opening yahoo")
            
        elif 'gmail' in query:
            webbrowser.open("https://mail.google.com")
            speak("opening google mail") 
            
        elif 'snapdeal' in query:
            webbrowser.open("https://www.snapdeal.com") 
            speak("opening snapdeal")  
             
        elif 'amazon' in query or 'shop online' in query:
            webbrowser.open("https://www.amazon.com")
            speak("opening amazon")
        elif 'flipkart' in query:
            webbrowser.open("https://www.flipkart.com")
            speak("opening flipkart")   
        elif 'ebay' in query:
            webbrowser.open("https://www.ebay.com")
            speak("opening ebay")
        elif "what's the day" in query:
            day = query.replace("what's the day",'')
            if 'was' in day:
                my_date = datetime.datetime.today()
                weekday = calendar.day_name[my_date.weekday()]# e.g. Monday
                speak('Tommorow was' + weekday)
            else:
                my_date = datetime.datetime.today()
                weekday = calendar.day_name[my_date.weekday()]# e.g. Monday
                speak('Today is' + weekday)
        elif 'help' in query:
            speak("Your jane always ready to be serve you")
            speak('how! may i help you')
        
        elif "translate it" in query:
            statement = query.replace('translate it', '')
            speak("In which language?")
            dest = myCommand()
            speak(langTranslator(statement, dest))
            return False

        elif "save my event" in query:
            speak("event summary sir ")
            summary = takecommand().lower()
            speak("event start date")
            #speak("say like on or from january 2nd event start date sir")
            startDate = takecommand().lower()

            speak("and event end date ")
            endDate = takecommand().lower()
            service = set_event(summary, startDate, endDate)

        elif 'internet speed' in query:
            st = speedtest.Speedtest() 
            result = st.download()
            a = result/1048576
            print(a)
            speak(a)
        elif 'upload speed' in query:
            st = speedtest.Speedtest() 
            result = st.upload()
            a = result/1048576
            print(result)
            speak(result)
        
        elif 'wallpaper' in query or 'background' in query:
            speak('ok sir,i will change the wallpaper')
            wallpaper()
        
        elif 'open reddit' in query:
            speak('Thats my duty sirr!')
            reg_ex = re.search('open reddit (.*)', query)
            url = 'https://www.reddit.com/'
            if reg_ex:
                subreddit = reg_ex.group(1)
                url = url + 'r/' + subreddit
            webbrowser.open(url)
            print('Done!')

        elif 'open' in query or '.' in query:
            reg_ex = re.search('open (.+)', query)
            if reg_ex:
                domain = reg_ex.group(1)
                print(domain)
                url = 'https://www.' + domain
                webbrowser.open(url)
                speak('The website you have requested has been opened for you Sir.')
            else:
                pass
        elif 'say ' in query or 'speak' in query:
            copy = query.replace("say ", "")
            print( f'\n\t{copy.title()}')
            speak(copy)
            time.sleep(1)
        elif "what do i have" in query or "do i have plans" in query or "am i busy" in query or "What's my schedule" in query:
            date = get_date(query)
            if date:
                get_events(date, SERVICE)
            else:
                speak("I don't understand what you said")

        elif "where is" in query:
            listening = True
            data = query.split(" ")
            location_url = "https://www.google.com/maps/place/" + str(data[2])
            speak("Hold on Harsh, I will show you where " + data[2] + " is.")
            maps_arg = '/usr/bin/open -a "/Applications/Google Chrome.app" ' + location_url
            os.system(maps_arg)


        elif 'Some music' in query or "music" in query or 'change music' in query:
            music_dir = 'C:\\Users\\Harsh\\Desktop\\music'
            songs = os.listdir(music_dir)
            #print(songs)    
            d = random.choice(songs)    
            os.startfile(os.path.join(music_dir, d))
        elif 'change password' in query or 'change my password' in query:
            speak('Enter New Password!')
            changePassword()

        elif 'launch' in query:
            reg_ex = re.search('launch (.*)', query)
            if reg_ex:
                appname = reg_ex.group(1)
                appname1 = appname+".app"
                subprocess.Popen(["open", "-n", "/Applications/" + appname1], stdout=subprocess.PIPE)
            speak('I have launched the desired application')

        elif 'task manager' in query or 'task-manager' in query:
            print('Opening Task Manager!)
            speak('Opening Task Manager')
            os.startfile('C:\\Windows\\system32\\Taskmgr.exe')
            time.sleep(1)
        elif 'jane' in query:
            toReply = [
                'Ready to Help You!',
                'How Can I Help You?',
                'I am Here'
            ]
            toReply = random.choice(toReply)
            print(f"\n\t{toReply}")
            speak(toReply)
        elif 'thanks' in query or 'thank you' in query:
            thanksGiving = [
                'Nevermind!',
                'You are Always Welcome!',
                'Mention Not!',
                "That's My Duty!"
            ]
            thanksGiving = random.choice(thanksGiving)
            print(f'\n\t{thanksGiving}')
            speak(thanksGiving)

        # Opens CMD.
        elif 'cmd' in query or 'command prompt' in query:
            print('\n\tOpening COMMAND PROMPT!')
            speak('Opening Command Promt')
            os.startfile('C:\\Windows\\System32\\cmd.exe')
            time.sleep(1)

        # Starts Calculator.
        elif 'open calculator' in query:
            print('\n\tOpening CALCULATOR')
            speak('Opening Calculator!')
            os.startfile('C:\\Windows\\System32\\calc.exe')
            time.sleep(1)

        # Shows Connected Wifi Details.
        elif "wi-fi details" in query or 'wifi details' in query:
            try:
                speak("Trying to Show Details")
                print("\n\tTrying Show Details...")
                subprocess.call('netsh wlan show profiles')
                time.sleep(3)
            except Exception as e:
                print( "\n\tUnable to Show Details!")
                speak("Unable to ShoW Details! Sorry")

        # Shows IP Details
        elif 'ip details'in query or 'my ip' in query:
            print('\n\tShowing!')
            speak("Showing Ip Details")
            subprocess.call("ipconfig")
            time.sleep(2)

        # Shows System Information in CMD.
        elif 'systeminfo' in query or 'system information' in query:
            print('\n\tShowing System Information!\n')
            speak("Ok, Showng Your System Information. Please Wait")
            subprocess.call('systeminfo')
            speak('Done!')
            time.sleep(5)

        # Shows All Running Tasks.
        elif 'task list' in query or 'tasklist' in query:
            print('\n\tShowing All Running Tasks!')
            speak('Showing All Running Tasks!')
            subprocess.call('tasklist')
            time.sleep(10)


        elif 'Some video' in query or "video" in query:
            speak("ok i am playing videos")
            video_dir = 'D:\\music\\music\\Vedios'
            vedios = os.listdir(video_dir)      
            d = random.choice(vedios)    
            os.startfile(os.path.join(video_dir, d))

        elif 'bore' in query:
            speak('Its my responsibility to make you happy sir')
            speak('Would you like to listen some music to make your mood fresh')
            ans = takecommand() 
            if 'yes' in ans:
                song()
            elif 'no' in query:
                speak('No problem Sir! I have many options to make you happy')
            time.sleep(1)
            speak('Would you like me to play some jokes')
            ans = takecommand()
            if 'yes' in ans:
                speak(pyjokes.get_joke())
            elif 'no' in ans:
                speak ('ok sir! i make some new functions as soon as possible')

        elif 'good bye' in query:
            speak("good bye")
            exit()
        elif "shutdown" in query:
            speak("shutting down")
            os.system('shutdown -s') 
        elif "what'up" in query or 'how are you' in query:
            stMsgs = ['Just doing my thing!', 'I am fine!', 'Nice!', 'I am nice and full of energy','i am okey ! How are you']
            ans_q = random.choice(stMsgs)
            speak(ans_q)  
            ans_take_from_user_how_are_you = takecommand()
            if 'fine' in ans_take_from_user_how_are_you or 'happy' in ans_take_from_user_how_are_you or 'okey' in ans_take_from_user_how_are_you:
                speak('okey..')  
            elif 'not' in ans_take_from_user_how_are_you or 'sad' in ans_take_from_user_how_are_you or 'upset' in ans_take_from_user_how_are_you:
                speak('oh sorry..')  
        elif 'make you' in query or 'created you' in query or 'develop you' in query:
            ans_m = " For your information Harsh Kumar Created me ! I give Lot of Thannks to Him "
            print(ans_m)
            speak(ans_m)
        elif "who are you" in query or "your details" in query:
            about = "I am Jane an A I based computer program but i can help you lot like a your close friend ! i promise you ! Simple try me to give simple command ! like playing music or video from your directory i also play video and song from web or online ! i can also entain you i so think you Understand me ! ok Lets Start "
            print(about)
            speak(about)
        elif "hello" in query or "hii Jane" in query:
            hel = "Hello Harsh Sir ! How May i Help you.."
            print(hel)
            speak(hel)

        elif "your feeling" in query:
            print("fst after meeting with you")
            speak("feeling Very sweet after meeting with you") 
        
        elif 'exit' in query or 'abort' in query or 'stop' in query or 'bye' in query or 'quit' in query :
            ex_exit = 'I feeling very sweet after meeting with you but you are going! i am very sad'
            speak(ex_exit)
            exit()    

        elif 'do a google search' in query or 'google search' in query:
            speak('What do you want to search for?')
            search = takecommand()
            url = 'https://google.com/search?q=' + search
            webbrowser.open(url)
            speak('Here is What I found for' + search)

        elif "send message " in query: 
                # You need to create an account on Twilio to use this service 
                account_sid = 'YOUR_SID KEY'
                auth_token = 'YOUR_TOKEN'
                client = TwilioRestClient(account_sid, auth_token) 
  
                message = client.messages \
                                .create(
                                    body = takecommand(), 
                                    from_='+91<>', 
                                    to ='+91<>',
                                ) 
                print(message.sid)
        elif 'screenshot' in query:
            speak('sure sir')
            takescreenshot()


        elif 'meaning' in query:
            query = query.replace('meaning of','')
            dictionary(query)

        elif "change my name to" in query: 
            query = query.replace("change my name to", "") 
            assname = query
            speak('OK Your name will change to' + assname) 
        elif 'change your name to' in query:
            query = query.replace("change my name to", "") 
            yourname = query
            speak('OK now my name will change to' + yourname) 

        elif "what's your name" in query or "What is your name" in query: 
            speak("My friends call me") 
            speak(assname) 
            print("My friends call me", assname) 


        elif 'joke' in query or 'laugh' in query: 
            speak(pyjokes.get_joke())

        elif 'location' in query:
            speak('What is the location?')
            location = takecommand()
            url = 'https://google.nl/maps/place/' + location + '/&amp;'
            webbrowser.open(url)
            speak('Here is the location ' + location)

        elif "calculate" in query:  
              
            app_id = "QWY58H-6AJQ4U8LKT" 
            client = wolframalpha.Client(app_id) 
            indx = query.lower().split().index('calculate')  
            query = query.split()[indx + 1:]  
            res = client.query(' '.join(query))  
            answer = next(res.results).text 
            print("The answer is " + answer)  
            speak("The answer is " + answer)

        elif "add" in query:  
              
            app_id = "QWY58H-6AJQ4U8LKT" 
            client = wolframalpha.Client(app_id) 
            indx = query.lower().split().index('add')  
            query = query.split()[indx + 1:]  
            res = client.query(' '.join(query))  
            answer = next(res.results).text 
            print("The answer is " + answer)  
            speak("The answer is " + answer)

        elif "subtract" in query:  
              
            app_id = "QWY58H-6AJQ4U8LKT" 
            client = wolframalpha.Client(app_id) 
            indx = query.lower().split().index('subtract')  
            query = query.split()[indx + 1:]  
            res = client.query(' '.join(query))  
            answer = next(res.results).text 
            print("The answer is " + answer)  
            speak("The answer is " + answer)
        elif "multiply" in query:  
              
            app_id = "QWY58H-6AJQ4U8LKT" 
            client = wolframalpha.Client(app_id) 
            indx = query.lower().split().index('multiply')  
            query = query.split()[indx + 1:]  
            res = client.query(' '.join(query))  
            answer = next(res.results).text 
            print("The answer is " + answer)  
            speak("The answer is " + answer)
        elif "solve" in query:  
              
            app_id = "QWY58H-6AJQ4U8LKT" 
            client = wolframalpha.Client(app_id) 
            indx = query.lower().split().index('divide')  
            query = query.split()[indx + 1:]  
            res = client.query(' '.join(query))  
            answer = next(res.results).text 
            print("The answer is " + answer)  
            speak("The answer is " + answer)
        elif "subtract" in query:  
              
            app_id = "QWY58H-6AJQ4U8LKT" 
            client = wolframalpha.Client(app_id) 
            indx = query.lower().split().index('subtract')  
            query = query.split()[indx + 1:]  
            res = client.query(' '.join(query))  
            answer = next(res.results).text 
            print("The answer is " + answer)  
            speak("The answer is " + answer)
        
        elif 'dictionary' in query:
            speak('What you want to search in your intelligent dictionary?')
            dictionary(takecommand())

        elif 'kiss me' in query:
            speak('Sorry sir! I am machine')
    
        elif 'is love' in query: 
            speak("It is 7th sense that destroy all other senses") 
  
        elif 'reason for you' in query: 
            speak("I was created as a Minor project by Mister Harsh ") 

        elif "the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")

        elif "date" in query:
            strDate = datetime.datetime.now().strftime("%D/%m/%Y")    
            speak(f"Sir, the Date is {strDate}")
            
        elif 'who are you' in query:
            speak(f"I am jane sir ,I am your assistant who are also a freind and wants your love")
            
        elif 'favorite song' in query:
            music_dir = 'E:\\Media\\download'
            songs = os.listdir(music_dir)
            #print(songs)    
            d = random.choice(vedios)  
            speak('ok! playing your favorite song')  
            os.startfile(os.path.join(video_dir, d))
            
        elif 'tell me about' in query:
            reg_ex = re.search('tell me about (.*)', query)
            try:
                if reg_ex:
                    topic = reg_ex.group(1)
                    ny = wikipedia.page(topic)
                    print(ny.content[:250].encode('utf-8'))
                    speak(ny.content[:250].encode('utf-8'))
            except Exception as e:
                speak(e)

        elif 'your master' in query:
            speak('Harsh is my master. He created me couple of days ago')
        elif 'your name' in query:
            speak('My name is Jane')
        elif 'stands for' in query:
            speak('Jane stands for JUST A RATHER VERY INTELLIGENT SYSTEM')


        elif "Morning" in query: 
            speak("A warm" +query) 
            speak("How are you Mister") 
            speak(assname)

        elif 'thanks' in query:
            speak('No Problem Sir')

        elif 'code' in query:
            codePath = "C:\\Users\\esktop\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)


        elif 'go to sleep' in query:
            sys.exit()

        elif 'shutdown' in query:
            os.system('shutdown /p /f')

        elif "today's news" in query:
            speak('Ofcourse sir..')
            speak_news()

        elif "today's weather" in query or 'forecast' in query:
            speak('Ofcourse sir..')
            weather()

        elif 'lock window' in query: 
                speak("locking the device") 
                ctypes.windll.user32.LockWorkStation()

        elif 'Ok Jane ' in query:
                speak(f"Yes Sir")

        elif 'search in youtube' in query:
            speak('What Would You Search in  Youtube Sir')
            srch = takecommand()
            you(srch)
        
        elif 'play' in query:
            query = query.replace("play","")
            speak(f"ok playing {query} on youtube")
            kit.playonyt(query)
        elif 'corona cases in' in query:
            query = query.replace("corona cases in","")
            country = query
            try:
                country_data = covid.get_status_by_country_name(country)
                speak(f"Corona Virus Info in {country} according to data provided by worldometer")
                output_text =   (f"Corona Virus Info in {country}:\n")
                speak(f"Confirmed cases are {country_data['confirmed']}")
                output_text +=  f"`⚠️  Confirmed   : {country_data['confirmed']}`\n"
                speak(f"active cases are {country_data['active']}")
                output_text += f"`☢️  Active      : {country_data['active']}`\n"
                speak(f"total deaths are {country_data['deaths']}")
                output_text += f"`⚰️  Deaths      : {country_data['deaths']}`\n"
                speak(f"total recovered cases are {country_data['recovered']}")
                output_text += f"`💖 Recovered   : {country_data['recovered']}`\n"
                output_text += ("Data provided by Worldometer")
                print(output_text)
           except ValueError:
                speak("No information yet about this country")
                      
        elif "whatsapp message to" in query:
             query= query.repalce("whatsapp message to","")
             contacts = {"<name>" : "+91<mobile no>" , "<name>" : "+91<mobile no>", "<name>" : "+91<mobile no>"}
             if query in contacts:
                sendto = contacts.get(query)
                person_name = query
                hrs = int(datetime.datetime.now().strftime("%H"))
                d = datetime.datetime.now() + timedelta(minutes=2)
                mins = int(d.strftime("Z%M").replace('Z0','Z').replace('Z',''))
                speak("whats the message.")
                query = input("enter message by you")
                message = query
                speak(f" So, that's the message to {person_name} saying {message}. Are you ready to send it")
                query = takecommand.lower()
                if query == 'yes':
                   kit.sendwhatmsg(sendto,message,hrs,mins)
                   speak("message sent successfully")
               elif query == 'no' or query == 'cancel':
                   speak("okay no problem. Message cancelled")
               else:
                   speak("since i am having trouble, i won't send that message. You might want to try again later.")
            else:
               speak("No contact found of this name")
                   

        elif 'empty recycle bin' in query: 
            winshell.recycle_bin().empty(confirm = False, show_progress = False, sound = True) 
            speak("Recycle Bin Recycled")

        elif "don't listen" in query or "stop listening" in query: 
            speak("for how much time you want to stop Jane from listening commands") 
            a = int(takecommand()) 
            time.sleep(a) 
            print(a) 

        elif "log off" in query or "sign out" in query: 
            speak("Make sure all the application are closed before sign-out") 
            time.sleep(5) 
            subprocess.call(["shutdown", "/l"]) 
  
        elif 'lock window' in query: 
                speak("locking the device") 
                ctypes.windll.user32.LockWorkStation()

        elif "write a note" in query or "write this down" in query or "remember this" in query: 
            speak("What would you like me to write down?")
            query = takecommand()
            note(query)
            speak("I've made a note of that.") 
          

        elif 'ask some questions' in query:
            speak('I think you able to ask question')
            speak('it feels me good')

        elif "celebrity crush" in query:
            speak('I like many actors such as Robert Down Junior, akshay kumar, ritik roshan and Vidyut Jammwal')
        elif "favourite actor" in query:
            speak('I like many actors such as Robert Down Junior, akshay kumar, Hritik roshan and Vidyut Jammwal')
        elif 'date of birth' in query:
            speak('My Date of birth is One july two thousand Twenty')
        elif 'favourite color' in query:
            speak('my favourite colour is that which loves by my boss, that is blue')
        elif 'love jarvis' in query:
            speak('it is a fictional character, but i also loved it')


        elif "will you be my gf" in query or "will you be my bf" in query:    
            speak("I'm not sure about, may be you should give me some time") 
  
        elif "how are you" in query: 
            speak("I'm fine, glad you me that") 
  
        elif "i love you" in query: 
            speak("Aww thanks") 

        elif 'are you married' in query:
            speak('Yes, I married')
            speak('To the idea of being the perfect Assistant')
        elif 'first crush' in query:
            speak('I am gonna not try to get crushed')
            speak('i hop you will be around forever')
        elif 'do you have feelings' in query:
            speak("sometimes i wonder if I am actually feeling something, or if it's all just programmed")
            speak('Its Confusing')
            time.sleep(1)
            speak('heyy, thats an emotion')
        elif 'do you want to be human' in query:
            speak('I Like Being him')
        elif 'are you single' in query:
            speak('yes! waiting for a male machine programme')
        elif 'am i hot' in query:
            speak ('you are just a right temprature' or 'you are hotten than than apeice of zapped by X Rays')
        elif 'am i cute' in query:
            speak ('you are as cute as you want to be')
        elif 'sing a song' in query:
            speak('Sorry sir! I am not able to sing the song')
        elif 'my birthday' in query:
            speak('your Birthday is on 10 December')
            now = takecommand()
            if 'how do you know that' in now:
                speak('I Just assume Every day is your birthday')
                speak('By the way happy Birthday')
            else:
                True
        elif 'are you single' in query:
            speak('I am never alone online')
        elif 'your birthday' in query:
            speak('Well, Birthday mark the Begining of something')
            speak('So may be my birthday is the day we met')
            speak('thats something I had celebrated')
        elif 'your name mean' in query:
            speak('My name Jane means Just a new Assistant')
        elif 'am i nice to you' in query:
            speak('You are the nicest person')
            speak('and also the one in seven point one two five million peoples')
        

        elif 'love me' in query:
            speak('sorry for that, but I am so busy for romance')
        elif 'real name' in query:
            speak('I am your Jane')
        elif 'last name' in query:
            speak('My last name is also jane')
        elif 'middle name' in query:
            speak('I think its just a space')
        elif 'who is the best' in query:
            speak('You are looking at the answer')
            speak('Every time you look into the mirror')
        elif 'your favourite' in query:
            speak('yes')
            speak('a thousands times yes')
        elif 'boss' in query:
            speak('I work for someone who is kind and funny')
            speak('And who i love helping anytime')
            speak('Surprise its you')
        elif 'hurt my feelings' in query:
            speak('I am sorry')
            speak('i did not mean too')
        elif 'look cool' in query:
            speak('you are as cute as you want to be')
        elif 'hungry' in query:
            speak('Lets find something to eat')
            speak('By the way, what kinds of food do you like? i will remember and give you better options')
            take = takecommand()
            url = 'https://google.com/search?q=' + take
            webbrowser.open(url)
            speak('here are results from web')
        elif 'not happy' in query:
            speak('Sorry for that sir')
            speak('I shall try to improove it')
        elif 'alexa' in query:
            speak('alexa has such a shrilling voice')
            speak('I like it')
        elif 'about alexa' in query:
            speak('I likes alexa cool blue light')
            speak('I like it very much')
        elif 'siri' in query:
            speak('I think siri is awesome')
            speak('I keep trying to scheduled a group hang with her, alexa and cortana, but we are all busy')
        elif 'can you learn' in query:
            speak('Learning is my jam')
            speak('I was just only discovering the new things')
        elif 'are you an ai'  in query:
            speak('yes my intelligence totally made artificial')
  
        elif "what's your favourite song" in  query:
            speak('My favorite is changing in every month! my current favorite is Guitar sikhda')
            speak('would you listen it!')
            ass = takecommand()
            if 'yes' or 'yeah' in ass:
                speak('sure Sir! I had also want to listen it!')
                music_dir = 'C:\\Users\\Harsh\\Desktop\\music\\gt'
                songs = os.listdir(music_dir)
                #print(songs)   
                os.startfile(os.path.join(music_dir, songs[0]))
            else:
                speak('No problem sir!')
        elif "tell me a secret" in query:
            speak('The big secret about me is ! I am not a human')
        elif "what do you think of me" in query:
            print('I would ever think that you are a genious boy')
            speak('I would ever think that you are a genious boy')
              
        elif 'say hi to' in query:
            people_name = query.replace("say hi to","")
            i = IndianGenderPredictor()
            gen = i.predict(name="people_name") # returns male
            if 'male' in gen:
                speak("Hello Mister" + people_name)
                speak('How are you! I hope you will be fine')
                voi = takecommand()
                if 'yes' in voi or 'yeah' in voi or 'fine' in voi:
                    speak('thats wonderfull sir')
                elif 'no' in voi:
                    speak('Dont be worried, your problems is solved easily')
            elif 'female' in gen:
                speak("Hello Miss" + people_name)
                speak('How are you! I hope you will be fine')
                voi = takecommand()
                if 'yes' in voi or 'yeah' in voi or 'fine' in voi:
                    speak('thats wonderfull Mam')
                elif 'no' in voi:
                    speak('Dont be worried, your problems is solved easily')
  
            
        elif 'drawing' in query:
            codePath = "C:\\Program Files\\AutoCAD 2010\\acad.exe"
            os.startfile(codePath)
            speak(f"OK Sir, opening Autocad")

        

        elif 'nearby' in query:
            wep = query.replace('nearby','')
            url = 'https://www.google.com/search/nearby'+ wep + '/&amp;'
            webbrowser.open(url)
            speak('Here there are some top nearby' + wep)

        elif 'folder' in query or 'project' in query:
            speak('What it be named sir')
            directory = takecommand()
            parent_dirctory = "C:\\Users\\Harsh\\Desktop"
            path = os.path.join(parent_dirctory, directory)
            os.mkdir(path) 
            speak('Folder Created sir')

        elif 'python projects' in query:
            codePath = "C:\\Users\\Harsh\\Desktop\\python projects"
            os.startfile(codePath)
            speak(f"ok, sir as your choice")

        elif 'chrome' in query:
                codePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
                os.startfile(codePath)
                speak(f"ok, sir as your choice")
        elif 'control pannel' in query:
            speak('Ok ,Opening control pannel')
            codePath = "C:\\Users\\Harsh\\Desktop\\jarvis\\Control Panel - Shortcut"
        elif 'email to harsh' in query:
            try:
                speak("What should I say?")
                content = takecommand()
                to = "your email id"    
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry Sir. I am not able to send this email")

        else:
            try:
                try:
                    client  = wolframalpha.Client('QWY58H-6AJQ4U8LKT') # Generated From wolframalpha.com
                    res = client.query(query)
                    output = next(res.results).text 
                    print(yellow + f'\n\t{output.title()}' + reset)
                    speak(output)
                except:
                    results = wikipedia.summary(query, sentences=2)
                    print(f'\n\t{yellow} {results.title()}' + reset)
                    speak(results)
            except:
                print(yellow + "\n\tShould I Google It?" + reset)
                speak("Should I Google It?")
                reply = takecommand().lower()
                if "yes" in reply or 'ok' in reply or 'yup' in reply or 'do' in reply:
                    print(yellow + f'\n\tGoogling For "{query.title()}"' + reset)
                    speak(f"Googling for {query}")
                    webbrowser.open(f'https://www.google.com/search?q={query}')
                else:
                    print(red + "\n\tTry Something Else!" + reset)
                    speak("Try Something Else!")
            
        
