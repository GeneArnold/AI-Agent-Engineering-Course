# 🎓 AI Agent Engineering Course

**Learn to build AI agents from scratch - designed for hands-on learning with Claude Code**

[![Course Progress](https://img.shields.io/badge/Modules-4%20Core%20%2B%20MCP-blue)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Made with Claude](https://img.shields.io/badge/Made%20with-Claude%20Code-purple)]()

---

## 🎯 What You'll Build

By the end of this course, you'll have built:
- ✅ A **simple agent** with tool calling and structured logging
- ✅ A **memory-enabled agent** using vector databases (RAG)
- ✅ A **multi-tool agent** that runs local and cloud models
- ✅ A **multi-agent system** with planner/worker/critic roles
- ✅ Custom **MCP servers** for standardized tool interfaces

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

### Learning Without Claude Code

Each module contains:
- `README.md` - Module overview and instructions
- `CONCEPTS.md` - Core concepts to learn
- `PROJECT.md` - What you'll build
- `SOLUTION/` - Reference solution (study after attempting!)

Work through each module sequentially. Build the projects yourself before looking at solutions.

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

### **Module 3: Tools & Local Models** (Week 3)
**What you'll learn:**
- Tool registries and dynamic dispatch
- Local inference with Ollama
- Model quantization (GGUF/AWQ)
- Cost vs quality tradeoffs

**What you'll build:**
- `tool_agent.py` - Multi-tool agent with local/cloud model switching

**Time:** 4-5 hours

---

### **Module 4: Multi-Agent Systems** (Week 4)
**What you'll learn:**
- Multi-agent orchestration
- Planner → Worker → Critic pattern
- Shared state and message passing
- Evaluation and testing

**What you'll build:**
- `multi_agent_system.py` - Collaborative agent system

**Time:** 4-5 hours

---

### **MCP Add-On Track** (Weeks 3-4)
**What you'll learn:**
- Model Context Protocol (MCP) fundamentals
- Building custom MCP servers
- Local vs remote server patterns
- Tool standardization

**What you'll build:**
- Custom MCP server
- MCP-powered agent integration

**Time:** 3-4 hours

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

## 📅 Weekly Release Schedule

**New modules released every Tuesday:**
- ✅ **Week 0** (Nov 19): Setup + Module 1 instructions
- 📅 **Week 1** (Nov 26): Module 1 solution + Module 2 instructions
- 📅 **Week 2** (Dec 3): Module 2 solution + Module 3 instructions
- 📅 **Week 3** (Dec 10): Module 3 solution + Module 4 instructions
- 📅 **Week 4** (Dec 17): Module 4 solution + MCP instructions
- 📅 **Week 5** (Dec 24): MCP solution + Course wrap-up

**Watch this repo** ⭐ to get notified of new releases!

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
