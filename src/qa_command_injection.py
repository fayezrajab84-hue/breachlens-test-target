# BreachLens QA — verify multi-line suggestion anchor (v42 clean run).
# Deliberate eval injection on line 11. Do not merge.
import os


def ping_host(user_host):
    os.system("ping -c 1 " + user_host)


def run_expr(user_expr):
    return eval(user_expr)  # code injection
