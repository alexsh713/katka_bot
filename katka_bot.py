#-*- coding: utf-8 -*-
import requests
import auth
import logging
#import red_watcher as rw
#import day_spent_time as DST
#import spent_time as ST
from config import token
from telegram.ext import Updater, CommandHandler, RegexHandler
from bittrex import Bittrex
from time import sleep
from subprocess import Popen, PIPE
from answers import ans
from random import choice
from requests.exceptions import ConnectionError

# Enable logging
valute_url = 'https://www.cbr-xml-daily.ru/daily_json.js'

my_btc = 0.05258306
my_eth = 0.94889211
my_xrp = 83.8603371
my_xmr = 1.39418595
foxy_btc = 0.01487875
foxy_eth = 1.08679013
foxy_xrp = 84.2696629
foxy_xmr = 0.5466565


requests_kwargs={'proxy_url': 'socks5://195.201.139.89:59020', 'urllib3_proxy_kwargs':{'username': 'proxy', 'password': 'nuiotlichno'}}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
# ans['Valute']['USD']['Value']

def usd_to_rub(usd):
    try:
        response = requests.get(valute_url)
        ans = response.json() 
        usd_price = ans['Valute']['USD']['Value']
        return usd*usd_price
    except ConnectionError:
        return None





def start(bot, update):
    #print update.message.chat_id
    update.message.reply_text('Ага')

def other(bot, update):
    update.message.reply_text(choice(ans))


def show_coin_price(bot, update, coin_name):
    pass


def bitcoin(bot, update):
    btc = requests.get('https://api.coinmarketcap.com/v1/ticker/bitcoin/')
    output = btc.json()[0]['price_usd'] + "$" + "       " + btc.json()[0]['percent_change_24h'] + "%"
    update.message.reply_text(output)


def zcash(bot, update):
    zcash = requests.get('https://api.coinmarketcap.com/v1/ticker/zcash/')
    output = zcash.json()[0]['price_usd'] + "$" + "       " + zcash.json()[0]['percent_change_24h'] + "%"
    update.message.reply_text(output)

def monacoin(bot, update):
    monacoin = requests.get('https://api.coinmarketcap.com/v1/ticker/monacoin/')
    output = monacoin.json()[0]['price_usd'] + "$" + "       " + monacoin.json()[0]['percent_change_24h'] + "%"
    update.message.reply_text(output)

def ethereum(bot, update):
    ethereum = requests.get('https://api.coinmarketcap.com/v1/ticker/ethereum/')
    output = ethereum.json()[0]['price_usd'] + "$" + "       " + ethereum.json()[0]['percent_change_24h'] + "%"
    update.message.reply_text(output)


def my_bittrex():
    total = []
    my_b = Bittrex(auth.api_key, auth.api_secret)
    balances = my_b.get_balances()
    for currency in balances['result']:
        if currency['Available'] > 0:
            curr = str(currency['Currency'])
            if curr == 'BTC':
                bal = currency['Available'] - my_btc - foxy_btc
                btc = requests.get('https://api.coinmarketcap.com/v1/ticker/bitcoin/')
                output = btc.json()[0]['price_usd']
                usd = float(output)*bal*0.5
                rub_btc = usd_to_rub(usd)
                total.append(rub_btc)
            elif curr == 'ETH':
                bal = currency['Available'] - my_eth - foxy_eth
                ethereum = requests.get('https://api.coinmarketcap.com/v1/ticker/ethereum/')
                output = ethereum.json()[0]['price_usd']
                usd = float(output)*bal*0.5
                rub_eth = usd_to_rub(usd)
                total.append(rub_eth)
            elif curr == 'DCR':
                bal = currency['Available']
                decred = requests.get('https://api.coinmarketcap.com/v1/ticker/decred/')
                output = decred.json()[0]['price_usd']
                usd = float(output)*bal*0.5
                rub_decred = usd_to_rub(usd)
                total.append(rub_decred)

            elif curr == 'ZEC':
                bal = currency['Available']
                zcash = requests.get('https://api.coinmarketcap.com/v1/ticker/zcash/')
                output = zcash.json()[0]['price_usd']
                usd = float(output)*bal*0.5
                rub_zcash = usd_to_rub(usd)
                total.append(rub_zcash)

        else:
            pass
    


    return int(sum(total))



def show_coin_price(bot, update, args):
    
    try:
        coin_name = args[0]
        coin = requests.get('https://api.coinmarketcap.com/v1/ticker/' + coin_name)
        if coin.status_code == 404:
            update.message.reply_text('coin not found')
        else:
            output = coin.json()[0]['price_usd'] + "$" + "       " + coin.json()[0]['percent_change_24h'] + "%"
            update.message.reply_text(output)

    except (IndexError, ValueError):
            update.message.reply_text('Usage: /coin <coin_name>')



def my_btc_handler(bot, update):
    if update.message.chat_id in auth.chat_idx:
        btc = requests.get('https://api.coinmarketcap.com/v1/ticker/bitcoin/')
        output = btc.json()[0]['price_usd']
        usd = float(output)*my_btc
        rub_btc = usd_to_rub(usd)
        if rub_btc:
            update.message.reply_text("Лаве " + str(rub_btc).split('.')[0])
        else:
            update.message.reply_text("Чет не могу посчитать в рублях, вот в баксах " + str(usd))

    else:
        update.message.reply_text("Не хватает прав для выполения. Попробуй с другой командой")

def my_eth_handler(bot, update):
    if update.message.chat_id in auth.chat_idx:
        ethereum = requests.get('https://api.coinmarketcap.com/v1/ticker/ethereum/')
        output = ethereum.json()[0]['price_usd']
        usd = float(output)*my_eth
        rub_eth = usd_to_rub(usd)
        if rub_eth:
            update.message.reply_text("Лаве " + str(rub_eth).split('.')[0])
        else:
            update.message.reply_text("Чет не могу посчитать в рублях, вот в баксах " + str(usd))
    else:
        update.message.reply_text("Не хватает прав для выполения. Попробуй с другой командой")

def my_ripple_handler(bot, update):
    if update.message.chat_id in auth.chat_idx:
        ripple = requests.get('https://api.coinmarketcap.com/v1/ticker/ripple/')
        output = ripple.json()[0]['price_usd']
        usd = float(output)*my_xrp
        rub_ripple = usd_to_rub(usd)
        if rub_ripple:
            update.message.reply_text("Лаве " + str(rub_ripple).split('.')[0])
        else:
            update.message.reply_text("Чет не могу посчитать в рублях, вот в баксах " + str(usd))
    else:
        update.message.reply_text("Не хватает прав для выполения. Попробуй с другой командой")


def my_monero_handler(bot, update):
    if update.message.chat_id in auth.chat_idx:
        monero = requests.get('https://api.coinmarketcap.com/v1/ticker/monero/')
        output = monero.json()[0]['price_usd']
        usd = float(output)*my_xmr
        rub_monero = usd_to_rub(usd)
        if rub_monero:
            update.message.reply_text("Лаве " + str(rub_monero).split('.')[0])
        else:
            update.message.reply_text("Чет не могу посчитать в рублях, вот в баксах " + str(usd))
    else:
        update.message.reply_text("Не хватает прав для выполения. Попробуй с другой командой")


def foxy_btc_handler(bot, update):
    if update.message.chat_id in auth.chat_idx:
        btc = requests.get('https://api.coinmarketcap.com/v1/ticker/bitcoin/')
        output = btc.json()[0]['price_usd']
        usd = float(output)*foxy_btc
        rub_btc = usd_to_rub(usd)
        if rub_btc:
            update.message.reply_text("Лаве " + str(rub_btc).split('.')[0])
        else:
            update.message.reply_text("Чет не могу посчитать в рублях, вот в баксах " + str(usd))
    else:
        update.message.reply_text("Не хватает прав для выполения. Попробуй с другой командой")

def foxy_eth_handler(bot, update):
    if update.message.chat_id in auth.chat_idx:
        ethereum = requests.get('https://api.coinmarketcap.com/v1/ticker/ethereum/')
        output = ethereum.json()[0]['price_usd']
        usd = float(output)*foxy_eth
        rub_eth = usd_to_rub(usd)
        if rub_eth:
            update.message.reply_text("Лаве " + str(rub_eth).split('.')[0])
        else:
            update.message.reply_text("Чет не могу посчитать в рублях, вот в баксах " + str(usd))
    else:
        update.message.reply_text("Не хватает прав для выполения. Попробуй с другой командой")


def foxy_ripple_handler(bot, update):
    if update.message.chat_id in auth.chat_idx:
        ripple = requests.get('https://api.coinmarketcap.com/v1/ticker/ripple/')
        output = ripple.json()[0]['price_usd']
        usd = float(output)*foxy_xrp
        rub_ripple = usd_to_rub(usd)
        if rub_ripple:
            update.message.reply_text("Лаве " + str(rub_ripple).split('.')[0])
        else:
            update.message.reply_text("Чет не могу посчитать в рублях, вот в баксах " + str(usd))
    else:
        update.message.reply_text("Не хватает прав для выполения. Попробуй с другой командой")


def foxy_monero_handler(bot, update):
    if update.message.chat_id in auth.chat_idx:
        monero = requests.get('https://api.coinmarketcap.com/v1/ticker/monero/')
        output = monero.json()[0]['price_usd']
        usd = float(output)*foxy_xmr
        rub_monero = usd_to_rub(usd)
        if rub_monero:
            update.message.reply_text("Лаве " + str(rub_monero).split('.')[0])
        else:
            update.message.reply_text("Чет не могу посчитать в рублях, вот в баксах " + str(usd))
    else:
        update.message.reply_text("Не хватает прав для выполения. Попробуй с другой командой")



def show_balances(bot, update):
    if update.message.chat_id in auth.masters_chat_idx:
        my_b = Bittrex(auth.api_key, auth.api_secret)
        balances = my_b.get_balances()
        for currency in balances['result']:
            if currency['Available'] > 0:
                curr = str(currency['Currency'])
                bal = str(currency['Available'])
                update.message.reply_text(curr + '  ' + bal)
    else:
        update.message.reply_text("Не хватает прав. Попробуй другую команду")


def total(bot, update):
    if update.message.chat_id in auth.chat_idx:
        btc = requests.get('https://api.coinmarketcap.com/v1/ticker/bitcoin/').json()[0]['price_usd']
        ethereum = requests.get('https://api.coinmarketcap.com/v1/ticker/ethereum/').json()[0]['price_usd']
        monero = requests.get('https://api.coinmarketcap.com/v1/ticker/monero/').json()[0]['price_usd']
        ripple = requests.get('https://api.coinmarketcap.com/v1/ticker/ripple/').json()[0]['price_usd']

        usd_total = float(btc)*my_btc + float(btc)*foxy_btc + float(ethereum)*my_eth + float(ethereum)*foxy_eth + \
                    float(monero)*my_xmr + float(monero)*foxy_xmr + float(ripple)*my_xrp + float(ripple)*foxy_xrp

        rub_total = usd_to_rub(usd_total) + my_bittrex()
        if rub_total:
            update.message.reply_text("Лаве " + str(rub_total).split('.')[0])
        else:
            update.message.reply_text("Чет не могу посчитать в рублях, вот в баксах " + str(usd_total))

    else:
        update.message.reply_text("Не хватает прав. Попробуй другую команду")     

# def spent_time(bot, update):
#     try:
#         answer = str(DST.spent_time())
#         update.message.reply_text("Spent time for today " + answer)
#     except:
#         update.message.reply_text("can't connect to redmine")

# def send_report(bot, update):
#      bot.send_document(chat_id=update.message.chat_id, document=open(str(ST.create_report()), 'rb'), timeout=5)


def status(bot, job):
    speeds = []

    try:
        response = requests.get(auth.katka_url)
        result = response.json()['result']
        for speed in result:
            speeds.append(speed['speed_sps'])
        #print speeds
        if sum(speeds) == 0:
            bot.send_message(job.context, text='Катка в ноль упала')
    

        
    except ConnectionError:
        bot.send_message(job.context, text='Чет катка не отвечает')






def set_timer(bot, update, args, job_queue, chat_data):
    """Add a job to the queue."""

    chat_id = update.message.chat_id
    if chat_id not in auth.masters_chat_idx:
        update.message.reply_text('Не хватает прав. Попробуй другую команду')

    else:
        try:
            # args[0] should contain the time for the timer in seconds
            due = int(args[0])
            if due < 0:
                update.message.reply_text('Не могу задать это')
                return

            # Add job to queue
            job = job_queue.run_repeating(status, interval=due, first=0, context=chat_id)
            chat_data['job'] = job

            update.message.reply_text('Ага, запускаю')

        except (IndexError, ValueError):
            update.message.reply_text('Usage: /set_polling <seconds>')


def unset(bot, update, chat_data):
    """Remove the job if the user changed their mind."""
    if update.message.chat_id in auth.masters_chat_idx:
        if 'job' not in chat_data:
            update.message.reply_text('А нет ниче')
            return

        job = chat_data['job']
        job.schedule_removal()
        del chat_data['job']

        update.message.reply_text('Ага, выключил')
    else:
        update.message.reply_text('Не хватает прав. Попробуй другую команду')

def check_for_cases(bot, job):
    if rw.show_recent_cases():
        for key in rw.show_recent_cases().viewkeys():
            for j,k in rw.show_recent_cases()[key].items():
                if j == 'update':
                    bot.send_message(job.context, text= j + ' ' + k)
                else:
                    bot.send_message(job.context, text= 'New case ' + str(j) + ' ' + k)


def redmine_sheduler(bot, update, args, job_queue, chat_data):
    """Add a job to the queue."""

    chat_id = update.message.chat_id
    if chat_id != auth.my_id:
        update.message.reply_text('Не хватает прав. Попробуй другую команду')

    else:
        try:
            # args[0] should contain the time for the timer in seconds
            due = int(args[0])
            if due < 0:
                update.message.reply_text('Не могу задать это')
                return

            # Add job to queue
            job = job_queue.run_repeating(check_for_cases, interval=due, first=0, context=chat_id)
            chat_data['job1'] = job

            update.message.reply_text('Запущено')

        except (IndexError, ValueError):
            update.message.reply_text('Usage: /redmine <seconds>')


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def on_pc(bot,update):
    chat_id = update.message.chat_id
    if chat_id != auth.my_id:
        update.message.reply_text('Не хватает прав. Попробуй другую команду')

    else:
        try:
            r = requests.get('http://192.168.88.1:1488')
        except ConnectionError:
            update.message.reply_text('Ага, включил')


def off_pc(bot,update):
    chat_id = update.message.chat_id
    if chat_id != auth.my_id:
        update.message.reply_text('Не хватает прав. Попробуй другую команду')

    else:
        try:
            r = requests.get('http://192.168.88.79:3000')
        except ConnectionError:
            update.message.reply_text('Ага, выключил')





def main():
    """Run bot."""
    updater = Updater(token, request_kwargs=requests_kwargs)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("bitcoin", bitcoin))
    dp.add_handler(CommandHandler("zcash", zcash))
    dp.add_handler(CommandHandler("monacoin", monacoin))
    dp.add_handler(CommandHandler("ethereum", ethereum))
    dp.add_handler(CommandHandler("coin", show_coin_price, pass_args=True))

    dp.add_handler(CommandHandler("balances", show_balances))
    dp.add_handler(CommandHandler("my_btc", my_btc_handler))
    dp.add_handler(CommandHandler("my_eth", my_eth_handler))
    dp.add_handler(CommandHandler("my_ripple", my_ripple_handler))
    dp.add_handler(CommandHandler("my_monero", my_monero_handler))
    
    dp.add_handler(CommandHandler("foxy_btc", foxy_btc_handler))
    dp.add_handler(CommandHandler("foxy_eth", foxy_eth_handler))
    dp.add_handler(CommandHandler("foxy_ripple", foxy_ripple_handler))
    dp.add_handler(CommandHandler("foxy_monero", foxy_monero_handler))
    #dp.add_handler(CommandHandler("spent", spent_time))
    #dp.add_handler(CommandHandler("report", send_report))
    dp.add_handler(CommandHandler("on", on_pc))
    dp.add_handler(CommandHandler("off", off_pc))
    dp.add_handler(CommandHandler("total", total))

    dp.add_handler(CommandHandler("set_polling", set_timer,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))

    dp.add_handler(CommandHandler("redmine", redmine_sheduler,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("unset", unset, pass_chat_data=True))
    dp.add_handler(RegexHandler('^.', other))
    # log all errors
    dp.add_error_handler(error)

    

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
