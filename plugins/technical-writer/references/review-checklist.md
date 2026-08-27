# Review Checklist

Diagnose in this order — type first, then structure, then sentences.
Read the ENTIRE document before judging anything.

## Step 1. Document type fit

- Is the type right for the reader's goal? (see `doc-types.md`)
- Does the document meet its type's checklist and must-include items?

## Step 2. Information architecture

1. **한 페이지에 하나만** — H4(`####`) 이상 깊이가 있는가? 여러 핵심 주제가 섞여 있는가?
2. **개요** — 제목 바로 아래에 개요가 있는가? "이 문서를 읽으면 무엇을 할 수 있는가"에 답하는가?
3. **예측 가능성** — 같은 수준 제목이 일관된 패턴인가? 기본 개념 → 상세 순서인가? 용어가 일관되는가? 설명이 코드보다 먼저 나오는가?
4. **가치 우선** — 도입부가 독자가 얻을 이점을 제시하는가? 세부 정보가 후순위인가?
5. **제목** — 핵심 키워드 포함, 30자 이내, 평서문, 동사형/명사형 통일인가?
6. **자세한 설명** — 새 개념이 정의 없이 등장하지 않는가? 값에 단위와 조건이 있는가?

## Step 3. Sentences

1. 문장이 불필요하게 길거나 한 문장에 여러 생각이 섞여 있지 않은가?
2. 메타 담화("앞서 설명했듯이", "아시다시피")가 없는가?
3. 모호한 표현 대신 구체적 동사·수치·기준을 쓰는가?
4. 같은 개념이 여러 표현으로 나타나지 않는가? 약어는 첫 등장에 풀어썼는가?
5. 수동형은 능동형으로, 도구가 아닌 독자가 주체인가?

## Reporting

- Order findings by severity, biggest impact first:
  - 🔴 Type/structure problems — wrong document type, missing overview, H4+ depth, value buried
  - 🟡 Principle violations — inconsistent headings/terms, unexplained concepts, illogical order
  - 🟢 Sentence-level polish
- Every finding must come with a concrete fix the author can paste in.
- Group repeated problems of the same kind ("그 외 N군데").
- Merge improvement options into one consolidated proposal, not a menu.

Report format:

```
## 🔴 {원칙 이름}
- 위치: <파일:줄 또는 인용>
- 문제: <무엇이 왜 문제인지 한 문장>
- 수정안: <그대로 붙여넣을 수 있는 대안>
```
