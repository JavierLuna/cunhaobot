from telegram import Bot, Update

from tg.utils.decorators import log_update


@log_update
def handle_chosen_inline_result(bot: Bot, update: Update):
    pass