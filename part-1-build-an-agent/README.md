# Part 1 — Build an Agent

## For decision-makers

Everyone says "AI agent". Here is the whole idea in one sentence: **an agent
is a language model that is allowed to call functions, and decides for
itself which ones to call, in which order, until it has an answer.**

In this part the agent answers product questions for an outdoor-gear shop
— *"I need a warm jacket under CHF 250"* — by searching a catalogue. That
is the same shape of task a shopping assistant performs on a real
storefront.

Why it matters for your shop: this is the mechanism behind every "AI
assistant" you will be pitched this year. Seeing it work once — and seeing
how *little* there is to it — turns vendor demos from magic into something
you can evaluate.

**From demo to production:** the agent here searches 12 products in a JSON
file and forgets everything between questions. A storefront assistant
searches tens of thousands of SKUs, has to stay fast and cheap on every
query, and must never recommend an out-of-stock item or invent a price.
Part 2 and Part 3 take the first steps in that direction — the rest is
engineering work, and it is the work that decides whether an agent is an
asset or a liability.

## For developers

Two notebooks. The same agent, built twice:

1. **`01-raw-agent.ipynb`** — the agent as a plain Python `while` loop on
   top of the OpenAI SDK. No framework. Around 40 lines of actual agent
   logic. This is the notebook that de-mystifies the word "agent".
2. **`02-langgraph-agent.ipynb`** — the *same* agent rebuilt with LangGraph
   (`langchain.agents.create_agent`). Shorter, and streaming plus
   conversation memory come for free. This shows what a framework actually
   buys you — which only makes sense once you have seen what it replaces.

Shared code in this folder:

- `tools.py` — the two commerce tools (`search_products`, `get_product_details`)
- `products.json` — the sample catalogue (12 products)

The model connection comes from [`../llm.py`](../llm.py).

Run the notebooks top to bottom. Start with `01`.
