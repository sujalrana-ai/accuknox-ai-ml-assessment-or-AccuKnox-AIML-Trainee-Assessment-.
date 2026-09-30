# accuknox-ai-ml-assessment-or-AccuKnox-AIML-Trainee-Assessment-.

# AccuKnox Technical Assessment - AI/ML Trainee

**Candidate:** Rana Sujal  
**Role:** AI/ML Trainee  
**Date:** September 2026  

---

## Overview
This repository contains the complete solutions for the AccuKnox AI/ML Trainee technical screening, spanning data engineering pipelines, data visualization, robust database ingestion, and comprehensive architectural analyses of LLM systems and vector databases.

---

## Section 1: Problem Statement 1 (Practical Engineering)

### 1.1 API Data Retrieval and Storage
- **Implementation:** `problem_1_practical/1_api_data_retrieval.py`
- **Approach:** Fetches live book records from the Open Library REST API, cleans and normalizes JSON payloads, and persists them into a local SQLite database (`books_catalog.db`).
- **Features:**
  - Idempotent storage via SQLite `INSERT OR REPLACE` / `ON CONFLICT DO UPDATE`.
  - Schema definition with typed columns and primary keys.
  - Formatted terminal table output using `tabulate`.

### 1.2 Data Processing and Visualization
- **Implementation:** `problem_1_practical/2_data_visualization.py`
- **Approach:** Pulls simulated test performance data, computes individual student subject averages alongside the overall cohort mean using Pandas, and outputs an annotated bar chart (`student_performance_chart.png`).
- **Features:**
  - Dynamic cohort mean benchmark line.
  - Direct value annotations on bar heads for quick readability.

### 1.3 CSV Data Import to Database
- **Implementation:** `problem_1_practical/3_csv_to_database.py`
- **Approach:** Memory-efficient generator streaming records from CSV into SQLite with batch transactions.
- **Features:**
  - Email format validation via compiled regex (`re.compile`).
  - Graceful skipping of malformed entries with line-by-line logging.
  - Indexed unique email field preventing duplicate insertions.

### 1.4 Code Portfolio Links
- **Most Complex Python Code:**
  - **Repository:** [LangGraph Multi-Tool AI Agent](https://github.com/sujalrana-ai/LangGraph-Based-Multi-Tool-AI
Chatbot/blob/main/chatbot_backend.py) 
  - **Description:** Stateful multi-agent system utilizing LangGraph for conditional execution paths, dynamic tool invocation, contextual memory management, and structured fallback recovery.
- **Most Complex Database Code:**
  - **Repository:** : [https://github.com/sujalrana-ai/Corrective-Retrieval-Augmented
Generation-CRAG-System-using-LangGraph/blob/main/crag_pipeline.py]
  - **Description:** High-throughput database schemas with relational constraints, indexed partitioning for time-series telemetry, complex window functions, and transactional batch loading.

---

## Section 2: Problem Statement 2 (Subjective & Architectural Analysis)

### 2.1 Self-Assessment Matrix

| Domain | Rating | Self-Appraisal & Justification |
| :--- | :---: | :--- |
| **LLMs (Large Language Models)** | **A** | **Can code independently.** Experience building autonomous agent workflows using LangChain and LangGraph, implementing RAG pipelines, prompt orchestration, token-budgeting, and local model inference (Llama, Mistral). |
| **Deep Learning** | **A** | **Can code independently.** Solid practical foundation implementing Neural Networks, CNNs, and Transformer-based architectures using PyTorch and TensorFlow, including loss function formulation and hyperparameter optimization. |
| **Artificial Intelligence** | **A** | **Can code independently.** Strong grounding in state-space search algorithms, heuristic optimization, agentic decision loops, dynamic graph traversal, and heuristic evaluation frameworks. |
| **Machine Learning** | **A** | **Can code independently.** Proficient in supervised and unsupervised pipelines (XGBoost, LightGBM, Random Forests, clustering), feature engineering, data normalization, cross-validation, and production inference deployment. |

---

### 2.2 Key Architectural Components to Create an LLM-Based Chatbot

An enterprise-grade LLM chatbot requires an event-driven, decoupled architecture ensuring low latency, contextual accuracy, and strict safety guardrails.

```text
+-------------------------------------------------------------------------+
|                        1. Ingestion & Security Gateway                  |
|   (Authentication, Rate Limiting, Prompt Injection Defense, PII Masking)|
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                  2. Context Retrieval & State Coordination              |
|  - Short-Term Memory: Redis sliding session buffer                      |
|  - Hybrid Retrieval: Dense Embeddings (HNSW) + Sparse Keyword (BM25)    |
|  - Reranker: Cross-Encoder filtering for semantic precision            |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                       3. Core LLM Inference & Reasoner                  |
|  - Structured Prompt (System Instructions, Domain Context, Few-Shot)    |
|  - Agentic Tool Calling (Querying Databases, REST APIs, Monitoring)     |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                  4. Output Verification & Streaming Gateway             |
|  - Hallucination Validation, Regex Output Schema Checking               |
|  - Real-Time Streaming Output via Server-Sent Events (SSE) / WebSockets |
+-------------------------------------------------------------------------+
