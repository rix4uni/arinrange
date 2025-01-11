import requests
from bs4 import BeautifulSoup
import urllib3
import re
import sys
import argparse
import time

# Warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# prints the version message
version = "v0.0.1"

def PrintVersion():
    print(f"Current arinrange version {version}")

def PrintBanner():
    banner = rf"""
                _                                       
  ____ _ _____ (_)____   _____ ____ _ ____   ____ _ ___ 
 / __ `// ___// // __ \ / ___// __ `// __ \ / __ `// _ \
/ /_/ // /   / // / / // /   / /_/ // / / // /_/ //  __/
\__,_//_/   /_//_/ /_//_/    \__,_//_/ /_/ \__, / \___/ 
                                          /____/"""
    print(f"{banner}\n\t\t\tCurrent arinrange version {version}\n")

# Argument parser setup
parser = argparse.ArgumentParser(description="Net Range scraping on whois.arin.net")
parser.add_argument('--timeout', default=15, type=int, help='Timeout (in seconds) for http client (default 15)')
parser.add_argument('--silent', action='store_true', help='Run without printing the banner')
parser.add_argument('--version', action='store_true', help='Show current version of arinrange')
args = parser.parse_args()

if args.version:
    PrintBanner()
    PrintVersion()
    exit(1)

if not args.silent:
    PrintBanner()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
}

# Process each line from standard input
for query_input in sys.stdin:
    query_input = query_input.strip()  # Remove leading/trailing whitespaces

    if query_input:  # If the line is not empty
        data = {
            'queryinput': query_input,
        }

        response = requests.post('https://whois.arin.net/ui/query.do', headers=headers, data=data, timeout=args.timeout)

        pattern = r'<td colspan="2">.*?<a href="([^"]+)'

        # Search for all matches
        urls = re.findall(pattern, response.text)

        # Add '/nets' to URLs containing 'https://whois.arin.net/rest/org'
        modified_urls = [url + '/nets' if 'https://whois.arin.net/rest/org' in url else url for url in urls]

        # Iterate over modified URLs and extract the required information
        for url in modified_urls:
            response = requests.get(url, timeout=args.timeout)
            # Parse the XML response
            soup = BeautifulSoup(response.text, 'xml')

            # Find all <netRef> tags and extract the startAddress and endAddress
            net_refs = soup.find_all('netRef')

            for net_ref in net_refs:
                start_address = net_ref.get('startAddress')
                end_address = net_ref.get('endAddress')
                print(f"{start_address}-{end_address}")
