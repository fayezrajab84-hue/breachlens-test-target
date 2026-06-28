# BreachLens Commit-stage QA — DELIBERATE vuln (re-trigger for policy-gate test).
# Do not merge to main.
import os


def ping_host(user_host):
    os.system("ping -c 1 " + user_host)


def run_expr(user_expr):
    return eval(user_expr)  # still vulnerable — verifying the policy gate blocks it
