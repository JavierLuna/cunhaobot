from telegram import Update, Bot

from models.phrase import Phrase

def handle_start(bot: Bot, update: Update):
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        f'¿Que pasa, {Phrase.get_random_phrase()}? '
        'Soy CuñaoBot, mi función principal es darte frases de cuñao, perfectas para cualquier ocasión.\n'
        'Puedes usar /submit <frase> para proponer tu frase de cuñado favorita.\n'
        'Tambien puedes invocarme en cualquier chat con @cunhaobot (como el bot de gifs '
        'para recibir frases de cuñao')
