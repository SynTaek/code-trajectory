# Code Trajectory MCP Server

[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-blue?style=flat&logo=anthropic)](https://modelcontextprotocol.io)
[![Python Version](https://img.shields.io/badge/python-3.14+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Code Style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/SynTaek/code-trajectory-mcp/graphs/commit-activity)
[![GitHub Stars](https://img.shields.io/github/stars/SynTaek/code-trajectory-mcp?style=social)](https://github.com/SynTaek/code-trajectory-mcp)

[![README](https://img.shields.io/badge/README-ENGLISH-blue)](README.md)
[![README_KR](https://img.shields.io/badge/README-KOREAN-blue)](README_ko.md)

> **Keep your coding momentum across AI sessions.**
>
> *Turn "State-Based" coding into "Flow-Based" development.*

**Code Trajectory MCP** is a Model Context Protocol (MCP) server that gives Large Language Models (LLMs) a persistent memory of your coding history. It tracks the *evolution* of your code in a shadow repository, allowing you to switch AI chat sessions without losing the context of your momentum, architectural intent, or recent decisions.

-----

## 🚀 Why Code Trajectory?

### The Problem: "New Session Amnesia"

Every developer using LLMs knows the struggle:

1.  **Context Overflow:** You are in a deep coding flow, but the chat gets too long. The LLM slows down or hits the token limit.
2.  **Forced Reset:** You have to start a **New Chat**.
3.  **Lost Context:** The new AI session knows nothing about your last 2 hours of work. You waste time re-explaining: *"I'm refactoring the login... remember we decided to use JWT?"*

### The Solution: Persistent Momentum

**Code Trajectory** acts as an external "hippocampus" (long-term memory) for your AI.

  * **Before:** The AI only sees the code as it is *now*.
  * **With Code Trajectory:** The AI sees *how* the code evolved and *where* you left off.
    > *"I see you were in the middle of migrating `auth.py` to OAuth2 in the previous session. I'll pick up exactly where you left off."*

-----

## ✨ Key Features

### 1\. ♾️ Session Continuity

This is the core superpower. When you start a fresh chat, the AI can query this MCP to retrieve a summary of your **recent trajectory**. It bridges the gap between disjointed chat sessions, ensuring your architectural decisions survive the "New Chat" button.

### 2\. ⚡ Automated Shadow Snapshots

A background file watcher automatically creates micro-commits in a **hidden shadow git repository** (`.trajectory`) whenever you save a file.

  * **Zero Pollution:** Your main project's `git` history remains clean.
  * **Full Granularity:** Every save is recorded, allowing the AI to analyze your trial-and-error process.

### 3\. 🌊 "Flow" Awareness

Current LLMs operate like a GPS that knows your location but not your speed. This tool provides the **vector**:

  * **`get_file_trajectory`**: Converts file history into a narrative story (Past -\> Present).
  * **`get_global_trajectory`**: Analyzes the "Ripple Effect" of how recent changes in one file impacted others.

### 4\. 🎯 Intent & Noise Filtering

  * **Intent Recording:** You can explicitly tell the system: *"I am refactoring the Auth system."* This intent is tagged to all subsequent snapshots until changed.
  * **Smart Consolidation:** The `consolidate` feature squashes noisy "trial & error" snapshots into clean, meaningful history points when a task is done.

-----

## 🛠️ Tech Stack

  * **Runtime:** Python 3.14+
  * **Package Manager:** [uv](https://github.com/astral-sh/uv) (Blazing fast Python package installer)
  * **Core Libraries:** `mcp`, `gitpython`, `watchdog`

-----

## 📦 Installation & Setup

### 1\. Prerequisites

Ensure you have `uv` installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2\. Project Setup

Ensure the target project is a git repository (the MCP uses this to root itself, though it stores data in `.trajectory`).

```bash
cd /path/to/your/project
git init
```

### 3. Configure Your AI Client

* **Claude Desktop:** `claude_desktop_config.json`
* **Cursor / IDEs:** `settings.json` (or "MCP Servers" configuration)

```json
"mcpServers": {
    "code-trajectory": {
        "command": "uvx",
        "args": [
            "--from",
            "git+https://github.com/SynTaek/code-trajectory-mcp.git",
            "code-trajectory-mcp"
        ]
    }
}
```

### 4. Setup AI Instructions (Recommended)

To ensure the AI uses Code Trajectory autonomously and effectively, you must provide it with the operational guidelines.

1.  Copy the full content of **[`AGENT_GUIDE.md`](AGENT_GUIDE.md)** from this repository.
2.  Paste it into your AI's custom instructions or system prompt:
    * **Cursor:** Create or append to the `.cursorrules` file in your project root.
    * **Claude Projects:** Add to "Project Instructions".
    * **General LLMs:** Add to the "System Prompt" or "Custom Instructions".

> **Tip:** This guide teaches the AI when to query the trajectory and how to consolidate history, ensuring it acts as a proactive coding partner.

-----

## 🤖 Agent Workflow Guide

To get the most out of **Code Trajectory**, follow this workflow. It ensures your AI context remains intact across sessions.

### Step 1: Initialization (New Session)

When you start a **New Chat**, always begin with:

1.  **Configure:** Call `configure_project(path="/path/to/project")`.
2.  **Restore Context:** Call `get_session_summary()` or `get_global_trajectory()`.
      * *Result:* The AI downloads the "memory" of your previous session (e.g., *"Last edit was 5 mins ago in `User.ts`, intent was 'Fixing API bug'"*).

### Step 2: The Work Loop

1.  **Set Intent:** `set_trajectory_intent("Implementing Dark Mode")`
      * *Why:* This tags every file save with this goal, making the history semantic.
2.  **Work:** You or the AI edit files. The server auto-snapshots `[AUTO-TRJ]` in the background.

### Step 3: Consolidation (Task Complete)

1.  **Consolidate:** `consolidate("Completed Dark Mode implementation")`
      * *Why:* This cleans up the messy intermediate saves into one clear history node, marking a solid checkpoint for the *next* session.

-----

## 📊 Visualizing Your Momentum

Since `.trajectory` is a standard Git repository, you can visualize your "Thought Process" using standard tools.

  * **VSCode:** Open the `.trajectory` folder in a new window and use **Git Graph**.
  * **Terminal:**
    ```bash
    # View the narrative log
    git --git-dir=.trajectory/.git log --graph --oneline --all
    ```

## 📄 License

MIT