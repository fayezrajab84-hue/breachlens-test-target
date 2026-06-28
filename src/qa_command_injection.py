# QA verify multi-line suggestion fix v42 (run 2).
import os


def ping_host(user_host):
    os.system("ping -c 1 " + user_host)


def run_expr(user_expr):
    return eval(user_expr)  # verifying suggestion anchor run 2
