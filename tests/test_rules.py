import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"backend"))
from app.services import normalize_section, compare_members

def test_normalize():
    assert normalize_section("W 18 × 35") == "W18X35"

def test_mismatch():
    d=[{"mark":"B21","section":"W18X35","page":1}]
    s=[{"mark":"B21","section":"W16X31","page":2}]
    assert compare_members(d,s)[0]["rule_id"]=="MEMBER_SIZE_MISMATCH"

def test_ambiguous_mark_not_confirmed():
    d=[{"mark":"B21","section":"W18X35","page":1},{"mark":"B21","section":"W18X35","page":2}]
    s=[{"mark":"B21","section":"W16X31","page":1}]
    assert compare_members(d,s)==[]
