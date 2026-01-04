# GFGBQ-Team-sourcerer
Repository for sourcerer - Vibe Coding Hackathon

# 📌 Problem Statement

Large-scale e-commerce and food delivery platforms like Swiggy, Amazon, and Flipkart face high operational costs and inconsistencies in Tier-1 customer support. Human agents handle repetitive queries such as order delays, wrong items, and refund requests, which leads to slow response times, refund abuse, and scalability issues.
The problem is to design a **safe, scalable, and intelligent system** that can autonomously handle Tier-1 customer support while enforcing policies, preventing misuse, and escalating only when necessary.

---

# 🚀 Project Name

**Agentic AI Customer Support System**

---

# 👥 Team Name

**Team Sourcerer**
*(You can change this if needed)*

---

# 🌐 Deployed Link (Optional)

*Not deployed yet (local/demo-based project)*
*(Optional: Add link if deployed later)*

---

# 🎥 2-Minute Demonstration Video Link

*To be added*
*(Place your Google Drive / YouTube demo link here)*

---

# 📊 PPT Link

*To be added*
*(Place your pitch deck link here)*

---

---

## 📖 Project Overview

This project is an **AI-Powered Autonomous Customer Support System** built using an **agentic multi-agent architecture**.
Instead of a single chatbot, the system consists of multiple specialized AI agents, each responsible for a specific decision such as intent detection, conversation handling, governance enforcement, and refund approval.

The system is designed to **replace Tier-1 human support**, reduce operational costs, prevent refund abuse, and ensure policy-compliant customer interactions.

Key highlights:

* True **agent-based architecture**
* Governance & jailbreak protection
* Rule-based automated refunds
* Safe escalation to humans
* Production-ready design using Supabase (PostgreSQL)

---

## 🧠 System Architecture & Agents

### 1️⃣ Intent Classification Agent

* Identifies user intent (order delay, wrong item, refund request, etc.)
* Extracts key entities like order ID and issue type
* Routes requests to the appropriate downstream agents

### 2️⃣ Conversation Agent

* Handles customer interaction
* Maintains chat context
* Generates polite, brand-safe responses
* Never directly promises refunds

### 3️⃣ Governance / Guardrail Agent

* Reviews every outgoing response
* Detects:

  * Policy violations
  * Prompt injection / jailbreak attempts
  * Unsafe or unprofessional language
* Acts as the final approval gate before responding to the user

### 4️⃣ Refund Decision Agent

* Uses rule-based logic (YAML-driven)
* Considers order value, delay, and policies
* Decides whether to:

  * Approve refund
  * Reject request
  * Escalate to human

---

## 🛠️ Tech Stack

**Backend**

* Python
* psycopg2
* Pydantic / PydanticAI (for structured agent outputs)

**AI**

* Gemini LLM
* Agent-based orchestration

**Database**

* Supabase (PostgreSQL)
* Secure access via environment variables

**Security**

* SSL-enforced DB connection
* Parameterized SQL queries
* No hardcoded credentials
* Jailbreak tracking via governance agent

---

## ⚙️ Setup & Installation Instructions

### 1️⃣ Clone the Repository

```bash
git clone <repository-url>
cd sample-customer-support-agent-e2e-1
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres:admin1234@db.sfegtvtsgvxbgkzlaibm.supabase.co:5432/postgres?sslmode=require
```

### 5️⃣ Run the Application

```bash
python main.py
```

---

## ▶️ Usage Instructions

1. Run the application
2. Enter a **User ID** when prompted
3. Interact as a customer by typing messages such as:

   * “My order is delayed”
   * “I received the wrong item”
   * “I want a refund”
4. The system:

   * Classifies intent
   * Generates a response
   * Applies governance checks
   * Makes refund decisions if applicable

---

## 🔐 Security & Governance Features

* Environment-based secret management
* No credentials stored in source code
* Jailbreak detection and tracking
* Policy-driven responses
* Safe refusal and escalation mechanisms

---

## 📈 Future Scope

* Fraud & Risk Detection Agent
* SLA Verification Agent
* Sentiment Analysis Agent
* Human Escalation Agent
* Analytics & Audit Dashboard
* Frontend chat UI (React)

---

## 🖼️ Relevant Screenshots

*(Add screenshots of:)*

* Chat interaction
* Supabase database tables
* Agent flow (diagram)

---

## 🏆 Why This Project Stands Out

* Demonstrates **true agentic AI**, not a simple chatbot
* Designed for **real-world deployment**
* Emphasizes **governance, safety, and compliance**
* Easily extensible with new agents
* Clear business impact and scalability