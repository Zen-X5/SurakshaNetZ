"""Calculate distance from a location centroid to nearby mapped waterways."""

from __future__ import annotations

import math
from typing import Any

import requests
from shapely.geometry import LineString, Point


def _project(longitude: float, latitude: float, point: list[float]) -> tuple[float, float]:
	x_scale = 111_320 * math.cos(math.radians(latitude))
	y_scale = 110_540
	return ((point[0] - longitude) * x_scale, (point[1] - latitude) * y_scale)


def get_nearest_waterway_distance_m(
	centroid: dict[str, Any],
	overpass_url: str,
	request_headers: dict[str, str],
) -> float | None:
	"""Find the nearest mapped river, stream, or canal vertex in metres."""
	longitude, latitude = centroid["coordinates"]
	query = f"""
	[out:json][timeout:45];
	way["waterway"~"river|stream|canal"](around:10000,{latitude},{longitude});
	out geom;
	"""
	response = requests.post(
		overpass_url,
		data={"data": query},
		headers=request_headers,
		timeout=60,
	)
	response.raise_for_status()
	payload = response.json()
	closest_distance: float | None = None
	longitude, latitude = centroid["coordinates"]
	origin = Point(0, 0)

	for element in payload.get("elements", []):
		points = [_project(longitude, latitude, [point["lon"], point["lat"]]) for point in element.get("geometry", [])]
		if len(points) < 2:
			continue
		distance = LineString(points).distance(origin)
		if closest_distance is None or distance < closest_distance:
			closest_distance = distance

	return round(closest_distance, 2) if closest_distance is not None else None
