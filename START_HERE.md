# 🎓 START HERE - How to Use This Course

**Welcome to AI Agent Engineering!** This course is designed to be learned WITH Claude Code as your AI tutor.

Before you start any module, **read this entire guide**. It explains exactly how this course works and how to get the most out of it.

---

## 🤖 What is Claude Code?

Claude Code is an AI-powered coding assistant that can:
- Read and explain code
- Answer questions about concepts
- Help you debug and modify solutions
- Guide you through understanding complex topics

**Think of it as having an expert tutor available 24/7.**

---

## 📚 How This Course Works

### The Course Structure

Each module contains **three types of files:**

```
module_X_name/
├── CONCEPTS.md          # Theory - Read this FIRST
├── PROJECT.md           # Architecture - Read this SECOND
├── README.md            # Module overview
└── SOLUTION/            # Working code - Study this THIRD
    └── example_agent.py
```

### What Each File Does

**1. CONCEPTS.md** - The Theory
- Explains the "why" behind what you're learning
- Teaches foundational concepts with examples
- Prepares you to understand the code
- **Read this BEFORE looking at any code**

**2. PROJECT.md** - The Architecture
- Explains WHAT we're building
- Describes the components and why they exist
- Shows design decisions and tradeoffs
- **Read this BEFORE running the solution**

**3. SOLUTION/** - The Working Code
- Complete, tested, production-quality example
- Extensively commented
- Ready to run and study
- **This is what you'll learn from and modify**

---

## 🎯 The Learning Workflow

### Step 1: Tell Claude Code to Read the Professor Guide

**First thing you do when you open Claude Code:**

```
You: "Read .claude/prompts/professor.md and understand your role as my AI Agent Engineering tutor"
```

Claude Code will then know:
- It's teaching you AI agents
- It should explain working code (not generate new code)
- It should use the CONCEPTS and PROJECT docs to teach
- It should help you understand, debug, and extend the solutions

### Step 2: Start a Module

**When you're ready to begin a module:**

```
You: "I want to start Module 1"
```

**Claude Code will:**
1. Read the module's README, CONCEPTS, and PROJECT files
2. Explain what you'll learn in this module
3. Walk through the key concepts with you
4. Answer any questions you have about the theory

### Step 3: Understand the Concepts

**Work with Claude Code to understand the theory:**

```
You: "Explain embeddings to me"
Claude: *reads CONCEPTS.md section on embeddings*
Claude: "Embeddings are coordinates in meaning-space..."

You: "I don't understand cosine similarity"
Claude: *explains with examples and analogies*

You: "Can you give me a real-world example?"
Claude: *provides concrete examples*
```

**Keep asking questions until the concepts click!**

### Step 4: Study the Solution Code

**Once you understand the concepts, examine the working code:**

```
You: "Show me the solution for Module 1"
Claude: *reads simple_agent.py*
Claude: "This solution has 3 main components..."

You: "Walk me through the agent loop"
Claude: *explains the while loop, line by line*

You: "Why do we check finish_reason here?"
Claude: *references CONCEPTS.md to explain*
```

**Claude Code can:**
- Explain any part of the code
- Connect code back to concepts
- Show you how to run it
- Help you understand design decisions

### Step 5: Run the Solution

**Get the solution working on your machine:**

```
You: "How do I run this?"
Claude: "First, make sure you've completed the setup..."

You: "I'm getting an error"
Claude: *reads error, helps you debug*

You: "It worked!"
Claude: "Great! Now let's look at the logs to see what happened..."
```

### Step 6: Experiment and Modify

**Now that it works, make it yours:**

```
You: "I want to add a second tool"
Claude: *analyzes the code*
Claude: "Here's where you'd add it... let me explain the pattern..."

You: "Can you help me debug this?"
Claude: *walks through the problem together*

You: "How would I make this production-ready?"
Claude: *discusses error handling, logging, etc.*
```

**This is where deep learning happens!**

### Step 7: Reflect and Move On

**Before moving to the next module:**

```
You: "What are the key takeaways from Module 1?"
Claude: *summarizes the insights*

You: "What should I remember for later modules?"
Claude: *highlights patterns you'll use again*
```

---

## 🎓 Example: Complete Module 1 Walkthrough

### Opening Claude Code

```bash
cd AI-Agent-Engineering-Course
claude-code
```

### Initial Setup (One Time)

```
You: "Read .claude/prompts/professor.md and understand your role"
Claude: "I've read the professor guide. I'm here to help you learn AI agent engineering by explaining working code and concepts. Ready to start Module 1?"
```

### Starting Module 1

```
You: "Yes, let's start Module 1"

Claude: "Great! Module 1 is about Agent Foundations. You'll learn:
- How LLM calls work (prompts → tokens → completion)
- What makes agents different from chatbots (the loop!)
- How to teach LLMs about tools (JSON contracts)

Let me read the CONCEPTS.md file to teach you these..."

Claude: *reads CONCEPTS.md*
Claude: "The first concept is LLM Call Anatomy. Think of it as a 3-stage pipeline..."

[Claude explains each concept]

You: "I understand the concepts. What are we building?"

Claude: *reads PROJECT.md*
Claude: "We're building simple_agent.py - a weather agent with tool calling. Here's the architecture..."

[Claude explains the design]

You: "Show me the solution"

Claude: *reads SOLUTION/simple_agent.py*
Claude: "Here's the working implementation. Let me walk through the key parts..."
```

### Understanding the Code

```
You: "Explain the agent loop (lines 150-180)"

Claude: "This is the core pattern. Here's what happens:
1. We call the LLM with the current messages
2. We check finish_reason
3. If it's 'tool_calls', we execute the tool
4. If it's 'stop', we're done
The while loop continues until finish_reason is 'stop'..."

You: "Why do we need max_iterations?"

Claude: "Great question! That's a safety limit. Without it, if the agent gets stuck in a loop, it would run forever. This is mentioned in the CONCEPTS.md under agent loops..."

You: "What's this JSONL logging for?"

Claude: "Observability! Every event is logged so you can see exactly what happened. Look at the log file after running - you'll see token counts, latency, tool calls... Let me show you..."
```

### Running It

```
You: "How do I run this?"

Claude: "Make sure you've completed setup (Module 0), then:
python module_1_foundations/SOLUTION/simple_agent.py

You should see output like..."

You: "It's running! I see the agent loop in action!"

Claude: "Excellent! Now check logs/simple_agent.jsonl to see the structured logs. Each event is recorded..."
```

### Experimenting

```
You: "I want to add a calculator tool"

Claude: "Great idea! Here's the pattern:
1. Define the tool function (like get_weather)
2. Add it to the tools array
3. The agent will automatically know how to use it
Let me show you where to add each part..."

You: "I added it but getting an error"

Claude: "Let me see the error... Ah, the function signature doesn't match the tool definition. The 'expression' parameter needs to be a string. Try this..."

You: "It works!"

Claude: "Perfect! You just extended the agent with a new capability. This is the power of tool calling!"
```

### Moving to Module 2

```
You: "I'm ready for Module 2"

Claude: "Great! Before we move on, let's reflect on Module 1:
- What was the biggest 'aha' moment for you?
- Do you understand why the agent loop is just a while loop?
- Are you comfortable with how tool calling works?

[Reflection discussion]

Claude: "Perfect! Module 2 builds on this. You discovered that context grows with each iteration - Module 2 solves that problem with memory and RAG. Ready to start?"
```

---

## 📅 Weekly Release Schedule

**New modules released every Sunday:**

- ✅ **Week 0** (Nov 24): Course structure + setup
- 📅 **Week 1** (Dec 1): Module 1 complete
- 📅 **Week 2** (Dec 8): Module 2 complete
- 📅 **Week 3** (Dec 15): Module 3 complete
- 📅 **Week 4** (Dec 22): Module 4 complete
- 📅 **Week 5** (Dec 29): MCP add-on complete

**⭐ Star the repo** to get notified of new releases!

---

## ✅ What Claude Code Will Do

**Claude Code is your tutor. It will:**
- ✅ Read and explain CONCEPTS.md to teach you theory
- ✅ Read and explain PROJECT.md to show you architecture
- ✅ Read and explain SOLUTION code to help you understand
- ✅ Answer questions by referencing the docs
- ✅ Help you debug when you modify the code
- ✅ Explain design decisions and tradeoffs
- ✅ Connect concepts to real-world applications
- ✅ Celebrate your wins and normalize struggles

---

## ❌ What Claude Code Will NOT Do

**Claude Code will NOT:**
- ❌ Generate solutions from scratch (solutions are already tested and provided)
- ❌ Skip concepts and jump straight to code
- ❌ Rush you through material
- ❌ Give you answers without explaining
- ❌ Make you feel bad for asking questions

---

## 💡 Pro Tips for Success

### 1. Read CONCEPTS Before Code
**Don't skip to the solution!** Understanding the "why" before the "how" makes everything click faster.

### 2. Ask "Dumb" Questions
There are no dumb questions. If something is confusing, ask Claude Code to explain it differently.

**Good questions:**
- "Can you explain this like I'm 12?"
- "What's a real-world example of this?"
- "Why did we choose this approach over another?"
- "What happens if I change this line?"

### 3. Break Things on Purpose
The best way to learn is to modify the code and see what breaks. Claude Code will help you understand WHY it broke.

### 4. Use the Logs
Every solution includes structured logging. Read the logs to see what's actually happening.

### 5. Work at Your Own Pace
This isn't a race. Spend a day on one concept if you need to. Deep understanding beats fast completion.

### 6. Experiment Fearlessly
Try adding features, changing parameters, breaking things. Git lets you reset if needed. Claude Code helps you debug.

---

## 🎯 Example Questions to Ask Claude Code

**Understanding Concepts:**
- "Explain embeddings in simple terms"
- "Why do we need RAG?"
- "What's the difference between a chatbot and an agent?"

**Understanding Code:**
- "Walk me through the agent loop line by line"
- "Why do we check finish_reason here?"
- "What does this function do and why?"

**Debugging:**
- "I'm getting this error, can you help?"
- "Why isn't my tool being called?"
- "The logs show X, what does that mean?"

**Extending:**
- "How would I add a new tool?"
- "Can this agent handle multiple users?"
- "How do I make this production-ready?"

**Connecting Ideas:**
- "How does this relate to ChatGPT?"
- "Where would I use this in real life?"
- "What are the limitations of this approach?"

---

## 🚨 Common Mistakes to Avoid

### Mistake 1: Skipping Setup (Module 0)
**Don't skip it!** Setup problems cause 90% of issues. Complete Module 0 first.

### Mistake 2: Jumping to Solutions Without Reading Concepts
You'll just copy code without understanding. Read CONCEPTS first!

### Mistake 3: Not Using Claude Code
This course is DESIGNED for AI-assisted learning. Don't struggle alone - ask Claude!

### Mistake 4: Rushing Through Modules
Slow down! Deep understanding in Module 1 makes Modules 2-4 way easier.

### Mistake 5: Not Experimenting
Reading code isn't learning. Modify it, break it, fix it!

---

## 📖 File Structure Quick Reference

```
AI-Agent-Engineering-Course/
├── START_HERE.md                    # ← You are here!
├── README.md                        # Course overview
├── .claude/prompts/professor.md     # Claude Code's instructions
│
├── setup/                           # Module 0: Get environment ready
│   ├── README.md
│   ├── requirements.txt
│   └── verify_setup.py
│
├── module_1_foundations/            # Week 1 release
│   ├── README.md                    # Module overview
│   ├── CONCEPTS.md                  # Theory to read first
│   ├── PROJECT.md                   # Architecture to read second
│   └── SOLUTION/                    # Working code to study third
│       └── simple_agent.py
│
├── module_2_memory/                 # Week 2 release
│   ├── README.md
│   ├── CONCEPTS.md                  # RAG, embeddings, vectors
│   ├── PROJECT.md                   # Memory agent architecture
│   └── SOLUTION/
│       └── memory_agent.py
│
├── module_3_tools/                  # Week 3 release
│   └── [Similar structure]
│
├── module_4_multi_agent/            # Week 4 release
│   └── [Similar structure]
│
└── mcp_addon/                       # Week 5 release
    └── [Similar structure]
```

---

## 🎉 You're Ready!

**To get started:**

1. ✅ Complete **Module 0: Setup** (setup/README.md)
2. ✅ Open Claude Code in this directory
3. ✅ Tell Claude: `"Read .claude/prompts/professor.md"`
4. ✅ Start learning: `"I want to start Module 1"`

**Remember:**
- Claude Code is your tutor, not your code generator
- All solutions are tested and working
- Ask questions freely
- Learn at your own pace
- Experiment and break things

---

## 🆘 Need Help?

**If you're stuck:**
1. Ask Claude Code for help (it has read all the docs)
2. Check the module's README for common issues
3. Look at the logs (JSONL files show what's happening)
4. Open an issue on GitHub: [Issues](https://github.com/GeneArnold/AI-Agent-Engineering-Course/issues)

---

## 🙏 A Note from the Creator

This course represents my learning journey with Claude Code. I'm sharing everything I learned, tested, and debugged.

Every solution works. Every concept is explained. Every module builds on the last.

Take your time. Ask questions. Experiment freely. You're learning a valuable skill that will serve you for years.

**Happy building!** 🚀

—Gene Arnold

---

**Now:** Complete setup, then tell Claude Code to read `.claude/prompts/professor.md` and start Module 1!
