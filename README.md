# 🎓 AI Agent Engineering Course

**Learn to build AI agents from scratch - designed for hands-on learning with Claude Code**

[![Course Progress](https://img.shields.io/badge/Modules-7%20Core-blue)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Made with Claude](https://img.shields.io/badge/Made%20with-Claude%20Code-purple)]()

---

## 🎯 What You'll Build

By the end of this course, you'll have built:
- ✅ A **simple agent** with tool calling and structured logging
- ✅ A **memory-enabled agent** using vector databases (RAG)
- ✅ A **multi-tool agent** with Pydantic schemas and dynamic registries
- ✅ A **multi-agent system** with planner/worker/critic roles
- ✅ An **evaluation system** using LLM as judge patterns
- ✅ A **visual recognition agent** with face detection and embeddings
- ✅ An **advanced visual agent** with hybrid storage architecture

**No prior agent experience required.** If you can code in Python, you can build agents.

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.11+**
- **Claude Code CLI** - [Install here](https://github.com/anthropics/claude-code)
- **Docker** (for MCP modules)
- **Git**
- **OpenAI or Anthropic API key**

### Setup (5 minutes)

```bash
# 1. Clone this repo
git clone https://github.com/GeneArnold/AI-Agent-Engineering-Course.git
cd AI-Agent-Engineering-Course

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r setup/requirements.txt

# 4. Configure API keys
cp setup/.env.example .env
# Edit .env and add your API keys

# 5. Verify setup
python setup/verify_setup.py

# 6. Start learning!
claude-code
```

---

## 🎓 How to Use This Course

### Learning with Claude Code (AI Professor Mode)

This course is designed to work with **Claude Code as your AI professor**. Here's how:

1. **Open the repo in Claude Code:**
   ```bash
   cd AI-Agent-Engineering-Course
   claude-code
   ```

2. **Start a module:**
   ```
   You: "Start Module 1"
   ```

3. **Claude Code will:**
   - Read the module's README
   - Teach you the concepts
   - Guide you through building the project
   - Help you debug and understand
   - Commit your progress

4. **Work at your own pace:**
   - Deep dive into concepts
   - Ask questions anytime
   - Experiment and break things
   - Build understanding, not just code

### Why Claude Code is Required

This course is designed for **AI-assisted learning** - the same way modern engineers actually work:
- Claude Code acts as your professor and pair programmer
- You learn concepts by discussing, not just typing
- Focus on understanding architecture and trade-offs
- Get unstuck immediately when confused
- This mirrors real-world AI-assisted development

**Don't have Claude Code?** [Install it here](https://github.com/anthropics/claude-code) - it's free to use with your own API keys.

---

## 📚 Course Curriculum

### **Module 0: Setup** (Start here)
- Environment configuration
- API keys and dependencies
- Verify everything works

### **Module 1: Agent Foundations** (Week 1)
**What you'll learn:**
- LLM call anatomy (prompts → tokens → completion)
- Agent loop fundamentals (policy + tools + stop condition)
- JSON contracts and function calling
- Structured logging with JSONL

**What you'll build:**
- `simple_agent.py` - A weather agent with tool calling

**Time:** 2-3 hours

---

### **Module 2: Memory & Context** (Week 2)
**What you'll learn:**
- Embeddings and semantic search
- Vector databases (ChromaDB/FAISS)
- Retrieval-augmented generation (RAG)
- Context window management

**What you'll build:**
- `memory_agent.py` - An agent that remembers past interactions

**Time:** 3-4 hours

---

### **Module 3: Tools & Registries** (Week 3)
**What you'll learn:**
- Pydantic schemas for type-safe tool definitions
- Dynamic tool registries with decorators
- Clean dispatch patterns (no if/elif chains)
- Cost tracking and observability

**What you'll build:**
- `tool_agent.py` - Multi-tool agent with dynamic registry
- `comparison_simple_vs_pydantic.py` - Bridge example

**Time:** 3-4 hours

---

### **Module 4: Multi-Agent Systems** (Week 4)
**What you'll learn:**
- Multi-agent orchestration
- Planner → Worker → Critic pattern
- Shared state and message passing
- Agent coordination strategies

**What you'll build:**
- `multi_agent_system.py` - Collaborative agent system

**Time:** 4-5 hours

---

### **Module 5: LLM as Judge & Evaluation** (Week 5)
**What you'll learn:**
- LLM as judge pattern
- Multi-criteria evaluation rubrics
- Quality scoring and metrics
- Evaluation frameworks

**What you'll build:**
- `judge_agent.py` - Evaluation system for agent outputs

**Time:** 3-4 hours

---

### **Module 6: Visual Recognition (Part 1)** (Week 6)
**What you'll learn:**
- Face detection and recognition
- Visual embeddings
- Image-based RAG patterns
- Multi-modal agents

**What you'll build:**
- `face_recognition_agent.py` - Face recognition with vector DB

**Time:** 4-5 hours

---

### **Module 7: Visual Recognition (Part 2)** (Week 7)
**What you'll learn:**
- Hybrid storage architectures
- Vector DB + SQLite integration
- Metadata-rich retrieval
- Production-grade visual agents

**What you'll build:**
- `hybrid_recognition_agent.py` - Advanced visual recognition system

**Time:** 4-5 hours

---

### **Advanced Topics** (Optional)
Explore infrastructure and production topics:
- **Model Context Protocol (MCP)** - Standardized tool interfaces
- **Local Models & Quantization** - Ollama, GGUF, cost optimization
- See `advanced_topics/` for details

**Time:** Varies by topic

---

## 🧠 Learning Philosophy

This course prioritizes **understanding over completion**:

- 🎯 **Concepts first, code second** - Know the "why" before the "how"
- 🔬 **Experiment freely** - Break things, ask questions, explore
- 📝 **Document your learning** - Keep a journal (see `TRAINING_JOURNAL.md` template)
- 🐌 **No rush** - Deep learning takes time
- 🎨 **Simplicity over production** - Focus on clarity, not enterprise patterns

---

## 📖 Resources

### Official Documentation
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

### Tools Used
- **Claude Code** - AI pair programming CLI
- **OpenAI/Anthropic APIs** - LLM providers
- **ChromaDB** - Vector database
- **Ollama** - Local model inference
- **Docker** - Containerization

---

## 🤝 Contributing

Found a bug? Have a suggestion? Contributions welcome!

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 🎁 Holiday Gift - Free AI Agent Course!

**This course is my holiday gift to the developer community.**

Learn to build AI agents with hands-on projects and AI-assisted guidance. Perfect for developers who want to understand how agents really work under the hood.

## 📅 Release Schedule

**New modules released every Sunday:**

- ✅ **Week 0** (Nov 24, 2024): Course structure + environment setup
- ✅ **Week 1** (Dec 1, 2024): Module 1 - Agent Foundations
- ✅ **Week 2** (Dec 8, 2024): Module 2 - Memory & Context
- ✅ **Week 3** (Dec 15, 2024): Module 3 - Tools & Registries
- 📅 **Week 4** (Dec 22, 2024): Module 4 - Multi-Agent Systems
- 📅 **Week 5** (Dec 29, 2024): Module 5 - LLM as Judge & Evaluation
- 📅 **Week 6** (Jan 5, 2025): Module 6 - Visual Recognition (Part 1)
- 📅 **Week 7** (Jan 12, 2025): Module 7 - Visual Recognition (Part 2)

**Watch this repo** ⭐ to get notified of weekly releases!

---

## 📜 License

This course is open source under the [MIT License](LICENSE).

Feel free to:
- ✅ Use for personal learning
- ✅ Share with your team
- ✅ Adapt for your needs
- ✅ Teach workshops using this material

---

## 👨‍💻 About

Created by **Gene Arnold** - [LinkedIn](https://linkedin.com/in/genearnold) | [Twitter](https://twitter.com/genearnold)

Built with **Claude Code** as an AI pair programming partner.

---

## 🙏 Acknowledgments

- Anthropic for Claude and Claude Code
- OpenAI for GPT models and function calling patterns
- The agent engineering community for inspiration

---

**Ready to build agents?** Start with [Module 0: Setup](setup/README.md)

Questions? Open an issue or reach out on [LinkedIn](https://linkedin.com/in/genearnold).

**Happy building!** 🚀
