import logging
from typing import List
import configparser as Conf
import asyncio
from asyncio.subprocess import PIPE, create_subprocess_shell
import nest_asyncio
from functools import lru_cache

from typing import Any
from telegram.ext import Filters, MessageHandler, Updater
from telegram.ext.utils.types import CCT
from telegram.update import Update

# Configs parameters
configParser = Conf.RawConfigParser()
configParser.read(r"config.txt")

TELEGRAM_TOKEN: str = configParser.get("conf", "TELEGRAM_TOKEN")
AUTHORIZED_USERS: List[str] = ["sanixdarker", "elhmn42"]
_LOOP = asyncio.get_event_loop()
_COMMAND_OUTPUT = ""


# the printer could be
async def run(command: str, printer: Any):
    """
    For commands that can take some time, i still want some ongoing output logs, stderr/stdout

    Args:
        - command: command line we want to execute
        - printer: callback, we're going to use to output
    """
    global _LOOP

    @lru_cache(maxsize=3)
    async def _read_stream(stream, callback):
        global _COMMAND_OUTPUT

        while True:
            line = await stream.readline()
            if line:
                _COMMAND_OUTPUT += line.decode("UTF8")
                callback(_COMMAND_OUTPUT)
            else:
                break

    process = await create_subprocess_shell(
        f"{command}", stdout=PIPE, stderr=PIPE, shell=True
    )

    out_task = _LOOP.create_task(
        _read_stream(process.stdout, lambda x: printer(text=x))
    )
    err_task = _LOOP.create_task(
        _read_stream(process.stderr, lambda x: printer(text=x))
    )

    await asyncio.wait({out_task, err_task})
    await process.wait()


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
    global _COMMAND_OUTPUT
    try:
        if is_authorized(update) and is_private(update):
            _command = update.message.text
            logging.info(f"{_command=}")

            msg = update.message.reply_text(f"Running your command {_command}...")

            _LOOP.run_until_complete(run(_command, msg.edit_text))
            # to flush the remaining previous command output
            _COMMAND_OUTPUT = ""
    except Exception as es:
        logging.exception(f"[x] Error {es}")


def set_callback() -> Updater:
    updater = Updater(token=TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.text, exec_callback))

    return updater


if __name__ == "__main__":
    print("::tg-interface service started...")

    nest_asyncio.apply()

    updater = set_callback()
    updater.start_polling()

    updater.idle()
