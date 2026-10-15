#!/usr/bin/env python3
"""GA4 onboarding lane: create a property + web data stream (and optionally
link a Google Ads customer) with zero browser clicks.

Usage:
  ga_onboard.py "Site Name" https://example.com --account accounts/123456789 \
      [--link-ads --ads-customer 1234567890] [--time-zone America/New_York] \
      [--currency USD]

Auth comes from the environment — nothing is read from disk and nothing is
printed:
  GOOGLE_OAUTH_CLIENT_ID       OAuth client ID (Web or Desktop app)
  GOOGLE_OAUTH_CLIENT_SECRET   OAuth client secret
  GOOGLE_ANALYTICS_REFRESH_TOKEN  Refresh token carrying
                               https://www.googleapis.com/auth/analytics.edit

The Analytics Admin API must be enabled on the Google Cloud project that owns
the OAuth client. See SKILL.md for the Admin-vs-Data API scope split.
"""
import argparse, json, os, sys, urllib.request, urllib.parse

BASE = "https://analyticsadmin.googleapis.com/v1alpha"

def _env(name):
    v = os.environ.get(name, "").strip()
    if not v:
        print(f"error: set {name} in the environment", file=sys.stderr)
        sys.exit(2)
    return v

def access_token():
    data = urllib.parse.urlencode({
        "client_id": _env("GOOGLE_OAUTH_CLIENT_ID"),
        "client_secret": _env("GOOGLE_OAUTH_CLIENT_SECRET"),
        "refresh_token": _env("GOOGLE_ANALYTICS_REFRESH_TOKEN"),
        "grant_type": "refresh_token"}).encode()
    return json.load(urllib.request.urlopen(
        urllib.request.Request("https://oauth2.googleapis.com/token", data=data)))["access_token"]

class GA:
    def __init__(self):
        self.at = access_token()
    def call(self, method, path, body=None):
        req = urllib.request.Request(BASE + path, method=method,
            headers={"Authorization": f"Bearer {self.at}", "Content-Type": "application/json"})
        if body is not None:
            req.data = json.dumps(body).encode()
        try:
            return json.load(urllib.request.urlopen(req))
        except urllib.error.HTTPError as e:
            print(f"HTTP {e.code} {path}\n{e.read().decode()[:900]}", file=sys.stderr)
            sys.exit(1)

def main():
    ap = argparse.ArgumentParser(description="Onboard a new website to GA4 via the Admin API.")
    ap.add_argument("name", help="Property display name, e.g. 'Example Site'")
    ap.add_argument("url", help="Site origin, e.g. https://example.com")
    ap.add_argument("--account", required=True, help="Analytics account, e.g. accounts/123456789")
    ap.add_argument("--link-ads", action="store_true", help="Link a Google Ads customer to the new property")
    ap.add_argument("--ads-customer", default=os.environ.get("GOOGLE_ADS_CUSTOMER_ID", ""),
                    help="Google Ads customer ID (bare ten digits); default $GOOGLE_ADS_CUSTOMER_ID")
    ap.add_argument("--time-zone", default="UTC", help="Property time zone (default UTC)")
    ap.add_argument("--currency", default="USD", help="Property currency code (default USD)")
    args = ap.parse_args()
    ga = GA()
    prop = ga.call("POST", "/properties", {
        "parent": args.account, "displayName": args.name,
        "timeZone": args.time_zone, "currencyCode": args.currency})
    print(f"property: {prop['name']}  '{prop['displayName']}'")
    stream = ga.call("POST", f"/{prop['name']}/dataStreams", {
        "type": "WEB_DATA_STREAM",
        "displayName": f"{args.name} — {args.url}",
        "webStreamData": {"defaultUri": args.url}})
    print(f"stream:   {stream['name']}  {stream['webStreamData']['measurementId']}")
    if args.link_ads:
        if not args.ads_customer:
            print("error: --link-ads needs --ads-customer or GOOGLE_ADS_CUSTOMER_ID", file=sys.stderr)
            sys.exit(2)
        link = ga.call("POST", f"/{prop['name']}/googleAdsLinks",
                       {"customerId": args.ads_customer})
        print(f"adsLink:  {link['name']}  customer {link['customerId']}")
    print(f"\nNext: install the gtag snippet with measurement ID "
          f"{stream['webStreamData']['measurementId']} on {args.url}")

if __name__ == "__main__":
    main()
