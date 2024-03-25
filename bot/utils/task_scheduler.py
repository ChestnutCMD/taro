import schedule
from database.requests import update_tokens


def daily_token_update():
    schedule.every().day.at('00:01').do(update_tokens)
    while True:
        schedule.run_pending()

