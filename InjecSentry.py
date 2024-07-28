# !/usr/bin/python3 
# code by Mr - Dark 
# twiter @Mr_Dark55

import argparse
import httpx
import time
import concurrent.futures
import csv
import json
import xml.etree.ElementTree as ET
from tqdm import tqdm
import random
import logging
from ratelimit import limits, sleep_and_retry
import fake_useragent
from colorama import Fore, Style, init
import pyfiglet
import schedule
import matplotlib.pyplot as plt

# Initialize colorama
init(autoreset=True)

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        timestamp = self.formatTime(record, self.datefmt)
        colored_timestamp = f"{Fore.CYAN}[{timestamp}]{Style.RESET_ALL}"
        return f"{colored_timestamp} - {record.levelname} - {record.getMessage()}"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(ColoredFormatter('%(asctime)s'))
logger.handlers = [handler]

def display_banner():
    banner = pyfiglet.figlet_format("URL Requester", font="slant")
    print(Fore.CYAN + banner + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 60 + Style.RESET_ALL)
    print(Fore.GREEN + "Advanced Multi-Protocol Request Tool" + Style.RESET_ALL)
    print(Fore.GREEN + "With proxy support, rate limiting, and more" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 60 + Style.RESET_ALL)
    print()

def load_proxies(proxy_file):
    with open(proxy_file) as file:
        return [line.strip() for line in file if line.strip()]

def verify_proxy(proxy):
    try:
        with httpx.Client(proxies={'http://': proxy, 'https://': proxy}, timeout=5) as client:
            response = client.get('http://httpbin.org/ip')
            return response.status_code == 200
    except:
        return False

@sleep_and_retry
@limits(calls=10, period=1)  # 10 calls per second
def perform_request(url, data, method='GET', headers=None, cookie=None, proxy=None, timeout=30, max_retries=3, verify_ssl=True):
    url_with_data = f"{url}{data}" if method == 'GET' else url
    ua = fake_useragent.UserAgent()
    headers = headers or {}
    headers['User-Agent'] = headers.get('User-Agent', ua.random)
    
    for attempt in range(max_retries):
        start_time = time.time()
        try:
            with httpx.Client(proxies={'http://': proxy, 'https://': proxy} if proxy else None, timeout=timeout, verify=verify_ssl) as client:
                if method == 'GET':
                    response = client.get(url_with_data, headers=headers, cookies={'cookie': cookie} if cookie else None)
                elif method == 'POST':
                    response = client.post(url, data=data, headers=headers, cookies={'cookie': cookie} if cookie else None)
                elif method == 'PUT':
                    response = client.put(url, data=data, headers=headers, cookies={'cookie': cookie} if cookie else None)
                elif method == 'DELETE':
                    response = client.delete(url, headers=headers, cookies={'cookie': cookie} if cookie else None)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                response.raise_for_status()
                status_code = response.status_code
                content = response.text
                if 'captcha' in content.lower():
                    raise Exception("CAPTCHA detected")
                return True, url_with_data, time.time() - start_time, None, status_code, content
        except httpx.HTTPStatusError as e:
            error_message = f"HTTP error: {e}"
        except Exception as e:
            error_message = str(e)
        
        logging.warning(f"Attempt {attempt + 1} failed for {url_with_data}: {error_message}")
        if attempt < max_retries - 1:
            time.sleep(2 ** attempt)  # Exponential backoff
    
    return False, url_with_data, time.time() - start_time, error_message, None, None

def worker(args):
    return perform_request(*args)

def export_results(results, output_file, format='csv'):
    if format == 'csv':
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['URL', 'Success', 'Response Time (seconds)', 'Error Message', 'Status Code', 'Content'])
            for result in results:
                writer.writerow(result)
    elif format == 'json':
        with open(output_file, 'w', encoding='utf-8') as jsonfile:
            json.dump(results, jsonfile, indent=2)
    elif format == 'xml':
        root = ET.Element("results")
        for result in results:
            item = ET.SubElement(root, "item")
            ET.SubElement(item, "url").text = str(result[0])
            ET.SubElement(item, "success").text = str(result[1])
            ET.SubElement(item, "response_time").text = str(result[2])
            ET.SubElement(item, "error_message").text = str(result[3])
            ET.SubElement(item, "status_code").text = str(result[4])
            ET.SubElement(item, "content").text = str(result[5])
        tree = ET.ElementTree(root)
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
    else:
        raise ValueError(f"Unsupported export format: {format}")

def plot_results(results):
    response_times = [result[2] for result in results if result[1]]  # Only successful requests
    plt.figure(figsize=(10, 5))
    plt.hist(response_times, bins=20, edgecolor='black')
    plt.title('Distribution of Response Times')
    plt.xlabel('Response Time (seconds)')
    plt.ylabel('Frequency')
    plt.savefig('response_times_histogram.png')
    plt.close()

def main():
    display_banner()

    parser = argparse.ArgumentParser(description="Advanced Multi-Protocol Request Tool")
    parser.add_argument("-u", "--urls", required=True, help="Text file containing URLs to send requests to.")
    parser.add_argument("-d", "--data", required=True, help="Text file containing data to be sent with the requests.")
    parser.add_argument("-m", "--method", default="GET", choices=["GET", "POST", "PUT", "DELETE"], help="HTTP method to use.")
    parser.add_argument("-c", "--cookie", help="Cookie to include in the request.")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of concurrent threads to use.")
    parser.add_argument("-o", "--output", help="Output file name for results.")
    parser.add_argument("-f", "--format", default="csv", choices=["csv", "json", "xml"], help="Output format.")
    parser.add_argument("-p", "--proxies", help="Text file containing a list of proxies.")
    parser.add_argument("--headers", help="JSON file containing additional headers.")
    parser.add_argument("--no-verify-ssl", action="store_true", help="Disable SSL certificate verification.")
    args = parser.parse_args()

    with open(args.urls) as file:
        urls = file.read().splitlines()
    with open(args.data) as file:
        data = file.read().splitlines()

    headers = {}
    if args.headers:
        with open(args.headers) as file:
            headers = json.load(file)

    if args.proxies:
        proxies = load_proxies(args.proxies)
        logging.info(f"Loaded {len(proxies)} proxies. Verifying...")
        verified_proxies = [proxy for proxy in tqdm(proxies, desc="Verifying proxies") if verify_proxy(proxy)]
        logging.info(f"Verified {len(verified_proxies)} working proxies.")
    else:
        verified_proxies = None

    tasks = []
    for url in urls:
        for d in data:
            proxy = random.choice(verified_proxies) if verified_proxies else None
            tasks.append((url, d, args.method, headers, args.cookie, proxy, 30, 3, not args.no_verify_ssl))

    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = [executor.submit(worker, task) for task in tasks]
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(tasks), desc="Request Progress"):
            success, url_with_data, response_time, error_message, status_code, content = future.result()
            results.append((url_with_data, success, response_time, error_message, status_code, content))
            if success and response_time <= 20:
                logging.info(f"{Fore.GREEN}URL {url_with_data} - {response_time:.2f} seconds - Status: {status_code}{Style.RESET_ALL}")
            else:
                logging.error(f"{Fore.RED}URL {url_with_data} - {response_time:.2f} seconds - Error: {error_message}{Style.RESET_ALL}")

    if args.output:
        export_results(results, args.output, args.format)
        logging.info(f"\nResults saved to {args.output}")

    plot_results(results)
    logging.info("Response times histogram saved as 'response_times_histogram.png'")

if __name__ == "__main__":
    main()
