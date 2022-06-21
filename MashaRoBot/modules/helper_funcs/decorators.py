from MashaRoBot.modules.disable import DisableAbleCommandHandler, DisableAbleMessageHandler
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, InlineQueryHandler
from telegram.ext.filters import BaseFilter, Filters
from MashaRoBot import dispatcher as d
from typing import Optional, Union, List


class SerenaTelegramHandler:
    def __init__(self, d):
        self._dispatcher = d

    def command(
            self, command: str, filters: Optional[BaseFilter] = None, admin_ok: bool = False, pass_args: bool = False,
            pass_chat_data: bool = False, run_async: bool = True, can_disable: bool = True,
            group: Optional[int] = 40
    ):
        if filters:
           filters = filters & ~Filters.update.edited_message
        else:
            filters = ~Filters.update.edited_message
        def _command(func):
            try:
                if can_disable:
                    self._dispatcher.add_handler(
                        DisableAbleCommandHandler(command, func, filters=filters, run_async=run_async,
                                                  pass_args=pass_args, admin_ok=admin_ok), group
                    )
                else:
                    self._dispatcher.add_handler(
                        CommandHandler(command, func, filters=filters, run_async=run_async, pass_args=pass_args), group
                    )
            except TypeError:
                if can_disable:
                    self._dispatcher.add_handler(
                        DisableAbleCommandHandler(command, func, filters=filters, run_async=run_async,
                                                  pass_args=pass_args, admin_ok=admin_ok, pass_chat_data=pass_chat_data)
                    )
                else:
                    self._dispatcher.add_handler(
                        CommandHandler(command, func, filters=filters, run_async=run_async, pass_args=pass_args,
                                       pass_chat_data=pass_chat_data)
                    )

            return func

        return _command

    def message(self, pattern: Optional[BaseFilter] = None, can_disable: bool = True, run_async: bool = True,
                group: Optional[int] = 60, friendly=None):
        if pattern:
           pattern = pattern & ~Filters.update.edited_message
        else:
           pattern = ~Filters.update.edited_message
        def _message(func):
            try:
                if can_disable:
                    self._dispatcher.add_handler(
                        DisableAbleMessageHandler(pattern, func, friendly=friendly, run_async=run_async), group
                    )
                else:
                    self._dispatcher.add_handler(
                        MessageHandler(pattern, func, run_async=run_async), group
                    )
            except TypeError:
                if can_disable:
                    self._dispatcher.add_handler(
                        DisableAbleMessageHandler(pattern, func, friendly=friendly, run_async=run_async)
                    )
                else:
                    self._dispatcher.add_handler(
                        MessageHandler(pattern, func, run_async=run_async)
                    )

            return func

        return _message

    def callbackquery(self, pattern: str = None, run_async: bool = True):
        def _callbackquery(func):
            self._dispatcher.add_handler(CallbackQueryHandler(pattern=pattern, callback=func, run_async=run_async))
            return func

        return _callbackquery

    def inlinequery(self, pattern: Optional[str] = None, run_async: bool = True, pass_user_data: bool = True,
                    pass_chat_data: bool = True, chat_types: List[str] = None):
        def _inlinequery(func):
            self._dispatcher.add_handler(
                InlineQueryHandler(pattern=pattern, callback=func, run_async=run_async, pass_user_data=pass_user_data,
                                   pass_chat_data=pass_chat_data, chat_types=chat_types))
            return func

        return _inlinequery


sercmd = SerenaTelegramHandler(d).command
sermsg = SerenaTelegramHandler(d).message
sercallback = SerenaTelegramHandler(d).callbackquery
serinline = SerenaTelegramHandler(d).inlinequery
