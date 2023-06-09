import schedule
#import parser_playstation
import xbox
from tamam_logger import tamam_logger

def run_parsers():
    tamam_logger('DEBUG', f'Таймер запускает парсеры, время {party_time}')
    xbox.main()

def main(party_time):
    schedule.every().day.at(party_time).do(run_parsers)

    while True:
        schedule.run_pending()

if __name__ == '__main__':
    party_time = '18:08'
    main(party_time)