from telebot.states import State
from telebot.types import CallbackQuery, Message
from telebot.async_telebot import AsyncTeleBot
from telebot.states import resolve_context

from typing import Union


class StateContext:
    """
    Class representing a state context.

    Passed through a middleware to provide easy way to set states.

    .. code-block:: python3

        @bot.message_handler(commands=['start'])
        async def start_ex(message: types.Message, state_context: StateContext):
            await state_context.set(MyStates.name)
            await bot.send_message(message.chat.id, 'Hi, write me a name', reply_to_message_id=message.message_id)
            # also, state_context.data(), .add_data(), .reset_data(), .delete() methods available.
    """

    def __init__(self, message: Union[Message, CallbackQuery], bot: AsyncTeleBot) -> None:
        self.message: Union[Message, CallbackQuery] = message
        self.bot: AsyncTeleBot = bot
        self.bot_id = self.bot.bot_id

    async def set(self, state: Union[State, str]) -> bool:
        """
        Set state for current user.

        :param state: State object or state name.
        :type state: Union[State, str]

        .. code-block:: python3

            @bot.message_handler(commands=['start'])
            async def start_ex(message: types.Message, state_context: StateContext):
                await state_context.set(MyStates.name)
                await bot.send_message(message.chat.id, 'Hi, write me a name', reply_to_message_id=message.message_id)
        """

        chat_id, user_id, business_connection_id, bot_id, message_thread_id = (
            resolve_context(self.message, self.bot.bot_id)
        )
        if isinstance(state, State):
            state = state.name
        return await self.bot.set_state(
            chat_id=chat_id,
            user_id=user_id,
            state=state,
            business_connection_id=business_connection_id,
            bot_id=bot_id,
            message_thread_id=message_thread_id,
        )

    async def get(self) -> str:
        """
        Get current state for current user.

        :return: Current state name.
        :rtype: str
        """

        chat_id, user_id, business_connection_id, bot_id, message_thread_id = (
            resolve_context(self.message, self.bot.bot_id)
        )
        return await self.bot.get_state(
            chat_id=chat_id,
            user_id=user_id,
            business_connection_id=business_connection_id,
            bot_id=bot_id,
            message_thread_id=message_thread_id,
        )

    async def delete(self) -> bool:
        """
        Deletes state and data for current user.

        .. warning::

                This method deletes state and associated data for current user.
        """
        chat_id, user_id, business_connection_id, bot_id, message_thread_id = (
            resolve_context(self.message, self.bot.bot_id)
        )
        return await self.bot.delete_state(
            chat_id=chat_id,
            user_id=user_id,
            business_connection_id=business_connection_id,
            bot_id=bot_id,
            message_thread_id=message_thread_id,
        )

    async def reset_data(self) -> bool:
        """
        Reset data for current user.
        State will not be changed.
        """

        chat_id, user_id, business_connection_id, bot_id, message_thread_id = (
            resolve_context(self.message, self.bot.bot_id)
        )
        return await self.bot.reset_data(
            chat_id=chat_id,
            user_id=user_id,
            business_connection_id=business_connection_id,
            bot_id=bot_id,
            message_thread_id=message_thread_id,
        )

    def data(self) -> dict:
        """
        Get data for current user.

        .. code-block:: python3

            with state_context.data() as data:
                print(data)
                data['name'] = 'John'
        """

        chat_id, user_id, business_connection_id, bot_id, message_thread_id = (
            resolve_context(self.message, self.bot.bot_id)
        )
        return self.bot.retrieve_data(
            chat_id=chat_id,
            user_id=user_id,
            business_connection_id=business_connection_id,
            bot_id=bot_id,
            message_thread_id=message_thread_id,
        )

    async def add_data(self, **kwargs) -> None:
        """
        Add data for current user.

        :param kwargs: Data to add.
        :type kwargs: dict
        """

        chat_id, user_id, business_connection_id, bot_id, message_thread_id = (
            resolve_context(self.message, self.bot.bot_id)
        )
        return await self.bot.add_data(
            chat_id=chat_id,
            user_id=user_id,
            business_connection_id=business_connection_id,
            bot_id=bot_id,
            message_thread_id=message_thread_id,
            **kwargs
        )
