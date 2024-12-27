# Configuration settings

# Target URL to send requests to
URL = "website_link"  # Replace with your target URL

# Proxy settings (optional)
USE_PROXY = True  # Set to True to enable proxy
PROXIES = [
    "username:password@ip:port",
]

# Number of concurrent threads
CONCURRENT_THREADS = 100

# Total number of requests to send
NUM_REQUESTS = 1000

# Maximum number of retries per request
RETRY_LIMIT = 5
REQUEST_TIMEOUT = 30  # Increased timeout
MIN_REQUEST_DELAY = 1.0  # Increased delay
MAX_REQUEST_DELAY = 2.0  # Increased delay