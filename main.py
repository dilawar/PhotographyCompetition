"""
Main script file
"""

from judging import judge
from retrieval import intranet


def judge_cal():
    judge.calculate_score("final_Scores.xlsx")


def intra():
    intranet.do_all("Landscapes", "27 September 2017")


intra()
