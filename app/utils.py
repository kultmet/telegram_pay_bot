from logger import info_logger, warning_logger

from aiogram import Bot, Dispatcher, executor, types
from config import bot
from app.buttons import exit_button

class MessageStack:
    """Стэк для ID Сообщений."""
    def __init__(self) -> None:
        self.messages = []

    def length(self):
        return len(self.messages)

    def push(self, message_id: int):
        self.messages.append(message_id)

    def pop(self):
        if len(self.messages) == 0:
            return None
        removed = self.messages.pop()
        return removed


message_stack = MessageStack()


async def delete_messages(message: types.Message):
    """Удалить сообщения из стека сообщений."""
    while message_stack.length() != 0:
        message_id = message_stack.pop()
        await bot.delete_message(
            chat_id=message.chat.id, message_id=message_id
        )
    info_logger.debug('delete_messages')



async def get_file(filename, message: types.Message):
    with open(filename, 'rb') as file:
        bot_message = await bot.send_document(message.chat.id, file)
        message_stack.push(bot_message.message_id)


async def exit_message(message: types.Message):
    bot_message = await message.answer(
        'Нажми /admin чтоб начать сначала',
        reply_markup=exit_button
    )
    message_stack.push(bot_message.message_id)