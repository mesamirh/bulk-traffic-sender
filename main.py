import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import threading
import time
import random
import config
from proxy_validator import ProxyValidator
from colorama import init, Fore, Style
import sys

init()

completed_requests = 0
failed_requests = 0
lock = threading.Lock()

def get_random_proxy():
    """Function to get a random proxy from the list."""
    if hasattr(config, 'PROXIES') and config.PROXIES and config.USE_PROXY:
        return random.choice(config.PROXIES)
    return None

def create_session():
    """Create a session with retry strategy"""
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy, 
                         pool_connections=100, 
                         pool_maxsize=100)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def send_request():
    """Function to send a single HTTP request."""
    global completed_requests, failed_requests
    session = create_session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.6',
        'Connection': 'keep-alive',
    }
    
    try:
        # Add rate limiting delay
        time.sleep(random.uniform(config.MIN_REQUEST_DELAY, config.MAX_REQUEST_DELAY))
        
        proxy = get_random_proxy()
        kwargs = {
            'timeout': config.REQUEST_TIMEOUT,
            'headers': headers,
            'allow_redirects': True,
            'verify': True
        }
        if proxy:
            kwargs['proxies'] = {"http": proxy, "https": proxy}
            
        response = session.get(config.URL, **kwargs)
        
        with lock:
            if response.status_code == 200:
                completed_requests += 1
                print(f"Success - Status Code: {response.status_code}")
            else:
                failed_requests += 1
                print(f"Failed - Status Code: {response.status_code}")
                
    except Exception as e:
        with lock:
            failed_requests += 1
            print(f"Request failed: {str(e)}")
    finally:
        session.close()

def worker():
    """Worker function to execute multiple requests."""
    for _ in range(config.NUM_REQUESTS // config.CONCURRENT_THREADS):
        send_request()

def print_banner():
    banner = f"""{Fore.CYAN}
    ███╗   ███╗███████╗███████╗ █████╗ ███╗   ███╗██╗██████╗ ██╗  ██╗
    ████╗ ████║██╔════╝██╔════╝██╔══██╗████╗ ████║██║██╔══██╗██║  ██║
    ██╔████╔██║█████╗  ███████╗███████║██╔████╔██║██║██████╔╝███████║
    ██║╚██╔╝██║██╔══╝  ╚════██║██╔══██║██║╚██╔╝██║██║██╔══██╗██╔══██║
    ██║ ╚═╝ ██║███████╗███████║██║  ██║██║ ╚═╝ ██║██║██║  ██║██║  ██║
    ╚═╝     ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
    {Style.RESET_ALL}
    {Fore.GREEN}[*] Target: {config.URL}
    [*] Threads: {config.CONCURRENT_THREADS}
    [*] Requests: {config.NUM_REQUESTS}
    [*] Proxy Enabled: {config.USE_PROXY}{Style.RESET_ALL}
    """
    print(banner)

def show_progress():
    """Show progress bar during execution"""
    while True:
        sys.stdout.write(f'\r{Fore.YELLOW}[*] Completed: {completed_requests} | Failed: {failed_requests}{Style.RESET_ALL}')
        sys.stdout.flush()
        time.sleep(0.1)
        if completed_requests + failed_requests >= config.NUM_REQUESTS:
            break

def main():
    print_banner()
    print(f"{Fore.BLUE}[*] Testing proxies...{Style.RESET_ALL}")
    validator = ProxyValidator()
    working_proxies = validator.validate_proxies(config.PROXIES)
    
    if not working_proxies:
        print("No working proxies found. Exiting...")
        return
        
    config.PROXIES = working_proxies
    print(f"Found {len(working_proxies)} working proxies")
    
    print("Starting load test...")
    threads = []
    for _ in range(config.CONCURRENT_THREADS):
        thread = threading.Thread(target=worker)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    print(f"Completed requests: {completed_requests}")
    print(f"Failed requests: {failed_requests}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Script terminated by user{Style.RESET_ALL}")
