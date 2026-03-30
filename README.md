# /infostyle — Claude Code Skill

Edit Russian text using Maxim Ilyakhov's information style methodology.

Based on principles from "Пиши, сокращай" (Write and Cut), Glavred service (glvrd.ru), and 12+ years of Russian editorial practice.

## What it does

- Removes stop-words, clichés, bureaucratic language, and vague claims
- Replaces them with concrete facts, numbers, and useful information
- Adapts to context: UI buttons, forms, error messages, landing pages, emails, articles
- Scores text on 4 dimensions: clarity, specificity, persuasion, voice
- Shows before/after with explanations for each change
- Three editing modes: Light, Standard, Deep

## Install

### Claude Code (CLI / Desktop / Web)

```bash
# Option 1: Install from GitHub
claude skill install <your-username>/infostyle-skill

# Option 2: Copy manually
cp -r infostyle-skill/ ~/.claude/skills/infostyle/

# Option 3: Add to project
cp -r infostyle-skill/ .claude/skills/infostyle/
```

### Other agents (Cursor, Codex, Windsurf)

Copy `SKILL.md` to your agent's skill/prompt directory. The skill follows the open Agent Skills spec.

## Usage

```
/infostyle Презентация за 5 минут — загрузите тему и получите готовые слайды

/infostyle [paste your text]

/infostyle path/to/file.md
```

The skill will:
1. Ask about context (text type, audience, placement, goal) if not obvious
2. Score the original text
3. Edit using two-stage process: clean → fill with facts
4. Show before/after with scores and explanations
5. Offer alternatives for key elements

## Editing modes

| Mode | When to use | What changes |
|------|-------------|-------------|
| **Light** | Text is mostly good, minor cleanup | Fix obvious issues, keep author's voice |
| **Standard** | Default for most tasks | Remove stop-words, add specificity, fix structure |
| **Deep** | Text doesn't work, needs rewrite | Full restructuring, may look very different |

## What's inside

```
SKILL.md                          # Main skill — workflow, rules, when to invoke
references/
  stop-words.md                   # 15 categories of stop-words with transformation examples
  text-types.md                   # Rules by text type: UI, landing, email, article, support
  scoring.md                      # 4-dimension scoring criteria + self-check checklist
  manipulation-patterns.md        # 12 manipulation anti-patterns to always remove
  examples.md                     # Before/after examples for every text type
```

## Methodology

The skill implements Ilyakhov's two-stage editing process:

1. **Clean** (Вычистить) — Remove all stop-words, clichés, bureaucratic language, intensifiers, vague references, nominalizations, excessive pronouns, passive voice, modal verbs
2. **Fill** (Наполнить) — Replace deleted material with concrete facts, data, examples. Never leave gaps.

Key principle from Ilyakhov himself:

> "Не выключайте голову." (Don't turn off your brain.)
> Infostyle is navigation, not autocorrect. Every rule requires judgment in context.

## Context awareness

The skill adapts strictness based on text type:

- **UI buttons/labels** — Relaxed. Brevity over everything. 1-3 words max.
- **Forms and errors** — Medium. What happened + how to fix.
- **Landing pages** — Medium. Concrete benefits, emotional hooks allowed.
- **Email** — Medium-strict. One topic, clear CTA.
- **Articles** — Strict. Full infostyle.
- **Legal text** — Don't apply. Precision over brevity.

## Sources

- Ильяхов М., Сарычева Л. "Пиши, сокращай" (2016, updated 2025)
- Ильяхов М. "Ясно, понятно" (2020)
- Ильяхов М., Сарычева Л. "Новые правила деловой переписки" (2018)
- [Glavred service](https://glvrd.ru) and [reference](https://soviet.glvrd.ru)
- [Bureau.ru electronic textbook](https://bureau.ru/projects/book-text/)
- [22 principles of infostyle](https://habr.com/ru/post/323232/)
- [Editor's checklist](http://maximilyahov.ru/blog/all/the-checklist/)

## License

MIT
