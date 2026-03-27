# Multilingual Legal Advisory Chatbot (MLAC)

> **MSc Dissertation Project — Robert Gordon University (Distinction)**
> Adebowale Odufuwa | 2022–2024

A proof-of-concept multilingual legal advisory chatbot providing UK criminal law guidance across three jurisdictions in English and French, built using Retrieval-Augmented Generation (RAG) architecture.

---

## 🎯 Overview

MLAC demonstrates how AI can democratise access to legal information. Users can query UK criminal law in natural language, selecting their jurisdiction and preferred language, and receive contextually accurate responses drawn from real legal documents.

**Key Objectives:**
- Make legal information accessible to non-lawyers
- Support all three UK jurisdictions with comparative analysis
- Deliver responses in English and French with accurate legal terminology
- Demonstrate RAG architecture in a domain-specific application

---

## ✨ Features

- 🌍 **Multilingual** — English and French with legal-grade translation via DeepL
- ⚖️ **Multi-Jurisdictional** — England & Wales, Scotland, Northern Ireland, and comparative mode
- 🧠 **RAG Architecture** — semantic retrieval from real legal documents using Pinecone
- 💬 **Conversation Memory** — maintains context across the session
- 📋 **Session Management** — satisfaction survey and session logging
- 🔒 **GDPR-Compliant** — data handling aligned with UK data protection requirements

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         Document Processing Layer        │
│  PDF Extraction → Chunking → Translation │
│  → Embedding Generation → Pinecone Index │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│           Core Chatbot Logic             │
│  Query Embedding → Retrieval → GPT-4    │
│  Response Generation → Translation       │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│         User Interaction Layer           │
│     Streamlit Interface → Session Mgmt   │
└─────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| UI Framework | Streamlit |
| LLM | OpenAI GPT-4 |
| Embeddings | OpenAI Embeddings (1536-dim) |
| Vector Store | Pinecone (cosine similarity) |
| RAG Framework | LangChain |
| Translation | DeepL API |
| PDF Extraction | PyMuPDF |
| Language | Python 3.8+ |

---

## 📦 Installation

### Prerequisites
- Python 3.8+
- API keys for: OpenAI, Pinecone, DeepL

### Steps

```bash
# Clone the repository
git clone https://github.com/Debo-Odufuwa/MLACprime.git
cd MLACprime

# Install dependencies
pip install pipenv
pipenv install
pipenv shell
```

### Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX=your_pinecone_index_name
DEEPL_API_KEY=your_deepl_api_key
```

> ⚠️ Never commit your `.env` file. It is included in `.gitignore`.

---

## ⚙️ Configuration

Place legal PDF documents in the `legal_files/` directory:

```
legal_files/
├── england&wales.pdf
├── scotland.pdf
└── n_ireland.pdf
```

Then run the document processor to extract, translate, embed, and index:

```bash
python document_processor.py
```

---

## 🚀 Usage

```bash
streamlit run app.py
```

Opens at `http://localhost:8501`

### Example Queries

```
What is the definition of theft?
Is the law on self-defence different in Scotland compared to England?
What happens if I'm arrested in Northern Ireland?
Quelle est la procédure pour plaider coupable en Angleterre?
```

---

## 📁 Project Structure

```
MLACprime/
├── app.py                  # Streamlit UI layer
├── chatbot.py              # Core chatbot logic and LLM integration
├── document_processor.py   # Document processing and Pinecone indexing
├── .env                    # Environment variables (not in repo)
├── .gitignore
├── README.md
└── legal_files/            # Legal source documents
    ├── england&wales.pdf
    ├── scotland.pdf
    └── n_ireland.pdf
```

---

## 🧪 User Acceptance Testing Results

| Metric | Result |
|--------|--------|
| Overall Pass Rate | 98.8% |
| User Experience Rating | 100% rated Good or Excellent |
| English Language Tests | 100% pass |
| French Language Tests | 88% pass |
| Jurisdiction Selection | 100% pass |

**10 participants** including legal professionals, law students, law enforcement, and bilingual users.

---

## ⚠️ Limitations

- Proof of concept — not suitable for production legal advice
- Covers UK criminal law only (not civil or employment law)
- Basic username authentication (not production-grade)
- Translation quality dependent on DeepL; some legal nuance may be lost
- Responses not verified by legal professionals

> **Disclaimer:** This chatbot provides general legal information only and is not a substitute for professional legal advice. Always consult a qualified solicitor for specific legal matters.

---

## 🔮 Future Enhancements

- Secure authentication and user management
- Expanded legal domains (civil, employment, family law)
- Additional language support
- Voice interface (speech-to-text / text-to-speech)
- Legal professional review and citation system
- Mobile application (iOS and Android)
- Document upload for personalised analysis

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **OpenAI** — GPT-4 and embedding models
- **Pinecone** — Vector database
- **DeepL** — Translation services
- **Streamlit** — Application framework
- **LangChain** — LLM application tooling

---

## 📞 Contact

**Adebowale Odufuwa**
- 🌐 [Portfolio](https://debo-odufuwa.github.io)
- 💼 [GitHub](https://github.com/Debo-Odufuwa)

---

*This is an academic proof-of-concept project developed as part of an MSc in Business Analytics (Distinction) at Robert Gordon University.*
