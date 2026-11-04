"""Helpers compartidos por las comprobaciones del Hito 1."""

from __future__ import annotations

import re

import yaml

FIXED_WB = ("NY.GDP.PCAP.CD", "SP.POP.TOTL")


def worldbank_indicator_ids(sources: dict) -> list[str]:
    """Códigos WDI declarados en sources.yaml (entrada habilitada)."""
    found: list[str] = []
    for src in sources.get("sources") or []:
        if not isinstance(src, dict):
            continue
        sid = str(src.get("id") or "")
        params = src.get("params") or {}
        meta = src.get("meta") or {}
        ind = params.get("indicator_id") or meta.get("indicator_id")
        url = str(src.get("url") or src.get("url_template") or "")
        looks_wb = "worldbank" in sid.lower() or "api.worldbank.org" in url
        if looks_wb and ind:
            found.append(str(ind))
        elif looks_wb:
            m = re.search(r"indicator/([A-Z0-9_.]+)", url)
            if m:
                found.append(m.group(1))
    return found


def source_mentions(sources: dict, needle: str) -> bool:
    return needle in yaml.dump(sources, allow_unicode=True)
