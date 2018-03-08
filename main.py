"""
Main script file
"""

from judging import judge
from retrieval import intranet, analyze
import logging

THEME = "Portraits"
DEADLINE = "25 January 2018"

def judge_cal():
    judge.calculate_score("final_Scores.xlsx")


def intra():
    intranet.do_all(THEME, DEADLINE)

def check_defaulters():
    analyze.get_defaulters(THEME, DEADLINE)

def main( args ):
    logging.basicConfig( level = args.loglevel 
            , format = '%(asctime)s %(name)-10s %(levelname)-5s %(message)s'
            )
    logging.debug( 'Calling intra' )
    intra()

if __name__ == '__main__':
    import argparse
    # Argument parser.
    description = '''Photography Club: It does everything!'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--output', '-o'
        , required = False
        , help = 'Output file'
        )
    parser.add_argument( '--debug', '-d'
        , required = False, action = 'store_const'
        , dest = 'loglevel', const = logging.DEBUG
        , default = logging.WARNING
        , help = 'Enable debug mode.'
        )
    parser.add_argument( '--verbose', '-v'
        , required = False, action = 'store_const'
        , dest = 'loglevel', const = logging.INFO
        , help = 'Be chatty. Like academic canteen and SLC.'
        )
    class Args: pass 
    args = Args()
    parser.parse_args(namespace=args)
    main( args )
    
