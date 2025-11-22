# Weekly Release Workflow

**For Gene Arnold - How to Release New Modules Each Week**

This document explains how to copy content from your private learning repo to the public course repo and publish it.

---

## 📅 Release Schedule

**Every Tuesday at 9:00 AM PT:**

- **Week 0** (Nov 19): Setup + Module 1 instructions ✅
- **Week 1** (Nov 26): Module 1 solution + Module 2 instructions
- **Week 2** (Dec 3): Module 2 solution + Module 3 instructions
- **Week 3** (Dec 10): Module 3 solution + Module 4 + MCP instructions
- **Week 4** (Dec 17): Module 4 + MCP solutions
- **Week 5** (Dec 24): Course wrap-up + bonus content

---

## 🔄 Weekly Release Steps

### Step 1: Complete the Module in Your Private Repo

Work through the module with Claude Code in:
```
~/Workspace/AI_Agent_Engineering_Training/
```

Make sure you:
- ✅ Complete the project (e.g., `simple_agent.py`)
- ✅ Test it thoroughly
- ✅ Update your personal TRAINING_JOURNAL.md
- ✅ Commit your progress

### Step 2: Prepare Content for Public Release

Navigate to the public repo:
```bash
cd ~/Workspace/AI-Agent-Engineering-Course
```

### Step 3: Copy Solution from Private to Public

**For Module 1 (Week 1 release):**

```bash
# Create SOLUTION directory
mkdir -p module_1_foundations/SOLUTION

# Copy your completed agent
cp ~/Workspace/AI_Agent_Engineering_Training/module_1_foundations/simple_agent.py \
   module_1_foundations/SOLUTION/

# Optional: Copy your reflection notes (adapted)
# Create SOLUTION_NOTES.md with key insights
```

**For Module 2 (Week 2 release):**

```bash
# Create Module 2 content and solution
mkdir -p module_2_memory/SOLUTION

# Copy solution
cp ~/Workspace/AI_Agent_Engineering_Training/module_2_memory/memory_agent.py \
   module_2_memory/SOLUTION/

# Copy any supporting files
cp ~/Workspace/AI_Agent_Engineering_Training/module_2_memory/*.py \
   module_2_memory/SOLUTION/
```

*Repeat for subsequent modules*

### Step 4: Add/Update Module Instructions

If releasing a NEW module (e.g., Module 2), add the content files:

```bash
# Copy CONCEPTS.md, PROJECT.md, README.md from your private notes
# OR write them based on what you learned

# Example structure:
module_2_memory/
├── README.md         # Module overview
├── CONCEPTS.md       # Core concepts
├── PROJECT.md        # Build spec
└── SOLUTION/         # Your working code
    └── memory_agent.py
```

**Template:** Use Module 1 as a template for structure.

### Step 5: Update Main README

Edit `/README.md` to mark the module as released:

```markdown
## 📅 Weekly Release Schedule

**New modules released every Tuesday:**
- ✅ **Week 0** (Nov 19): Setup + Module 1 instructions
- ✅ **Week 1** (Nov 26): Module 1 solution + Module 2 instructions  ← Update this
- 📅 **Week 2** (Dec 3): Module 2 solution + Module 3 instructions
...
```

### Step 6: Create Release Notes

Create a file: `RELEASES/week-X-release-notes.md`

```markdown
# Week X Release - Module Y

**Release Date:** Nov 26, 2025

## 🎉 What's New

### Module 1 Solution Released
- Complete working `simple_agent.py`
- Detailed comments and explanations
- Reference implementation

### Module 2 Instructions Available
- Learn about embeddings and vector search
- Build a memory-enabled agent
- Solve the context growth problem

## 📚 What to Do This Week

1. Review Module 1 solution
2. Compare with your implementation
3. Start Module 2 concepts
4. Ask questions via GitHub issues

## 🔗 Links

- [Module 1 Solution](module_1_foundations/SOLUTION/)
- [Module 2 Instructions](module_2_memory/README.md)

---

**Next week:** Module 2 solution + Module 3 instructions
```

### Step 7: Commit and Push

```bash
# Add all changes
git add .

# Create detailed commit message
git commit -m "Week 1 Release: Module 1 solution + Module 2 instructions

Added:
- Module 1 SOLUTION/ with simple_agent.py
- Module 2 full content (README, CONCEPTS, PROJECT)
- Week 1 release notes

Students can now:
- Review Module 1 reference implementation
- Start learning Module 2 concepts
- Begin building memory_agent.py

Next release: Module 2 solution (Dec 3)
"

# Push to GitHub
git push origin main
```

### Step 8: Create GitHub Release (Optional but Recommended)

On GitHub:
1. Go to **Releases** → **Draft a new release**
2. **Tag:** `week-1-release`
3. **Title:** "Week 1: Module 1 Solution + Module 2"
4. **Description:** Copy from release notes
5. **Publish release**

This sends notifications to watchers!

### Step 9: Create Social Media Announcement

**LinkedIn Post Template:**

```
🚀 Week 1 of the AI Agent Engineering Course is live!

This week:
✅ Module 1 solution released (simple_agent.py)
✅ Module 2 now available (Memory & Vector Search)

Module 1 taught us:
- Agent loops are surprisingly simple
- How LLMs use tools
- The context growth problem

Module 2 solves that problem with:
- Embeddings & semantic search
- Vector databases (ChromaDB)
- RAG pattern implementation

Free, open-source, designed for hands-on learning with Claude Code.

👉 https://github.com/GeneArnold/AI-Agent-Engineering-Course

#AI #Agents #LLM #OpenSource #MachineLearning
```

**Twitter/X Post Template:**

```
🤖 Week 1 of my AI Agent Engineering Course is live!

📦 Module 1 solution
🧠 Module 2: Memory & RAG

Learn to build real agents from scratch.
Free & open source.

https://github.com/GeneArnold/AI-Agent-Engineering-Course

#AI #Agents
```

---

## 🔍 Pre-Release Checklist

Before pushing each week, verify:

- [ ] Solution code runs without errors
- [ ] All paths/imports work in public repo
- [ ] No API keys or secrets in code
- [ ] README updated with release status
- [ ] Release notes created
- [ ] Links in documentation work
- [ ] Code comments are clear
- [ ] Module instructions are complete

---

## 🐛 Common Issues

### Issue: File Paths Don't Match

**Cause:** Private repo uses different structure
**Fix:** Adjust relative paths when copying

```python
# Private repo
LOG_FILE = "logs/simple_agent.jsonl"

# Public repo (might be same, but verify)
LOG_FILE = "logs/simple_agent.jsonl"
```

### Issue: Missing Dependencies

**Cause:** You installed something in private repo not in requirements.txt
**Fix:** Update `setup/requirements.txt` before release

```bash
# In private repo, check what's installed
pip freeze > temp_requirements.txt

# Compare with public repo
diff temp_requirements.txt ~/Workspace/AI-Agent-Engineering-Course/setup/requirements.txt

# Add missing packages
```

### Issue: Code References Personal Info

**Cause:** Hardcoded paths or names
**Fix:** Search and replace before committing

```bash
# Search for your name or paths
grep -r "genearnold" .
grep -r "/home/genearnold" .

# Replace with generic equivalents
```

---

## 📊 Metrics to Track (Optional)

After each release, check:

- ⭐ **Stars:** How many people starred the repo?
- 👁️ **Views:** GitHub traffic stats
- 🍴 **Forks:** How many people forked it?
- 💬 **Issues:** Questions or bug reports?
- 🐦 **Engagement:** Social media responses

Use this feedback to improve future modules!

---

## 🎯 Quick Reference

### Week 1 (Module 1 Solution)
```bash
mkdir -p module_1_foundations/SOLUTION
cp ~/Workspace/AI_Agent_Engineering_Training/module_1_foundations/simple_agent.py module_1_foundations/SOLUTION/
git add . && git commit -m "Week 1 Release: Module 1 solution" && git push
```

### Week 2 (Module 2 Solution)
```bash
mkdir -p module_2_memory/SOLUTION
cp ~/Workspace/AI_Agent_Engineering_Training/module_2_memory/*.py module_2_memory/SOLUTION/
git add . && git commit -m "Week 2 Release: Module 2 solution" && git push
```

---

## ❓ Questions?

If you're unsure about anything, you can always:
1. Check how you did it for the previous week
2. Open a draft PR to preview changes
3. Use Claude Code to help prepare the release!

---

**Happy releasing!** 🚀
