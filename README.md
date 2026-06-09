# build-an-agent

**Build a working AI agent on your laptop — no cloud account, no GPU, no vendor lock-in.**

This is a brev-free rebuild of the kind of "build an agent" workshop that
normally runs on a managed cloud-GPU platform. Everything here runs on a
normal laptop against a free hosted API. Three short parts take you from
*"what even is an agent"* to a retrieval-grounded shopping assistant whose
answers you can actually measure.

> Built and maintained by [MEMOTECH](https://memotech.ch) — IT expertise since 1998 · Swiss Based.

---

## For decision-makers — read this (3 minutes, no code)

An **AI agent** is software that, given a goal, *decides which steps to
take* instead of following a fixed script. A shopping agent asked for "a
warm jacket under CHF 250" decides on its own to search the catalogue,
read a product's details, and compose an answer.

This repository teaches that idea by building one — small, in the open,
with nothing hidden. By the end you will understand, concretely, what the
"AI assistant" in every vendor pitch this year actually is.

The honest part: this tutorial builds a **demo**. A demo agent and a
production agent that touches your real catalogue, your real customers and
your real revenue are different animals. The table near the bottom —
[**What this tutorial shows vs. what production needs**](#what-this-tutorial-shows-vs-what-production-needs)
— is the most important thing on this page if you are evaluating agents
for your business.

## For developers

Three parts. Each is a self-contained folder with its own README:

| Part | You build | Key idea | GPU? |
|---|---|---|---|
| [Part 1 — Build an Agent](part-1-build-an-agent/) | A tool-calling shopping assistant | An agent is a loop: model → tool → model | No |
| [Part 2 — Agentic RAG](part-2-agentic-rag/) | The same agent, grounded in a product catalogue | Retrieval, so it answers from real data | No |
| [Part 3 — Evaluation & Guardrails](part-3-evaluation-guardrails/) | An evaluation + guardrail harness | "Is it good? Is it safe?" — measured, not hoped | No |

Part 1 is built **twice** on purpose: once as a plain Python loop (so you
see what an agent really is), then once with LangGraph (so you see what a
framework adds). Nothing in the three parts needs a GPU — it all runs
against a hosted API.

Each part also has a companion deep-dive on *m3mo Bytes*:

- Part 1 — [An AI Agent Is Just a Loop](https://mehmetgoekce.substack.com/p/an-ai-agent-is-just-a-loop)
- Part 2 — [The Product Your Search Bar Can't Find](https://mehmetgoekce.substack.com/p/the-product-your-search-bar-cant)
- Part 3 — [A Fluent Answer and a Correct Answer Look the Same](https://mehmetgoekce.substack.com/p/a-fluent-answer-and-a-correct-answer)

## Setup — 10 minutes

Full walkthrough in [setup.md](setup.md). Short version:

1. Get a free API key at <https://build.nvidia.com> (no GPU, no credit card).
2. `cp .env.example .env` and paste your key.
3. `uv sync` (or `pip install -e .`), then `jupyter lab`.

## Runs anywhere — that is the point

The default configuration uses the hosted **NVIDIA Nemotron™** model: free
tier, no GPU. But **no tutorial code is provider-specific.** Every model
call goes through [`llm.py`](llm.py), which speaks the OpenAI
chat-completions protocol. Point `.env` at OpenAI, a local
[Ollama](https://ollama.com), or a self-hosted vLLM and every notebook
still runs unchanged. Removing the cloud-platform lock-in is the whole
reason this rebuild exists.

## What this tutorial shows vs. what production needs

A demo proves the idea. It does **not** make the idea production-ready.
The gap between the two columns below is real engineering work:

| This tutorial (demo) | Your production agent needs |
|---|---|
| Sample catalogue, 12 products | Real catalogue, 10k–100k SKUs, data-quality cleanup |
| A notebook on your laptop | Deployment, scaling, a latency and cost budget per query |
| No guardrails | An agent that never invents prices, delivery dates or product facts |
| A ~25-item evaluation set | Continuous evaluation in production, regression monitoring |
| No data-protection context | Swiss nDSG compliance, data residency |
| A standalone agent | Integration into your real Shopware checkout / Store API |

**That right-hand column is what MEMOTECH does.** If you want an agent like
this running on *your* product catalogue, start with a free needs analysis:
[memotech.ch/agentic-commerce](https://memotech.ch/agentic-commerce) ·
[mehmetgoekce@memotech.ch](mailto:mehmetgoekce@memotech.ch).

## Credits & licence

Independent **clean-room rebuild** — inspired by NVIDIA's "build an agent"
workshop, but written from scratch with its own code and examples. Not
affiliated with, sponsored by, or endorsed by NVIDIA; the tutorial simply
uses NVIDIA's publicly available free API as one (swappable) option.

Licensed under [Apache-2.0](LICENSE). © 2026 MEMOTECH.
