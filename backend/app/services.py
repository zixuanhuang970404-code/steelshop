"""Conservative MVP text extraction and deterministic section matching."""
import re
import fitz

SECTION = r"(?:W\\s*\\d+\\s*[Xx×]\\s*\\d+(?:\\.\\d+)?|UB\\s*\\d+\\s*[Xx×]\\s*\\d+\\s*[Xx×]\\s*\\d+|HSS\\s*\\d+(?:\\.\\d+)?\\s*[Xx×]\\s*\\d+(?:\\.\\d+)?\\s*[Xx×]\\s*\\d+(?:/\\d+|\\.\\d+)?)"
PAIR = re.compile(rf"\\b(?P<mark>[BC]\\d+[A-Z]?)\\s*[:=\\-]?\\s*(?P<section>{SECTION})\\b", re.IGNORECASE)

def normalize_section(value: str) -> str:
    return re.sub(r"\\s+", "", value.upper().replace("×", "X"))

def extract_member_records(pdf_bytes: bytes) -> list[dict]:
    try:
        pdf = fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception as exc:
        raise ValueError("Invalid or unreadable PDF") from exc
    records = []
    with pdf:
        for page_index, page in enumerate(pdf):
            text = page.get_text("text", sort=True)
            for match in PAIR.finditer(text):
                records.append({"mark": match.group("mark").upper(),
                                "section": normalize_section(match.group("section")),
                                "page": page_index + 1})
    return records

def compare_members(design: list[dict], shop: list[dict]) -> list[dict]:
    """Only unique marks on BOTH sides can produce confirmed size mismatches."""
    from collections import Counter
    design_counts = Counter(item["mark"] for item in design)
    shop_counts = Counter(item["mark"] for item in shop)
    design_unique = {m["mark"]: m for m in design if design_counts[m["mark"]] == 1}
    shop_unique = {m["mark"]: m for m in shop if shop_counts[m["mark"]] == 1}
    issues = []
    for mark in sorted(design_unique.keys() & shop_unique.keys()):
        d, s = design_unique[mark], shop_unique[mark]
        if d["section"] != s["section"]:
            issues.append({"rule_id": "MEMBER_SIZE_MISMATCH", "mark": mark,
                           "design_section": d["section"], "shop_section": s["section"],
                           "design_page": d["page"], "shop_page": s["page"],
                           "status": "OPEN",
                           "comment": "Member size differs from engineer-issued drawing. Verify intended substitution."})
    return issues
