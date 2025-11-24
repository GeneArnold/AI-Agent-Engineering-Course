# AI Agent Engineering Course - START HERE

**Welcome!** This course teaches you to build AI agents from scratch using a unique learning model: **study working code with AI assistance**.

---

## 🎯 How This Course Works

### The Learning Model

**You are NOT building code from scratch.** Instead:
1. Each module provides **working, tested code** (the SOLUTION)
2. You **study and understand** that code
3. **Claude Code acts as your professor** - explaining, answering questions, helping you experiment
4. You **modify and test** the code to deepen understanding

**Why this approach?**
- Guaranteed working examples (no debugging syntax errors)
- Focus on concepts, not syntax
- Learn how professional engineers actually work (with AI assistance)
- Faster, deeper learning

---

## 📚 Course Structure

### Files in Each Module

Every module has the same structure:

```
module_X_name/
├── README.md          # Overview and how to use this module
├── CONCEPTS.md        # Theory: What and why
├── PROJECT.md         # Architecture: How and with what tools
└── SOLUTION/          # Working code to study
    └── agent.py
```

### What Each File Does

**README.md**
- Module overview
- Learning objectives
- How to use the module (your roadmap)

**CONCEPTS.md**
- **Theory and concepts**
- What problem we're solving
- Why this solution matters
- How things work conceptually
- **Read this FIRST** - You need the theory before the code

**PROJECT.md**
- **Architecture and tools**
- What tools we're using (ChromaDB, OpenAI, etc.)
- How the code is structured
- Key design decisions and why we made them
- **Seed questions** to ask Claude Code
- **Read this SECOND** - Understand the design before the implementation

**SOLUTION/agent.py**
- **Working, tested code**
- Complete implementation
- Extensive comments
- **Read this THIRD** - Study the code with Claude's help

---

## 🎓 Your Learning Workflow (Use This Every Module!)

### Step 1: Read CONCEPTS.md
**Goal:** Understand the theory

Open `CONCEPTS.md` and read through the concepts. You can ask Claude Code:
- "Explain embeddings in simpler terms"
- "Why does context growth matter?"
- "Give me an analogy for vector search"

### Step 2: Read PROJECT.md
**Goal:** Understand the architecture

Open `PROJECT.md` to learn how the solution is designed. Pay attention to:
- Tools used and why
- Architecture diagrams
- Design decisions

**Use the seed questions!** PROJECT.md includes starter questions like:
- "Walk me through the MemoryManager class"
- "Why ChromaDB instead of FAISS?"

### Step 3: Study SOLUTION/agent.py
**Goal:** Understand the implementation

Open the code and study it with Claude Code as your professor:
- "Explain this function line by line"
- "Why did we use this pattern here?"
- "What would happen if I changed X to Y?"

### Step 4: Run the Code
**Goal:** See it work

```bash
# Activate your environment
source venv/bin/activate

# Run the agent
python module_X/SOLUTION/agent.py
```

Watch the output, check the logs, verify it works.

### Step 5: Ask Deep Questions
**Goal:** Fill knowledge gaps

Now that you've seen it work, ask:
- "How does the agent handle errors?"
- "What are the edge cases?"
- "How would this scale to 1000 users?"

### Step 6: Experiment
**Goal:** Learn by doing

Make modifications and test:
- Change parameters (top_k=3 → top_k=5)
- Add features (metadata filtering)
- Break things intentionally to see what happens
- Fix what you broke

### Step 7: Reflect
**Goal:** Cement understanding

Answer the reflection questions in README.md:
- What did you learn?
- What surprised you?
- What would you do differently?

---

## 🤖 How to Use Claude Code (Your AI Professor)

### What Claude Code WILL Do ✅

**Explain concepts:**
- "Explain how RAG works"
- "What's the difference between embeddings and tokens?"

**Walk through code:**
- "Explain this function step-by-step"
- "Why is this variable named like that?"

**Answer questions:**
- "What happens if I remove this line?"
- "How would I add feature X?"

**Help you experiment:**
- "Help me add timestamp filtering"
- "Show me how to change the embedding model"

**Debug issues:**
- "I changed X and now I get error Y - why?"

### What Claude Code WON'T Do ❌

**Generate solutions from scratch:**
- Solutions already exist and are tested
- Your goal is understanding, not code generation

**Skip the learning:**
- Claude won't just give you answers
- It will guide you to discover them

**Do the work for you:**
- You must read the docs
- You must study the code
- You must experiment

---

## 📅 Weekly Release Schedule

Content releases every Sunday:

| Week | Date | Content Released |
|------|------|------------------|
| Week 0 | Nov 24 | Course structure + Setup |
| Week 1 | Dec 1 | Module 1: Agent Foundations |
| Week 2 | Dec 8 | Module 2: Memory & Context |
| Week 3 | Dec 15 | Module 3: Tools & Local Models |
| Week 4 | Dec 22 | Module 4: Multi-Agent Systems |
| Week 5 | Dec 29 | MCP Add-on: Model Context Protocol |

**Pace yourself!** One module per week is plenty. Deep understanding > speed.

---

## 🛠️ Prerequisites & Setup

### Before Starting Module 1

Complete the `setup/` folder:
1. Read `setup/README.md`
2. Install dependencies: `pip install -r setup/requirements.txt`
3. Configure API keys in `.env`
4. Run `python setup/verify_setup.py` - ensure all checks pass

### System Requirements

- Python 3.11+
- 4GB RAM minimum
- OpenAI API key
- Claude Code installed
- Text editor (VS Code, Sublime, etc.)

**Note:** This course uses OpenAI for simplicity. If you prefer Anthropic, you can ask Claude Code: "Help me convert this agent to use Anthropic's API" after understanding the OpenAI version.

---

## ❓ Example Learning Session

Here's what a typical module session looks like:

**Starting Module 2 (Memory & Context):**

```
You: "I'm ready to start Module 2. What should I do first?"

Claude: "Great! Let's start with CONCEPTS.md. This will teach you about
embeddings, vector databases, and RAG. Would you like me to summarize
the key concepts, or would you prefer to read it first and then ask questions?"

You: "I'll read it first."
[You read CONCEPTS.md]

You: "Okay, I read it. Can you explain embeddings using an analogy?"

Claude: "Sure! Think of embeddings as coordinates on a map of meaning..."
[Claude explains]

You: "That makes sense! Now I'm ready for PROJECT.md."
[You read PROJECT.md]

You: "Walk me through the MemoryManager class - how does it work?"

Claude: "Great question! Let's open SOLUTION/memory_agent.py and I'll
explain it step by step..."
[Claude explains the code]

You: "Now I want to run it and see it work."
[You run the code]

You: "Cool! What happens if I change top_k from 3 to 5?"

Claude: "Good experiment! That will retrieve more facts from memory.
Try it and let's see what changes..."
[You experiment]
```

---

## 💡 Pro Tips

### Tip 1: Ask "Why" Often
Don't just learn HOW code works - learn WHY it was built that way.
- "Why ChromaDB instead of FAISS?"
- "Why top_k=3 instead of 10?"

### Tip 2: Break Things Intentionally
Best way to learn:
- Comment out a line - what breaks?
- Change a value - what happens?
- Remove a function - what errors occur?

### Tip 3: Use the Logs
Every agent logs to JSONL files. Study them:
- What happened in each iteration?
- How many tokens were used?
- What did the LLM see at each step?

### Tip 4: Compare Modules
As you progress, compare approaches:
- How does Module 2 differ from Module 1?
- What pattern repeats across modules?
- What's the evolution?

### Tip 5: Take Notes
Keep a learning journal:
- What clicked?
- What confused you?
- What would you do differently?

---

## 🚨 Common Mistakes to Avoid

**❌ Mistake 1: Skipping CONCEPTS.md**
Don't jump straight to code. You'll be lost without theory.

**❌ Mistake 2: Not Asking Questions**
Claude Code is your professor - use it! No question is too basic.

**❌ Mistake 3: Not Running the Code**
Reading code ≠ understanding code. Run it!

**❌ Mistake 4: Not Experimenting**
The code works - great! Now break it, change it, extend it.

**❌ Mistake 5: Rushing**
One module per week is enough. Deep understanding > speed.

---

## 📖 Module Overview

### Module 1: Agent Foundations
**What:** Build your first agent with tool calling
**Key Concepts:** Agent loops, function calling, JSONL logging
**Time:** 1 week

### Module 2: Memory & Context
**What:** Add long-term memory with vector databases
**Key Concepts:** Embeddings, RAG, ChromaDB
**Time:** 1 week

### Module 3: Tools & Local Models
**What:** Multi-tool agent with local LLM support
**Key Concepts:** Tool registry, Ollama, quantization
**Time:** 1 week

### Module 4: Multi-Agent Systems
**What:** Multiple agents working together
**Key Concepts:** Coordination, evaluation, orchestration
**Time:** 1 week

### MCP Add-on: Model Context Protocol
**What:** Use MCP servers for extended capabilities
**Key Concepts:** MCP architecture, server integration
**Time:** 1 week

---

## 🎯 Success Criteria

You'll know you've mastered a module when:

✅ You can explain the concepts without looking at docs
✅ You can walk someone through the code
✅ You can modify the code to add features
✅ You understand why design decisions were made
✅ You can compare this approach to alternatives

---

## 🤝 Getting Help

### From Claude Code
Your primary resource! Ask questions constantly.

### From the Code
Study the comments, follow the logic, trace execution.

### From the Logs
JSONL logs show exactly what happened - use them.

### From Experiments
Try things, break things, fix things - that's learning.

---

## 🎉 Ready to Begin?

1. ✅ Complete `setup/` (verify_setup.py passes)
2. ➡️ Start with Module 1: `module_1_foundations/`
3. ➡️ Open `module_1_foundations/README.md`
4. ➡️ Follow the 7-step workflow above

**Remember:** You're not racing. You're learning deeply. Take your time, ask questions, and experiment.

**Welcome to AI Agent Engineering!** 🚀

---

## 📞 Questions About This Course?

If you're confused about how to use the course:
- Re-read this START_HERE.md
- Ask Claude Code: "How do I use this course?"
- Check the README.md in the current module

If you're confused about technical content:
- Read CONCEPTS.md for theory
- Read PROJECT.md for architecture
- Ask Claude Code specific questions about the code

---

**Last Updated:** November 24, 2024
**Version:** 1.0
