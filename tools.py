import os

from crewai.tools import tool
from firecrawl import FirecrawlApp, ScrapeOptions

# @tool
def web_search_tool(query):
    app=FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

    response = app.search(
        query=query,
        limit=5, #temp
        scrape_options=ScrapeOptions(formats=["markdown"])
    )

    print(response)

print(web_search_tool("Data Scientist Jobs in Paris."))