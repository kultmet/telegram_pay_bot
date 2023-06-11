from aiogram.dispatcher.filters import state


class AmountInput(state.StatesGroup):
    amount = state.State()


class BallanceInput(state.StatesGroup):
    balance = state.State()
    user_id = state.State()
