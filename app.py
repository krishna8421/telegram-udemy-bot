import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
TOKEN = ""

###___Telegram___###
# Logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                   level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text('Hi!')

def help(update, context):
    update.message.reply_text('Send URL and I will do the rest!')
## Main Function
def Udemy(update, context):
    if update.message.text[0:5] == 'https':
        ###___Udemy___###
        udemyURL = update.message.text

        getSourceCode = requests.get(udemyURL)

        soup = BeautifulSoup(getSourceCode.text, 'html.parser')
        # Image
        for item in soup.find_all('img', limit=2):
            if item['src'][0:5] == 'https':
                imgURL = item['src']
        # Info

        title           = soup.find('h1', class_='clp-lead__title--small').getText()
        description     = soup.find('div', class_='clp-lead__headline').getText()
        rating          = soup.find('div', attrs={'data-purpose':'rating'}).getText()
        time            = soup.find('div', attrs={'data-purpose':'curriculum-stats'}).getText()
        instructor      = soup.find('div', attrs={'data-purpose':'instructor-name-top'}).getText()
        info      = soup.find('div', attrs={'class':'clp-lead__element-meta'}).getText()

        rating = rating.split(" ")
        info = info.strip().split("\n")


        ## Final Variable
        title           = title.strip()
        description     = description.strip()+"\n"
        ratedBy         = "Rated by: " + rating[5][1:] + "students"
        rating          = "Rating: " + rating[1]
        time            = time+"\n"
        instructor      = "Creator: " + instructor[11:]
        lang            = "Lang: " + info[10]
        lastUpdated     = "Last Update: " + info[0][12:]

        caption = title+"\n\n"+description+"\n"+time+"\n"+rating+"\n"+ratedBy+"\n"+lastUpdated+"\n"+lang

        # Send Msg
        context.bot.send_photo(chat_id=update.effective_chat.id, photo = imgURL, caption=caption)
    else:
        update.message.reply_text('Send a URL')
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, Udemy))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()
if __name__ == '__main__':
    main()