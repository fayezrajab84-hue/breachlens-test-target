# BreachLens Commit-stage QA — re-trigger to verify the multi-line suggestion fix (api:v42).
# Do not merge to main.
import os


def ping_host(user_host):
    os.system("ping -c 1 " + user_host)


def run_expr(user_expr):
    return eval(user_expr)  # still vulnerable — verifying suggestion anchors to the function range
