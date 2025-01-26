from langchain_community.tools.tavily_search import TavilySearchResults


def get_profile_url(name: str):
    """searches for Linkedin or Twitter profile pages"""
    search = TavilySearchResults()

    res = search.run(f"{name}")

    return res
