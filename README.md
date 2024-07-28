# URL Requester

URL Requester is an advanced multi-protocol request tool designed for performing HTTP requests to multiple URLs with comprehensive support for proxy usage, rate limiting, and other advanced features. This tool is specifically tailored for testing SQL injection vulnerabilities, including SQL sleep vulnerabilities.

## Features

- **Multi-Protocol Support**: Handles GET, POST, PUT, and DELETE HTTP methods.
- **Custom Headers & Cookies**: Easily include custom headers and cookies in requests.
- **Rotating User Agents**: Utilizes a rotating user agent for each request to mimic different browsers and devices.
- **Proxy Support**: Integrates proxy usage and verification to anonymize and distribute requests.
- **Rate Limiting**: Implements rate limiting to avoid server overloads and potential bans.
- **Retry Mechanism**: Retries failed requests with exponential backoff.
- **Exportable Results**: Exports results in CSV, JSON, or XML formats.
- **Response Time Analysis**: Generates a histogram of response times for performance analysis.
- **SQL Injection Testing**: Specifically designed for identifying SQL injection vulnerabilities, including SQL sleep attacks.
- **Detailed Logging**: Provides detailed logging with colored output for enhanced readability.

## Installation

```sh
git clone https://github.com/Mr-dark55/URL-RequESTER/
cd URL-RequESTER/
pip install -r requirements.txt
```



## Command-line Arguments

```sh
    -u, --urls: Text file containing URLs to send requests to.
    -d, --data: Text file containing data to be sent with the requests.
    -m, --method: HTTP method to use (default: GET).
    -c, --cookie: Cookie to include in the request.
    -t, --threads: Number of concurrent threads to use (default: 10).
    -o, --output: Output file name for results.
    -f, --format: Output format (csv, json, xml) (default: csv).
    -p, --proxies: Text file containing a list of proxies.
    --headers: JSON file containing additional headers.
    --no-verify-ssl: Disable SSL certificate verification.
```
## Example Command

```sh
python url_requester.py -u urls.txt -d data.txt -m POST -c "session_id=xyz" -t 20 -o results.csv -f csv -p proxies.txt --headers headers.json --no-verify-ssl
```



This `README.md` file provides a clear and comprehensive overview of your tool, including its features, installation instructions, usage guidelines, command-line arguments, example command, output details, and contribution information.





