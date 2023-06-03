import schedule
import parser_playstation
import parser_xbox

from table_delete_alchemy import delete_table
from table_create_alchemy import create_table

def run_parsers():
    #delete_table('xbox')
    #create_table('xbox')
    #parser_xbox.xbox_parser()
    #delete_table('playstation')
    #create_table('playstation')
    parser_playstation.playstation_parser()


def main():
    schedule.every().day.at('12:12').do(run_parsers)

    while True:
        schedule.run_pending()

if __name__ == '__main__':
    main()