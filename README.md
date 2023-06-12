# telegram_pay_bot
This telegram-bot knows how to pay and administer user-unit

## How to start?

сбилдить образ

```
docker build -t payment_bot .
```

запуск контейнера с ботом (НЕ РАБОТАЕТ БЕЗ API)

```
docker run --env TELEGRAM_TOKEN=5412219453:AAExZmPDpq998Pjan2i_-4dDyoyzOc7LJg0 --env PAYMENTS_TOKEN=401643678:TEST:10a79676-94a1-4759-badd-2060fe042310 --network=host --name payment_bot --rm -p 8080:8080 payment_bot
```
### Здесь используется Telegram Payments так как заказчик сказал что Qiwi сейчас багует

Search 

Напишите на @BotFather команду /start 

далее /newbot следуйте инструкциям по созданию бота

копируйте токен в в файл .env в переменную

TELEGRAM_TOKEN=<ваш_токен>

далее
введите команту /mybots
выберите вашего бота -> нажмите кнопку Payments -> следуйте инструкциям по вубору провайдера

полученый токен скопируйте в переменную
PAYMENTS_TOKEN=<ваш_платежный_токен>

### тестовая карта

Номер карты	4111 1111 1111 1111
Дата истечения срока действия	
2024/12

Проверочный код на обратной стороне	123
3-D Secure	veres=y, pares=y
Проверочный код 3-D Secure	12345678