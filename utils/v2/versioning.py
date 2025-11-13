import re
from flask import request
from datetime import datetime

def detect_version(default="v5"):
    """Detect API version from query param or Accept header."""
    # 1. Query param: ?version=1
    version = request.args.get("version")
    if version:
        return f"v{version}"

    # 2. Header-based: Accept: application/vnd.api.v2+json
    accept = request.headers.get("Accept", "")
    match = re.search(r"vnd\.api\.v([\w\-]+)\+json", accept)
    if match:
        return f"v{match.group(1)}"

    # 3. Default fallback
    return default

# Versions that are deprecated
DEPRECATED_VERSIONS = ["v1", "v2"]
# Version sunset dates
SUNSET_DATES = {
    "v1": "Sun, 16 Nov 2025 23:59:59 GMT",
    "v2": "Sun, 23 Nov 2025 23:59:59 GMT",
}


def add_sunset_headers(response, version):
    """
    Adds Sunset + Deprecation headers if the version is deprecated.
    Usage:
        response = make_response(jsonify(payload))
        return add_sunset_headers(response, version)
    """
    if version in DEPRECATED_VERSIONS:
        sunset = SUNSET_DATES.get(version)
        if sunset:
            response.headers["Sunset"] = sunset
        response.headers["Deprecation"] = "true"
    return response