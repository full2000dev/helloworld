import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup

def extract_news_headlines(html_content: str | None) -> list[str]:
    """
    Parses HTML content from Google News and extracts news headlines.

    Args:
        html_content: The HTML content as a string.

    Returns:
        A list of headline strings, or an empty list if no headlines
        are found or if the input is invalid.
    """
    if not html_content:
        print("HTML content is empty or None. Cannot extract headlines.")
        return []

    headlines = []
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Google News headlines are often within <h3> tags.
        # These <h3> tags might be inside <article> tags, and often contain <a> tags.
        # Strategy: Find all <h3> tags and extract their text.
        h3_tags = soup.find_all('h3')
        
        if h3_tags:
            for tag in h3_tags:
                text = tag.get_text(strip=True)
                if text:  # Ensure text is not empty
                    headlines.append(text)
        else:
            print("No <h3> tags found. Trying to find <a> tags with specific classes (e.g., 'DY5T1d', 'JtKRv', 'IP7VFc') as a fallback.")
            # Fallback: Try common (but potentially changing) class names for headline links
            # Note: These class names (DY5T1d, JtKRv, IP7VFc) are examples and might need updates
            # if Google changes its site structure.
            potential_classes = ['DY5T1d', 'JtKRv', 'IP7VFc', 'VDXfz'] # Added VDXfz from previous thoughts
            found_by_class = False
            for cls in potential_classes:
                headline_links = soup.find_all('a', class_=cls)
                if headline_links:
                    found_by_class = True
                    print(f"Found {len(headline_links)} links with class '{cls}'")
                    for link in headline_links:
                        text = link.get_text(strip=True)
                        if text:
                            headlines.append(text)
                    break # Found headlines with one class, no need to check others
            if not found_by_class:
                 print("No headlines found using common class name patterns for <a> tags.")
                 # As a further fallback, one could look for all <a> tags within <article> tags.
                 articles = soup.find_all('article')
                 if articles:
                     print(f"Found {len(articles)} <article> tags. Looking for <a> tags within them.")
                     for article in articles:
                         # Look for a prominent link within the article
                         # This could be the first <a> tag with non-empty text, or one inside a heading
                         article_link = article.find('a') 
                         if article_link:
                             text = article_link.get_text(strip=True)
                             if text:
                                 headlines.append(text)
                 else:
                     print("No <article> tags found either.")


        if not headlines:
            print("WARNING: No headlines extracted after attempting all strategies. The HTML structure might have changed, the page might not contain news headlines in the expected format, or the content was empty.")

    except Exception as e:
        print(f"ERROR: An exception occurred during HTML parsing or headline extraction: {e}")
        return []
        
    return list(set(headlines)) # Return unique headlines

def get_google_news(search_query: str) -> list[str]:
    """
    Fetches and extracts news headlines from Google News for a given search query.

    Args:
        search_query: The search term to look for on Google News.

    Returns:
        A list of headline strings, or an empty list if an error occurs
        or no headlines are found.
    """
    print(f"\nAttempting to get news for query: '{search_query}'")
    html_content = fetch_google_news_html(search_query)
    
    # If html_content is None (due to fetching error), 
    # extract_news_headlines will receive None and correctly return an empty list.
    headlines = extract_news_headlines(html_content)
    return headlines

def fetch_google_news_html(search_query: str) -> str | None:
    """
    Fetches the HTML content of a Google News search results page.

    Args:
        search_query: The search term to look for on Google News.

    Returns:
        The HTML content of the search results page as a string,
        or None if an error occurs.
    """
    base_url = "https://news.google.com/search"
    params = {"q": search_query}
    encoded_params = urlencode(params)
    full_url = f"{base_url}?{encoded_params}"

    print(f"Fetching URL: {full_url}")  # For debugging

    try:
        response = requests.get(full_url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - URL: {full_url}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err} - URL: {full_url}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err} - URL: {full_url}")
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected error occurred during the request: {req_err} - URL: {full_url}")
    
    return None

if __name__ == '__main__':
    # Example usage of the new get_google_news function:
    
    queries_to_test = [
        "Python programming",
        "你好世界", # Unicode query
        "artificial intelligence advancements 2024 latest news",
        "" # Empty query (to see how it's handled)
    ]

    for query in queries_to_test:
        headlines = get_google_news(query)
        if headlines:
            print(f"Found {len(headlines)} headlines for '{query}':")
            for i, headline in enumerate(headlines):
                print(f"{i+1}. {headline}")
        else:
            if query == "": # Specific message for empty query if needed
                 print(f"No headlines found for the empty query (or it was handled by Google News, e.g. redirect).")
            else:
                 print(f"No headlines found for '{query}', or an error occurred during fetching/parsing.")
        print("-" * 30) # Separator

    # Test with HTML content being None directly for extract_news_headlines (low-level test)
    print("\n--- Testing direct headline extraction with None HTML content ---")
    headlines_none = extract_news_headlines(None)
    if not headlines_none:
        print("Correctly returned empty list for None HTML content.")
    else:
        print(f"Unexpectedly returned {len(headlines_none)} headlines for None HTML content.")
