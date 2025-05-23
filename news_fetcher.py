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
        
        print("Attempting to find headlines using <a> tags with class 'JtKRv'.")
        headline_links_jtKrv = soup.find_all('a', class_='JtKRv')
        if headline_links_jtKrv:
            print(f"Found {len(headline_links_jtKrv)} links with class 'JtKRv'.")
            for link in headline_links_jtKrv:
                text = link.get_text(strip=True)
                if text:
                    headlines.append(text)
        
        if not headlines:
            print("No headlines found with class 'JtKRv'. Trying <h3> tags.")
            h3_tags = soup.find_all('h3')
            if h3_tags:
                print(f"Found {len(h3_tags)} <h3> tags.")
                for tag in h3_tags:
                    text = tag.get_text(strip=True)
                    if text:
                        headlines.append(text)
            else:
                print("No <h3> tags found.")

        if not headlines:
            print("No headlines found with <h3> tags. Trying <a> tags within <article> tags.")
            articles = soup.find_all('article')
            if articles:
                print(f"Found {len(articles)} <article> tags.")
                for article in articles:
                    article_link = article.find('a') 
                    if article_link:
                        text = article_link.get_text(strip=True)
                        if text:
                            headlines.append(text)
            else:
                print("No <article> tags found.")
        
        if not headlines:
            print("WARNING: No headlines extracted after attempting all strategies. The HTML structure might have changed, the page might not contain news headlines in the expected format, or the content was empty.")

    except Exception as e:
        print(f"ERROR: An exception occurred during HTML parsing or headline extraction: {e}")
        return []
        
    return list(set(headlines))

def fetch_google_news_html(search_query: str, language: str = "en", country: str = "US") -> str | None:
    """
    Fetches the HTML content of a Google News search results page.

    Args:
        search_query: The search term to look for on Google News.
        language: The language code (e.g., "en", "ko"). Defaults to "en".
        country: The country code (e.g., "US", "KR"). Defaults to "US".

    Returns:
        The HTML content of the search results page as a string,
        or None if an error occurs.
    """
    base_url = "https://news.google.com/search"
    params = {
        "q": search_query,
        "hl": language,
        "gl": country
    }
    encoded_params = urlencode(params)
    full_url = f"{base_url}?{encoded_params}"

    print(f"Fetching URL: {full_url}")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(full_url, headers=headers, timeout=10)
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

def get_google_news(search_query: str, language: str = "en", country: str = "US") -> list[str]:
    """
    Fetches and extracts news headlines from Google News for a given search query,
    with language and country customization.

    Args:
        search_query: The search term to look for on Google News.
        language: The language code (e.g., "en", "ko"). Defaults to "en".
        country: The country code (e.g., "US", "KR"). Defaults to "US".

    Returns:
        A list of headline strings, or an empty list if an error occurs
        or no headlines are found.
    """
    print(f"\nAttempting to get news for query: '{search_query}' (lang: {language}, country: {country})")
    html_content = fetch_google_news_html(search_query, language=language, country=country)
    
    headlines = extract_news_headlines(html_content)
    return headlines

if __name__ == '__main__':
    # --- Interactive Command-Line Interface ---
    print("Welcome to News Fetcher Agent!")
    print("You can enter a search query directly.")
    print("Type 'config' to change language/country settings.")
    print("Type 'quit' or 'exit' to stop the agent.")

    current_language = "en"
    current_country = "US"
    print(f"Default language is '{current_language}', default country is '{current_country}'.")

    while True:
        print("-" * 30)
        prompt_message = f"Enter search query (or 'config', 'quit', 'exit') [lang:{current_language}, country:{current_country}]: "
        user_input = input(prompt_message).strip()

        if not user_input: 
            continue

        if user_input.lower() in ['quit', 'exit']:
            print("Exiting News Fetcher Agent. Goodbye!")
            break
        
        elif user_input.lower() == 'config':
            print("\n--- Configure Language and Country ---")
            
            new_lang = input(f"Enter language code (e.g., en, ko) [current: {current_language}, press Enter to keep]: ").strip()
            if new_lang:
                current_language = new_lang.lower()
            
            new_country = input(f"Enter country code (e.g., US, KR) [current: {current_country}, press Enter to keep]: ").strip()
            if new_country:
                current_country = new_country.upper()
            
            print(f"Settings updated: Language set to '{current_language}', Country set to '{current_country}'.")
            continue

        else:
            search_query = user_input
            # The get_google_news function already prints "Attempting to get news for query..."
            # and fetch_google_news_html prints "Fetching URL..."
            # extract_news_headlines also prints its steps.
            headlines = get_google_news(search_query, language=current_language, country=current_country)

            if headlines:
                print(f"\n--- Headlines for '{search_query}' ({current_language}-{current_country}) ---")
                for i, headline in enumerate(headlines):
                    print(f"{i+1}. {headline}")
            else:
                print(f"\nNo headlines found for '{search_query}' with language '{current_language}' and country '{current_country}'.")
                print("This could be due to the query, language/country combination, or a change in Google News HTML structure.")
