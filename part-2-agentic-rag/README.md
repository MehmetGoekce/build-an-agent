# Part 2 — Agentic RAG

## For decision-makers

Your product catalogue is full of language your customers never use. A
description says *"three-layer hardshell, taped seams"*; the customer types
*"a jacket that keeps the rain out"*. Keyword search — the kind in Part 1,
and the kind in most webshop search bars — needs the words to line up. When
they don't, the right product is simply invisible.

**Retrieval** fixes that: it searches by *meaning*, not spelling, so the
customer's words and your catalogue's words can be completely different and
still connect. This is the single most valuable upgrade you can make to a
shopping agent — the difference between an agent that understands your
catalogue and one that just matches strings.

In this part the agent answers questions like *"what should I wear to stay
dry in a downpour?"* by retrieving the genuinely relevant products — even
when none of those words appear in the product text.

**From demo to production:** retrieval over 12 short documents is easy.
Retrieval over 10k–100k real SKUs is an engineering discipline — splitting
long content into chunks, keeping the index fresh as stock and prices
change, filtering by category and availability, and *measuring* retrieval
quality so you know the agent is fetching the right thing. Part 3 is about
that last word: knowing.

## For developers

One notebook, `01-rag-agent.ipynb`, in four steps:

1. **Embed the catalogue** — every product document becomes a 1024-number
   vector via NVIDIA's `nv-embedqa-e5-v5`, stored in a FAISS index.
2. **Search by meaning** — `retrieve()` embeds a query and returns the
   nearest products. One function, about ten lines.
3. **Plain RAG** — retrieve once, paste the documents into the prompt,
   answer. The baseline.
4. **Agentic RAG** — wrap `retrieve()` as a `@tool` and hand it to the
   LangGraph agent from Part 1. Now the model decides when and what to
   search, and can search more than once for a multi-part question.

Files in this folder:

- `catalog/` — the knowledge base: one Markdown document per product (the
  same 12 products as Part 1, in prose instead of JSON rows).
- `01-rag-agent.ipynb` — the notebook above.

The model and embedding connections both come from [`../llm.py`](../llm.py).

### One NVIDIA-specific detail

`nv-embedqa-e5-v5` is an *asymmetric* retrieval model: it embeds a search
query differently from a stored document, and must be told which is which
(`input_type`: `"query"` / `"passage"`). `llm.py` keeps that in
`embed_extra_body()` and returns `{}` for providers that don't need it, so
the notebook itself stays provider-agnostic. Point `.env` at OpenAI or a
local embedding model and it still runs.
