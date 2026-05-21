"""
llm.py — the one place this tutorial talks to a language model.

Every notebook in build-an-agent goes through this file. The tutorial is
provider-agnostic on purpose: it speaks the OpenAI chat-completions
protocol, which NVIDIA, OpenAI, Ollama, vLLM and most others expose.

Swap providers by editing .env — never the tutorial code.
"""
from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

_NVIDIA_DEFAULT = "https://integrate.api.nvidia.com/v1"


def _require(name: str) -> str:
    """Read an env var, with a friendly error if it is still a placeholder."""
    value = os.getenv(name, "")
    if not value or "REPLACE-ME" in value:
        raise RuntimeError(
            f"{name} is not set. Copy .env.example to .env and paste your "
            f"API key. See setup.md for a 2-minute walkthrough."
        )
    return value


def llm_config() -> dict:
    """Return {base_url, api_key, model} for the chat model."""
    return {
        "base_url": os.getenv("LLM_BASE_URL", _NVIDIA_DEFAULT),
        "api_key": _require("LLM_API_KEY"),
        "model": os.getenv("LLM_MODEL", "nvidia/nemotron-3-nano-30b-a3b"),
    }


def embed_config() -> dict:
    """Return {base_url, api_key, model} for the embedding model."""
    return {
        "base_url": os.getenv("EMBED_BASE_URL", os.getenv("LLM_BASE_URL", _NVIDIA_DEFAULT)),
        "api_key": _require("EMBED_API_KEY"),
        "model": os.getenv("EMBED_MODEL", "nvidia/nv-embedqa-e5-v5"),
    }


def raw_client():
    """A plain OpenAI-SDK client — used by the 'minimal-first' notebooks."""
    from openai import OpenAI

    cfg = llm_config()
    return OpenAI(base_url=cfg["base_url"], api_key=cfg["api_key"])


def chat_model(temperature: float = 0.1):
    """A LangChain chat model — used by the LangGraph notebooks."""
    from langchain_openai import ChatOpenAI

    cfg = llm_config()
    return ChatOpenAI(
        model=cfg["model"],
        base_url=cfg["base_url"],
        api_key=cfg["api_key"],
        temperature=temperature,
    )


if __name__ == "__main__":
    # Quick connectivity check:  python llm.py
    cfg = llm_config()
    print(f"Endpoint : {cfg['base_url']}")
    print(f"Model    : {cfg['model']}")
    print("Calling the model ...")
    reply = raw_client().chat.completions.create(
        model=cfg["model"],
        messages=[{"role": "user", "content": "Reply with exactly: connection ok"}],
        max_tokens=16,
    )
    print(f"Reply    : {reply.choices[0].message.content.strip()}")
