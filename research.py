from duckduckgo_search import DDGS

def search_web(query):
    results = []

    with DDGS() as ddgs:
        search_results = ddgs.text(
            query,
            max_results=5
        )

        for result in search_results:
            results.append({
                "title": result["title"],
                "link": result["href"],
                "body": result["body"]
            })

    return results