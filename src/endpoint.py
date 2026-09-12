import requests

def get_paginated_works_by_subject(
    base_url: str, offset: int=0, limit: int=20) -> list:
    """Performs paginated calls to the works-by-subject endpoint.

    Args:
        base_url (str): Base URL for API requests
        offset (int, optional): Page offset for pagination. Defaults to 0.
        limit (int, optional): Number of elements per page. Defaults to 20.

    Returns:
        list: Request responses stored as a list
    """
    
    works_data = []

    # Create a dummy response_json to enter the while loop
    response_json = {"works": [1]}
    try:
        while len(response_json.get("works", [])) > 0:

            if "?" in base_url:
                request_url = f"{base_url}&offset={offset}&limit={limit}"
            else:
                request_url = f"{base_url}?offset={offset}&limit={limit}"

            response = requests.get(url=request_url)
            response_json = response.json()

            works_data.extend(response_json.get("works", []))
            
            offset += limit

        return works_data

    except Exception as err:
        print(f"Error occurred during request: {err}")
        return []
        
        
def get_authors(
    base_url: str,
    author_key: str,
    offset: int=0,
    limit: int=20
) -> dict:
    """Performs paginated requests to the author endpoint

    Args:
        base_url (str): Base URL for endpoint requests
        author_key (str): Key of the author to be queried.
        offset (int, optional): Page offset for pagination. Defaults to 0.
        limit (int, optional): Number of elements per page. Defaults to 20.

    Returns:
        dict: Author details and works
    """
    ### Exercise 3:
    ### START CODE HERE ### (~ 6 lines of code)

    # Build the URL for the author's details.
    # Note: author_key already starts with "/authors/", so concatenate directly with
    # base_url. Do NOT add an extra "/" between them.
    author_details_url = f"{base_url}{author_key}.json"

    # Build the base URL for the author's works (offset/limit get appended in the loop).
    author_works_url = f"{base_url}{author_key}/works.json"

    try:
        # Perform a GET request to author_details_url.
        details_response = requests.get(url=author_details_url)

        # Convert the response to JSON using the json() method.
        details_response_json = details_response.json()

        # Collect the author's works across pages.
        works_data = []

        # Create a dummy works_response_json to enter the while loop
        works_response_json = {"entries": [1]}

        while len(works_response_json.get("entries", [])) > 0:

            works_url = f"{author_works_url}?offset={offset}&limit={limit}"

            # Perform a GET request to works_url.
            works_response = requests.get(url=works_url)

            # Convert the response to JSON using the json() method.
            works_response_json = works_response.json()

            # Extend the works_data list with the value from "entries" in works_response_json.
            works_data.extend(works_response_json.get("entries", []))

            # Update the offset value
            offset = offset + limit
        ### END CODE HERE ###
        return {
            "details": details_response_json,
            "works": works_data,
        }
    

    except Exception as err:
        print(f"Error occurred during request: {err}")
        return {
            "details": {},
            "works": [],
        }
