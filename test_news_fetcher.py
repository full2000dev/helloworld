import unittest
from unittest.mock import patch, Mock
import requests # Required for requests.exceptions.RequestException

# Assuming news_fetcher.py is in the same directory or accessible via PYTHONPATH
from news_fetcher import get_google_news, fetch_google_news_html, extract_news_headlines

# Sample HTML snippets for mocking responses
# Based on current news_fetcher.py logic, JtKRv class is important
SAMPLE_HTML_SUCCESS = """
<html><body>
    <a class="JtKRv">Global Tech Advances in 2024</a>
    <a class="JtKRv">The Future of AI in Healthcare</a>
    <div><a class="JtKRv">Another Tech Story</a></div> 
</body></html>
"""

SAMPLE_HTML_NO_RESULTS = """
<html><body>
    <p>Your search - <b>a_very_obscure_and_unlikely_query_xyz123</b> - did not match any documents.</p>
    <div>No articles found.</div>
</body></html>
"""

SAMPLE_HTML_EMPTY_QUERY_RESULTS = """
<html><body>
    <a class="JtKRv">Top Stories Today</a>
    <a class="JtKRv">Local News Highlights</a>
    <a class="JtKRv">Picks for you</a>
</body></html>
"""

class TestGetGoogleNews(unittest.TestCase):

    @patch('news_fetcher.requests.get')
    def test_successful_query(self, mock_requests_get):
        """Test get_google_news with a typical query that should return headlines."""
        # Configure the mock response for a successful fetch
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = SAMPLE_HTML_SUCCESS
        mock_requests_get.return_value = mock_response

        query = "technology"
        headlines = get_google_news(query)

        self.assertIsInstance(headlines, list, "Should return a list.")
        self.assertTrue(len(headlines) > 0, "Should return a non-empty list of headlines.")
        for headline in headlines:
            self.assertIsInstance(headline, str, "Each headline should be a string.")
        
        # Check if the mock was called correctly (optional, but good practice)
        mock_requests_get.assert_called_once()
        self.assertIn(query, mock_requests_get.call_args[0][0], "Request URL should contain the query.")


    @patch('news_fetcher.requests.get')
    def test_obscure_query_returns_empty_list(self, mock_requests_get):
        """Test get_google_news with an obscure query unlikely to yield results."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = SAMPLE_HTML_NO_RESULTS
        mock_requests_get.return_value = mock_response

        query = "a_very_obscure_and_unlikely_query_xyz123"
        headlines = get_google_news(query)

        self.assertIsInstance(headlines, list)
        self.assertEqual(len(headlines), 0, "Should return an empty list for obscure queries with no results.")
        mock_requests_get.assert_called_once()

    @patch('news_fetcher.requests.get')
    def test_empty_query_returns_generic_topics(self, mock_requests_get):
        """Test get_google_news with an empty query string."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = SAMPLE_HTML_EMPTY_QUERY_RESULTS
        mock_requests_get.return_value = mock_response

        query = ""
        headlines = get_google_news(query)

        self.assertIsInstance(headlines, list)
        # Based on live tests, empty queries can return generic topics.
        # The exact number might vary, so we check if it's non-empty.
        self.assertTrue(len(headlines) > 0, "Should return a non-empty list for empty query (generic topics).")
        for headline in headlines:
            self.assertIsInstance(headline, str)
        mock_requests_get.assert_called_once()
        # Google News URL for empty query is usually just /search?q=
        self.assertTrue(mock_requests_get.call_args[0][0].endswith("q="), "Request URL for empty query should end with q=")


    @patch('news_fetcher.requests.get')
    def test_network_error_returns_empty_list(self, mock_requests_get):
        """Test get_google_news when a network error occurs during fetch."""
        # Configure the mock to raise a ConnectionError (or any RequestException)
        mock_requests_get.side_effect = requests.exceptions.ConnectionError("Simulated network connection error")

        query = "any_query_network_error"
        headlines = get_google_news(query)

        self.assertIsInstance(headlines, list)
        self.assertEqual(len(headlines), 0, "Should return an empty list when a network error occurs.")
        mock_requests_get.assert_called_once()
        
    @patch('news_fetcher.requests.get')
    def test_http_error_returns_empty_list(self, mock_requests_get):
        """Test get_google_news when an HTTP error (e.g., 404, 500) occurs."""
        mock_response = Mock()
        mock_response.status_code = 404 # Simulate Not Found
        # requests.get().raise_for_status() would be called in fetch_google_news_html
        # So, we need to make the mock_response itself capable of raising this error.
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Simulated HTTP 404 error")
        mock_requests_get.return_value = mock_response
        
        query = "any_query_http_error"
        headlines = get_google_news(query)

        self.assertIsInstance(headlines, list)
        self.assertEqual(len(headlines), 0, "Should return an empty list when an HTTP error occurs.")
        mock_requests_get.assert_called_once()

if __name__ == '__main__':
    unittest.main()
