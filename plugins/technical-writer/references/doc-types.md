# Document Types

Technical documents are classified by the reader's goal. Pick the type first —
each type has an established structure that makes writing and reading easier.

## Type decision table

| Type | Reader's goal | Typical documents |
| --- | --- | --- |
| **Learning (학습)** | First contact with a technology; wants to understand the overall flow | Get-started, tutorial |
| **Problem-solving (문제 해결)** | Has background knowledge; wants to solve a specific problem or task | How-to guide, troubleshooting |
| **Reference (참조)** | Knows the basics; wants to look up exact usage of a feature/API | API reference, error codes |
| **Explanation (설명)** | Wants to deeply understand a concept, principle, or background | Concept docs, domain docs |

Quick decision guide:

- "동작 원리나 등장 배경을 알고 싶다" → **Explanation**
- "특정 기능을 구현하는 방법을 알고 싶다" → **Problem-solving (How-to)**
- "발생한 에러를 해결하고 싶다" → **Problem-solving (Troubleshooting)**
- "함수의 매개변수·반환값을 확인하고 싶다" → **Reference**
- "처음 접해서 흐름부터 익히고 싶다" → **Learning**

Types can be combined when it serves the reader (e.g. a learning doc that opens
with explanation elements). A how-to guide and a reference doc often pair well:
the reference explains the options, the guide shows how to apply them.

## Learning (학습 중심 문서)

Helps the reader learn a new technology or tool. Present a clear picture of
what the reader will be able to do.

- The reader must get from start to finish without getting stuck — verify every
  example actually runs, and list all prerequisites.
- Explain step by step; raise example difficulty gradually.
- Include runnable code examples, not concept-only text.
- **Get-started vs tutorial**: get-started introduces the main flow and concepts
  (install, setup, core ideas); a tutorial has a concrete goal and deliverable.
  If setup is trivial, fold it into the tutorial's opening.
- Keep the main body focused on the success path; move common problems to a FAQ
  section at the end, or into collapsible blocks.

Must include: learning goal and what the reader gains; prerequisites and setup;
step-by-step guidance (what and why per step); runnable examples from simple to
harder; FAQ or common problems at the end.

Checklist:
- [ ] 학습 목표를 명확하게 제시했나요?
- [ ] 직접 따라 해 봤을 때 오류가 생기지는 않나요?
- [ ] 단계별로 설명되어 있나요?
- [ ] 읽는 사람이 직접 실행할 수 있는 코드 예제가 포함되어 있나요?

## Problem-solving (문제 해결 문서)

Helps the reader solve the problem in front of them, fast. The only measure of
success: can the reader solve their problem with this document?

- Define the problem clearly — separate cause from symptom; include error
  messages and log samples.
- Provide immediately applicable solutions: code, commands, settings — and
  mention why the solution works.
- Cover environment differences (OS, library versions).
- **How-to guide vs troubleshooting**: a how-to focuses on implementing a
  specific feature or goal; troubleshooting focuses on diagnosing and fixing a
  problem that already happened. An error-code doc is a dictionary ("what does
  this error mean?"); troubleshooting is a resolution guide ("how do I fix it?").

Must include: clear problem or goal definition; background needed to understand
the cause; step-by-step solution; runnable code or commands; environment-specific
notes; why the solution works.

Checklist:
- [ ] 에러 원인만이 아니라 에러에 대한 기본 지식도 충분히 제공했나요?
- [ ] 즉시 적용할 수 있는 해결 방법이 포함되어 있나요?
- [ ] 환경별(운영체제, 라이브러리 버전 등) 차이를 고려했나요?

## Reference (참조 문서)

Lets the reader find accurate, complete information fast. Core values:
accuracy, completeness, searchability.

- Every piece of information must be accurate, complete, and current.
- Use one consistent structure (e.g. name → parameters → return value → example).
- Make navigation easy: sections by topic, table of contents, anchor links.
- Provide example code for every element.
- Put information the reader must know beforehand (API keys, auth, headers) at
  the front where it can't be missed.

Must include: concise overview and main features; syntax and parameters (type,
default, required); return values and types; examples from basic to advanced;
related APIs; caveats and limitations.

Checklist:
- [ ] 검색 및 탐색이 쉬운 구조인가요?
- [ ] 정보가 정확하고 완전한가요?
- [ ] 일관된 구조와 형식으로 작성되어 있나요?
- [ ] 실용적인 예시 코드가 포함되어 있나요?

## Explanation (설명 문서)

Helps the reader deeply understand a technology or concept — beyond usage, into
principles and philosophy.

- Explain the background first: why the technology appeared, what problem it solves.
- Use visuals (diagrams, flows, tables) for complex concepts, overall structure,
  and data flow.
- Compare with alternative approaches and state trade-offs.
- Works for concept docs (how Virtual DOM works) and domain docs (commerce,
  payments, finance).

Must include: background and the problem being solved; principles and detailed
behavior; comparison with other approaches; visual aids; real use cases.

Checklist:
- [ ] 핵심 원리와 배경이 명확하게 설명되었나요?
- [ ] 복잡한 개념을 시각화하여 설명했나요?
- [ ] 선행 지식이 충분히 안내되었나요?
