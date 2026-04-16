# 🚀 Findora – AI-Powered Product Assistant

> Smarter Shopping Starts Here.

Findora is an intelligent AI-powered assistant designed to help users find, compare, and purchase products.
It combines **AI decision-making**, **structured datasets**, and **real-time web data** to deliver the best product recommendations in seconds.

---

# 🧠 Overview

Finding the best product online is frustrating.
Too many options, inconsistent prices, and time-consuming comparisons.

**Findora solves this problem by:**

* 🔍 Searching internal product databases
* 🤖 Using AI to analyze and compare products
* 🏆 Selecting the best option based on value
* 🌐 Fetching real-time deals from Amazon & eBay

All in one seamless experience.

---

# ✨ Features

* 🧠 **AI Decision Making** (LLM-powered recommendations)
* 📊 **Top 3 Product Comparison**
* 🏆 **Best Product Selection**
* 🌐 **Real-Time Price Search (Amazon + eBay)**
* 🎤 **Voice Input Support**
* 💬 **Interactive Chat UI**
* 📦 **Multiple Categories** (Phones, Laptops, Cars)
* ⭐ **User Feedback System**

---

# 🏗️ Architecture

```
User → Streamlit UI
        ↓
   Chat Interface
        ↓
   AI Agent (LangGraph + Gemini)
        ↓
 ┌───────────────┬───────────────┐
 │ Internal DB   │ External APIs │
 │ (CSV files)   │ (Amazon/eBay) │
 └───────────────┴───────────────┘
        ↓
   Final Recommendation + UI
```

---

# 📂 Project Structure

```
Findora/
│
├── app.py          # Main entry point & navigation
├── home.py         # Landing page UI
├── chat.py         # Core AI logic + tools + chat system
│
├── data/
│   ├── mobile_phones.csv
│   ├── laptops.csv
│   └── cars.csv
│
├── media/          # Images, icons, assets
├── html.txt        # Background animation
│
└── README.md
```

---

# ⚙️ How It Works

1. User enters a query (e.g., "Best phone under $500")
2. AI agent understands the request
3. Internal database is searched
4. Top 3 products are selected
5. Best product is chosen
6. Amazon & eBay APIs fetch live deals
7. Results are displayed with links and UI cards

---

# 🧰 Tech Stack

### 💻 Core

* Python
* Streamlit

### 🧠 AI & Agents

* LangChain
* LangGraph
* Google Gemini API

### 📊 Data Processing

* Pandas

### 🌐 APIs

* SerpAPI (Amazon Search)
* eBay API

### 🎤 Extras

* SpeechRecognition (Voice input)

---

# 🚀 Getting Started

## 1. Clone the repo

```bash
git clone https://github.com/Abdallah-Fekry/Findora---Smart-AI-Product-Assistant.git
cd findora
```

---

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Setup environment variables

Create a `.streamlit/secrets.toml` file:

```toml
GeminiAPI = "YOUR_GEMINI_API_KEY"
SerpAPI = "YOUR_SERPAPI_KEY"
EBAY_CLIENT_ID = "YOUR_EBAY_CLIENT_ID"
EBAY_CLIENT_SECRET = "YOUR_EBAY_CLIENT_SECRET"
```

---

## 4. Run the app

```bash
streamlit run app.py
```

---

### Test the app

https://findora-ai-assistant.streamlit.app/

# 📸 Demo

[![Watch the demo](https://img.youtube.com/vi/1qybCcar-vE/0.jpg)](https://youtu.be/1qybCcar-vE)
---

# 💡 Example Queries

* "Best iPhone under $800"
* "Laptop for programming with 16GB RAM"
* "Car under $20,000 with good fuel efficiency"

---

# 📈 Future Improvements

* 🔄 Multi-agent architecture (planner, retriever, comparator)
* ⚡ Faster performance with caching
* 🧑‍💼 User accounts & personalization
* 🛍️ More marketplaces (Jumia, Noon)
* 📊 Advanced ranking algorithms
* ☁️ Cloud deployment (AWS / GCP)

---

# ⭐ Final Note

Findora is more than just a chatbot…
It’s a **smart decision-making system** designed to make online shopping faster, easier, and more intelligent.

> Try it. Compare smarter. Shop better.
