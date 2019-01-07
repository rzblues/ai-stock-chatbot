
from rasa_nlu.model import Interpreter
from iexfinance import Stock
interpreter = Interpreter.load("/Users/rukawa/Desktop/stockchatbot/models/current/nlu")
import json
f = open("/Users/rukawa/Desktop/stockchatbot/symbols.json", encoding='utf-8')
global setting 
setting = json.load(f)


global stock_re
global remember
global flag
stock_re = ''
remember = ''
flag = False
global response

def send_message(policy, state, message):
    global response
    print("USER : {}".format(message))
    new_state, response = respond(policy, state, message)
    print("BOT : {}".format(response))
    return new_state

def respond(policy, state, message):
    new_msg = interpret(message)
    policy = policyrule()
    (new_state, response) = policy[(state, new_msg)]
    return new_state, response

def interpret(message):
    global flag
    global remember

    result = interpreter.parse(message)   #此处用到Rasa
    intent = result.get('intent').get('name')     #定义message的四种状态
    if intent == None:
        intent = 'none'
    if intent == 'stock_search':
        if result.get('entities')[0].get('entity') == 'company' or flag:  #要进入pending或者已经进入
            stock_pending(message)
        else:
            stock_return(message)
    return intent

def stock_return(message):
    result = interpreter.parse(message)

    global stock_re
    global setting

    if 'open' in result.get('entities')[0].get('value'):
        company = result.get('entities')[1].get('value')      
        for i in setting:
            if company in i.get('name'):
                company = i.get('symbol')
        open_price = Stock(company).get_open()
        stock_re = "The open price is {}".format(open_price)

    if 'close' in result.get('entities')[0].get('value'):
        company = result.get('entities')[1].get('value')
        for i in setting:
            if company in i.get('name'):
                company = i.get('symbol')
        close_price = Stock(company).get_price()
        stock_re = "The close price is {}".format(close_price)

    if 'volume' in result.get('entities')[0].get('value'):
        company = result.get('entities')[1].get('value')
        for i in setting:
            if company in i.get('name'):
                company = i.get('symbol')
        volume = Stock(company).get_volume()
        stock_re = "The volume is {}".format(volume)




def stock_pending(message):
    result = interpreter.parse(message)

    global stock_re
    global remember
    global flag
    global setting

    company = ''

    if 'open' in result.get('entities')[0].get('value'):
        if remember != '':
            company = remember
        else:
            company = result.get('entities')[1].get('value')
        for i in setting:
            if company in i.get('name'):
                company = i.get('symbol')
        open_price = Stock(company).get_open()
        stock_re = "The open price is {}".format(open_price)

    if 'close' in result.get('entities')[0].get('value'):
        if remember != '':
            company = remember
        else:
            company = result.get('entities')[1].get('value')
        for i in setting:
            if company in i.get('name'):
                company = i.get('symbol')
        close_price = Stock(company).get_price()
        stock_re = "The close price is {}".format(close_price)

    if 'volume' in result.get('entities')[0].get('value'):
        if remember != '':
            company = remember
        else:
            company = result.get('entities')[1].get('value')
        for i in setting:
            if company in i.get('name'):
                company = i.get('symbol')
        volume = Stock(company).get_volume()
        stock_re = "The volume is {}".format(volume)

    if result.get('entities')[0].get('entity') == 'company':
        stock_re = "Do you wanna look at open price, close price or volume?"
        remember = result.get('entities')[0].get('value')
        for i in setting:
            if remember in i.get('name'):
                remember = i.get('symbol')

    flag = True


# Define the states
INIT = 0
PENDING = 1
CHOOSED = 2
THANK = 3

# Define the policy rules dictionary
def policyrule():
    global stock_re
    policy = {
        (INIT, "none"): (INIT, "I'm sorry - I'm not sure how to help you"),
        (INIT, "greet"): (PENDING, "Hello. I'm a stock inquiry bot. You can ask questions about the stock of a specific company"),
        (INIT, "thankyou"): (THANK, "You are very welcome"),
        (INIT, "stock_search"): (CHOOSED, stock_re),

        (PENDING, "none"): (PENDING, "I'm sorry, which stock do you wanna look at?"),
        (PENDING, "greet"): (PENDING, "I'm sorry, which stock do you wanna look at?"),
        (PENDING, "thankyou"): (PENDING, "I'm sorry, which stock do you wanna look at?"),
        (PENDING, "stock_search"): (CHOOSED, stock_re),

        (CHOOSED, "none"): (CHOOSED, "I'm sorry, which stock do you wanna look at?"),
        (CHOOSED, "greet"): (CHOOSED, "I'm sorry, which stock do you wanna look at?"),
        (CHOOSED, "thankyou"): (THANK, "You are very welcome"),
        (CHOOSED, "stock_search"): (CHOOSED, stock_re),

        (THANK, "none"): (INIT, "I'm sorry - I'm not sure how to help you"),
        (THANK, "greet"): (PENDING, "Hello. I'm a stock inquiry bot. You can ask questions about the stock of a specific company"),
        (THANK, "thankyou"): (THANK, "You are very welcome"),
        (THANK, "stock_search"): (CHOOSED, stock_re),
    }
    return policy


# Send the messages
global state
state = INIT

from wxpy import *

bot = Bot()

"""my_friend = bot.friends().search('RoyZ🐬')[0]"""

@bot.register(bot.self,except_self=False)

def reply_self(msg):
    global state
    global response
    message = str(msg.text)
    state = send_message(policyrule(), state, message)

    return response

embed()
