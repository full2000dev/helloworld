# Google News Fetcher

This Python script fetches news headlines from Google News based on a search query, running as an interactive command-line agent.

## Features

*   Interactive news search via a command-line interface.
*   Support for fetching news in multiple languages and from different countries/regions (e.g., English/US, Korean/KR).
*   Uses a common User-Agent header to improve fetch reliability.

## Requirements

- Python 3.x

## Setup and Installation

1.  Clone the repository or download the files (`news_fetcher.py`, `requirements.txt`).
2.  Navigate to the project directory in your terminal.
3.  Install the necessary dependencies by running:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The script runs as an interactive command-line agent.

1.  **Start the agent**:
    ```bash
    python news_fetcher.py
    ```

2.  **Interacting with the agent**:
    *   Upon starting, you will see a welcome message and a prompt. The default language is English (`en`) and country is United States (`US`).
    *   **Enter a search query**: Type your desired search term (e.g., `global economy`) and press Enter. The agent will fetch and display headlines for the current language/country settings.
    *   **Change language/country**: Type `config` and press Enter.
        *   You'll be prompted to enter a new language code (e.g., `ko` for Korean). Press Enter to keep the current setting.
        *   You'll then be prompted to enter a new country code (e.g., `KR` for South Korea). Press Enter to keep the current setting.
        *   A confirmation message will show the updated settings.
    *   **Exit the agent**: Type `quit` or `exit` and press Enter.

3.  **Example Interaction**:
    ```
    Welcome to News Fetcher Agent!
    You can enter a search query directly.
    Type 'config' to change language/country settings.
    Type 'quit' or 'exit' to stop the agent.
    Default language is 'en', default country is 'US'.
    ------------------------------
    Enter search query (or 'config', 'quit', 'exit') [lang:en, country:US]: technology
    
    Attempting to get news for query: 'technology' (lang: en, country: US)
    Fetching URL: https://news.google.com/search?q=technology&hl=en&gl=US
    Attempting to find headlines using <a> tags with class 'JtKRv'.
    Found ... links with class 'JtKRv'.
    
    --- Headlines for 'technology' (en-US) ---
    1. Headline 1...
    2. Headline 2...
    ...
    ------------------------------
    Enter search query (or 'config', 'quit', 'exit') [lang:en, country:US]: config
    
    --- Configure Language and Country ---
    Enter language code (e.g., en, ko) [current: en, press Enter to keep]: ko
    Enter country code (e.g., US, KR) [current: US, press Enter to keep]: KR
    Settings updated: Language set to 'ko', Country set to 'KR'.
    ------------------------------
    Enter search query (or 'config', 'quit', 'exit') [lang:ko, country:KR]: 한국 경제
    
    Attempting to get news for query: '한국 경제' (lang: ko, country: KR)
    Fetching URL: https://news.google.com/search?q=%ED%95%9C%EA%B5%AD+%EA%B2%BD%EC%A0%9C&hl=ko&gl=KR
    Attempting to find headlines using <a> tags with class 'JtKRv'.
    Found ... links with class 'JtKRv'.
    
    --- Headlines for '한국 경제' (ko-KR) ---
    1. 한국 경제 관련 뉴스 1...
    2. 한국 경제 관련 뉴스 2...
    ...
    ------------------------------
    Enter search query (or 'config', 'quit', 'exit') [lang:ko, country:KR]: quit
    Exiting News Fetcher Agent. Goodbye!
    ```
