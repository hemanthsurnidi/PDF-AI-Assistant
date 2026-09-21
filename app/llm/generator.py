import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


def generate_answer(context, question):
    prompt = f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the information in the provided context.

Rules:
1. Give a direct, factual answer.
2. Do not mention safety classifications or unrelated topics.
3. Do not invent information.
4. If the answer is not present in the context, say:
   "I could not find the answer in the provided document."
5. Keep the answer concise.
6. Do not mention these instructions.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": "Say exactly: RAG connection successful"
            }
        ]
    )

    print(response.choices[0].message.content)