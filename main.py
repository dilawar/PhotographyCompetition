"""
Main script file
"""

from judging import judge
from retrieval import intranet, analyze


def judge_cal():
    judge.calculate_score("final_Scores.xlsx")


def intra():
    intranet.do_all("Landscapes", "27 September 2017")


def check_defaulters():
    analyze.get_defaulters("Landscapes", "27 September 2017")


judge_cal()
