# Part 3 — Evaluation & Guardrails

## For decision-makers

Parts 1 and 2 built an agent that gives fluent, confident answers. Here is
the uncomfortable truth no demo shows you: **a fluent answer and a correct
answer look exactly the same.** An agent that invents a price, recommends a
sold-out product, or confidently describes an item you do not sell will say
it just as smoothly as it says something true.

Before an agent talks to real customers, you need to answer one question:
*how often is it right — and how do you know?* This part builds the harness
that answers it, in two layers:

- **Guardrails** — automatic, deterministic checks for the things that must
  never happen: an invented product, a wrong price, a sold-out item
  recommended as available. These are the non-negotiables. They cost
  nothing to run, and they either pass or fail — no judgement call.
- **Quality scoring** — an LLM-as-judge that rates how *helpful* each answer
  is. The softer, qualitative half.

The output is a **scorecard**: pass rates, an average quality score, and a
list of every failure. That scorecard is what turns "the demo looked good"
into a number you can put in front of a decision.

**From demo to production:** this part checks 20 questions, once. A
production agent is evaluated continuously — every change re-scored against
a growing test set, regressions caught before customers see them, and the
guardrails wired into the live system so a bad answer is *blocked*, not just
counted. That is the difference between an agent you demo and an agent you
trust with revenue.

## For developers

One notebook, `01-evaluation.ipynb`:

1. **The system under test** — a compact RAG `shop_assistant()` (the Part 2
   assistant, condensed).
2. **Guardrails** — three deterministic checks: cited product ids are real,
   stated prices match the catalogue, out-of-stock items are flagged. Plain
   Python, no LLM, instant.
3. **LLM-as-judge** — one transparent prompt that scores answer quality 1–5
   against a per-question rubric.
4. **The eval loop** — run the assistant over `eval_dataset.json`, apply the
   guardrails and the judge to every answer, print a scorecard.

Files in this folder:

- `eval_dataset.json` — 20 test questions, each with a short rubric of what
  a good answer should do.
- `01-evaluation.ipynb` — the notebook above.

It evaluates the assistant from Part 2 (it retrieves over the same
`../part-2-agentic-rag/catalog/`) and checks answers against the structured
facts in `../part-1-build-an-agent/products.json`.

### Why not RAGAS?

Frameworks like [RAGAS](https://docs.ragas.io) automate richer RAG metrics
(faithfulness, context precision, answer relevancy). They are worth knowing
— but they make many LLM calls per sample, expect well-formed JSON from the
judge model, and hide the mechanics. A tutorial wants the opposite: see
every check. A hand-built harness also makes the point that the single most
important guardrail for a shop — *never invent a price* — is a five-line
deterministic function, not a metric you import. Reach for RAGAS once you
have outgrown this; the principle is identical.
