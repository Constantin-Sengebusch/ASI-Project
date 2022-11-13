#!/usr/bin/env python
# coding: utf-8

# Import libraries
import pandas as pd
from datetime import date, datetime, timedelta
import urllib
import urllib.parse
import urllib.request
from PyDictionary import PyDictionary
from googletrans import Translator
translator = Translator()
import requests
from currency_converter import CurrencyConverter
c = CurrencyConverter()
import random 
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import wikipedia
from bs4 import BeautifulSoup
import wolframalpha
import spacy
import json

with open('config_params.json', 'r') as f:
  config_params = json.load(f)

with open('config_credentials.json', 'r') as f:
  config_credentials = json.load(f)


def errorMessage():
    '''
    Generate error message 
    '''
    url = "https://themarkettrend.org"
    timeout = 5
    try:
        request = requests.get(url, timeout=timeout)
        errorMessage = ("Data is unavailable for the moment (unknown reason).")
    except (requests.ConnectionError, requests.Timeout) as exception:
        errorMessage = ("Data is unavailable for the moment due to no internet connection. Answer 'Help' to discover offline tools")
    return errorMessage


# Get documentation for help 
def helpCommand():
    return config_params['help']

    
def nextBirthday():
    '''
    Get next birthday
    '''
    jourAnniversary = pd.read_excel(r'data/birthday.xlsx')
    jourAnniversary['Date'] = pd.to_datetime(jourAnniversary['Date']).dt.strftime('%m/%d/%Y')
    jourAnniversary = jourAnniversary.sort_values(by='Date').reset_index(drop=True)
    dateToday = datetime.now().strftime('%m/%d')
    
    # Find next name and date
    try:
        nextName = jourAnniversary['Nom'][jourAnniversary['Date'] > dateToday].iloc[0]
        nextDate = jourAnniversary['Date'][jourAnniversary['Date'] > dateToday].iloc[0]
    except:
        nextName = jourAnniversary['Nom'].iloc[0]
        nextDate = jourAnniversary['Date'].iloc[0]
    nextDateRaw = datetime.strptime(nextDate,'%m/%d/%Y')
    nextDate = datetime.strptime(nextDate,'%m/%d/%Y').strftime('%d %B')    
    
    # Compute the age
    today = date.today()
    age = today.year - nextDateRaw.year - ((today.month, today.day) < (nextDateRaw.month, nextDateRaw.day))
    
    textAnswer = f"The next birthday day will be the one of {nextName} on the {nextDate} and will turn {age}."
    #return textAnswer
    return textAnswer


def getTime():
    '''
    Get the time
    '''
    now = datetime.now()
    currentTime = now.strftime("%Hh%M")
    textTime = "It is now " + currentTime + "."
    return textTime


def getDate():
    '''
    Get the date
    '''
    today = date.today()
    currentDate = today.strftime("%B %d, %Y")
    textDate = "Today is " + currentDate + "."
    return textDate


def getDefinition(word): 
    '''
    Get definition of english word
    Ex: Definition Dog
    '''
    dictionary = PyDictionary(word)
    definition = dictionary.printMeanings()
    return definition


def getTranslation(text, destLang):
    '''
    Get translation of text
    Ex: Translation This is my friend FR
    '''
    translation = translator.translate(text, dest=destLang)
    textTranslated = translation.text
    return textTranslated


def convertCurrency(amount, currency):
    '''
    Convert Currency
    Ex: convertCurrency 100 EUR/USD
    '''
    currency = currency.upper()
    currency = currency.split('/')
    currSrc = currency[0]
    currDest = currency[1]
    result = str(round(c.convert(float(amount), currSrc, currDest), 2)) + ' ' + currDest
    return result

def calculator(computation):
    '''
    Make computations
    '''
    computation = str(computation)
    computation = eval(computation)
    return computation


def getNews():    
    '''
    Get top 10 news from BBC 
    '''
    url = 'https://www.bbc.com/news'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.find('body').find_all('h3')
    unwanted = ['BBC World News TV', 'BBC World Service Radio',
                'News daily newsletter', 'Mobile app', 'Get in touch',
               'Video']

    newsList = []

    for x in list(dict.fromkeys(headlines)):
        if x.text.strip() not in unwanted:
            newsList.append(x.text.strip())

    top10News = newsList[:10]

    top10News = str(top10News)
    top10News = top10News.replace("'",'')
    top10News = top10News.replace("[",'')    
    top10News = top10News.replace("]",'')
    top10News = top10News.replace(',','\n- ')
    textNews = "Top 10 news on BBC:\n- " + top10News
    
    return textNews


def randomHello():
    '''
    Answer with a random "Hello"
    '''
    choicesHello = ["Greetings, Boss!", "Hi Constantin!", "Welcome Back, Sir!",
                    "Bonjour Monsieur!", "Hello, Sir!", "Hey, Boss!"]
    answerRandom = random.choice(choicesHello)
    return answerRandom 


def randomWelcome():
    '''
    Answer with a random "You are welcome"
    '''
    choicesWelcome = ["You got it, Boss!", "Don’t mention it!", "No worries!",
                      "Not a problem!", "My pleasure!", "It was nothing!",
                      "I’m happy to help!", "Sure!", "Anytime, Sir!"]

    answerRandom = random.choice(choicesWelcome)

    return answerRandom 


def getAnswerWolframalpha(text):
    # App id obtained by the above steps
    app_id = config_credentials['Wolframalpha']
      
    # Instance of wolf ram alpha 
    # client class
    client = wolframalpha.Client(app_id)
      
    # Stores the response from 
    # wolf ram alpha
    res = client.query(text)
      
    # Includes only text from the response
    answer = next(res.results).text
      
    return answer


def identifyTopicSentence(text):
    nlp = spacy.load("en_core_web_sm")
    
    sentences=[text]
    
    def get_subject_phrase(doc):
        for token in doc:
            if ("subj" in token.dep_):
                subtree = list(token.subtree)
                start = subtree[0].i
                end = subtree[-1].i + 1
                return doc[start:end]
            
    def get_object_phrase(doc):
        for token in doc:
            if ("dobj" in token.dep_):
                subtree = list(token.subtree)
                start = subtree[0].i
                end = subtree[-1].i + 1
                return doc[start:end]
            
    for sentence in sentences:
        doc = nlp(sentence)
        subject_phrase = get_subject_phrase(doc)
        return subject_phrase



def getAnswerWikipedia(keyword):
    try:
        # finding result for the search
        # sentences = 2 refers to numbers of line
        wikipedia.set_lang("en")
        result = wikipedia.summary(keyword, sentences = 2)
        # printing the result
        return result
    except:
        try:
            keyword = wikipedia.suggest(keyword)
            result = wikipedia.summary(keyword, sentences = 2)
            return result
        except:
            return 'Sorry, I could not find a result on Wikipedia. Please reformulate your question.'


def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)


def getAnswerGoogle(text):
    textPlus = text.replace(" ", "+")
    url = "https://www.google.com/search?q=" + textPlus
    
    # Perform the request
    request = urllib.request.Request(url)
    # Set a normal User Agent header, otherwise Google will block the request.
    request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
    raw_response = urllib.request.urlopen(request).read()
    # Read the repsonse as a utf-8 string
    html = raw_response.decode("utf-8")
    
    
    # The code to get the html contents here.
    
    soup = BeautifulSoup(html, 'html.parser')
    
    resultTranslate = []
    
    # Find all the search result divs
    divs = soup.select("#search div.g")
    for div in divs:
        # Search for a h3 tag
        results = div.select("div")
        #results = div.select("a")
        #results = div.select("span")
    
        # Check if we have found a result
        if (len(results) >= 1):
    
            # Print the title
            h3 = results[0]
            resultTranslate.append(h3.get_text())
    
    
    
    # Create list of date in the right format
    start_dt = date(2005, 1, 1)
    end_dt = date.today()
    
    listDate = []
    
    for dt in daterange(start_dt, end_dt):
        dateFormat = (dt.strftime("%e %b. %Y").lower())
        if dateFormat[0] == " ":
             dateFormat = dateFormat[1:]
    
        else:
            pass
        listDate.append(dateFormat)
    
    resultSelect = resultTranslate[0]
    
    # Must add "Featured snippet from the web" in local langage
    if resultSelect.find('Extrait optimisé sur le ') == 0 or resultSelect.find('Hervorgehobenes Snippet aus dem ') == 0 or resultSelect.find('Featured snippet from the ') == 0:
        try:
            dateFound = [date for date in listDate if date in resultSelect]
            resultSelectSplit = resultSelect.split(dateFound[0])
        except:
            resultSelectSplit = resultSelect.split(".")
        resultClean = resultSelectSplit[0].replace("Extrait optimisé sur le Web", "")
        resultClean = resultClean.replace("Hervorgehobenes Snippet aus dem Web", "")
        resultClean = resultClean.replace("Featured snippet from the web", "")
    
        # Make sure we did not forget statistics
        try:
            int(resultClean[-1])
            countLoop = 0
    
            try:
                for part in resultSelectSplit[1:]:
                    countLoop += 1
                    int(part[-1])
                    resultClean += ". " + part
            except:
                pass
    
            resultClean += ". " + resultSelectSplit[countLoop]
    
        except:
            pass 
    
        return resultClean
            
    else:
        try:
            # Let's try to find the answer with Wolframalpha
            answer = getAnswerWolframalpha(text)
                
            if answer != '(data not available)':
                return answer
            else:
                return getAnswerWolframalpha(text)
        except:
            try:
                # Let's try to find the answer with wikipedia.
                # For this, we will first find the subject of the sentence
                return getAnswerWikipedia(identifyTopicSentence(text))
                
            except:
                return "Sorry, I could not find an answer on the search engine. Please be more precise or try to find an answer on Wikipedia. You can also ask for help if you need."
    
