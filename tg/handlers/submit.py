import os
from typing import Union, Type

from telegram import Update, Bot, InlineKeyboardMarkup, ParseMode
from telegram.ext import CallbackContext

from tg.markup.keyboards import build_vote_keyboard
from models.phrase import Phrase, LongPhrase
from models.proposal import Proposal, LongProposal
from tg.decorators import log_update

curators_chat_id = os.environ.get("MOD_CHAT_ID", "")
SIMILARITY_DISCARD_THRESHOLD = int(os.getenv("PHRASE_DISMISSAL_SIMILARITY_THRESHOLD", 90))

proposal_t = Union[Type[Proposal], Type[LongProposal]]
phrase_t = Union[Type[Phrase], Type[LongPhrase]]


def submit_handling(bot: Bot, update: Update, proposal_class: proposal_t, phrase_class: phrase_t):
    submitted_by = update.effective_user.name

    proposal = proposal_class.from_update(update)
    if proposal.text == '':
        return update.effective_message.reply_text(
            f'Tienes que decirme que quieres proponer, por ejemplo: "/proponer {Phrase.get_random_phrase()}"'
            f' o "/proponerfrase {LongPhrase.get_random_phrase()}".'
        )

    # Fuzzy search. If we have one similar, discard.
    most_similar, similarity_ratio = phrase_class.get_most_similar(proposal.text)
    if SIMILARITY_DISCARD_THRESHOLD < similarity_ratio:
        text = f'Esa ya la tengo, {Phrase.get_random_phrase()}, {Phrase.get_random_phrase()}.'
        if similarity_ratio != 100:
            text += f'\nSe parece demasiado a "<b>{most_similar}</b>", {Phrase.get_random_phrase()}.'
        return update.effective_message.reply_text(text, parse_mode=ParseMode.HTML)

    proposal.save()

    curators_reply_markup = InlineKeyboardMarkup(build_vote_keyboard(proposal.id, proposal.kind))
    curators_message_text = f"{submitted_by} dice que deberiamos añadir la siguiente {phrase_class.name} a la lista:" \
                            f"\n'<b>{proposal.text}</b>'" \
                            f"\nLa mas parecida es: '<b>{most_similar}</b>' ({similarity_ratio}%)"

    bot.send_message(curators_chat_id, curators_message_text, reply_markup=curators_reply_markup,
                     parse_mode=ParseMode.HTML)
    update.effective_message.reply_text(
        f"Tu aportación será valorada por un consejo de cuñaos expertos y te avisaré una vez haya sido evaluada, "
        f"{Phrase.get_random_phrase()}.",
        quote=True,
    )


@log_update
def handle_submit(update: Update, context: CallbackContext):
    if len(update.effective_message.text.split(" ")) > 5:
        return update.effective_message.reply_text(
            f'¿Estás seguro de que esto es una frase corta, {Phrase.get_random_phrase()}?\n'
            f'Mejor prueba con /proponerfrase {Phrase.get_random_phrase()}.',
            quote=True
        )
    submit_handling(context.bot, update, Proposal, Phrase)


@log_update
def handle_submit_long(update: Update, context: CallbackContext):
    submit_handling(context.bot, update, LongProposal, LongPhrase)
