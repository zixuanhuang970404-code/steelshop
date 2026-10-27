# MVP architecture

Browser (Next.js/TypeScript/Tailwind) → FastAPI → PyMuPDF text parser → normalized member records → deterministic member matcher → findings list.

The initial vertical slice is deliberately local/stateless. Next work: SQLAlchemy + Alembic and PostgreSQL persistence, private S3/Azure storage, background ingestion worker, pdfplumber schedule-table parser, PDF.js evidence viewer, and review audit records.

Do not deploy this scaffold to a public environment with sensitive drawings. Add authentication, authorization, upload scanning and encrypted storage before production use. GitHub Pages cannot host the Python API.
