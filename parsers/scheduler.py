import schedule
#import parser_playstation
import xbox
from tamam_logger import tamam_logger

def run_parsers():
    tamam_logger('DEBUG', f'Таймер запускает парсеры, время 13:05')
    xbox.main()

def main(party_time):
    schedule.every().day.at(party_time).do(run_parsers)

    while True:
        schedule.run_pending()

if __name__ == '__main__':
    main('13:05')