## chatbot.py
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
# The messageHandler is used for all message updates
import configparser
import logging
import omdb
from googleapiclient.discovery import build

OMDB_API_KEY= '70dae977'
omdb.set_default('apikey', OMDB_API_KEY)

YOUTUBE_API_KEY = 'AIzaSyB4G75-bAT33T5SVZDI2whjxJNqY1gTlrw'
youtube = build('youtube','v3',developerKey=YOUTUBE_API_KEY)

def main():
    # Load your token and create an Updater for your Bot
    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher
    # You can set this logging module, so you will know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    
    # register a dispatcher to handle message: here we register an echo dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    # on different commands - answer in Telegram
    #dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("trailer", trailer))
    dispatcher.add_handler(CommandHandler("search", search))
    dispatcher.add_handler(CommandHandler("hello", greeting))

    # To start the bot:
    updater.start_polling()
    updater.idle()

def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)

def listToString(s): 
    str1 = " "  
    return (str1.join(s))

def trailer(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /search is issued."""
    try: 
        logging.info(context.args[0])
        nm = listToString(context.args[0:len(context.args)])   # /search keyword <-- this should store the keyword
        request = youtube.search().list(
            part='id,snippet',
            q=nm,
            maxResults=5,
            type='video'
            )
        response = request.execute()
        video_link_1='https://www.youtube.com/watch?v='+response['items'][0]['id']['videoId']
        video_link_2='https://www.youtube.com/watch?v='+response['items'][1]['id']['videoId']
        video_link_3='https://www.youtube.com/watch?v='+response['items'][2]['id']['videoId']
        video_link_4='https://www.youtube.com/watch?v='+response['items'][3]['id']['videoId']
        video_link_5='https://www.youtube.com/watch?v='+response['items'][4]['id']['videoId']
        update.message.reply_text('Link:' + video_link_1)
        update.message.reply_text('Link:' + video_link_2)
        update.message.reply_text('Link:' + video_link_3)
        update.message.reply_text('Link:' + video_link_4)
        update.message.reply_text('Link:' + video_link_5)
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /search <keyword>')

def search(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /search is issued."""
    try: 
        logging.info(context.args[0])
        nm = listToString(context.args[0:len(context.args)])   # /search keyword <-- this should store the keyword
        movie_detail=omdb.get(title=nm, fullplot=True, tomatoes=True)
        update.message.reply_text('Plot:' + movie_detail['plot'])
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /search <keyword>')

def greeting(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /hello is issued."""
    try: 
        logging.info(context.args[0])
        nm = context.args[0]   # /hello keyword <-- this should store the keyword
        update.message.reply_text('Good Day, ' + nm +  '!')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /hello <keyword>')

if __name__ == '__main__':
    main()