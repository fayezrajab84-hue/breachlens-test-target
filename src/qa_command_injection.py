# BreachLens Commit-stage QA — DELIBERATE vulnerabilities for PR-gate validation.
# Do not merge to main. Introduced to verify scan-on-PR + check run + auto-fix.
import os


def ping_host(user_host):
    # OS command injection (untrusted input concatenated into a shell command)
    os.system("ping -c 1 " + user_host)


def run_expr(user_expr):
    # Code injection via eval of untrusted input
    return eval(user_expr)
