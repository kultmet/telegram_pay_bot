import asyncio
import datetime
import logging

from aiogram import executor, types

from aiogram.dispatcher import FSMContext
from aiogram.types.message import ContentType
from dotenv import load_dotenv

from app.api import (
    create_blacklist_object,
    create_payments,
    create_user,
    exists_user,
    get_blacklist_sync,
    get_payments, get_users,
    update_ballance
)
from app.buttons import (
    fill_balance_buttons,
    admin_buttons,
    balance_buttons,
    user_management_buttons
)
from config import ADMINS, PAYMENTS_TOKEN, bot, dp
from constants import (
    ERROR_LOGS,
    GREETING,
    INFO_LOGS,
    USER_BALLANCE,
    PAYMENT_MESSAGE
)
from app.utils import delete_messages, exit_message, get_file, message_stack
from logger import info_logger, warning_logger
from app.states import AmountInput, BallanceInput

BANNED_USERS = set(get_blacklist_sync())
logging.basicConfig(level=logging.INFO)

load_dotenv()


@dp.message_handler(user_id=BANNED_USERS)
async def kick_user(message: types.Message):
    message_stack.push(message.message_id)
    await delete_messages(message)
    bot_message = await message.answer('FUCK YOU')
    await asyncio.sleep(3)
    message_stack.push(bot_message.message_id)
    await delete_messages(message)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    info_logger.info('start')
    try:
        if not (await exists_user(message.from_user.id)).get('exists'):
            await create_user(dict(message.from_user))
            info_logger.info('create_user')
        bot_message = await message.answer(
            GREETING.format(username=message.from_user.username),
            reply_markup=fill_balance_buttons
        )
        message_stack.push(bot_message.message_id)
    except AttributeError:
        warning_logger.error('AttributeError')


@dp.callback_query_handler(text='add_amount')
async def add_amount(call: types.CallbackQuery):
    info_logger.info(f'add_amount-call: {call.from_user.id}')
    try:
        bot_message = await call.message.answer(
            'Введите сумму, на которую вы хотите пополнить баланс'
        )
        message_stack.push(bot_message.message_id)
        await AmountInput.amount.set()
    except AttributeError:
        warning_logger.error('AttributeError')


@dp.message_handler(state=AmountInput.amount)
async def amount_reciver(message: types.Message, state: FSMContext):
    info_logger.info(
        f'amount_reciver: {message.from_user.id} send {message.text}'
    )
    try:
        int(message.text)
    except ValueError:
        bot_message = await message.answer(
            'Проверьте корректность ввода! Можно вводить тоько число!'
        )
        message_stack.push(bot_message.message_id)
        message_stack.push(message.message_id)
        warning_logger.warning(
            f'uncorrect input: {message.from_user.id} send "{message.text}"'
        )

        return
    bot_message = await message.answer(message.text)
    message_stack.push(bot_message.message_id)
    message_stack.push(message.message_id)
    try:
        price = types.LabeledPrice(
            label=f'Пополнить баланс на {message.text}',
            amount=int(message.text) * 100
        )
        info_logger.info(f'amount_reciver: {price}')
    except ValueError:
        bot_message = await message.answer(
            "Не корректный тип данных. Введите число"
        )
        message_stack.push(bot_message.message_id)
    await delete_messages(message)
    bot_invoice = await bot.send_invoice(
        chat_id=message.chat.id,
        title='Пополнение баланса',
        description='Пополнить баланс пользователя',
        provider_token=PAYMENTS_TOKEN,
        currency='rub',
        prices=[price],
        is_flexible=False,
        payload=datetime.datetime.now()
    )
    await state.finish()
    message_stack.push(bot_invoice.message_id)


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_cheskout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(
        pre_checkout_q.id, ok=True
    )
    info_logger.info(f'pre_cheskout_query: {pre_checkout_q}')


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    payment_info = message.successful_payment.to_python()
    info_logger.info(f'pre_cheskout_query: {payment_info}')
    await create_payments(message.from_user.id, payment_info)
    info_logger.info('successful_payment: complete')
    await delete_messages(message)


@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    message_stack.push(message.message_id)
    if message.from_user.id not in ADMINS:
        bot_message: types.Message = await message.answer(
            'Админ панель не доступна'
        )
        info_logger.info('admin: rejected')
        message_stack.push(bot_message.message_id)
    else:
        bot_message: types.Message = await message.answer(
            'Добро пожаловать!', reply_markup=admin_buttons
        )
        await delete_messages(message)
        message_stack.push(bot_message.message_id)
        info_logger.info('admin: accepted')


async def users(call: types.CallbackQuery, buttons):
    try:
        users = await get_users()
        for user in users:
            info_logger.info(f'get_balances: {user}')
            total_ballance = user.pop('total_ballance')
            bot_message = await call.message.answer(
                USER_BALLANCE.format(**user, ballance=total_ballance / 100),
                reply_markup=buttons
            )
            message_stack.push(bot_message.message_id)
    except TypeError:
        await call.answer(
            'Что-то пошло не так, скорее всего проблеммы на сервере.'
        )


@dp.callback_query_handler(text='get_balances')
async def get_balances(call: types.CallbackQuery):
    await delete_messages(call.message)
    info_logger.info(f'get_balances-call: {call.from_user.id}')
    bot_message = await call.message.answer('get_ballances')
    message_stack.push(bot_message.message_id)
    await users(call, balance_buttons)


@dp.callback_query_handler(text='payments')
async def payments(call: types.CallbackQuery):
    await delete_messages(call.message)
    # info_logger.info(f'payments-call: {call.from_user.id}')
    message = call.message.to_python()
    user_id = message.get('text').split('\n')[0].split(': ')[1]
    payments = await get_payments(user_id)
    if payments:
        if not payments:
            bot_message = await call.message.answer(
                f'У {user_id} пользователя Платежей не было'
            )
            message_stack.push(bot_message.message_id)
            info_logger.info('payments: None')
        for payment in payments:
            bot_message = await call.message.answer(
                PAYMENT_MESSAGE.format(**payment)
            )
            message_stack.push(bot_message.message_id)
            info_logger.info(f'payments: {payment}')
        await exit_message(call.message)
    else:
        await call.answer(
            'Что-то пошло не так, скорее всего проблеммы на сервере.'
        )


@dp.callback_query_handler(text='change_ballance')
async def change_ballance(call: types.CallbackQuery, state: FSMContext):
    info_logger.info(f'change_ballance-call: {call.from_user.id}')
    await call.answer('Введите сумму остатка')
    last_message = call.message.to_python()
    user_id = last_message.get('text').split('\n')[0].split(': ')[1]
    await BallanceInput.balance.set()
    async with state.proxy() as data:
        data['user_id'] = user_id


@dp.message_handler(state=BallanceInput.balance)
async def ballance_reciver(message: types.Message, state: FSMContext):
    info_logger.info(
        f'ballance_reciver: {message.from_user.id} send {message.text}'
    )
    async with state.proxy() as data:
        user_id = data['user_id']
    await message.answer(message.text)
    try:
        await update_ballance(
            user_id, {'total_ballance': float(message.text) * 100}
        )
        info_logger.info('update_ballance')
    except ValueError:
        await message.answer("Не корректный тип данных. Введите число")
        warning_logger.warning(
            f'uncorrect input: {message.from_user.id} send "{message.text}"'
        )
    await state.finish()


@dp.callback_query_handler(text='user_managment')
async def user_managment(call: types.CallbackQuery):
    await users(call, user_management_buttons)


@dp.callback_query_handler(text='add_to_blacklist')
async def add_to_blacklist(call: types.CallbackQuery):
    message = call.message.to_python()
    user_id = message.get('text').split('\n')[0].split(': ')[1]
    status = await create_blacklist_object(user_id)
    if status == 403:
        await call.answer('Этот пользователь уже в черном списке')
    elif status == 201:
        BANNED_USERS.add(user_id)
        await call.answer(f'Пользователь {user_id} добавлен в перный список')
    await delete_messages(call.message)


@dp.callback_query_handler(text='exit')
async def exit_admin(call: types.CallbackQuery):
    await delete_messages(call.message)


@dp.callback_query_handler(text='get_logs')
async def get_logs(call: types.CallbackQuery):
    await get_file(INFO_LOGS, call.message)
    await get_file(ERROR_LOGS, call.message)
    await exit_message(call.message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
