# Skill Registry — elocuencia-sin-miedo-landing

Last updated: 2026-09-24

## Contract

This is an index, not a summary. `SKILL.md` is the source of truth. Delegators pass exact paths and workers read the full skill.

## Sources scanned

- `/home/julian/.claude/skills`
- `/home/julian/.codex/skills`

## Skills

| Skill | Trigger / description | Scope | Path |
| --- | --- | --- | --- |
| `chained-pr` | Trigger: PRs over 400 lines, stacked PRs, review slices. Split oversized changes into chained PRs that protect review focus. | user | `/home/julian/.claude/skills/chained-pr/SKILL.md` |
| `cognitive-doc-design` | Design docs that reduce cognitive load. Trigger: writing guides, READMEs, RFCs, onboarding, architecture, or review-facing docs. | user | `/home/julian/.claude/skills/cognitive-doc-design/SKILL.md` |
| `go-testing` | Trigger: Go tests, go test coverage, Bubbletea teatest, golden files. Apply focused Go testing patterns. | user | `/home/julian/.claude/skills/go-testing/SKILL.md` |
| `judgment-day` | Trigger: judgment day, dual review, adversarial review, juzgar. Run explicit blind dual review with at most two scoped fix/re-judgment rounds. | user | `/home/julian/.claude/skills/judgment-day/SKILL.md` |
| `skill-creator` | Trigger: new skills, agent instructions, documenting AI usage patterns. Create LLM-first skills with valid frontmatter. | user | `/home/julian/.claude/skills/skill-creator/SKILL.md` |
| `skill-improver` | Trigger: improve skills, audit skills, refactor skills, skill quality. Audit and upgrade existing LLM-first skills. | user | `/home/julian/.claude/skills/skill-improver/SKILL.md` |
| `work-unit-commits` | Plan commits as reviewable work units. Trigger: implementation, commit splitting, chained PRs, or keeping tests and docs with code. | user | `/home/julian/.claude/skills/work-unit-commits/SKILL.md` |

## Project conventions

- No convention files found in the repository.

## Loading protocol

1. Match task and file context against the trigger column.
2. Pass matching exact `SKILL.md` paths to the worker.
3. The worker reads those files before task-specific work.

Indexed skills: 7.
Skipped or duplicate entries: 31.
