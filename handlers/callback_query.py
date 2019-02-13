import os

from telegram import Update, Bot, InlineKeyboardMarkup

from constants import LIKE, DISLIKE
from markup.keyboards import build_vote_keyboard
from models.phrase import Phrase
from models.proposal import Proposal

curators_chat_id = int(os.environ["MOD_CHAT_ID"])


def handle_callback_query(bot: Bot, update: Update):
    data = update.callback_query.data
    vote, proposal_id = data.split(":")

    proposal = Proposal.load(proposal_id)
    if proposal is None:
        # replying to a message that is not a proposal anymore, most likely erased proposal
        update.callback_query.answer("Esa propuesta ha muerto")
        return

    if update.callback_query.from_user.id in proposal.voted_by:
        # Ignore users who already voted
        update.callback_query.answer("Tu ya has votado maquina")
        return

    proposal.add_vote(vote == LIKE, update.callback_query.from_user.id)
    proposal.save()
    update.callback_query.answer(f"Tu voto: {vote} ha sido añadido")

    if proposal.likes >= 2:
        update.callback_query.edit_message_text(
            f"La propuesta '{proposal.text}' queda formalmente aprobada y añadida a la lista"
        )
        bot.send_message(
            proposal.from_chat_id, f"Tu propuesta '{proposal.text}' ha sido aprobada, felicidades, máquina",
            reply_to_message_id=proposal.from_message_id
        )
        Phrase.upload_from_proposal(proposal)
    elif proposal.dislikes >= 2:
        update.callback_query.edit_message_text(
            f"La propuesta '{proposal.text}' queda formalmente rechazada")
        bot.send_message(
            proposal.from_chat_id, f"Tu propuesta '{proposal.text}' ha sido rechazada, lo siento figura",
            reply_to_message_id=proposal.from_message_id
        )
    else:
        text = update.callback_query.message.text
        user = update.callback_query.from_user.username or update.callback_query.first_name
        reply_markup = InlineKeyboardMarkup(build_vote_keyboard(proposal.id))
        update.callback_query.edit_message_text(f"{text}\n{user}: {vote}", reply_markup=reply_markup)




