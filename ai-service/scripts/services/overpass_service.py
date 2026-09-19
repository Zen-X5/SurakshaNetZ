"""
Service for querying OpenStreetMap features via Overpass API.
"""

import requests
from scripts.config import OVERPASS_API, DEFAULT_OVERPASS_QUERY

def fetch_overpass_elements(query: str = DEFAULT_OVERPASS_QUERY, api_url: str = OVERPASS_API, timeout: int = 90) -> list[dict]:
    """
    Executes Overpass QL query against Overpass API and returns raw JSON elements.
    """
    print(f"📡 Fetching boundary relations from Overpass API ({api_url})...")
    response = requests.post(
        api_url,
        data={"data": query},
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()
    elements = data.get("elements", [])
    print(f"✅ Received {len(elements)} raw elements from OSM.\n")
    return elements
