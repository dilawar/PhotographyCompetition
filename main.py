"""
Main script file
"""

from judging import judge
from retrieval import intranet


def judge_cal():
    judge.calculate_score("final_Scores.xlsx")


def intra():
    intranet.do_all("Theme Name", "last date", True)


judge_cal()
