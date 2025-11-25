import os
import json
import re
import pycountry
import pandas as pd
from bs4 import BeautifulSoup

# ---------------------------------------------
# Clean HTML → plain text
# ---------------------------------------------
def strip_html(html):
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator=" ", strip=True)

# ---------------------------------------------
# Recursively collect all blocks
# ---------------------------------------------
def walk_blocks(node, collected):
    if isinstance(node, dict):
        if "block_type" in node:
            collected.append(node)

        children = node.get("children")
        if isinstance(children, list):
            for child in children:
                walk_blocks(child, collected)

    elif isinstance(node, list):
        for item in node:
            walk_blocks(item, collected)

# ---------------------------------------------
# Fix broken lines inside a block
# ---------------------------------------------
def clean_multiline_text(text):
    if not text:
        return ""
    text = text.replace("\n", " ").replace("\r", " ")
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()

# ---------------------------------------------
# COUNTRY MAP + DETECTOR
# ---------------------------------------------
def build_canonical_country_map():
    canonical = {}

    for country in pycountry.countries:
        base = country.name.lower()
        canonical[country.name.lower()] = base
        if hasattr(country, "official_name"):
            canonical[country.official_name.lower()] = base

    custom = {
        # USA
        "usa": "united states of america",
        "u.s.a": "united states of america",
        "us": "united states of america",
        "united states": "united states of america",

        # UK
        "uk": "united kingdom",
        "u.k": "united kingdom",
        "england": "united kingdom",
        "great britain": "united kingdom",

        # Russia
        "russian federation": "russia",
        "russia": "russia",

        # Korea
        "south korea": "south korea",
        "republic of korea": "south korea",
        "north korea": "north korea",

        # Czech
        "czech republic": "czechia",
    }

    for k, v in custom.items():
        canonical[k.lower()] = v.lower()

    return canonical


def extract_countries(sentence):
    COUNTRY_MAP = build_canonical_country_map()

    country_keywords_regex = re.compile(
        r"\b(" + "|".join(map(re.escape, COUNTRY_MAP.keys())) + r")\b",
        flags=re.IGNORECASE
    )

    found = set()
    matches = country_keywords_regex.findall(sentence.lower())

    for m in matches:
        canon = COUNTRY_MAP.get(m.lower())
        if canon:
            found.add(canon)

    return sorted(found)

# --------------------------------------------------------------
# PROCESS ONE JSON FILE
# --------------------------------------------------------------
def process_one_json(json_path):
    TARGET_TYPES = {"Text", "ListItem", "Code", "Footnote"}

    with open(json_path, "r") as f:
        data = json.load(f)

    all_blocks = []
    walk_blocks(data, all_blocks)

    page_countries = set()

    for b in all_blocks:
        block_type = b.get("block_type", "")
        block_id = b.get("id", "")

        if block_type not in TARGET_TYPES:
            continue

        if not block_id.startswith(("/page/0/", "/page/1/")):
            continue

        raw = strip_html(b.get("html", ""))
        txt = clean_multiline_text(raw)

        countries = extract_countries(txt)
        if countries:
            page_countries.update(countries)

    return page_countries

# --------------------------------------------------------------
# MAIN RUNNER (IMPORTABLE)
# --------------------------------------------------------------
def country_fetch_main(input_folder, output_csv):
    results = []

    for file in os.listdir(input_folder):
        if not file.endswith(".json"):
            continue

        json_path = os.path.join(input_folder, file)
        countries = process_one_json(json_path)

        results.append({
            "file_name": file.replace(".json",""),
            "country_fetched": ", ".join(countries) if countries else ""
        })

    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)

    print("\nCountry Fetching Pipeline Completed Successfully!")
