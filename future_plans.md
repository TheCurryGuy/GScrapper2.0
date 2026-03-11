# Future Plans

## 🔐 Authentication & Security
- **API Key Authentication** — Require API keys for accessing endpoints to prevent abuse and track usage per user
- **OAuth2 / JWT Login** — Add user accounts with token-based authentication so researchers can save search history
- **Rate Limiting (per-user)** — Implement SlowAPI or a Redis-backed rate limiter to throttle requests per IP/user

---

## 🗄️ Database & Caching
- **Database Integration** — Add PostgreSQL or MongoDB to store search results, user profiles, and saved publications
- **Redis Caching** — Cache search results using Redis to avoid redundant API calls and improve response times (config already exists)
- **Search History** — Let users view and revisit their past searches without re-querying external APIs

---

## 📚 Additional Academic Sources
- **Semantic Scholar API** — Integrate Semantic Scholar for AI/ML-focused papers with rich citation graphs
- **ORCID API** — Directly query ORCID profiles to fetch publications linked to a researcher's ORCID ID
- **PubMed / Europe PMC** — Add biomedical literature from PubMed for medical/life sciences researchers
- **DBLP** — Integrate DBLP for comprehensive computer science publication data
- **Scopus / Web of Science** — Add support for these premium databases (requires institutional API keys)
- **arXiv API** — Pull preprints from arXiv for cutting-edge research not yet formally published

---

## 📊 Advanced Analytics & Visualization
- **Citation Trend Charts** — Show year-over-year citation growth with interactive line/bar charts (Chart.js or D3.js)
- **Co-Author Network Graph** — Visualize collaboration networks between authors
- **Publication Timeline** — Interactive timeline showing when each paper was published
- **Topic/Keyword Analysis** — Word cloud or topic clustering from paper titles and abstracts
- **Source Comparison** — Side-by-side comparison of what each data source returns for the same author
- **Research Impact Dashboard** — A comprehensive dashboard with citation velocity, field-weighted metrics, etc.

---

## 🔍 Search Enhancements
- **Fuzzy Name Matching** — Handle name variations (initials, missing middle names, transliterations)
- **Multi-Author Search** — Search for publications by multiple co-authors simultaneously
- **Full-Text / Keyword Search** — Search by paper title, abstract keywords, or DOI directly
- **Search Filters** — Filter by year range, publication type, minimum citations, venue, etc.
- **Auto-Suggest Author IDs** — When entering a name, auto-suggest matching Google Scholar author IDs
- **Batch Search** — Upload a CSV of author names/emails and get aggregated results for all

---

## 📥 Export & Reporting
- **BibTeX / RIS Export** — Export publications in standard citation formats for use in LaTeX, Zotero, Mendeley, etc.
- **PDF Report Generation** — Generate a formatted PDF report of an author's publication profile
- **Excel Export** — Add `.xlsx` export option alongside the existing CSV
- **Email Reports** — Schedule and email periodic publication reports to researchers

---

## 🎨 Frontend Improvements
- **Dark Mode** — Add a dark theme toggle for comfortable reading
- **Responsive Mobile Design** — Optimize the UI for smartphones and tablets
- **Pagination** — Add pagination for large result sets instead of loading all at once
- **Sort Options** — Let users sort publications by year, citations, title, or source
- **Abstract Preview** — Expandable abstract sections in publication cards
- **Author Profile Photos** — Display thumbnails from Google Scholar when available
- **Loading Skeleton Screens** — Replace the spinner with skeleton loading animations for better UX
- **Bookmark / Favorite Papers** — Let users star individual publications for later reference

---

## ⚙️ Backend & Infrastructure
- **Background Task Queue** — Use Celery or FastAPI BackgroundTasks for long-running multi-source searches
- **WebSocket Progress Updates** — Send real-time search progress to the frontend as each source responds
- **API Versioning (v2)** — Design a v2 API with improved response models and new features
- **Docker Containerization** — Add Dockerfile and docker-compose for easy deployment
- **CI/CD Pipeline** — Set up GitHub Actions for automated testing, linting, and deployment
- **Unit & Integration Tests** — Add pytest test suite covering all services, endpoints, and utils
- **Health Check Improvements** — Actually ping each external API in the health check endpoint
- **Logging Improvements** — Add structured JSON logging and log rotation

---

## 🌐 Deployment & Scalability
- **Cloud Deployment Guides** — Add docs for deploying on AWS EC2, Google Cloud Run, or Railway
- **NGINX Reverse Proxy Config** — Production-ready NGINX config with SSL/HTTPS
- **Horizontal Scaling** — Support multiple workers with shared Redis cache
- **CDN for Static Files** — Serve the frontend via a CDN for faster global access

---

## 📝 Documentation & Developer Experience
- **Swagger UI Customization** — Customize the auto-generated FastAPI docs with examples and descriptions
- **Postman Collection** — Provide a ready-to-use Postman collection for all API endpoints
- **Contributing Guide** — Add `CONTRIBUTING.md` with code style, PR process, and development setup
- **Changelog** — Maintain a `CHANGELOG.md` to track version history
