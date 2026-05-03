# Intentionally vulnerable Python file for BreachLens SAST + SECRET scanners.
# DO NOT RUN — every block exists to trigger a known check.

import hashlib
import os
import pickle
import requests
import shlex
import sqlite3
import subprocess
import yaml
from flask import Flask, request, render_template_string
from lxml import etree

app = Flask(__name__)

# ───────────────────────────────────────────────────────────────
# Hardcoded credentials (TruffleHog + Semgrep secret rules)
# ───────────────────────────────────────────────────────────────

# Snowflake connection string with embedded password
SNOWFLAKE_URL = "snowflake://admin:hunter2_PROD_secret@xy12345.us-east-1.snowflakecomputing.com/SALES"

# Datadog API + APP keys (32-hex / 40-hex format)
DATADOG_API_KEY = "8a3f5c2d9e1b7a4f6c8d2e9b5a3f7c1d"
DATADOG_APP_KEY = "3e8b7c2a9d6f1b5e4c8a3d7f2b9e1c6a4d8f3b7e"

# Discord bot token (3 dot-separated base64 segments)
DISCORD_BOT_TOKEN = "MTAwODg5OTk5OTk5OTk5OTk5OQ.GxXYzA.aBcDeFgHiJkLmNoPqRsTuVwXyZ"

# npm publish token (npm_<36 chars>)
NPM_TOKEN = "npm_8NkR2LpQ7XwM4FvYhT3BdGc6jZ9PaSeVuKnH"

# Hugging Face token (hf_<37 chars>)
HUGGINGFACE_TOKEN = "hf_xQwertyUiopAsdfGhjKlZxcvBnm123456789Abc"

# Hardcoded admin password (Bandit B105: hardcoded_password_string)
ADMIN_PASSWORD = "admin123_DO_NOT_COMMIT"

# ───────────────────────────────────────────────────────────────
# SSRF — unvalidated URL fetched from user input (Semgrep python.flask.security.audit.ssrf)
# ───────────────────────────────────────────────────────────────

@app.route("/proxy")
def proxy_url():
    target = request.args.get("url")
    # No allowlist, no scheme check — attacker can hit internal IPs (169.254.169.254 metadata, etc.)
    return requests.get(target).text

# ───────────────────────────────────────────────────────────────
# Path traversal — open() with user-controlled path (Bandit B108 / Semgrep python.lang.security.audit.path-traversal-open)
# ───────────────────────────────────────────────────────────────

@app.route("/file")
def read_file():
    name = request.args.get("name")
    # Attacker can pass ../../etc/passwd
    with open(f"/var/data/{name}", "r") as f:
        return f.read()

# ───────────────────────────────────────────────────────────────
# Insecure deserialization — pickle on user data (Bandit B301)
# ───────────────────────────────────────────────────────────────

@app.route("/restore", methods=["POST"])
def restore_session():
    blob = request.data
    # pickle.loads on untrusted data → arbitrary code execution
    return pickle.loads(blob)

# ───────────────────────────────────────────────────────────────
# Command injection — subprocess shell=True with user input (Bandit B602)
# ───────────────────────────────────────────────────────────────

@app.route("/ping")
def ping():
    host = request.args.get("host")
    # shell=True + string concat = RCE
    output = subprocess.check_output("ping -c 4 " + host, shell=True)
    return output

# ───────────────────────────────────────────────────────────────
# SQL injection — string formatting in query (Semgrep python.lang.security.audit.formatted-sql-query)
# ───────────────────────────────────────────────────────────────

@app.route("/user")
def get_user():
    user_id = request.args.get("id")
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    # f-string in raw SQL → SQLi
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    return str(cursor.fetchone())

# ───────────────────────────────────────────────────────────────
# Weak crypto — MD5 for password hashing (Bandit B303)
# ───────────────────────────────────────────────────────────────

def hash_password(pw: str) -> str:
    # MD5 is broken; should be bcrypt / argon2
    return hashlib.md5(pw.encode()).hexdigest()

# ───────────────────────────────────────────────────────────────
# XXE — lxml parser with external entity resolution enabled (Bandit B320)
# ───────────────────────────────────────────────────────────────

def parse_xml(xml_bytes: bytes):
    # resolve_entities=True (the default for plain XMLParser) enables XXE
    parser = etree.XMLParser(resolve_entities=True)
    return etree.fromstring(xml_bytes, parser)

# ───────────────────────────────────────────────────────────────
# Server-side template injection — render_template_string with user input (Semgrep python.flask.security.audit.render-template-string)
# ───────────────────────────────────────────────────────────────

@app.route("/greet")
def greet():
    name = request.args.get("name")
    # User input directly in template string → SSTI → RCE in Jinja2
    template = f"<h1>Hello {name}!</h1>"
    return render_template_string(template)

# ───────────────────────────────────────────────────────────────
# yaml.load — accepts arbitrary Python objects (Bandit B506)
# ───────────────────────────────────────────────────────────────

def load_config(yaml_text: str):
    # yaml.load with default Loader allows !!python/object → RCE
    # Should be yaml.safe_load
    return yaml.load(yaml_text)

if __name__ == "__main__":
    app.run(debug=True)  # Bandit B201 — debug=True in production
