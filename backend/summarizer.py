from newspaper import Article
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate


def summarize_articles_from_urls(urls, openai_api_key, topic):
    print(f"Summarizing {len(urls)} articles...")

    # Robustly extract full article text using newspaper3k
    article_dicts = []
    docs = []
    for i, url in enumerate(urls):
        try:
            article = Article(url)
            article.download()
            article.parse()
            text = article.text
            print(f"Article {i+1}: Extracted {len(text)} chars from {url}")
            article_dicts.append({'article_text': text, 'url': url})
            if text:
                docs.append(text)
        except Exception as e:
            print(f"Failed to extract {url}: {e}")

    # Prepare documents for LLM
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    split_docs = text_splitter.create_documents(docs)

    # Set up the LLM
    llm = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-4o-mini")

    # Summarize all documents using the default prompt
    custom_prompt = PromptTemplate(
        input_variables=["text", "topic"],
        template="""
        Give a summary of all documents provided. Give a proper tone as if you are giving a daily news digest on a given topic. 
        Don't make it too verbose, something easy to read for the users.
        The topic is: {topic}. 
        Below is the text:\n{text}"""
    )
    chain = load_summarize_chain(llm, chain_type="stuff", prompt=custom_prompt)
    summary = chain.run(input_documents=split_docs, topic=topic)
    return {
        'urls': urls,
        'summary': summary,
        'articles': article_dicts
    }

# Example usage:
# urls = ["https://example.com/article1", "https://example.com/article2", ...]
# summary = summarize_articles_from_urls(urls, openai_api_key="YOUR_OPENAI_API_KEY")
