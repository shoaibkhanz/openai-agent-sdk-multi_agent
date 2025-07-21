# Multi-Agent Interaction using OpenAI Agent SDK Example

This project demonstrates how to build and orchestrate multiple intelligent
agents using the OpenAI Agent SDK. The system supports:

- **Tool-augmented agents** – Each agent can invoke domain-specific tools
  (e.g. SQL queries, metadata inspection).
- **Agent memory** – Agents maintain conversational context across multiple
  interactions.
- **Agent handoffs** – Tasks can be delegated between agents dynamically
  based on user intent.

The goal is to showcase how to design composable, intelligent agent systems
capable of working collaboratively and contextually.

---

## Installation

This project uses [`uv`](https://github.com/astral-sh/uv), a modern Python
package manager designed for speed and reliability.

### Step 1: Install `uv`

If `uv` is not already installed, you can install it by running (mac and linux):
explore `uv` docs [here](https://docs.astral.sh/uv/getting-started/installation/)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Alternatively, if you use Homebrew:

```bash
brew install uv
```

### Step 2: Sync the environment

Once `uv` is installed, synchronise the project environment using:

```bash
uv sync
```

## Environment Setup

To run the project, create a `.env` file in the project root directory and
add your OpenAI API key:

```bash
OPENAI_API_KEY=your-openai-api-key-here
```

## Running the Project

To start the main application, use the following command:

```bash
uv run python src/main.py
```

## Project Overview

- Built using the OpenAI Agent SDK
- Modular and extensible agent definitions
- Enables stateful interaction and inter-agent communication
- Designed for experimentation with agent-based systems
