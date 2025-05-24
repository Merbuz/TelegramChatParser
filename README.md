# Telegram Chat Parser

This project was made for free for the portfolio.

A telegram bot that allows you to search for messages in your selected chats by keywords and sends links to the messages you found.
It works with both public and private chats.

## Download
```cmd
git clone https://github.com/Merbuz/TelegramChatParser.git
```
```cmd
cd TelegramChatParser
```
```cmd
pip install -r requirements.txt
```

Next, change the **settings.ini** file, add your ID as an administrator there (you can add several if you specify them separated by commas without spaces)
```ini
# settings.ini
[Bot]
white_list = 1234,12345
view_logs = true
```

Next, create the **.env** file
```.env
API_ID=1234
API_HASH="api hash here"
BOT_TOKEN="bot token here"
```

That`s all! You can run it

## Usage
```cmd
python main.py &
```
