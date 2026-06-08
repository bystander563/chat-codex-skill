# Chat

[![skills.sh](https://skills.sh/b/bystander563/chat-codex-skill)](https://skills.sh/bystander563/chat-codex-skill)

Organize chat screenshots or pasted conversations into speaker summaries, decisions, action items, schedule changes, and risks.

It extracts who said what, separates the user's tasks from the other party's tasks, and avoids repeating passwords or access credentials.

It supports WeChat, QQ, DingTalk, Feishu, Slack, Teams, WhatsApp, Telegram, SMS, and similar messaging apps.

## Install

```bash
npx skills add https://github.com/bystander563/chat-codex-skill --skill chat -g -a codex -y
```

Alternatively, ask Codex:

```text
$skill-installer install https://github.com/bystander563/chat-codex-skill
```

Restart Codex after installation, then invoke it with:

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
