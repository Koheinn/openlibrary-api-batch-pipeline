import datetime as dt
import json

from endpoint import get_paginated_works_by_subject, get_authors

# Open Library endpoints
URL_SUBJECT = "https://openlibrary.org/subjects/programming.json?published_in=2022-2026"
# BASE_URL is the root of the API. Author keys already start with "/authors/...",
# so it concatenates directly with the key (no extra slash).
BASE_URL = "https://openlibrary.org"


def main():
    kwargs = {
        "offset": 0,
        "limit": 50,
    }
    
    # Get works
    works = get_paginated_works_by_subject(
        base_url=URL_SUBJECT,
        **kwargs
    )

    print("Works have been extracted.")

    # Extract author keys for each work
    author_keys = []
    for work in works:
        work_id = work.get("key")  # e.g. "/works/OL123W"
        authors = work.get("authors", [])
        for author in authors:
            key = author.get("key")  # e.g. "/authors/OL123A"
            if key:
                author_keys.append(key)

        print(f"Total number of authors extracted for {work_id}: {len(authors)}")

    # Remove duplicate author keys
    author_keys = list(set(author_keys))
    print(f"Total number of unique authors: {len(author_keys)}")

    # Fetch author details and works
    print("Getting details for each author")
    author_items = {}   

    ### Exercise 4
    ### START CODE HERE ### (~ 6 lines of code)
    for author_key in author_keys:
        author_data = get_authors(
            base_url=BASE_URL,
            author_key=author_key,
            **kwargs
        )

        author_items[author_key] = author_data
        print(f"Author {author_key} processed successfully")
    ### END CODE HERE ###

    # Saving processed data to a JSON file.
    if len(author_items.keys()) > 0:
        current_time = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        filename = f"author_items_{current_time}"

        with open(f"./{filename}.json", "w+") as f:
            json.dump(author_items, f, indent=2)

        print(f"Data has been saved successfully to {filename}.json")
    else:
        print("No data was available to be saved.")


if __name__ == "__main__":
    main()