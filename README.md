# ◈ LAURA — AI Study Planning Agent

> *Learning Assistant, Unlimited Research Agent — give her a subject, she searches, reads, and builds your study plan*

🌐 **Live Demo** → [Try LAURA](https://huggingface.co/spaces/Maymuunah14/LAURA)

---

## ✨ Overview

LAURA is an autonomous AI agent that goes far beyond a regular chatbot. Give her any subject, a timeframe, and your experience level — she will **search the live internet, read real articles, evaluate their relevance, and generate a grounded, day-by-day study plan** citing the actual resources she found.

Unlike a chatbot that only answers from memory, or a RAG app that only reads documents you upload, LAURA **takes autonomous multi-step actions** to accomplish a goal — deciding for herself what to search, what to read, and when she has enough information to build your plan.

---

## 🤖 What Makes LAURA an Agent (Not Just a Chatbot)

| | Regular Chatbot | RAG App (like ILMA) | Agent (LAURA) |
|---|---|---|---|
| Answers questions | ✅ | ✅ | ✅ |
| Reads documents | ❌ | ✅ (uploaded files) | ✅ (live web pages) |
| Searches the internet | ❌ | ❌ | ✅ |
| Takes multi-step actions | ❌ | ❌ | ✅ |
| Works autonomously toward a goal | ❌ | ❌ | ✅ |

---

## 🚀 Live Demo

👉 **[https://huggingface.co/spaces/Maymuunah14/LAURA](https://huggingface.co/spaces/Maymuunah14/LAURA)**

Enter any subject — "Machine Learning", "Web Development", "Fine-tuning LLMs" — pick a duration and your level, and watch LAURA work.

---

## 🧠 How LAURA Thinks — The Agent Pipeline

LAURA follows a deterministic, safety-checked pipeline rather than freely guessing what to do — this prevents the most common agent failure: hallucinating fake sources.

```
1. SMART QUERY GENERATION
   LLM rewrites your subject into a precise, unambiguous search query
        ↓
2. WEB SEARCH
   Searches the live internet via DuckDuckGo
        ↓
3. RELEVANCE FILTERING
   Discards results that don't actually relate to the subject
   (retries with a different query if everything gets filtered out)
        ↓
4. REAL CONTENT EXTRACTION
   Reads the top 3 relevant pages and extracts their actual text
        ↓
5. HONESTY CHECKPOINT
   If nothing relevant was found, LAURA explicitly says so
   instead of inventing fake resources
        ↓
6. GROUNDED PLAN GENERATION
   LLM builds a day-by-day plan citing [Resource 1], [Resource 2] etc,
   using ONLY real content actually retrieved
```

---

## 🛡️ Built-In Hallucination Safeguards

Early versions of LAURA suffered from a classic LLM failure: when search results were poor, she would **invent fake resource titles and pretend to have read them**. This was caught and fixed with several layers of protection:

- **Relevance filtering** — search results are checked against subject keywords before being trusted
- **Query retry logic** — if the first search returns garbage, LAURA tries a reformulated query automatically
- **Hard-stop context check** — if literally nothing relevant was found, the system explicitly flags this rather than passing an empty context to the LLM
- **Explicit prompt rules** — the LLM is directly instructed never to assume or invent resources that weren't actually provided
- **Mandatory honesty** — if resources are irrelevant, LAURA says so and falls back to her own training knowledge instead of forcing a fake connection

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **Python 3.10+** | Core programming language |
| **Gradio 6** | Web interface |
| **Groq API** | Access to LLaMA 3.3 70B language model |
| **LLaMA 3.3 70B** | The reasoning engine behind every decision LAURA makes |
| **DuckDuckGo Search** | Live web search tool |
| **BeautifulSoup4** | Webpage content extraction |
| **Requests** | HTTP fetching for reading webpages |
| **python-dotenv** | Secure API key management |

---

## 📁 Project Structure

```
LAURA-study-agent/
├── app.py               # Gradio web interface
├── agent.py             # Core agent logic — the ReAct-style decision loop
├── tools.py             # LAURA's toolbox — search, read, format, relevance check
├── requirements.txt     # Python dependencies
├── .gitignore           # Files excluded from Git
└── README.md            # This file
```

---

## 🧰 LAURA's Tools

Defined in `tools.py`, these are the actions LAURA can take:

| Tool | What it does |
|---|---|
| `search_web(query)` | Searches DuckDuckGo and returns titles, URLs, and snippets |
| `read_webpage(url)` | Fetches a page and extracts clean, readable text content |
| `is_relevant(subject, resource)` | Checks if a search result actually relates to the subject |
| `create_study_plan(...)` | Formats the final resource list into a clean reference block |

---

## ⚙️ Run It Locally

### 1. Clone the repository

```bash
git clone https://github.com/fofMaymunah/LAURA-study-agent.git
cd LAURA-study-agent
```

### 2. Create a virtual environment

```bash
# Windows
python -m venv laura-env
laura-env\Scripts\activate

# macOS / Linux
python -m venv laura-env
source laura-env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

Create a `.env` file in the root folder:

```
GROQ_API_KEY=your-groq-api-key-here
```

Get a free API key at [console.groq.com](https://console.groq.com)

### 5. Run LAURA

```bash
python app.py
```

Then open your browser and go to:

```
http://127.0.0.1:7860
```

---

## 📖 How to Use

1. Type the subject you want to learn (e.g. "Data Science")
2. Select your available study duration
3. Select your current experience level
4. Click **Generate Study Plan**
5. Watch the progress log as LAURA searches, filters, and reads resources in real time
6. Receive a grounded, citation-backed study plan with a resource list at the end

---

## 🔑 Key Concepts

### What is an AI agent?
An agent is an AI that doesn't just answer questions — it takes actions to accomplish a goal, deciding for itself which tools to use and when, observing the results, and adjusting its approach until the goal is achieved.

### What is the ReAct pattern?
Short for **Reason + Act**, this is the core loop agents use: the LLM reasons about what to do next, takes an action (like searching or reading), observes the result, then reasons again — repeating until the task is complete.

### Why does relevance filtering matter?
Search engines can return misleading results for ambiguous queries (LAURA once received Lidl supermarket locations when searching for "fine tuning"). Filtering results against subject keywords before trusting them prevents the agent from building a plan around irrelevant content.

### What is hallucination, and why is it dangerous in agents?
Hallucination is when an LLM confidently generates plausible-sounding but false information — like inventing fake article titles it never actually read. In an agent, this is especially risky because the fabricated information can look just as credible as real retrieved content unless explicit safeguards are built in.

---

## 🌱 What I Learned Building LAURA

- How autonomous agents differ from chatbots and RAG apps
- How to design a multi-step decision loop (think → act → observe → repeat)
- How to give an LLM tools and describe them so it knows when to use them
- How to catch and prevent LLM hallucination with explicit safeguards
- How to filter and validate search results before trusting them
- How to debug a multi-file Python project with interacting components
- How to design fallback behavior for when tools fail or return nothing useful

---

## 🔗 Related Projects

- 🤖 **MUNAH** — AI chatbot with memory → [GitHub](https://github.com/fofMaymunah/MUNAH-chatbot) | [Live Demo](https://huggingface.co/spaces/Maymuunah14/MUNAH)
- 📄 **ILMA** — RAG-powered PDF document assistant → [GitHub](https://github.com/fofMaymunah/ILMA-Document-assistant) | [Live Demo](https://huggingface.co/spaces/Maymuunah14/ILMA)

---

## 👩🏾‍💻 About the Developer

**Fofana Maimouna** — software engineer and AI enthusiast passionate about building innovative solutions that leverage the power of artificial intelligence, from chatbots to RAG pipelines to autonomous agents.

- 🤗 Hugging Face → [Maymuunah14](https://huggingface.co/Maymuunah14)
- 🐙 GitHub → [fofMaymunah](https://github.com/fofMaymunah)

---

## 📄 License

This project is licensed under the MIT License — feel free to use, modify and share it.

---

*Built with curiosity, persistence, and a healthy distrust of confident-sounding AI. ◈*
