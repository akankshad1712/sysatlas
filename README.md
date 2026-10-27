# ◈ SYSATLAS
### SYSTEMS OBSERVABILITY · RELIABILITY ENGINEERING · SYSTEMS SOFTWARE

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&height=230&color=0:070B16,35:111C3B,70:3730A3,100:06B6D4&text=SYSATLAS&fontColor=F8FAFC&fontSize=68&fontAlignY=38&desc=FROM%20SYSTEM%20SIGNALS%20TO%20ENGINEERING%20INSIGHT&descAlignY=61&descSize=14&animation=fadeIn" width="100%" alt="SysAtlas premium project banner"/>
</p>

<p align="center">
  <strong>Observe the system. Understand the signals. Engineer for reliability.</strong>
</p>

<p align="center">
  <a href="https://github.com/akankshad1712/sysatlas">
    <img src="https://img.shields.io/badge/GITHUB-SOURCE-111827?style=for-the-badge&logo=github&logoColor=white" alt="Source repository"/>
  </a>
  <img src="https://img.shields.io/badge/C-C11-00599C?style=for-the-badge&logo=c&logoColor=white" alt="C"/>
  <img src="https://img.shields.io/badge/PYTHON-APPLICATION-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/FASTAPI-REST%20SERVICES-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/SQLITE-PERSISTENCE-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite"/>
</p>

<p align="center">
  <a href="https://github.com/akankshad1712/sysatlas/tree/main/docs">ENGINEERING DOCUMENTATION</a>
  &nbsp; ◆ &nbsp;
  <a href="https://github.com/akankshad1712/sysatlas/tree/main/portfolio">PORTFOLIO MATERIAL</a>
  &nbsp; ◆ &nbsp;
  <a href="https://www.linkedin.com/in/akanksha-deshmukh-26210b244/">LINKEDIN</a>
</p>

---

## 01 / Executive overview

**SysAtlas is a Linux systems observability and reliability engineering project created by Akanksha Deshmukh.**

It explores how operating-system metrics can be collected through a native C component, passed across a Python application boundary, exposed through REST APIs, persisted in a local database, and evaluated against alert conditions.

The project brings together systems programming, backend development, process management, structured data, automated testing, containerization, and operational documentation in one codebase.

The central engineering question is:

> How can we transform low-level system signals into structured, accessible, and useful operational information?

### At a glance

| Dimension | Project details |
|---|---|
| Project | SysAtlas |
| Author | Akanksha Deshmukh |
| Category | Systems observability and reliability engineering |
| Systems component | C-based Linux collector |
| Application layer | Python and FastAPI |
| Persistence | SQLite |
| Interfaces | HTTP and JSON |
| Quality engineering | Pytest, shell tests, GitHub Actions configuration |
| Deployment configuration | Docker and Docker Compose |
| Documentation | Architecture, security, reliability, testing, and design records |
| Source code | [GitHub repository](https://github.com/akankshad1712/sysatlas) |

## 02 / The visual language

SysAtlas uses a focused, high-contrast visual identity inspired by modern developer platforms and technical product interfaces.

| Design token | Hex color | Intended use |
|---|---|---|
| Midnight | `#070B16` | Primary background |
| Deep Navy | `#111C3B` | Main surfaces |
| Electric Cyan | `#06B6D4` | Data flow and technical highlights |
| Indigo | `#6366F1` | Application and service boundaries |
| Violet | `#8B5CF6` | Architecture accents |
| Mint | `#34D399` | Successful validation and healthy states |
| Cloud White | `#F8FAFC` | Primary text |
| Slate | `#94A3B8` | Secondary information |

The palette establishes a consistent visual direction. GitHub controls the actual page styling, so the colors are expressed through banners, diagrams, badges, and visual assets rather than arbitrary README CSS.

## 03 / The engineering challenge

A monitoring pipeline is more than a metric collector. It needs a reliable way to move information between components, handle invalid output, expose useful interfaces, retain observations, and make failure conditions visible.

SysAtlas organizes these concerns into a sequence of explicit engineering boundaries.

```mermaid
flowchart TD
    A(["LINUX HOST"]) --> B["Read supported system metrics"]
    B --> C["Native C collector"]
    C --> D["Python process adapter"]
    D --> E{"Execution and output valid?"}
    E -->|Yes| F["FastAPI application"]
    E -->|No| G["Error handling and diagnostics"]
    F --> H[("SQLite persistence")]
    F --> I["Alert evaluation"]
    I --> H
    H --> J["Metric and alert retrieval"]
    J --> K["HTTP clients"]
    K --> L(["Operational visibility"])

    classDef host fill:#111827,stroke:#64748B,color:#F8FAFC
    classDef collect fill:#082F49,stroke:#06B6D4,color:#ECFEFF
    classDef service fill:#312E81,stroke:#818CF8,color:#EEF2FF
    classDef data fill:#052E2B,stroke:#34D399,color:#ECFDF5
    classDef error fill:#451A03,stroke:#F59E0B,color:#FFFBEB

    class A,L host
    class B,C,D collect
    class F,I,J,K service
    class H data
    class E,G error
```

*Architecture illustration: the precise runtime behavior should be verified against the implementation.*

### What each stage contributes

| Stage | Input | Responsibility | Output |
|---|---|---|---|
| Collection | Linux system interfaces | Read supported operating-system metrics | Collector output |
| Process boundary | Collector executable | Execute and manage the collection process | Process result |
| Validation | Collector output | Check data before downstream use | Accepted data or error |
| Application | Validated information | Coordinate API operations | Application responses |
| Persistence | Metrics and alert records | Store and retrieve information | Historical records |
| Alert evaluation | Observations and thresholds | Evaluate configured conditions | Alert-related records |
| API access | HTTP requests | Make supported operations accessible | HTTP responses |

## 04 / Architecture at a glance

```mermaid
flowchart LR
    subgraph SYSTEM["01 · SYSTEM LAYER"]
        PROC["Linux /proc"]
        COLLECTOR["C collector"]
        PROC --> COLLECTOR
    end

    subgraph APPLICATION["02 · APPLICATION LAYER"]
        ADAPTER["Python adapter"]
        VALIDATOR["Output validation"]
        API["FastAPI"]
        ADAPTER --> VALIDATOR --> API
    end

    subgraph STORAGE["03 · DATA LAYER"]
        DB[("SQLite")]
        METRICS["Metric history"]
        EVENTS["Alert events"]
        DB --> METRICS
        DB --> EVENTS
    end

    subgraph ACCESS["04 · ACCESS LAYER"]
        CLIENT["HTTP clients"]
        DOCS["Interactive API docs"]
    end

    COLLECTOR --> ADAPTER
    API <--> DB
    CLIENT <--> API
    DOCS -. "documents API" .-> API

    classDef system fill:#082F49,stroke:#06B6D4,color:#ECFEFF
    classDef app fill:#1E1B4B,stroke:#818CF8,color:#EEF2FF
    classDef storage fill:#052E2B,stroke:#34D399,color:#ECFDF5
    classDef access fill:#3B0764,stroke:#C084FC,color:#FAF5FF

    class PROC,COLLECTOR system
    class ADAPTER,VALIDATOR,API app
    class DB,METRICS,EVENTS storage
    class CLIENT,DOCS access
```

### Component ownership

| Component | File | Responsibility |
|---|---|---|
| C collector | `collector/src/collector.c` | Linux-oriented system collection |
| Python adapter | `app/collector.py` | Collector process integration |
| Configuration | `app/config.py` | Application settings |
| API | `app/main.py` | HTTP endpoints and application orchestration |
| Database | `app/db.py` | Persistence and database operations |
| Alert logic | `app/alerts.py` | Alert evaluation |
| Application tests | `tests/test_app.py` | Python application tests |
| Collector tests | `collector/tests/test_collector.sh` | Collector test script |
| CI | `.github/workflows/ci.yml` | Automated workflow configuration |
| Container build | `Dockerfile` | Container image configuration |
| Container services | `docker-compose.yml` | Local service configuration |

## 05 / Feature matrix

| Capability | Engineering value | Implementation |
|---|---|---|
| Native systems collection | Explore low-level Linux interfaces | C collector |
| Process integration | Separate collection from application logic | Python adapter |
| Output validation | Define a boundary between components | Collector integration |
| REST API | Provide structured application access | FastAPI |
| Metric persistence | Retain observations | SQLite |
| Alert evaluation | Apply monitoring conditions | Alert module |
| Automated tests | Detect regressions | Pytest and shell tests |
| CI configuration | Automate selected checks | GitHub Actions |
| Containerization | Define a repeatable runtime environment | Docker |
| Engineering records | Explain technical decisions | `docs/engineering/` |
| Operational guidance | Document reliability and response considerations | `docs/` |

## 06 / API reference

The following routes are present in the project's documented interface. Check `app/main.py` for the authoritative HTTP methods, schemas, parameters, and response codes.

| Endpoint | Method | Intended operation |
|---|---|---|
| `/health` | GET | Application health check |
| `/ready` | GET | Application readiness check |
| `/api/v1/collect` | POST | Trigger metric collection |
| `/api/v1/metrics` | GET | Retrieve metric observations |
| `/api/v1/alerts` | GET | Retrieve alert information |

### Explore the API

When the application is running and FastAPI's documentation routes are enabled:

- Interactive Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

Example PowerShell requests:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
Invoke-RestMethod http://127.0.0.1:8000/api/v1/metrics
Invoke-RestMethod http://127.0.0.1:8000/api/v1/alerts
```

These examples assume the service listens on port `8000`. They do not establish that the application has been started or that the endpoints have been tested in the current environment.

## 07 / Data and persistence model

SQLite is used as the local persistence technology.

```mermaid
flowchart TD
    INPUT["Collected observations"] --> VALIDATE["Application validation"]
    VALIDATE --> STORE[("SQLite database")]
    STORE --> QUERY["Metric query operations"]
    STORE --> ALERTS["Alert evaluation and event operations"]
    QUERY --> RESPONSE["API response"]
    ALERTS --> RESPONSE

    classDef input fill:#082F49,stroke:#06B6D4,color:#ECFEFF
    classDef logic fill:#312E81,stroke:#818CF8,color:#EEF2FF
    classDef database fill:#052E2B,stroke:#34D399,color:#ECFDF5

    class INPUT input
    class VALIDATE,QUERY,ALERTS,RESPONSE logic
    class STORE database
```

| Data concern | Design objective |
|---|---|
| Metric records | Retain observations for retrieval |
| Alert records | Preserve alert-related information |
| Validation | Avoid passing malformed information into downstream processing |
| Database lifecycle | Initialize and access storage consistently |
| Growth | Consider retention, indexing, and query costs |
| Reliability | Handle persistence failures explicitly |

For the actual database schema, column definitions, transaction behavior, and initialization logic, refer to `app/db.py`.

## 08 / Repository structure

```text
sysatlas/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── __init__.py
│   ├── alerts.py
│   ├── collector.py
│   ├── config.py
│   ├── db.py
│   └── main.py
├── collector/
│   ├── src/
│   │   └── collector.c
│   └── tests/
│       └── test_collector.sh
├── docs/
│   ├── engineering/
│   ├── CAPACITY_PLANNING.md
│   ├── ENGINEERING_AUDIT.md
│   ├── ERROR_BUDGET.md
│   ├── INCIDENT_RESPONSE.md
│   ├── QUALITY_REPORT.md
│   ├── SECURITY_ARCHITECTURE.md
│   ├── SRE_PLAYBOOK.md
│   ├── TECHNICAL_DEBT.md
│   ├── TEST_MATRIX.md
│   └── THREAT_MODEL.md
├── portfolio/
│   ├── ARCHITECTURE_DEFENSE.md
│   ├── DEMO_SCRIPT.md
│   ├── GITHUB_ABOUT.md
│   ├── INTERVIEW_QA.md
│   ├── PROJECT_SUMMARY.md
│   ├── RESUME_BULLETS.md
│   └── TECHNICAL_WALKTHROUGH.md
├── tests/
│   └── test_app.py
├── .env.example
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── Dockerfile
├── docker-compose.yml
├── LICENSE
├── Makefile
├── README.md
├── requirements.txt
└── SECURITY.md
```

## 09 / Run locally

### Prerequisites

- Git
- A compatible Python installation
- Linux or WSL2 for the native Linux collector
- A C compiler for building and testing the collector
- Docker and Docker Compose for the containerized workflow

### Clone the repository

```bash
git clone https://github.com/akankshad1712/sysatlas.git
cd sysatlas
```

### Install Python dependencies

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Linux / WSL2**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Run application tests

```bash
python -m pytest -q
```

### Run collector checks

From a compatible Linux environment:

```bash
sh collector/tests/test_collector.sh
```

### Run with Docker Compose

```bash
docker compose up --build
```

To stop the services:

```bash
docker compose down
```

**Important:** Confirm the build targets, startup commands, and service configuration in the repository before relying on these instructions. Running Python under Windows does not itself provide Linux `/proc` interfaces.

## 10 / Reliability and failure analysis

A useful observability system needs to handle failure, not only successful collection.

```mermaid
flowchart TD
    START["Collection request"] --> RUN["Execute collector"]
    RUN --> RESULT{"Process succeeded?"}
    RESULT -->|No| PROCESS_ERROR["Handle execution failure"]
    RESULT -->|Yes| FORMAT{"Output valid?"}
    FORMAT -->|No| DATA_ERROR["Reject invalid output"]
    FORMAT -->|Yes| PERSIST["Persist observations"]
    PERSIST --> DB_RESULT{"Persistence succeeded?"}
    DB_RESULT -->|No| STORAGE_ERROR["Report storage failure"]
    DB_RESULT -->|Yes| EVALUATE["Evaluate alert conditions"]
    EVALUATE --> DONE["Return appropriate result"]

    classDef decision fill:#312E81,stroke:#818CF8,color:#EEF2FF
    classDef success fill:#052E2B,stroke:#34D399,color:#ECFDF5
    classDef failure fill:#451A03,stroke:#F59E0B,color:#FFFBEB

    class RESULT,FORMAT,DB_RESULT decision
    class PERSIST,EVALUATE,DONE success
    class PROCESS_ERROR,DATA_ERROR,STORAGE_ERROR failure
```

| Failure mode | Expected engineering concern |
|---|---|
| Collector timeout | Bound execution time |
| Non-zero process exit | Capture and surface diagnostics |
| Malformed output | Validate before processing |
| Database failure | Handle errors and preserve consistency |
| Alert threshold exceeded | Evaluate configured monitoring rules |
| API request invalid | Return appropriate HTTP behavior |
| CI check fails | Diagnose the failing stage before merging |

The diagram describes a recommended failure-analysis model. Verify that each branch is implemented and tested before presenting it as a guaranteed runtime behavior.

## 11 / Testing and CI/CD

| Quality layer | Repository location | Verification goal |
|---|---|---|
| Python tests | `tests/test_app.py` | Exercise application behavior |
| Collector tests | `collector/tests/test_collector.sh` | Check collector behavior |
| Dependency installation | `requirements.txt` | Reproduce Python environment setup |
| Container build | `Dockerfile` | Validate configured image construction |
| Service configuration | `docker-compose.yml` | Validate the container workflow |
| CI automation | `.github/workflows/ci.yml` | Execute the checks configured in CI |

The CI workflow should be treated as evidence only for the commands it actually executes. A successful workflow is not, by itself, a production-readiness certification.

## 12 / Security architecture

Security considerations for this project include:

- Keep real secrets out of source control.
- Use `.env.example` for placeholders, never live credentials.
- Avoid shell-based command construction where direct subprocess execution is appropriate.
- Bound process time and output.
- Validate data crossing component boundaries.
- Review API exposure before making the service publicly accessible.
- Check container privileges and filesystem access.
- Review dependency versions and database handling.

Related documentation:

| Document | Focus |
|---|---|
| `SECURITY.md` | Project security guidance |
| `docs/THREAT_MODEL.md` | Threat analysis |
| `docs/SECURITY_ARCHITECTURE.md` | Security design |
| `docs/engineering/SECURITY_REVIEW.md` | Security review material |
| `docs/engineering/RISK_REGISTER.md` | Risk tracking |

## 13 / Engineering decision records

The engineering documentation is intended to make design choices understandable and reviewable.

| Document | Engineering question |
|---|---|
| `docs/engineering/ADR-001-local-sqlite.md` | Why use local SQLite persistence? |
| `docs/engineering/ADR-002-c-collector.md` | Why use a native C collector? |
| `docs/engineering/SYSTEM_DESIGN.md` | How is the system organized? |
| `docs/engineering/ARCHITECTURE_EVOLUTION.md` | How might the architecture evolve? |
| `docs/engineering/SCALABILITY_ANALYSIS.md` | What limits scaling? |
| `docs/engineering/PERFORMANCE_REPORT.md` | What performance evidence exists? |
| `docs/engineering/TECHNICAL_DEBT.md` | What trade-offs or limitations remain? |
| `docs/engineering/OPERABILITY_REVIEW.md` | How should operational behavior be reviewed? |

Keep measured results, proposed improvements, and assumptions clearly distinguished in these documents.

## 14 / Development roadmap

- [ ] Verify the documented startup process from a clean environment.
- [ ] Publish passing application and collector test results.
- [ ] Add a genuine screenshot of the running dashboard, if available.
- [ ] Document concrete request and response examples.
- [ ] Measure collector latency and persistence behavior.
- [ ] Add reproducible performance tests.
- [ ] Validate container security and resource limits.
- [ ] Establish a clear retention strategy for stored metrics.
- [ ] Document known limitations and future architectural options.

These are improvement opportunities, not claims that the features are already complete.

## 15 / About the author

<p align="center">
  <strong>AKANKSHA DESHMUKH</strong>
  <br/>
  Software Engineer · Computer Engineering
  <br/><br/>
  <a href="https://www.linkedin.com/in/akanksha-deshmukh-26210b244/">
    <img src="https://img.shields.io/badge/LINKEDIN-LET'S%20CONNECT-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="Akanksha Deshmukh on LinkedIn"/>
  </a>
  <a href="https://github.com/akankshad1712">
    <img src="https://img.shields.io/badge/GITHUB-EXPLORE%20MY%20WORK-111827?style=for-the-badge&logo=github&logoColor=white" alt="Akanksha Deshmukh on GitHub"/>
  </a>
</p>

SysAtlas is my engineering portfolio project for exploring systems programming, backend APIs, persistence, automated testing, and reliability-focused design.

My focus is on building understandable systems, documenting technical trade-offs, validating behavior, and continuously improving engineering quality.

## 16 / Explore the project

| Resource | Destination |
|---|---|
| Source code | [SysAtlas repository](https://github.com/akankshad1712/sysatlas) |
| Engineering documentation | [Documentation directory](https://github.com/akankshad1712/sysatlas/tree/main/docs) |
| Portfolio materials | [Portfolio directory](https://github.com/akankshad1712/sysatlas/tree/main/portfolio) |
| Professional profile | [Akanksha Deshmukh on LinkedIn](https://www.linkedin.com/in/akanksha-deshmukh-26210b244/) |

---

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&height=130&section=footer&color=0:06B6D4,50:3730A3,100:070B16" width="100%" alt="SysAtlas footer"/>
  <strong>SYSATLAS · ENGINEERED WITH INTENT</strong>
  <br/>
  <sub>Observe deeply. Design deliberately. Build reliably.</sub>
</p>
