# Information Architecture

Design the document from the reader's point of view — readers come to solve a
problem, learn, or look something up. Six principles, each with checks and a
representative Do/Don't.

## 1. 한 페이지에서는 하나만 다루기

One core goal per page. Too many concepts on one page make the core hard to find.

- Heading depth reaching `#### (H4)` is the signal to split the document.
- Use an overview page that links out when several concepts need introducing.
- Cover the most specific topic possible; two or more core topics → split.

```
Don't                              Do
# React 사용법                      # React 컴포넌트 생성하기
## 컴포넌트 생성
### 컴포넌트 기본 구조                ## 컴포넌트 기본 구조
#### JSX 사용법                     ## 상태 관리
##### JSX 문법 세부사항              ## 라이프사이클 메서드
## 상태 관리 ...
```

## 2. 가치를 먼저 제공하기

Lead with what the reader gains, not with features or background.

- Put supplementary detail and history later.
- Replace feature-first descriptions with reader-value descriptions.

> Don't: "리버스 프록시 설정은 2019년에 도입되었고, 많은 수정이 있었습니다..."
> Do: "리버스 프록시 설정을 적용하면 네트워크 지연 문제를 최소화할 수 있어요."

> Don't: "이 API는 여러 설정 옵션을 제공합니다."
> Do: "이 API를 사용하면 로그 데이터를 실시간으로 처리할 수 있습니다."

## 3. 효과적인 제목 쓰기

Titles must convey the core content at a glance and be easy to search.

- Include the key search keyword: `# NOT_FOUND_USER 에러를 해결하는 방법`, not `# 에러를 해결하는 방법은?`.
- Keep style consistent at the same level — unify on verb-form or noun-form
  (`키워드 포함하기 / 일관성 유지하기 / 평서문으로 작성하기`); number stepwise sections.
- 30 characters or fewer.
- Declarative sentences — no `!` or `?`.

## 4. 개요 빠트리지 않기

Every document opens with an overview, right below the title.

- The overview alone should convey the document's subject and purpose.
- Answer "이 문서를 읽으면 무엇을 할 수 있는가?" explicitly.
- Core information before technical background — no long abstract preambles.

> Don't: "React에서 상태 관리란 무엇일까요? React는 컴포넌트 기반 UI 라이브러리로..." (추상적, 장황)
> Do: "이 문서는 React에서 상태(state) 관리의 개념과 주요 기법을 설명합니다. `useState`, `useReducer`, Context API, Redux를 비교하고 장단점을 안내합니다."

## 5. 예측 가능하게 하기

Consistent structure lowers the reader's cognitive load.

- Keep heading hierarchy consistent; same-level concepts get same-level headings.
- Use the same section names and order across documents ("설치" vs "환경 설정" 혼용 금지).
- Order information logically: 핵심 개념 → 구체적인 사용법 → 예제 코드 → 심화 내용.
- Explanation first, then code — never make readers decode an unexplained snippet.
- Use terms consistently (하나의 문서에서 "상태/데이터/값" 혼용 금지); keep a glossary.

## 6. 자세히 설명하기

Write for the reader's knowledge level — they are reading this for the first time.

- Define every new concept in one or two sentences when it first appears,
  including why it matters and where it's used.

> Don't: "이 서비스는 이벤트 소싱 방식을 사용해 상태를 관리합니다."
> Do: "이 서비스는 이벤트 소싱(Event Sourcing) 방식을 사용해 상태를 관리합니다. 이벤트 소싱은 상태의 최종 결과만 저장하는 대신, 상태 변화를 일으킨 모든 이벤트를 기록하는 방식입니다."

- Fully specify how a feature behaves — conditions, states, and units.

> Don't: "`sessions[].duration`: 세션의 지속 시간을 나타냅니다."
> Do: "`sessions[].duration`: 사용자가 로그인을 유지한 시간입니다. 수동 로그아웃 시 실제 이용 시간, 시간 초과 시 마지막 활동 시점까지의 시간입니다. 단위는 밀리초(ms)입니다."
