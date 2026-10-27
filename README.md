# SteelShop — Steel Shop Drawing Review MVP

Engineering-first comparison of structural steel member schedules in engineer-issued and fabricator PDFs.

## Scope (Version 1)
- Create projects and upload design/shop PDFs
- Extract PDF text and schedule-like member rows
- Normalize steel section names (W, HSS, UB)
- Compare only verified member marks and flag section mismatches
- Display review findings with source page references

**Engineering safeguard:** This tool assists review; it does not approve substitutions or replace a licensed engineer's review. Unmatched or ambiguous members require manual checking.

## Quickstart
```bash
docker compose up --build
```
- Frontend: http://localhost:3000
- API docs: http://localhost:8000/docs

See [architecture](docs/architecture.md), [engineering rules](docs/engineering-rules.md), and [roadmap](docs/roadmap.md).

This first scaffold runs locally. PostgreSQL and S3 adapters are planned for the next increment; the initial API uses in-memory demo project records and local PDF processing. Uploaded PDF bytes are not persisted in this scaffold.
