# 🧠 Multi-Agent Research & Writing System

A modular **multi-agent pipeline** built with **OpenAI**, **LangChain**, and **Gradio**.  
This system coordinates three AI agents — **Researcher**, **Writer**, and **Critic** — to automatically research a topic, generate structured content, and review it for quality.

---

## 🚀 Features

- **Multi-Agent Orchestration**
  - Research Agent → gathers topic info via Wikipedia & APIs
  - Writer Agent → creates a structured, human-like article
  - Critic Agent → evaluates, improves, and suggests edits

- **Pipeline-Based Orchestrator**
  - Passes data seamlessly between agents
  - Saves intermediate outputs for transparency

- **Interactive Web App (Gradio UI)**
  - Run everything in a clean, tabbed interface
  - View Research (JSON), Draft, and Critic Feedback in real time

- **Configurable via Environment Variables**
  - Supports `.env` for API keys and model selection

---

## 🏗️ Project Structure

