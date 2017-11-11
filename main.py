"""
Main script file
"""

from judging import judge
from retrieval import intranet, analyze

THEME = "Food across the world"

DEADLINE = "26 November 2017"


def judge_cal():
    judge.calculate_score("final_Scores.xlsx")


def intra():
    intranet.do_all(THEME, DEADLINE)


def check_defaulters():
    analyze.get_defaulters(THEME, DEADLINE)


intra()
