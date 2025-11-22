# Module 0: Environment Setup

Before you can build AI agents, you need to set up your development environment. This should take about 5-10 minutes.

## Prerequisites

- **Python 3.11 or higher** - [Download here](https://www.python.org/downloads/)
- **Git** - [Download here](https://git-scm.com/downloads)
- **Code editor** - VS Code, Sublime Text, or your preference
- **Claude Code CLI** (optional but recommended) - [Install here](https://github.com/anthropics/claude-code)

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone https://github.com/GeneArnold/AI-Agent-Engineering-Course.git
cd AI-Agent-Engineering-Course
```

### 2. Create Virtual Environment

A virtual environment keeps your project dependencies isolated.

```bash
# Create venv
python3 -m venv venv

# Activate it
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows
```

You should see `(venv)` in your terminal prompt when activated.

### 3. Install Dependencies

```bash
pip install -r setup/requirements.txt
```

This installs:
- `openai` - OpenAI API client
- `anthropic` - Anthropic API client
- `chromadb` - Vector database for memory
- `python-dotenv` - Environment variable management
- And more (see `requirements.txt`)

### 4. Configure API Keys

You'll need at least ONE of these:
- **OpenAI API key** - [Get one here](https://platform.openai.com/api-keys)
- **Anthropic API key** - [Get one here](https://console.anthropic.com/)

```bash
# Copy the example env file
cp setup/.env.example .env

# Edit .env and add your API keys
nano .env  # or use your preferred editor
```

Your `.env` file should look like:
```
# At least one of these is required
OPENAI_API_KEY=sk-...your-key-here...
ANTHROPIC_API_KEY=sk-ant-...your-key-here...

# Optional (for Module 3)
OLLAMA_BASE_URL=http://localhost:11434
```

**Important:** Never commit your `.env` file! It's already in `.gitignore`.

### 5. Verify Setup

Run the verification script to make sure everything works:

```bash
python setup/verify_setup.py
```

You should see:
```
✅ Python version: 3.12.3
✅ Virtual environment: Active
✅ OpenAI API: Connected
✅ Dependencies: All installed

🎉 Setup complete! You're ready to start Module 1.
```

## Troubleshooting

### Python version too old
```bash
# Check your Python version
python3 --version

# If < 3.11, download the latest from python.org
```

### pip install fails
```bash
# Upgrade pip first
pip install --upgrade pip

# Then try again
pip install -r setup/requirements.txt
```

### API key not working
- Make sure you copied the FULL key (they're long!)
- Check for extra spaces before/after the key
- Verify the key is active in your provider's dashboard

### Virtual environment issues
```bash
# Delete and recreate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r setup/requirements.txt
```

## Optional: Docker Setup

Docker is only needed for Module 4 (MCP track). You can install it later:
- [Docker Desktop](https://www.docker.com/products/docker-desktop)

## Optional: Claude Code CLI

Claude Code makes this course much more interactive:

```bash
# Install Claude Code
npm install -g @anthropic/claude-code

# Or use official instructions:
# https://github.com/anthropics/claude-code
```

## Next Steps

Once setup is complete:

**With Claude Code:**
```bash
claude-code
# Then say: "Start Module 1"
```

**Without Claude Code:**
- Read [module_1_foundations/README.md](../module_1_foundations/README.md)
- Work through the concepts and project
- Check your work against the solution

---

**Setup complete?** Head to [Module 1: Agent Foundations](../module_1_foundations/README.md)

Need help? [Open an issue](https://github.com/GeneArnold/AI-Agent-Engineering-Course/issues)
