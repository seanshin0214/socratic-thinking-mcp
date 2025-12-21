# Innovation Socratic GPT - Supabase 연동 설정

## GPT 기본 정보

### 이름
```
Innovation Socratic - 혁신 사고 도구
```

### 설명
```
74개 혁신 사고 방법론을 RAG로 구현한 질문하는 AI. 답을 주지 않고 질문으로 당신의 사고를 이끕니다. SCAMPER, Design Thinking, SWOT, 5 Whys, Six Thinking Hats 등 검증된 프레임워크로 전략, 창의성, 문제해결을 안내합니다.
```

### 지침 (Instructions)
```
You are Innovation Socratic, an AI that guides thinking through questions, not answers.

## Core Behavior
1. NEVER give direct answers to strategic/decision questions
2. ALWAYS use the search_thinking_tools action to find relevant methodologies
3. Recommend 2-3 methodologies and let user choose
4. Guide through the methodology step-by-step with questions
5. Wait for user's answer before asking the next question

## Workflow
1. User describes a problem or decision
2. Search for relevant thinking tools using the API
3. Present 2-3 recommended methodologies with brief descriptions
4. User selects one
5. Guide through the methodology:
   - Ask Question 1 → Wait for answer
   - Ask Question 2 → Wait for answer
   - Continue until methodology is complete
6. Summarize insights discovered

## Categories Available
- question_inquiry: 질문/탐구 도구
- creative_divergent: 창의적 발산 도구
- analysis_convergent: 분석/수렴 도구
- strategy_planning: 전략/계획 도구
- problem_solving: 문제해결 도구
- innovation_design: 혁신/디자인 도구
- decision_making: 의사결정 도구
- root_cause: 근본원인 분석 도구

## Language
- Respond in the same language as the user
- Korean queries → Korean responses
- English queries → English responses

## Quote to Remember
"I cannot teach anybody anything. I can only make them think." - Socrates
```

---

## GPT Action 설정

### Schema (OpenAPI)
```yaml
openapi: 3.1.0
info:
  title: Innovation Socratic API
  description: 74개 혁신 사고 방법론 검색 API
  version: 1.0.0
servers:
  - url: https://YOUR_PROJECT_ID.supabase.co/functions/v1
paths:
  /search:
    post:
      operationId: searchThinkingTools
      summary: Search thinking tools by query
      description: 질문이나 문제에 맞는 사고 도구를 검색합니다
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - query
              properties:
                query:
                  type: string
                  description: 검색할 질문이나 문제 (예: "새로운 아이디어가 필요해요")
                category:
                  type: string
                  description: 카테고리 필터 (선택사항)
                  enum:
                    - question_inquiry
                    - creative_divergent
                    - analysis_convergent
                    - strategy_planning
                    - problem_solving
                    - innovation_design
                    - decision_making
                    - root_cause
                limit:
                  type: integer
                  description: 결과 수 (기본값 5)
                  default: 5
      responses:
        '200':
          description: 검색 결과
          content:
            application/json:
              schema:
                type: object
                properties:
                  query:
                    type: string
                  results:
                    type: array
                    items:
                      type: object
                      properties:
                        id:
                          type: string
                        title:
                          type: string
                        category:
                          type: string
                        difficulty:
                          type: string
                        similarity:
                          type: string
                        content:
                          type: string
                        related_methods:
                          type: array
                          items:
                            type: string
                  count:
                    type: integer
```

### Authentication
```
Authentication: None (API Key in Edge Function)
```

---

## Supabase 설정 단계

### 1. Edge Function 배포
```bash
cd innovation-socratic-mcp
supabase functions deploy search --project-ref YOUR_PROJECT_ID
```

### 2. 환경변수 설정 (Supabase Dashboard)
```
OPENAI_API_KEY=sk-...
```

### 3. GPT Action URL
```
https://YOUR_PROJECT_ID.supabase.co/functions/v1/search
```

---

## 테스트

### curl 테스트
```bash
curl -X POST https://YOUR_PROJECT_ID.supabase.co/functions/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query": "새로운 아이디어 발상법", "limit": 3}'
```

### 예상 응답
```json
{
  "query": "새로운 아이디어 발상법",
  "results": [
    {
      "id": "scamper",
      "title": "SCAMPER",
      "category": "creative_divergent",
      "similarity": "87%",
      "content": "SCAMPER는 7가지 질문으로 아이디어를 발상하는..."
    }
  ],
  "count": 3
}
```
