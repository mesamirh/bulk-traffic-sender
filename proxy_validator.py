import requests
import concurrent.futures
from urllib.parse import urlparse

class ProxyValidator:
    def __init__(self):
        self.working_proxies = []
        self.test_url = "https://api.ipify.org?format=json"
        self.timeout = 10

    def format_proxy_url(self, proxy):
        """Format proxy URL correctly"""
        if not proxy.startswith(('http://', 'https://')):
            proxy = f"http://{proxy}"
        return proxy

    def test_proxy(self, proxy):
        """Test single proxy and return if working"""
        formatted_proxy = self.format_proxy_url(proxy)
        proxies = {
            "http": formatted_proxy,
            "https": formatted_proxy
        }
        
        try:
            response = requests.get(
                self.test_url,
                proxies=proxies,
                timeout=self.timeout,
                verify=True
            )
            if response.status_code == 200:
                print(f"✓ Working proxy found: {proxy}")
                return proxy
        except Exception as e:
            print(f"✗ Failed proxy: {proxy} - Error: {str(e)}")
            return None

    def validate_proxies(self, proxy_list):
        """Test multiple proxies concurrently"""
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            results = executor.map(self.test_proxy, proxy_list)
            self.working_proxies = [p for p in results if p]
        return self.working_proxies