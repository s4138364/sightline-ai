# Sightline AI

Sightline AI is a full-stack multimodal AI prototype that analyzes user-provided images and intent tags to generate alignment insights.

The project demonstrates:
- Clean backend architecture
- Image + text inference pipelines
- Real API consumption from a frontend
- Validation, logging, and error handling

---

## Tech Stack

- **Backend:** FastAPI (Python)
- **Frontend:** Vanilla HTML + JavaScript
- **Inference:** Modular service layer (vision + text)
- **Config:** Environment-based settings

---

## Project Structure
sightline-ai/
├── backend/
│ ├── main.py
│ ├── config.py
│ ├── services/
│ └── init.py
├── frontend/
│ └── index.html
├── requirements.txt
└── README.md

---

## Running the Backend

1. Create and activate a virtual environment (recommended)

```bash
python -m venv venv
venv\Scripts\activate  # Windows

```md
---

## Architecture Overview

Sightline AI is designed with a layered architecture:

Frontend (HTML + JS)
↓
FastAPI API Layer
↓
Service Layer (business logic)
↓
Inference Layer (vision + text)

markdown
Copy code

### Layer Responsibilities

**Frontend**
- Collects user input
- Sends requests to API
- Displays results and errors

**API Layer**
- Validates inputs
- Handles HTTP concerns
- Returns predictable responses

**Service Layer**
- Orchestrates business logic
- Combines model outputs
- Generates insights

**Inference Layer**
- Isolated model logic
- Easy to replace or upgrade models
- No web dependencies

### Benefits
- Easy testing
- Clear ownership
- Model swapping without frontend changes
- Scales to production patterns