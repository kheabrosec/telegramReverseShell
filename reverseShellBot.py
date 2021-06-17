import logging
import subprocess
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import platform
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def osinfo(update: Update, context: CallbackContext) -> None:
        update.message.reply_text("System: "+platform.uname()[0]+"\n"+"Node: "+platform.uname()[1]+"\n"+"Release: "+platform.uname()[2]+"\n"+"Version: "+platform.uname()[3]+"\n"+"Machine: "+platform.uname()[4]+"\n"+"Processor: "+platform.uname()[5])

def chunkstring(string,length):
    return (string[0 + i:length + i] for i in range(0, len(string), length))

def execute(update: Update, contect:CallbackContext) -> None:
    print(update.message.text.split(" "))
    user = update.message.from_user
    print(user.id)
    if str(user.id) in ["YOUR ID"]:
        try:
            p = subprocess.run(update.message.text.split(" "), shell=True, capture_output=True)
            out=p.stdout
            if int(len(out)) < 4090:
                update.message.reply_text(out.decode("latin-1"))
            else:
                for element in list(chunkstring(out,4090)):
                    update.message.reply_text(element.decode("latin-1"))
        except Exception as e:
            print(e)
            update.message.reply_text("<b>Command error.</b>", parse_mode="html")
    else:
        update.message.reply_text("<b>Command error.</b>", parse_mode="html")

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("YOUR TOKEN")
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("osinfo", osinfo))
    dispatcher.add_handler(CommandHandler("help", help_command))
    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, execute))
    # Start the Bot
    updater.start_polling()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
