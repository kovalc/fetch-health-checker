import yaml
import requests
import time
from urllib.parse import urlparse
from collections import defaultdict
import sys
import signal

class HealthChecker:
    def __init__(self, config_path):
        # Read and parse YAML config
        with open(config_path, 'r') as file:
            self.endpoints = yaml.safe_load(file)
        
        # Initialize statistics tracking
        self.stats = defaultdict(lambda: {'up': 0, 'total': 0})
        
        # Setup signal handler for graceful exit
        signal.signal(signal.SIGINT, self.handle_exit)

    def check_endpoint(self, endpoint):
        """Check if an endpoint is UP or DOWN based on response code and latency"""
        try:
            # Prepare request parameters
            method = endpoint.get('method', 'GET')
            headers = endpoint.get('headers', {})
            body = endpoint.get('body', None)
            
            # Send request and measure latency
            start_time = time.time()
            response = requests.request(
                method=method,
                url=endpoint['url'],
                headers=headers,
                data=body,
                timeout=1
            )
            latency = (time.time() - start_time) * 1000
            
            # Check if endpoint is UP (200-299 response and latency < 500ms)
            return (200 <= response.status_code < 300) and (latency < 500)
            
        except Exception:
            return False

    def run_health_checks(self):
        """Run health checks for all endpoints"""
        while True:
            # Check each endpoint
            for endpoint in self.endpoints:
                # Get domain from URL
                domain = urlparse(endpoint['url']).netloc
                
                # Check endpoint health
                is_up = self.check_endpoint(endpoint)
                
                # Update statistics
                self.stats[domain]['total'] += 1
                if is_up:
                    self.stats[domain]['up'] += 1

            # Log availability percentages
            self.log_availability()
            
            # Wait for next check cycle
            time.sleep(15)

    def log_availability(self):
        """Log availability percentage for each domain"""
        for domain, stats in self.stats.items():
            availability = round(100 * stats['up'] / stats['total'])
            print(f"{domain} has {availability}% availability percentage")

    def handle_exit(self, signum, frame):
        """Handle graceful exit on CTRL+C"""
        sys.exit(0)

def main():
    if len(sys.argv) != 2:
        print("Usage: python health_checker.py <config_file_path>")
        sys.exit(1)
        
    config_path = sys.argv[1]
    checker = HealthChecker(config_path)
    checker.run_health_checks()

if __name__ == "__main__":
    main()