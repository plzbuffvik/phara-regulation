#!/usr/bin/env python3
"""
Minimal test: can this machine/environment reach fda.gov's RSS feed
without getting bot-blocked?

Run this from wherever you plan to eventually schedule the real
automation (your own PC, a server, GitHub Actions, etc.) BEFORE
building anything more elaborate on top of it.

Usage:
    pip install requests
    python test_fda_rss_access.py
"""

import sys
import requests

RSS_URL = "https://www.fda.gov/about-fda/contact-fda/stay-informed/rss-feeds/ora-foia-electronic-reading-room/rss.xml"

# Realistic browser-like headers. Bare "python-requests/x.x" User-Agents
# are one of the easiest signals for a WAF/bot-manager to flag.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    ),
    "Accept": "application/rss+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}


def main():
    print(f"Requesting: {RSS_URL}\n")

    try:
        resp = requests.get(RSS_URL, headers=HEADERS, timeout=15)
    except requests.RequestException as e:
        print(f"REQUEST FAILED (network/connection error): {e}")
        sys.exit(1)

    body = resp.content
    print(f"Status code   : {resp.status_code}")
    print(f"Content length: {len(body)} bytes")
    print(f"Content-Type  : {resp.headers.get('Content-Type')}")
    print()

    # The known bot-block signature from the earlier test: a tiny
    # ~10-byte "Not found" body with a 200 or 404 status.
    if len(body) < 100:
        print("!! SUSPECTED BOT BLOCK !!")
        print("Response body is suspiciously short for an RSS feed.")
        print(f"Raw body: {body!r}")
        print("\nResult: This environment appears to be BLOCKED, "
              "same as the GitHub Actions/local dev test noted earlier.")
        sys.exit(2)

    if resp.status_code != 200:
        print(f"Non-200 status code ({resp.status_code}) — likely blocked "
              f"or the URL/route has changed.")
        print(f"First 300 bytes of body:\n{body[:300]!r}")
        sys.exit(2)

    # Basic sanity check that we got real RSS/XML content, not a
    # block page dressed up with a 200 status.
    text_preview = body[:500].decode("utf-8", errors="replace")
    if "<rss" in text_preview or "<?xml" in text_preview:
        print("SUCCESS — this looks like real RSS/XML content.")
        print("\nFirst 500 bytes of response:\n")
        print(text_preview)
        print("\nResult: This environment can reach fda.gov normally. "
              "Safe to build the full automation on top of this.")
    else:
        print("UNCLEAR — got a 200 response, but it doesn't look like "
              "RSS/XML. Could be a block page or a CAPTCHA challenge.")
        print(f"\nFirst 500 bytes of response:\n{text_preview}")
        sys.exit(2)


if __name__ == "__main__":
    main()
