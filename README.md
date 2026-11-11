# Intelligent Continuous Compliance & Evidence Automation Platform

## Overview

The **Intelligent Continuous Compliance & Evidence Automation Platform** is a backend-focused cybersecurity compliance project designed to automate the collection of technical evidence, evaluate compliance controls continuously, detect configuration drift, generate findings, and maintain a complete audit history.

Traditional compliance processes often rely on spreadsheets, manually collected evidence, and periodic audits. This project explores a more automated approach where evidence is collected from connected systems and continuously evaluated against defined compliance controls.

The platform combines **Backend Engineering, Automation, AI/ML, Semantic Retrieval, and LLM-assisted analysis**.

---

## The Problem

Organizations often manage cybersecurity and IT compliance through:

- Spreadsheets
- Manual evidence collection
- Periodic compliance audits
- Disconnected systems
- Manual control mapping

This can result in:

- Outdated evidence
- Delayed detection of configuration changes
- Manual compliance checks
- Difficulty tracing why a control passed or failed
- Limited auditability
- Difficulty processing unstructured evidence

This project aims to address these problems through continuous evidence collection and automated compliance evaluation.

---

# Core Design Principle

The platform uses different evaluation mechanisms depending on the type of evidence.

### Structured and machine-verifiable evidence

Objective technical configurations are evaluated automatically using deterministic rules.

Example:

```text
Branch Protection = Disabled
Required = Enabled

Result → FAIL
```

### Unstructured or semantic evidence

AI/ML techniques are used to understand the meaning of evidence and identify relevant compliance controls.

Example:

```text
Evidence Text
      ↓
Embeddings
      ↓
Vector Search
      ↓
Relevant Controls
      ↓
Confidence Score
      ↓
Human Review when required
```

The goal is to use AI where semantic understanding is valuable while maintaining traceability and reliability for objective technical checks.

---

# System Architecture

The platform is organized around four main engines.

## 1. Compliance Automation Engine

Responsible for:

- Collecting technical evidence
- Normalizing evidence
- Evaluating deterministic compliance rules
- Generating PASS or FAIL results
- Detecting compliance drift
- Creating findings
- Maintaining evaluation history

Example flow:

```text
GitHub Repository
        ↓
Evidence Collection
        ↓
Evidence Normalization
        ↓
Compliance Rule Engine
        ↓
PASS / FAIL / REVIEW
        ↓
Drift Detection
        ↓
Finding
        ↓
Audit History
```

---

## 2. Evidence Intelligence Engine

Responsible for understanding and mapping unstructured evidence to relevant compliance controls.

Pipeline:

```text
Evidence Text
      ↓
Text Processing
      ↓
Embeddings
      ↓
Vector Search
      ↓
Top-K Candidate Controls
      ↓
Optional Reranking
      ↓
Confidence Score
      ↓
Suggested Mapping
      ↓
Human Approval / Rejection
```

The system will evaluate retrieval quality using metrics such as:

- Precision@K
- Recall@K
- MRR
- Hit Rate@K

---

## 3. Compliance Knowledge Graph

The platform models relationships between:

- Frameworks
- Controls
- Assets
- Evidence
- Evaluations
- Findings
- Remediation actions

Example relationships:

```text
Framework
    ↓ HAS_CONTROL
Control
    ↓ REQUIRES
Evidence

Asset
    ↓ PRODUCES
Evidence

Evidence
    ↓ SUPPORTS
Control

Finding
    ↓ AFFECTS
Asset

Finding
    ↓ VIOLATES
Control
```

The initial implementation uses PostgreSQL relational tables to represent these relationships.

---

## 4. Compliance Assistant

The Compliance Assistant provides human-readable explanations using verified system data.

Example question:

> Why is `payments-api` currently non-compliant?

The backend retrieves:

- Asset information
- Latest evidence
- Failed control
- Rule evaluation
- Previous evaluation
- Current evaluation
- Related findings
- Relevant relationships

This verified context is then provided to an LLM to generate:

- Human-readable explanations
- Evidence summaries
- Remediation suggestions
- Related controls to inspect

The assistant does not modify historical evidence or evaluations.

---

# Key Features

## Authentication and Authorization

- JWT-based authentication
- Role-Based Access Control (RBAC)

Roles include:

- Admin
- Auditor
- Control Owner

---

## Compliance Framework Management

The platform supports:

- Compliance frameworks
- Controls
- Control requirements
- Rule definitions
- Rule versioning

The project focuses on a manageable subset of controls rather than attempting to implement an entire framework.

---

## Asset Management

Assets may include:

- GitHub repositories
- Applications
- Servers
- Databases
- User accounts

Each asset can have associated evidence, compliance evaluations, and findings.

---

## Automated Evidence Collection

Evidence collection runs asynchronously.

Example:

```text
Scheduler
    ↓
Background Job
    ↓
Connector
    ↓
Raw Evidence
    ↓
Normalization
    ↓
Database
```

The first real integration is designed around GitHub.

Potential evidence includes:

- Repository visibility
- Branch protection
- Repository configuration
- Security settings
- Collaborator permissions

---

## Continuous Compliance Evaluation

Controls are automatically re-evaluated when relevant evidence changes.

Example:

```text
Monday:
Branch Protection = Enabled
Result = PASS

Thursday:
Branch Protection = Disabled
Result = FAIL
```

The system identifies this transition as:

```text
PASS → FAIL
```

This is recorded as a compliance drift event.

---

## Findings

When a control fails, the system can create a finding containing:

- Affected asset
- Failed control
- Supporting evidence
- Severity
- Timestamp
- Status
- Recommended remediation

---

## Audit Trail

The platform maintains historical records of important events, including:

- Evidence collection
- Compliance evaluations
- Rule versions
- Previous and current results
- Compliance drift
- Finding creation
- Human review decisions

---

# Technology Stack

## Backend

- Python
- FastAPI

## Database

- PostgreSQL

## Authentication

- JWT
- Role-Based Access Control

## Background Processing

- Celery

## Queue and Cache

- Redis

## AI/ML

- Sentence Transformers
- Embeddings
- Semantic Retrieval

## Vector Search

- pgvector

## LLM Integration

The system is designed with a provider abstraction that can support different LLM providers, including:

- OpenAI
- Gemini
- Claude
- Local models

## Frontend

- React

## Testing

- pytest

## Containerization

- Docker

---

# Project Structure

The backend is organized into modules such as:

```text
app/
│
├── api/
│   └── v1/
│
├── models/
├── repositories/
├── services/
│
├── auth/
├── assets/
├── frameworks/
├── controls/
├── evidence/
├── evaluations/
├── findings/
├── audit/
├── jobs/
│
├── db/
└── core/

tests/
```

The project follows separation of responsibilities between:

```text
API Layer
    ↓
Service Layer
    ↓
Repository / Data Access Layer
    ↓
Database
```

---

# Development Roadmap

## Phase 1: Foundation

- Authentication
- JWT
- RBAC
- Database design
- Asset management
- Framework management
- Basic project structure

### Goal

Create a secure backend foundation for the platform.

---

## Phase 2: Compliance Automation Engine

- Evidence collection
- Connector architecture
- Rule engine
- Compliance evaluation
- Drift detection
- Findings
- Audit history

### Goal

Automatically collect technical evidence and generate compliance results.

---

## Phase 3: Evidence Intelligence and Knowledge Relationships

- Embeddings
- Vector search
- Evidence-to-control mapping
- Confidence scoring
- Human review
- Relationship modelling
- ML evaluation

### Goal

Automatically identify relevant compliance controls from unstructured evidence.

---

## Phase 4: Compliance Assistant

- Verified context retrieval
- LLM provider abstraction
- Grounded explanations
- Remediation suggestions

### Goal

Provide understandable explanations for compliance results.

---

## Phase 5: Dashboard, Testing and Documentation

- React dashboard
- Integration testing
- Security improvements
- Docker configuration
- Documentation
- Deployment

### Goal

Deliver a complete end-to-end demonstration of the platform.

---

# Example End-to-End Flow

Consider a GitHub repository called:

```text
payments-api
```

### Step 1: Evidence Collection

The GitHub connector collects repository configuration.

```text
Branch Protection = Disabled
```

### Step 2: Evidence Normalization

The external GitHub data is converted into a common internal evidence format.

### Step 3: Rule Evaluation

The compliance rule requires:

```text
Administrative repositories must have branch protection enabled.
```

The rule engine evaluates:

```text
Expected: Enabled
Observed: Disabled

Result: FAIL
```

### Step 4: Finding

A compliance finding is created.

### Step 5: Drift Detection

If the previous evaluation was:

```text
PASS
```

and the new evaluation is:

```text
FAIL
```

the system records:

```text
PASS → FAIL
```

as compliance drift.

### Step 6: AI-Assisted Explanation

The Compliance Assistant can explain:

- Why the control failed
- Which evidence caused the failure
- What changed
- Recommended remediation steps

---

# AI/ML Evaluation

The Evidence Intelligence Engine will be evaluated using a labelled dataset.

Each example contains:

```text
Evidence
    ↓
Correct Compliance Control(s)
```

The system will compare retrieval approaches and evaluate performance using:

- Precision@K
- Recall@K
- MRR
- Hit Rate@K

This ensures that the AI/ML component is measured using quantitative results rather than subjective demonstrations.

---

# Security Considerations

The platform is designed with attention to:

- JWT security
- Role-Based Access Control
- Secure connector credentials
- Secrets management
- Input validation
- API authorization
- Auditability
- Idempotency for background jobs
- Rate limiting
- Protection against duplicate processing
- Prompt injection considerations for AI components

Sensitive credentials and API keys should never be committed to the repository.

---

# Project Goals

This project is being developed as a backend-heavy portfolio project focused on learning and demonstrating:

- Backend architecture
- API development
- Database design
- Asynchronous processing
- Background workers
- Compliance automation
- Evidence normalization
- AI/ML semantic retrieval
- Vector databases
- LLM integration
- Auditability
- Testing
- Docker and deployment

The focus is on building a smaller number of features deeply and being able to explain the complete system architecture and implementation decisions.

---

# Current Status

**Under Active Development**

The project is being developed incrementally.

Current development focuses on building the backend foundation before implementing the complete compliance automation and AI/ML pipelines.

---

# Future Enhancements

Potential future enhancements include:

- Additional external connectors
- Advanced reranking
- More compliance frameworks
- GitHub webhook-based evidence collection
- Automated remediation workflows
- Advanced relationship visualization
- Additional AI models
- Cloud deployment
- Advanced monitoring and observability


## License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.
