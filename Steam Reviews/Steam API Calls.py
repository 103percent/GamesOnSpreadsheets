import re
import time
import csv
import requests
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

REVIEW_URL = "https://store.steampowered.com/appreviews/{appid}?json=1"

def extract_appid(input_str):
    """
    Accepts either an integer-like appid string or a Steam store URL and
    returns the numeric appid.
    Examples:
        "570" -> "570"
        "https://store.steampowered.com/app/570/Dota_2/" -> "570"
    """
    # if it already looks like an integer, return it
    if re.match(r"^\d+$", input_str.strip()):
        return input_str.strip()
    m = re.search(r"/app/(\d+)", input_str)
    if m:
        return m.group(1)
    raise ValueError("Could not extract appid. Provide either numeric appid or full store URL.")

def strip_html_to_text(html):
    """Strip HTML tags and collapse whitespace to return plaintext."""
    if html is None:
        return ""
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator=" ")
    # collapse multiple whitespace/newlines
    return re.sub(r"\s+", " ", text).strip()

def fetch_reviews(appid, max_reviews=1000, per_request=100, filter="recent", language="all", sleep=1.0):
    """
    Fetch up to max_reviews plaintext reviews for the given appid.
    - per_request: number of reviews requested per call (max Steam accepts is typically 100).
    - filter: 'recent' | 'updated' | 'all' | 'english'? (use 'recent' or 'most_helpful' depending on behavior)
    - language: 'all' or 'english' or e.g. 'german'
    Returns list of dicts with keys: author_steamid, review_text, recommended(bool), timestamp_created, helpful_score
    """
    reviews_out = []
    cursor = "*"
    while len(reviews_out) < max_reviews:
        params = {
            "json": 1,
            "num": per_request,
            "filter": filter,
            "language": 'english',
            "purchase_type": "all",
            "cursor": cursor
        }
        # Build URL with encoded cursor param (requests will encode automatically if passed in params)
        resp = requests.get(REVIEW_URL.format(appid=appid), params=params, timeout=15)
        if resp.status_code != 200:
            raise RuntimeError(f"HTTP {resp.status_code} fetching reviews: {resp.text[:200]}")
        j = resp.json()
        batch = j.get("reviews", [])
        if not batch:
            break
        for r in batch:
            text_html = r.get("review", "")
            text = strip_html_to_text(text_html)
            entry = {
                "author_steamid": r.get("author", {}).get("steamid", ""),
                "review_text": text,
                "recommended": r.get("voted_up", False),
                "timestamp_created": r.get("timestamp_created"),
                "votes_helpful": r.get("votes_up", 0),
                "review_id": r.get("recommendationid")
            }
            reviews_out.append(entry)
            if len(reviews_out) >= max_reviews:
                break
        # Steam provides a 'cursor' value in the JSON. If not present, derive from response:
        cursor = j.get("cursor") or cursor
        # If Steam indicates there are no more results, break
        if not j.get("success", True) or not j.get("reviews"):
            break
        time.sleep(sleep)  # be polite
    return reviews_out

def save_reviews_csv(reviews, filename="steam_reviews.csv"):
    fieldnames = ["review_id", "author_steamid", "timestamp_created", "recommended", "votes_helpful", "review_text"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in reviews:
            writer.writerow({
                "review_id": r.get("review_id"),
                "author_steamid": r.get("author_steamid"),
                "timestamp_created": r.get("timestamp_created"),
                "recommended": r.get("recommended"),
                "votes_helpful": r.get("votes_helpful"),
                "review_text": r.get("review_text")
            })

if __name__ == "__main__":
    # Example usage:
    # supply either numeric appid like "570" or store url
    input_app = "https://store.steampowered.com/app/570/Dota_2/"
    appid = extract_appid(input_app)
    print("AppID:", appid)
    reviews = fetch_reviews(appid, max_reviews=500, per_request=100, sleep=1.0)
    print(f"Fetched {len(reviews)} reviews.")
    save_reviews_csv(reviews, filename=f"steam_reviews_{appid}.csv")
    print("Saved to CSV.")
