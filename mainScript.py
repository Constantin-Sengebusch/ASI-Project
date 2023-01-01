#!/usr/bin/env python
# coding: utf-8

import commandLibrary as cl
from fuzzywuzzy import process
import json
import os

curr_path = os. getcwd()

with open(f'{curr_path}/config_params.json', 'r') as f:
    config_params = json.load(f)


def analyseCommand(messageInput):
    '''
    This function analyse the command in the text.
    If the analysis is not sure enough it will return an error message.
    '''

    choices = ['hello', 'hi', 'hey', 'news', 'help', 'calculator', 
               'definition', 'convertcurrency', 'translation',
               'nextbirthday', 'time', 'date', 'goodmorning', 'thankyou',
              'whoareyou', 'whocreatedyou', 'whatsyourpurpose', 'whereareyou',
              'wikipedia', 'name']

    resultInput = process.extractOne(messageInput, choices)

    #print("Confidence level on command is: " + str(resultInput[1]))    

    if resultInput[1] > 60:
        commandInput = resultInput[0]
        return commandInput
    else:
        return messageInput


def defineSecondEntry(parametersEntry):
    '''
    Define the parameters for argument in function
    '''
    entrySplit = parametersEntry.split()
    if len(entrySplit) > 1:
        text = [' '.join(entrySplit[0:-1])][0]
        extraParameter = entrySplit[-1]
    else:
        text = entrySplit[0:][0]
        extraParameter = ''

    return text, extraParameter


def nameCommand(entry, secondEntry):

    '''
    Launch the requested command from commandLibrary
    '''
    if entry == 'hello' or entry == 'goodmorning' or entry == 'hi' or entry == 'hey':
        return cl.randomHello()
    if entry == 'help':
        return cl.helpCommand()
    if entry == 'whoareyou' or entry == 'name':
        return config_params['whoareyou']
    if entry == 'whocreatedyou':
        return config_params['whocreatedyou']
    if entry == 'whatsyourpurpose':
        return config_params['whatsyourpurpose']
    if entry == 'whereareyou':
        return config_params['whereareyou']
    if entry == 'nextbirthday':
        return cl.nextBirthday(secondEntry)
    if entry == 'time':
        return cl.getTime()
    if entry == 'date':
        return cl.getDate()
    if entry == 'thankyou':
        return cl.randomWelcome()
    if entry == 'definition':
        try:
            return cl.getDefinition(secondEntry)
        except:
            return cl.errorMessage()
    if entry == 'translation':
        secondEntry = defineSecondEntry(secondEntry)
        try:
            return cl.getTranslation(secondEntry[0], secondEntry[1])
        except:
            return cl.errorMessage()
    if entry == 'convertcurrency':
        secondEntry = defineSecondEntry(secondEntry)
        try:
            return cl.convertCurrency(secondEntry[0], secondEntry[1])
        except:
            return cl.errorMessage()
    if entry == 'news':
        try:
            return cl.getNews()
        except:
            return cl.errorMessage()

    if entry == 'wikipedia':
        try:
            return cl.getAnswerWikipedia(secondEntry)
        except:
            return cl.errorMessage()
    else:
        try:
            #return cl.getAnswerGoogle(entry)
            return cl.get_answer_chatgpt(entry)
        except:
            return cl.errorMessage()


# Command to launch the full script

def mainScript(entryInput):
    #Clean the input
    entryInput = entryInput.replace("please", "")

    #Split main command and parameters
    if ":" in entryInput:
        entrySplit = entryInput.split(": ")
        entry = entrySplit[0]
        parametersEntry = entrySplit[1]
    else:
        entry = entryInput
        parametersEntry = ''

    # Return the command
    return nameCommand(analyseCommand(entry), parametersEntry)