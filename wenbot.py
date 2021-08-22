import logging

from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler

# Set up logging module, to know when (and why) things don't work as expected
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Call the 'start' function everytime the Bot receives a Telegram message that contains the /start command. 
def start(update: Update, context: CallbackContext) -> None:
  context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
 
# Echo all text messages using MessageHandler
def echo(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

# Implement a /caps command that will take some text as an argument and reply to it in CAPS
def caps(update: Update, context: CallbackContext) -> None:
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

# Implement inline functionality https://core.telegram.org/bots/api#answerinlinequery
# Not necessary for wenbot, just leaving it here for possible future reference.
def inline_caps(update: Update, context: CallbackContext) -> None:
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)

# Reply to all commands that were not recognized by the previous handlers.
def unknown(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def main() -> None:
    """Run bot."""
    # Create the Updater and replace TOKEN with the Bot's API token.
    updater = Updater("TOKEN", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add the different handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))
    dispatcher.add_handler(CommandHandler("caps", caps))
    dispatcher.add_handler(InlineQueryHandler(inline_caps))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
