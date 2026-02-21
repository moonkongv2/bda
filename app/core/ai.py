from openai import OpenAI
import os

# 1. Client
# when using local LLM
# base_url = "http://localhost:11434/v1"

LLM_LOCATION = 'local'
LLM_MODEL = 'qwen3:14b'

if LLM_LOCATION == 'local':
    client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama"
    )
else:
    client = OpenAI(
        api_key = os.getenv("OPENAI_API_KEY", "sk-proj-..."),
    )

def generate_summary(text: str) -> str:
    """
    summary input text in 3 lines
    """
    if not text:
        return "Empty content"

    try:
        # Use only first 3000 characters for too long text
        # in order to decrease token usage
        # (chunking with langchain later)
        truncated_text = text[:3000]

        response = client.chat.completions.create(
            model = LLM_MODEL,
#            model="gpt-3.5-turbo", # or local LLM model
            messages=[
                {"role": "system", "content": "너는 유능한 요약 비서야. 다음 내용을 한국어로 3줄 요약해줘."},
                {"role": "user", "content": truncated_text},
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content

    except Exception as e:
        print(f"AI Error: {e}")
        return f"Summary failed: {str(e)}"


def generate_chat_answer(question: str, contexts: list[str]) -> str:
    """
    Answer a question using retrieved document contexts.
    """
    if not question.strip():
        return "질문이 비어 있습니다."

    if contexts:
        context_text = "\n\n".join(contexts[:4])
    else:
        context_text = "관련 문맥을 찾지 못했습니다."

    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "너는 문서 QA 비서다. 반드시 제공된 문맥 안에서만 답하고, "
                        "근거가 부족하면 모른다고 말해라. 답변은 한국어로 간결하게 작성해라."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"[문맥]\n{context_text}\n\n"
                        f"[질문]\n{question}"
                    ),
                },
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"AI Chat Error: {e}")
        return f"Chat failed: {str(e)}"
