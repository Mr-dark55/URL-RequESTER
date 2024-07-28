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
git clone https://github.com/yourusername/url-requester.git
cd URL-RequESTER/
pip install -r requirements.txt
