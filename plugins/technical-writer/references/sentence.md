# Sentence Polishing (Korean)

Five principles for sentences that are easy to read and easy to write.
Examples are in Korean — the language these rules are about.

## 1. 문장의 주체를 분명하게 하기

The reader (a developer) is the actor. Write around what the reader can do.

- Don't make tools, technology, or systems the subject of an action.

> Don't: "**이 라이브러리는** 데이터베이스 초기화를 수행해요."
> Do: "이 명령어를 실행하면 데이터베이스를 초기화할 수 있어요."

- Exception: when describing how a tool itself behaves, the tool may be the
  subject ("특정 접근성 요소가 화면에 나타나면 자동으로 수집돼요.").
- Prefer active voice — passive sentences hide the actor.

> Don't: "애플리케이션이 실행되기 전에 설정이 완료되어야 합니다."
> Do: "애플리케이션을 실행하기 전에 설정을 완료하세요."

## 2. 필요한 정보만 남기기

- Short sentences; one thought per sentence.

> Don't: "이 API를 호출할 때 요청 헤더를 포함해야 하며, 올바른 인증 정보를 제공해야 정상적으로 응답을 받을 수 있습니다."
> Do: "이 API를 호출할 때 요청 헤더와 인증 정보를 포함하세요."

- Minimize metadiscourse (말에 대한 말):
  - 흐름 설명: '다음으로', '앞서 설명했듯이', '이제 알아보겠습니다'
  - 불필요한 강조: '사실은', '솔직히 말하면', '결론적으로'
  - 독자 반응 유도: '아시겠지만', '여러분도 아실 것입니다'

## 3. 구체적으로 쓰기

- Verbs over derived nouns — drop '수행', '진행', '실시'.

> Don't: "코드 최적화 진행 후 배포 수행이 필요합니다."
> Do: "코드를 최적화한 후 배포하세요."

- Replace vague expressions ('가능성이 있다', '일부 경우', '필요할 수도 있다') with certain facts.

> Don't: "일부 브라우저에서 정상적으로 동작하지 않을 가능성이 있습니다."
> Do: "Internet Explorer에서는 정상적으로 동작하지 않습니다."

- Spell out who, what, where, how — no context-dependent sentences.

> Don't: "파일을 업로드하면 자동으로 저장됩니다."
> Do: "사용자가 파일을 업로드하면 서버에 자동으로 저장됩니다."

> Don't: "에러가 발생하면 로그를 확인하세요."
> Do: "에러가 발생하면 애플리케이션 서버에서 에러 로그 파일(`/var/log/app/error.log`)을 확인하세요."

- Describe actual behavior, not jargon ("Exception을 던집니다" → "예외(`Exception`)를 일으킵니다").
- Give concrete numbers and criteria.

> Don't: "데이터가 많을 때는 성능이 저하될 수 있습니다."
> Do: "데이터가 10,000건을 넘으면 응답 시간이 1초 이상 걸립니다."

- Explain the context of referenced values — where a variable was set, and where
  it will be used later, with links between the steps.

## 4. 자연스러운 한국어 표현 쓰기

- Remove unnecessary Sino-Korean verbs: '~하는 작업을 수행합니다' → '~합니다'.

> Don't: "로그 파일을 삭제하는 작업을 수행합니다."
> Do: "로그 파일을 삭제합니다."

- Fix translationese — English nominalization ('-tion', '-ing') reads unnaturally;
  rewrite around what the reader does.

> Don't: "API 키를 이용한 사용자 인증 처리가 완료된 후, 데이터베이스 접속 설정 진행이 가능합니다."
> Do: "API 키로 사용자를 인증한 후, 데이터베이스에 접속하도록 설정할 수 있습니다."

> Don't: "이 API를 통해 데이터를 가져올 수 있습니다."
> Do: "이 API로 데이터를 가져올 수 있습니다."

## 5. 일관되게 쓰기

- Follow official names for technologies, including casing: "K8" → "쿠버네티스(Kubernetes)".
- One expression per concept within a document ("추가/첨부/넣다" 혼용 → "업로드"로 통일).
- Expand abbreviations on first use, abbreviation attached without a space:
  "SSR" → "SSR(Server-Side Rendering)" 또는 "클라이언트 사이드 렌더링(Client-Side Rendering, CSR)".
- For loanword spelling, prefer the form the industry actually uses over strict
  orthography (예: '프런트엔드'보다 '프론트엔드') when it is clearly dominant.

## Quick substitution list

| Pattern | Fix |
| --- | --- |
| ~수행/진행/실시합니다 | 동사로 직접 표현 |
| ~될 필요가 있습니다, ~되어야 합니다 | ~하세요 (능동형) |
| ~할 수도 있습니다, 가능성이 있습니다 | 확정 조건과 결과 명시 |
| ~을 통해 | ~로/으로 |
| 많을 때, 빠르게, 일부 경우 | 구체적 수치·기준 |
| 이 라이브러리는/이 코드는 ~합니다 | 독자가 무엇을 할 수 있는지로 재구성 |
