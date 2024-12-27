# Bulk Traffic Sender

A powerful Python-based tool for bulk traffic sending to websites with proxy support.

## Features

- 🚀 Multi-threaded requests
- 🔄 Proxy support with auto-validation
- 📊 Real-time progress monitoring
- 🛡️ Configurable retry mechanism
- 🎨 Beautiful terminal interface
- 🔧 Highly customizable settings

## Prerequisites

- Python 3.7+
- pip (Python package installer)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mesamirh/bulk-traffic-sender.git
   cd bulk-traffic-sender
   ```
2. Create and activate virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the script:
   ```bash
   python3 main.py
   ```

## Configuration

1. Open `config.py` file and modify the following settings:

- URL: Replace with your target URL.
- USE_PROXY: Set to True to enable proxy support.
- PROXIES: List of proxy servers to use.
- CONCURRENT_THREADS: Number of concurrent threads.
- NUM_REQUESTS: Total number of requests to send.

2. Save the file and run the script again.

## Customization

1. Open `main.py` file and modify the following settings:

- USER_AGENTS: List of user agents to use.
- MIN_REQUEST_DELAY: Minimum delay between requests.
- MAX_REQUEST_DELAY: Maximum delay between requests.
- RETRY_LIMIT: Maximum number of retries per request.
- REQUEST_TIMEOUT: Timeout for each request.

2. Save the file and run the script again.

## Features Explained

### 1. Proxy Validation
- Automatically tests proxies before use
- Supports HTTP/HTTPS proxies
- Filters out non-working proxies

### 2. Request Management
- Concurrent request handling
- Automatic retry mechanism
- Connection pooling
- Rate limiting

### 3. Monitoring
- Real-time success/failure counting
- Progress visualization
- Detailed error reporting