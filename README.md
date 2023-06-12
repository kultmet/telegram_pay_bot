# telegram_pay_bot
This telegram-bot knows how to pay and administer user-unit


|Проект состоит из ДВУХ сервисов|



# How to start?



## Сервис №1 - API
клонировать telegram_pay_admin (API)


```
git clone https://github.com/kultmet/telegram_pay_admin.git
```

<hr>

запуск

```
cd /<путь к корневой папке проекта>

docker-compose up -d
```

## Сервис №2

клонировать telegram_pay_bot


```
git clone https://github.com/kultmet/telegram_pay_bot.git
```


#### токен 

Напишите на @BotFather команду /start 

далее /newbot следуйте инструкциям по созданию бота

копируйте токен в в файл .env в переменную

TELEGRAM_TOKEN=<ваш_токен>

<hr>

#### Платежный токен 

далее

введите команту /mybots

выберите вашего бота -> нажмите кнопку Payments -> следуйте инструкциям по вубору провайдера

полученый токен скопируйте в переменную

PAYMENTS_TOKEN=<ваш_платежный_токен>

<hr>

сбилдить образ

```
docker build -t payment_bot .
```




запуск контейнера с ботом (НЕ РАБОТАЕТ БЕЗ API)

```
docker run --env TELEGRAM_TOKEN=<ваш токен> --env PAYMENTS_TOKEN=<ваш платежный токен> --network=host --name payment_bot --rm -p 8080:8080 payment_bot
```
### Здесь используется Telegram Payments так как заказчик сказал что Qiwi сейчас багует




### тестовая карта

Номер карты	4111 1111 1111 1111
Дата истечения срока действия	
2024/12

Проверочный код на обратной стороне	123
3-D Secure	veres=y, pares=y
Проверочный код 3-D Secure	12345678