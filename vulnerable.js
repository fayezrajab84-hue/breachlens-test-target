// PR-Check-Runs validation @ 2026-05-03T18:23:45.913Z
// Intentionally vulnerable file for BreachLens demo
// DO NOT MERGE — this exists to trigger security scanners.

const jwt = require('jsonwebtoken');
const exec = require('child_process').exec;
const crypto = require('crypto');

// ───────────────────────────────────────────────────────────────
// Hardcoded credentials (TruffleHog will catch these)
// ───────────────────────────────────────────────────────────────

const AWS_ACCESS_KEY_ID     = "AKIAIOSFODNN7EXAMPLE";
const AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY";
const GITHUB_PAT            = "ghp_1234567890abcdefghijklmnopqrstuvwxyzABCD";
const STRIPE_LIVE_KEY       = process.env.STRIPE_LIVE_KEY;
const JWT_SECRET            = "supersecret-do-not-commit-eyJhbGciOiJIUzI1NiJ9";
const PRIVATE_KEY = `-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAvJ4FAKEKEYDOTNOTREALSomeoneJustGeneratedThis
-----END RSA PRIVATE KEY-----`;

// ───────────────────────────────────────────────────────────────
// SQL injection (Semgrep SAST — string concat in query)
// ───────────────────────────────────────────────────────────────

function getUser(req, res) {
  const userId = req.query.id;
  const query = "SELECT * FROM users WHERE id = " + userId;
  return db.query(query);
}

// ───────────────────────────────────────────────────────────────
// Command injection (Semgrep SAST — exec with user input)
// ───────────────────────────────────────────────────────────────

function pingHost(req, res) {
  const host = req.query.host;
  exec("ping -c 4 " + host, (err, stdout) => res.send(stdout));
}

// ───────────────────────────────────────────────────────────────
// Insecure crypto (Semgrep SAST — MD5 for password hashing)
// ───────────────────────────────────────────────────────────────

function hashPassword(pw) {
  return crypto.createHash('md5').update(pw).digest('hex');
}

// ───────────────────────────────────────────────────────────────
// Insecure deserialization (Semgrep SAST — eval on user input)
// ───────────────────────────────────────────────────────────────

function processRequest(req, res) {
  const data = JSON.parse(req.body.payload);
  res.json(data);
}

module.exports = { getUser, pingHost, hashPassword, processRequest };
