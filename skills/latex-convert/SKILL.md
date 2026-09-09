---
name: latex-convert
description: Convert markdown files to proper LaTeX math formatting: inline and display math, symbols, and consistent notation. Use when the user asks to fix or convert math in markdown notes.
---

# /latex-convert

Convert markdown files to use proper LaTeX math formatting.

## Description

This command converts all `.md` files in a directory from informal math notation (backticks, Unicode symbols) to proper LaTeX formatting suitable for Obsidian or other LaTeX-rendering markdown editors.

## Usage

```
/latex-convert [path]
```

If no path is provided, ask the user whether to:
- Process current directory only (`*.md`)
- Process recursively (all subdirectories)

## Conversions

Apply these transformations to each file:

1. **Inline code math to LaTeX**: Convert backtick math expressions to `$...$`
   - `` `a ∧ b` `` → `$a \wedge b$`
   - `` `R^3` `` → `$\mathbb{R}^3$`
   - `` `x + y` `` → `$x + y$`

2. **Code block math to display LaTeX**: Convert math in code blocks to `$$...$$`

3. **Fix wrong LaTeX delimiters** (critical for Obsidian compatibility):
   - `\(...\)` → `$...$` (inline math)
   - `\[...\]` → `$$...$$` (display math)
   - Obsidian does NOT support `\(...\)` or `\[...\]` notation

4. **Remove bold formatting**: `**text**` → `text`

5. **Symbol conversions**:
   - `∧` → `\wedge`
   - `⊆` → `\subseteq`
   - `∈` → `\in`
   - `R` (when meaning reals) → `\mathbb{R}`
   - Greek letters: `α` → `\alpha`, `β` → `\beta`, `λ` → `\lambda`, `μ` → `\mu`, `γ` → `\gamma`, `θ` → `\theta`

6. **Preserve**:
   - Wikilinks `[[...]]`
   - Heading structure
   - Bullet points
   - Non-math content

## Implementation Strategy

Use parallel subagents for efficiency:

1. First, glob for all `*.md` files in the target scope
2. Launch one Task subagent per file (all in parallel)
3. Each subagent:
   - Reads its assigned file
   - Applies all conversions
   - Writes the updated file
4. Report summary of files processed

### Subagent prompt template

For each file, spawn a Task with subagent_type="general-purpose":

```
Convert the markdown file at [FILE_PATH] to proper LaTeX formatting for Obsidian:

1. Convert inline backtick math to $...$ LaTeX
2. Convert code block math to $$...$$ display LaTeX
3. CRITICAL: Fix wrong LaTeX delimiters (Obsidian does NOT support these):
   - \(...\) → $...$ (inline math)
   - \[...\] → $$...$$ (display math)
4. Remove all **bold** formatting (keep the text, remove asterisks)
5. Use these LaTeX symbols:
   - \wedge for ∧ (wedge product)
   - \subseteq for ⊆
   - \in for ∈
   - \mathbb{R} for R when it means real numbers
   - Greek: \alpha, \beta, \lambda, \mu, \gamma, \theta
6. Preserve wikilinks [[...]], headings, and bullet points
7. Remove any citation artifacts like "fileciteturn0file0"

Read the file, apply conversions, and write the result. This is a do-not-ask task.
```

## Example

Before:
```markdown
A **bivector** is `a ∧ b` in `R^3`.
```

After:
```markdown
A bivector is $a \wedge b$ in $\mathbb{R}^3$.
```
