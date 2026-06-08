# Chat

A Codex skill for organizing chat screenshots or pasted conversations into:

- who said what;
- confirmed decisions and schedule changes;
- the user's action items and the other party's action items;
- unresolved questions, dependencies, and risks;
- redacted summaries that do not repeat passwords or access credentials.

It supports WeChat, QQ, DingTalk, Feishu, Slack, Teams, WhatsApp, Telegram, SMS, and similar messaging apps.

## Install

```text
Install the chat skill from https://github.com/bystander563/chat-codex-skill
```

After installation, invoke it with:

```text
Use $chat to organize these chat screenshots or pasted messages.
```

Chinese example:

```text
用 $chat 整理这些聊天，告诉我彼此说了什么、我需要做什么。
```

## Input

- one or more chat screenshots;
- directly pasted chat text;
- unlabeled conversational text where speaker identity must be inferred.

## Output

The skill prioritizes:

1. identity and uncertainty;
2. a concise conclusion;
3. the user's action items;
4. topic-based statements from each party;
5. decisions, changes, open questions, and risks.

## Privacy

The bundled `scripts/redact_chat.py` utility masks common credentials. Use `--level personal` to also mask phone numbers, email addresses, and IP addresses.

```powershell
python scripts/redact_chat.py chat.txt --output chat.redacted.txt --level personal
```

## Validation

```powershell
python -X utf8 path\to\quick_validate.py .
python -m unittest discover -s scripts -p "test_*.py" -v
```
