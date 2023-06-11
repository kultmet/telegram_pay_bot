from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


replenishment = InlineKeyboardButton(
    'Пополнить баланс', callback_data='add_amount'
)

fill_balance_buttons = InlineKeyboardMarkup()

fill_balance_buttons.add(replenishment)


users_button = InlineKeyboardButton(
    'Выгрузить всех пользователей с балансами', callback_data='get_balances'
)
logs_buttot = InlineKeyboardButton('Выгрузить логи', callback_data='get_logs')
user_managment = InlineKeyboardButton(
    'Управление Пользователями', callback_data='user_managment'
)

admin_buttons = InlineKeyboardMarkup()
admin_buttons.row(users_button)
admin_buttons.row(user_managment)
admin_buttons.add(logs_buttot)


user_payment = InlineKeyboardButton(
    'Платежи пользователя',
    callback_data='payments',
    switch_inline_query_current_chat='ps'
)
change_ballance = InlineKeyboardButton(
    'Изменить балланс',
    callback_data='change_ballance',
    switch_inline_query_current_chat='rs'
)

balance_buttons = InlineKeyboardMarkup().add(user_payment, change_ballance)

add_to_blacklist = InlineKeyboardButton(
    'В черный список', callback_data='add_to_blacklist'
)

user_management_buttons = InlineKeyboardMarkup()
user_management_buttons.add(add_to_blacklist)


admin_user_ballances = InlineKeyboardMarkup()

exit_button = InlineKeyboardMarkup()
exit_button.add(
    InlineKeyboardButton('Выйти из админки', callback_data='exit')
)
