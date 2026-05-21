# Setup — about 10 minutes

You need: a laptop, Python 3.10 or newer, and an internet connection.
You do **not** need a GPU, a cloud account, or a credit card.

## 1. Get a free API key (~2 minutes)

The tutorial calls a hosted language model. The default is NVIDIA's free
tier — generous enough for the whole tutorial.

1. Go to <https://build.nvidia.com> and sign in (a free account).
2. Pick any model (for example *Nemotron*).
3. Click **Get API Key**. Copy the key — it starts with `nvapi-`.

> Prefer another provider? Any OpenAI-compatible endpoint works — OpenAI,
> a local [Ollama](https://ollama.com), or a self-hosted vLLM. See step 3.

## 2. Install the dependencies (~5 minutes)

Clone or download this repository, then from its root:

```bash
# Recommended: uv (https://docs.astral.sh/uv/)
uv sync

# Or with plain pip + a virtual environment
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

## 3. Configure your key (~1 minute)

```bash
cp .env.example .env
```

Open `.env` and paste your key into `LLM_API_KEY` and `EMBED_API_KEY`.

To use a different provider, change only the three `LLM_*` lines — for
example, for a local Ollama:

```
LLM_BASE_URL=http://localhost:11434/v1
LLM_API_KEY=ollama
LLM_MODEL=llama3.1
```

## 4. Check the connection

```bash
python llm.py
```

Expected output:

```
Endpoint : https://integrate.api.nvidia.com/v1
Model    : nvidia/nemotron-3-nano-30b-a3b
Calling the model ...
Reply    : connection ok
```

If you see `LLM_API_KEY is not set`, your `.env` still has the placeholder.

## 5. Open the notebooks

```bash
jupyter lab
```

Start with [`part-1-build-an-agent/01-raw-agent.ipynb`](part-1-build-an-agent/).
Run the cells top to bottom.

---

### A note on the free tier

The free tier is rate-limited (roughly 40 requests per minute) and metered
in credits. Parts 1 and 2 use very few calls. Part 3 evaluates a small
dataset and is deliberately kept to ~25 items so it stays inside the free
allowance. If you hit a rate limit, wait a minute and re-run the cell.
