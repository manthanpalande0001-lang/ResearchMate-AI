from research import search_web

topic = "Artificial Intelligence"

results = search_web(topic)

for result in results:
    print("\nTitle:", result["title"])
    print("Link:", result["link"])
    print("Description:", result["body"])