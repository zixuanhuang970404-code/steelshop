# Engineering rules

1. Compare only verified same-member identifiers. The first implementation requires each mark to occur exactly once on each document set.
2. Ignore whitespace, capitalization, and multiplication glyph formatting in section designations.
3. If normalized sizes differ, generate MEMBER_SIZE_MISMATCH with source page evidence.
4. Repeated marks, unidentified levels, scanned PDFs, and unparsed schedules require manual review; never declare a PASS based solely on absence of findings.
5. A mismatch is a review finding, not a structural determination that a proposed substitution is unacceptable.
