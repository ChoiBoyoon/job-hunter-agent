import os, re

from crewai.tools import tool
from firecrawl import FirecrawlApp, ScrapeOptions

@tool
def web_search_tool(query):
    """
    Web Search Tool.
    Args:
        query: str
            The query to search the web for.
    Returns
        A list of search results with the website content in Markdown format.
    """
    app=FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

    response = app.search(
        query=query,
        limit=5, #temp
        scrape_options=ScrapeOptions(formats=["markdown"])
    )

    if not response.success:
        return "Error using tool."

    cleaned_chunks = []

    for result in response.data:
        title = result["title"]
        url = result["url"]
        markdown = result["markdown"]

        cleaned = re.sub(r"\\+|\n+", "", markdown).strip() #remove unnecessary whitespaces to save tokens
        cleaned = re.sub(r"\[[^\]]+\]\([^\)]+\)|https?://[^\s]+", "", cleaned) #remove urls
        cleaned_result = {
            'title':title,
            'url':url,
            'markdown':cleaned,
        }

        cleaned_chunks.append(cleaned_result)
    return cleaned_chunks

print(web_search_tool("Data Scientist Jobs in Paris."))