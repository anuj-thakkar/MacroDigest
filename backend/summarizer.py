from openai import OpenAI
client = OpenAI()

def summarize_articles(articles):
    joined = "\n\n".join(articles)
    prompt = f"Summarize these news articles into a short daily digest:\n{joined}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

