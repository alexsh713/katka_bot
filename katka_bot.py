#-*- coding: utf-8 -*-
import requests
import auth
import logging
from config import token
from telegram.ext import Updater, CommandHandler, RegexHandler
from bittrex import Bittrex
from time import sleep
from subprocess import Popen, PIPE
from answers import ans
from random import choice

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
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



def bittrex(bot, update):
    my_b = Bittrex(auth.api_key, auth.api_secret)
    balance = my_b.get_balance('ZEC')
    zec_value = balance['result']['Available']
    update.message.reply_text(zec_value)

def show_balances(bot, update):
    my_b = Bittrex(auth.api_key, auth.api_secret)
    balances = my_b.get_balances()
    for currency in balances['result']:
        if currency['Available'] > 0:
            curr = str(currency['Currency'])
            bal = str(currency['Available'])
            update.message.reply_text(curr + '  ' + bal)



def status(bot, update):
    data = 'iperf -c 192.168.62.65 -p 3389 -t1'
    stdout = Popen(data, shell=True, stdout=PIPE).stdout
    if stdout.read() != '':
        update.message.reply_text('Катка в порядке')
    else:
        update.message.reply_text('Чет не так с каткой')




def check_status(bot, job):
    """Send the alarm message."""
    data = 'iperf -c 192.168.62.65 -p 3389 -t1'
    stdout = Popen(data, shell=True, stdout=PIPE).stdout
    if stdout.read() == '':
        bot.send_message(job.context, text='Катка подохла')


def set_timer(bot, update, args, job_queue, chat_data):
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(args[0])
        if due < 0:
            update.message.reply_text('Не могу задать это')
            return

        # Add job to queue
        job = job_queue.run_repeating(check_status, interval=due, first=0, context=chat_id)
        chat_data['job'] = job

        update.message.reply_text('Ага, запускаю')

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set_polling <seconds>')


def unset(bot, update, chat_data):
    """Remove the job if the user changed their mind."""
    if 'job' not in chat_data:
        update.message.reply_text('А нет ниче')
        return

    job = chat_data['job']
    job.schedule_removal()
    del chat_data['job']

    update.message.reply_text('Ага, выключил')


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Run bot."""
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("bitcoin", bitcoin))
    dp.add_handler(CommandHandler("zcash", zcash))
    dp.add_handler(CommandHandler("monacoin", monacoin))
    dp.add_handler(CommandHandler("ethereum", ethereum))

    #dp.add_handler(CommandHandler("bittrex", bittrex))
    #dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("balances", show_balances))

    # dp.add_handler(CommandHandler("set_polling", set_timer,
    #                               pass_args=True,
    #                               pass_job_queue=True,
    #                               pass_chat_data=True))
    # dp.add_handler(CommandHandler("unset", unset, pass_chat_data=True))
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