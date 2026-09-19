"""
Property and tag extraction helpers for GeoJSON feature properties and OSM/OpenCity tags.
"""

def extract_name(properties: dict, fallback_index: int | None = None, fallback_id: str | int | None = None) -> str:
    """Extract location name from properties, OpenCity tags, or OSM tags."""
    name_keys = [
        "name", "NAME", "name:en", "ward_name", "WARD_NAME", "Ward_Name",
        "label", "LABEL", "locality", "LOCALITY"
    ]
    for key in name_keys:
        if key in properties and properties[key]:
            return str(properties[key]).strip()
    
    # Fallback to ward code if available
    ward_codes = extract_ward_codes(properties)
    if ward_codes:
        return f"Ward {', '.join(ward_codes)}"

    if fallback_id:
        return f"Ward {fallback_id}"
    if fallback_index is not None:
        return f"Location {fallback_index + 1}"
    return "Unknown Location"


def extract_ward_codes(properties: dict) -> list[str]:
    """Extract list of ward codes from properties, OpenCity tags, or OSM tags."""
    code_keys = [
        "ref", "ref:ward", "ward_no", "WARD_NO", "Ward_No", "ward_code",
        "WARD_CODE", "gmc_ward", "GMC_WARD", "ward_number", "WARD_NUM", "wards", "WARDS"
    ]
    codes: list[str] = []
    for key in code_keys:
        if key in properties and properties[key]:
            raw_val = properties[key]
            if isinstance(raw_val, list):
                for v in raw_val:
                    val_str = str(v).strip()
                    if val_str and val_str not in codes:
                        codes.append(f"0{val_str}" if val_str.isdigit() and len(val_str) == 1 else val_str)
            else:
                val_str = str(raw_val).strip()
                # If comma or slash separated list, e.g. "1, 2" or "01/02"
                for item in val_str.replace("/", ",").split(","):
                    item_str = item.strip()
                    if item_str:
                        formatted = f"0{item_str}" if item_str.isdigit() and len(item_str) == 1 else item_str
                        if formatted not in codes:
                            codes.append(formatted)
    return codes


