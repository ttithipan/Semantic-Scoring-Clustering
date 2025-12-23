# Local AI Support Consolidator 🛡️

A **privacy‑first, zero‑cost microservice** that automatically consolidates large volumes of support tickets using **local semantic search** and **density‑based clustering**.

**No API keys. No cloud fees. Runs entirely on your local machine.**

---

## ⚡ Features

### 🔹 Semantic Grouping

Uses **SentenceTransformers** (`all-mpnet-base-v2`) to understand that tickets like *"cant sign in"* and *"I cannot login"* describe the same issue.

### 🔹 Density Clustering

Uses **DBSCAN** to automatically detect ticket clusters **without pre‑defining the number of groups**.

### 🔹 Heuristic Scoring

Automatically ranks tickets within each cluster to identify a **"Champion" ticket** — the one with the highest technical value and clarity.

### 🔹 High Performance

Optimized for **CUDA (GPU) acceleration** when available, with automatic fallback to CPU.

---

## 🛠️ Tech Stack

* **Framework:** FastAPI + Uvicorn
* **ML Engine:** PyTorch, SentenceTransformers
* **Clustering Algorithm:** Scikit‑Learn (DBSCAN)

---

## 📦 Installation

### 1️⃣ Clone the Repository

Clone the repository, or create a new project folder and copy the files.

### 2️⃣ Set Up a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Linux / macOS)
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note:** For GPU acceleration, ensure you have the correct **PyTorch CUDA build** installed for your system.

---

## 🚀 Running the Server

Start the API server with hot‑reloading enabled:

```bash
uvicorn main:app --reload
```

* Server URL: `http://127.0.0.1:8000`
* Interactive API Docs: `http://127.0.0.1:8000/docs`

---

## 🔌 API Usage

### 📍 Endpoint: `POST /cluster`

**Request Body (JSON):**

```json
{
  "tickets": [
    "I cannot login",
    "Login button broken",
    "Error 403: Access Denied when clicking login",
    "cant sign in",
    "Server is down",
    "Api is not responding",
    "500 Internal Server Error at /api/v1/checkout",
    "IT BROKE HELP",
    "The printer is out of paper"
  ]
}
```

**Response (JSON):**

```json
{
  "0": [0, 1, 2, 3, 4],
  "1": [5, 6],
  "-1": [7, 8]
}
```

---

### 📍 Endpoint: `POST /score`

**Request Body (JSON):**

```json
{
  "tickets": [
    "I cannot login",
    "Login button broken",
    "Error 403: Access Denied when clicking login",
    "cant sign in",
    "Server is down",
    "Api is not responding",
    "500 Internal Server Error at /api/v1/checkout",
    "IT BROKE HELP",
    "The printer is out of paper"
  ]
}
```

**Response (JSON):**

```json
[-9, -9, 19, -9, -9, 2, 29, -9, 2]
```

---

## ⚙️ Configuration

You can adjust clustering sensitivity by modifying the `eps` parameter inside:

```python
cluster_tickets_by_semantics()
```

located in `server.py`.
