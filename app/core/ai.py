from openai import OpenAI
import os

# 1. Client
# when using local LLM
# base_url = "http://localhost:11434/v1"

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
            model="gpt-3.5-turbo", # or local LLM model
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
