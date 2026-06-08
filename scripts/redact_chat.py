#!/usr/bin/env python3
"""Redact common secrets and optional personal data from chat text."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SECRET_LABEL = re.compile(
    r"(?im)^(\s*(?:password|passwd|pwd|passcode|secret|token|"
    r"api[\s_-]?key|access[\s_-]?key|client[\s_-]?secret|"
    r"密码|口令|密钥|令牌)(?:\s*[:：=]\s*|\s+))(.+?)\s*$"
)
PRIVATE_KEY = re.compile(
    r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----.*?"
    r"-----END [A-Z0-9 ]*PRIVATE KEY-----",
    re.DOTALL,
)
URL_CREDENTIAL = re.compile(
    r"(?P<scheme>[a-zA-Z][a-zA-Z0-9+.-]*://)"
    r"(?P<user>[^/\s:@]+):(?P<password>[^/\s@]+)@"
)
BEARER_TOKEN = re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{12,}")
EMAIL = re.compile(r"(?<![\w.+-])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}(?![\w.-])")
PHONE = re.compile(r"(?<!\d)(?:\+?86[- ]?)?1[3-9]\d{9}(?!\d)")
IPV4 = re.compile(
    r"(?<!\d)(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}"
    r"(?:25[0-5]|2[0-4]\d|1?\d?\d)(?!\d)"
)
SERVER_LABEL = re.compile(
    r"(?i)^\s*(?:服务器地址|服务器|主机地址|server(?:\s+address)?|host)\s*[:：]?\s*$"
)
USERNAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_.-]{0,63}$")
LIKELY_SECRET = re.compile(r"^(?=\S{6,128}$)(?=.*[A-Za-z])(?=.*\d).*$")


def redact_server_blocks(text: str) -> str:
    lines = text.splitlines(keepends=True)
    for index, line in enumerate(lines):
        if not SERVER_LABEL.match(line.rstrip("\r\n")):
            continue

        candidates: list[int] = []
        cursor = index + 1
        while cursor < len(lines) and len(candidates) < 3:
            value = lines[cursor].rstrip("\r\n")
            if value.strip():
                candidates.append(cursor)
            cursor += 1

        if len(candidates) < 3:
            continue

        host_index, user_index, secret_index = candidates
        host = lines[host_index].strip()
        user = lines[user_index].strip()
        secret = lines[secret_index].strip()
        if not IPV4.fullmatch(host):
            continue
        if not USERNAME.fullmatch(user):
            continue
        if not LIKELY_SECRET.fullmatch(secret):
            continue

        endings = [
            "\n" if lines[item].endswith("\n") else ""
            for item in (host_index, user_index, secret_index)
        ]
        lines[host_index] = "[REDACTED_HOST]" + endings[0]
        lines[user_index] = "[REDACTED_USERNAME]" + endings[1]
        lines[secret_index] = "[REDACTED_SECRET]" + endings[2]
    return "".join(lines)


def redact(text: str, level: str = "secrets") -> str:
    text = PRIVATE_KEY.sub("[REDACTED_PRIVATE_KEY]", text)
    text = URL_CREDENTIAL.sub(
        lambda match: f"{match.group('scheme')}{match.group('user')}:[REDACTED]@",
        text,
    )
    text = BEARER_TOKEN.sub("Bearer [REDACTED_TOKEN]", text)
    text = SECRET_LABEL.sub(lambda match: f"{match.group(1)}[REDACTED]", text)
    text = redact_server_blocks(text)

    if level in {"personal", "strict"}:
        text = EMAIL.sub("[REDACTED_EMAIL]", text)
        text = PHONE.sub("[REDACTED_PHONE]", text)
        text = IPV4.sub("[REDACTED_IP]", text)

    return text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Redact secrets and optional personal data from chat text."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="-",
        help="UTF-8 text file, or - to read stdin.",
    )
    parser.add_argument(
        "--output",
        help="Write redacted UTF-8 text to this file instead of stdout.",
    )
    parser.add_argument(
        "--level",
        choices=("secrets", "personal", "strict"),
        default="secrets",
        help="secrets masks credentials; personal also masks email, phone, and IP.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.input == "-":
        source = sys.stdin.read()
    else:
        source = Path(args.input).read_text(encoding="utf-8-sig")

    result = redact(source, args.level)
    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
    else:
        sys.stdout.write(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
