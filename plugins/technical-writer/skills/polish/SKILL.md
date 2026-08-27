---
name: polish
description: Polish Korean technical sentences — clear subjects, concise and concrete wording, natural Korean, consistent terms. Use when the user asks to refine, tighten, or naturalize sentences or paragraphs in documentation.
argument-hint: "[text, or file path]"
---

# Polish

Sentence-level polishing, applied inline (no delegation) so it works directly
on text the user pasted into the conversation.

## Instructions

1. Read `${CLAUDE_PLUGIN_ROOT}/references/sentence.md` and apply its five
   principles and the quick substitution list to the target text: $ARGUMENTS
2. Touch sentences only — do not restructure the document or change its type.
3. Keep the document's existing speech level (해요체 or 합쇼체) consistent.
4. Never alter technical meaning; if a sentence is ambiguous, ask instead of guessing.

## Output

Show the polished text, followed by a short list of the changes and which
principle each one applies. If the target is a file, apply the edits to the
file and summarize the changes.
