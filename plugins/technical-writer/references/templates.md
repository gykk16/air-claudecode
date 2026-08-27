# Templates

Copy-ready skeletons per document type, and a process for multi-page structure.
Templates are in Korean — the default output language for documents.

## 1. Learning (튜토리얼)

```markdown
# [튜토리얼 제목]

## 목표

[이 튜토리얼을 따라하고 나면 독자가 달성할 목표를 간략히 설명하세요.]

## 사전 요구사항

- [필요한 사전 지식, 설치해야 할 도구를 정리하세요. 없다면 생략해도 돼요.]
- [예: Node.js 버전, API 키, 필수 패키지 등]

## 단계별 가이드

### [첫 번째 단계 제목]

[이 단계에서 해야 할 작업을 설명하고 코드 예제 또는 UI 캡처를 포함하세요.]

### [두 번째 단계 제목]

[다음 단계에서 수행할 작업을 설명하세요.]

### 최종 결과 확인

[독자가 목표를 달성했을 때, 어떤 결과가 나오는지 설명하세요.]
```

## 2. Problem-solving (How-to / 트러블슈팅)

```markdown
# [문제 해결 문서 제목]

## 문제 정의

[독자가 겪을 수 있는 문제 상황을 설명하세요.]

## 사전 요구사항

[문제를 해결하기 전에 필요한 환경 설정이나 필수 조건을 정리하세요. 없다면 생략해도 돼요.]

## 해결 방법

### [첫 번째 해결 방법]

[첫 번째 해결 방법을 설명하세요.]

### [두 번째 해결 방법]

[다른 해결 방법이 있다면 추가하세요.]

### 문제 해결 후 확인 방법

[문제가 해결된 후의 모습이나 확인하는 방법을 설명하세요.]
```

## 3. Reference (참조 문서)

```markdown
# [참조 문서 제목]

## 개요

[이 요소가 무엇이며, 언제 사용하는지, 어떤 가치를 제공하는지 설명하세요.]

## 속성 및 옵션

| 속성명 | 타입 | 기본값 | 설명 |
|--------|------|--------|------|
| prop1 | string | "default" | 이 속성은 ... |

## 시그니처

[// 예제 코드]

## 반환 값

[이 함수나 API가 반환하는 값을 설명하세요.]

## 사용 예제

[어떤 상황에서 사용하는지 구체적인 예시와 함께 예제 코드를 알려주세요.]
```

## 4. Explanation (설명 문서)

```markdown
# [개념명]

## 개념 소개

[이 개념이 무엇인지 간략히 설명하세요.]

## 등장 배경

[이 개념이 왜 등장했는지, 어떤 문제를 해결하는지 정리하세요.]

## 활용

[실제 프로젝트에서 이 개념이 어떻게 사용되는지 설명하세요.]
```

## Multi-page structure

Design multi-page docs in three steps:

1. **Decide which types are needed** — split the subject into learning,
   problem-solving, explanation, and reference documents from the reader's
   point of view.
2. **Design the structure** — think of it as designing the left navigation menu.
3. **Add cross-links** — link related documents (e.g. a tutorial links to the
   guide or reference that covers a topic in depth) so readers can go deeper
   when they need to.

Default template:

```
docs/
├── get-started.md
├── tutorials/          # 학습 중심 문서
├── how-tos/            # 문제 해결 중심 문서
├── explanations/       # 개념 설명 문서
├── reference/          # 참조 문서
├── troubleshooting.md  # 에러 해결 가이드
└── glossary.md         # 용어 사전
```

Notes:
- Learning docs start from the overall flow and can layer practice and advanced
  problem-solving beneath.
- Problem-solving and explanation docs can sit flat at the same level.
- Reference docs can live in their own listing page.
- Don't be bound by the template — combine types when it serves the reader.
