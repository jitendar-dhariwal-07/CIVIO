"""
Hotspot detection service using DBSCAN clustering.

Groups geo-located complaints into spatial clusters to identify areas with
concentrated civic issues, enabling proactive intervention by authorities.
"""

from __future__ import annotations

import logging
import math
from collections import Counter
from typing import Any, Dict, List, Optional

import numpy as np

from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Compute the Haversine distance in kilometres between two GPS points."""
    R = 6371.0  # Earth's radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def detect_hotspots(
    complaints: List[Dict[str, Any]],
    eps: float = 0.01,
    min_samples: int = 3,
) -> List[Dict[str, Any]]:
    """
    Run DBSCAN clustering on complaint GPS coordinates to find hotspots.

    Args:
        complaints: List of dicts with keys: id, latitude, longitude, category, state, district.
        eps: Maximum distance (in degrees ≈ 1.1 km) between points in a cluster.
        min_samples: Minimum complaints to form a cluster.

    Returns:
        List of hotspot dicts suitable for storing in the hotspots table.
    """
    if len(complaints) < min_samples:
        return []

    try:
        from sklearn.cluster import DBSCAN
    except ImportError:
        logger.error("scikit-learn is required for hotspot detection.")
        return []

    coords = np.array(
        [[c["latitude"], c["longitude"]] for c in complaints],
        dtype=np.float64,
    )

    # DBSCAN with haversine-like metric (using degrees as proxy; 0.01° ≈ 1.1 km)
    clustering = DBSCAN(
        eps=eps,
        min_samples=min_samples,
        metric="euclidean",
    ).fit(coords)

    labels = clustering.labels_
    unique_labels = set(labels)
    unique_labels.discard(-1)  # Remove noise label

    hotspots: List[Dict[str, Any]] = []

    for cluster_id in sorted(unique_labels):
        mask = labels == cluster_id
        cluster_indices = np.where(mask)[0]
        cluster_complaints = [complaints[i] for i in cluster_indices]

        # Centroid
        cluster_coords = coords[mask]
        centroid_lat = float(np.mean(cluster_coords[:, 0]))
        centroid_lng = float(np.mean(cluster_coords[:, 1]))

        # Radius (max distance from centroid to any point in cluster)
        max_dist = 0.0
        for c in cluster_coords:
            d = _haversine_km(centroid_lat, centroid_lng, float(c[0]), float(c[1]))
            if d > max_dist:
                max_dist = d
        radius_km = round(max(max_dist, 0.1), 2)

        # Category breakdown
        categories = Counter(c["category"] for c in cluster_complaints)
        primary_category = categories.most_common(1)[0][0]

        # State / district (most common)
        states = Counter(c.get("state", "") for c in cluster_complaints)
        districts = Counter(c.get("district", "") for c in cluster_complaints)
        most_state = states.most_common(1)[0][0] if states else None
        most_district = districts.most_common(1)[0][0] if districts else None

        # Severity score (heuristic: count * category weight)
        category_weight = {
            "public_safety": 5, "corruption": 4, "healthcare": 4,
            "electricity": 3, "water_supply": 3, "sanitation": 3,
            "pollution": 3, "roads": 2, "education": 2,
            "public_transport": 2, "housing": 2, "food_safety": 2,
            "telecom": 1, "banking": 1, "government_service": 1, "other": 1,
        }
        severity = min(100, sum(
            category_weight.get(c["category"], 1) for c in cluster_complaints
        ) * 5)

        hotspots.append({
            "cluster_id": int(cluster_id),
            "latitude": round(centroid_lat, 6),
            "longitude": round(centroid_lng, 6),
            "complaint_count": len(cluster_complaints),
            "radius_km": radius_km,
            "primary_category": primary_category,
            "categories": dict(categories),
            "state": most_state,
            "district": most_district,
            "severity_score": min(severity, 100.0),
            "complaint_ids": [c["id"] for c in cluster_complaints],
        })

    # Sort by severity descending
    hotspots.sort(key=lambda h: h["severity_score"], reverse=True)
    logger.info("Detected %d hotspots from %d complaints.", len(hotspots), len(complaints))
    return hotspots


def get_hotspot_geojson(hotspots: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Convert hotspot data to GeoJSON FeatureCollection for map rendering.
    """
    features = []
    for h in hotspots:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [h["longitude"], h["latitude"]],
            },
            "properties": {
                "cluster_id": h["cluster_id"],
                "complaint_count": h["complaint_count"],
                "radius_km": h["radius_km"],
                "primary_category": h["primary_category"],
                "categories": h.get("categories", {}),
                "severity_score": h["severity_score"],
                "state": h.get("state"),
                "district": h.get("district"),
            },
        }
        features.append(feature)

    return {
        "type": "FeatureCollection",
        "features": features,
    }
