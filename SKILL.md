---
name: chat
description: Organize messaging conversation records from WeChat, QQ, DingTalk, Feishu, Slack, Teams, WhatsApp, Telegram, SMS, or similar apps. Use when the user provides chat screenshots/images or directly pasted chat text and asks to 整理聊天记录, identify who said what, extract my action items, summarize decisions, reconstruct schedules, track requirement changes, find open questions, or produce a follow-up checklist.
---

# Organize Chat Records

Turn screenshots or pasted chat text into an evidence-grounded Chinese brief. Optimize for the user's real question: what each side communicated, what was decided, and what the user needs to do next.

## Workflow

1. Ingest every screenshot or pasted block.
2. Reconstruct a canonical message sequence with source and speaker confidence.
3. Remove or mask secrets before repeating or saving content.
4. Group messages by topic and resolve later corrections.
5. Extract decisions, tasks, deadlines, dependencies, and open questions.
6. Return the concise brief in chat. Create a Markdown file only when the user requests a file or the record is too long for a useful inline answer.

## Read The Input

### Screenshots

- Process screenshots in visible chronological order. Use timestamps first and filenames only as a fallback.
- Detect overlap between consecutive scrolling screenshots and include each message once.
- Treat the right side as `我` and the left side as `对方` only when the app layout supports that interpretation. Verify avatars, bubble colors, names, or UI conventions before assigning.
- Preserve visible sender names and group-chat reply context.
- Represent voice messages, files, images, deleted messages, and unreadable text as explicit placeholders.
- Mark uncertain OCR as `[识别不清]`; never silently complete obscured text.

### Pasted Text

- Trust explicit `姓名: 内容`, timestamps, export metadata, or reply markers.
- If speaker labels are absent, infer identity from vocatives, self-reference, commitments, question-answer adjacency, and topic continuity.
- Never assign speakers by strict line alternation. One person may send several consecutive messages.
- If the user's identity can be inferred, state the assumption, for example `身份判断：你是聊天中的师弟（高置信）`.
- If identity remains uncertain, use `说话人 A`, `说话人 B`, or `未知` and keep tasks conditional. Ask one clarification only when identifying `我` changes the requested action list materially.

Maintain an internal record for each message:

```text
order | source | visible time | speaker | text | speaker confidence
```

## Protect Sensitive Information

- Never repeat passwords, access tokens, API keys, cookies, private keys, recovery codes, or complete credential bundles.
- Mask server hosts, usernames, and paths when they appear together with a usable secret unless the user explicitly needs a secure local inventory.
- Describe masked content by purpose, such as `提供了服务器登录信息（已遮盖）`.
- Do not preserve raw sensitive chat in a new file unless the user explicitly requests it. Prefer a redacted derivative.
- For local text files, use `scripts/redact_chat.py` before analysis or delivery when secrets may be present.
- Keep security, confidentiality, workplace policy, and access-control concerns in `风险与注意事项`. Do not turn advice to bypass rules, monitoring, or authorization into an action item.

```powershell
python scripts/redact_chat.py chat.txt --output chat.redacted.txt
```

Use `--level personal` when phone numbers, email addresses, and IP addresses must also be hidden.

## Extract Without Inventing

### Who Said What

- Summarize meaningful statements by topic and speaker.
- Omit routine acknowledgments such as `ok`, `好的`, and `收到` unless they confirm acceptance of a decision or task.
- Preserve disagreements, corrections, and requirement changes.
- Quote only short phrases when exact wording matters.

### Decisions And Schedule

- Distinguish `已确认`, `暂定`, `提议`, `被否决`, and `已变更`.
- When messages conflict, prefer the latest clearly accepted statement and show the earlier state as a change.
- Do not convert `下周一`, `明早`, or `周五` to a calendar date unless the chat date is visible or supplied. Preserve the relative date and mark the anchor as missing.

### Tasks

Classify each task:

- `明确`: directly assigned, requested, or accepted.
- `推断`: necessary to carry out an accepted decision, but not explicitly assigned.
- `建议`: a recommendation from the organizer; keep it outside the committed task list.

For each task capture:

```text
task | owner | due/time | status | dependency | evidence | confidence
```

- Put only tasks owned by the user in `我的待办`.
- Put tasks owned by others in `对方待办`.
- Keep unresolved ownership in `待确认事项`.
- Do not mistake a question, capability statement, or brainstorming option for a commitment.
- Split compound work into executable steps when dependencies or deadlines differ.

## Output

Follow `references/output-template.md`. Adapt sections to the evidence and omit empty sections.

Lead with:

1. `身份判断与范围`
2. `一句话结论`
3. `我的待办`

Then include:

- `彼此说了什么`
- `已确认决定与时间安排`
- `对方待办`
- `待确认事项`
- `需求/决定变更`
- `风险与注意事项`
- `关键原话证据`

Make uncertainty operational. Prefer `未看到最终确认`, `说话人归属中置信`, or `相对日期缺少聊天日期锚点` over vague caveats.

## Quality Check

Before returning:

- confirm every high-priority task has evidence;
- confirm `我的待办` is not contaminated by the other person's work;
- confirm later corrections override earlier proposals;
- confirm no secret is reproduced;
- confirm screenshot overlaps are deduplicated;
- confirm inferred speakers and dates are labeled;
- confirm policy-bypassing language is flagged rather than operationalized.
