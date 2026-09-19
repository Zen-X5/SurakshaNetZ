"""Shared HTTP client helpers for GIS data providers."""

from __future__ import annotations

from typing import Any

import requests

REQUEST_HEADERS = {"User-Agent": "SurakshaNetZ/1.0 (GIS location service)"}


def get_json(
    url: str,
    *,
    params: dict[str, Any] | None = None,
    data: dict[str, Any] | None = None,
) -> dict[str, Any] | list[Any]:
    if data is None:
        response = requests.get(url, params=params, headers=REQUEST_HEADERS, timeout=30)
    else:
        response = requests.post(url, params=params, data=data, headers=REQUEST_HEADERS, timeout=60)
    response.raise_for_status()
    return response.json()