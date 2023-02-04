import logging
import subprocess
from typing import List
import configparser as Conf

from telegram.ext import Filters, MessageHandler, Updater
from telegram.ext.utils.types import CCT
from telegram.update import Update

# Configs parameters
configParser = Conf.RawConfigParser()
configParser.read(r"config.txt")

TELEGRAM_TOKEN: str = configParser.get("conf", "TELEGRAM_TOKEN")
AUTHORIZED_USERS: List[str] = ["sanixdarker", "elhmn42"]


def execute_cmd(_input: str):
    logging.info(f"{_input=}")
    logging.info(f'{_input.split(" ")=}')

    return subprocess.getoutput(_input)
    # return (
    #     result.stdout.decode("utf-8") if result.stdout is not None else None,
    #     result.stderr.decode("utf-8") if result.stderr is not None else None
    # )

def is_private(update: Update) -> bool:
    if update.message.chat.type == "private":
        return True
    return False


def is_authorized(update: Update) -> bool:
    user_name = str(update.message.from_user["username"])
    logging.info(f"{user_name=}")

    if len(user_name) > 1 and user_name in AUTHORIZED_USERS:
        return True
    return False


def exec_callback(update: Update, context: CCT) -> None:
    try:
        if is_authorized(update) and is_private(update):
            _command = update.message.text
            stdout = execute_cmd(_command)

            context.bot.send_message(
                chat_id=update.message.chat_id,
                text=(
                    f"::stdout::\n {stdout}\n\n"
                )
            )
    except Exception as es:
        logging.exception(f"[x] Error {es}")


def set_callback() -> Updater:
    updater = Updater(token=TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text, exec_callback))

    return updater


if __name__ == "__main__":
    updater = set_callback()
    updater.start_polling()

    updater.idle()
