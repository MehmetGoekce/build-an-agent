"""
llm.py — the one place this tutorial talks to a language model.

Every notebook in build-an-agent goes through this file. The tutorial is
provider-agnostic on purpose: it speaks the OpenAI chat-completions
protocol, which NVIDIA, OpenAI, Ollama, vLLM and most others expose.

Swap providers by editing .env — never the tutorial code.
"""
from __future__ import annotations

import os
from typing import TYPE_CHECKING

from dotenv import load_dotenv

if TYPE_CHECKING:
    from langchain_openai import ChatOpenAI
    from openai import OpenAI

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


def llm_config() -> dict[str, str]:
    """Return {base_url, api_key, model} for the chat model."""
    return {
        "base_url": os.getenv("LLM_BASE_URL", _NVIDIA_DEFAULT),
        "api_key": _require("LLM_API_KEY"),
        "model": os.getenv("LLM_MODEL", "nvidia/nemotron-3-nano-30b-a3b"),
    }


def embed_config() -> dict[str, str]:
    """Return {base_url, api_key, model} for the embedding model."""
    return {
        "base_url": os.getenv(
            "EMBED_BASE_URL", os.getenv("LLM_BASE_URL", _NVIDIA_DEFAULT)
        ),
        "api_key": _require("EMBED_API_KEY"),
        "model": os.getenv("EMBED_MODEL", "nvidia/nv-embedqa-e5-v5"),
    }


def _extra_body() -> dict[str, object]:
    """Provider-specific request options.

    NVIDIA's Nemotron models are *reasoning* models: by default they spend
    tokens "thinking" before they answer. That is slower, costs more, and
    can leave the real answer empty or wrapped in <think> tags. For a
    tutorial we want direct answers, so we switch reasoning off.

    This option is NVIDIA-specific, so it is only sent to NVIDIA endpoints.
    Point .env at OpenAI / Ollama / vLLM and this returns {} — the tutorial
    code stays provider-agnostic.
    """
    if "nvidia" in os.getenv("LLM_BASE_URL", _NVIDIA_DEFAULT):
        return {"chat_template_kwargs": {"enable_thinking": False}}
    return {}


# Pass this as `extra_body=EXTRA_BODY` on every chat call (see the notebooks).
EXTRA_BODY: dict[str, object] = _extra_body()


def embed_extra_body(input_type: str) -> dict[str, object]:
    """Provider-specific options for an embedding request (Part 2 onwards).

    NVIDIA's nv-embedqa models are *asymmetric* retrieval models: a search
    query and a stored document are embedded differently, and the model has
    to be told which is which. Pass "passage" when you embed a catalogue
    document and "query" when you embed a user's question. Getting this
    wrong quietly wrecks retrieval accuracy.

    This option is NVIDIA-specific. Point .env at OpenAI / Ollama and it
    returns {} — their embedding models are symmetric and need no hint, so
    the tutorial code stays provider-agnostic.
    """
    base = os.getenv("EMBED_BASE_URL", os.getenv("LLM_BASE_URL", _NVIDIA_DEFAULT))
    if "nvidia" in base:
        return {"input_type": input_type, "truncate": "END"}
    return {}


def raw_client() -> OpenAI:
    """A plain OpenAI-SDK client — used by the 'minimal-first' notebooks."""
    from openai import OpenAI

    cfg = llm_config()
    return OpenAI(base_url=cfg["base_url"], api_key=cfg["api_key"])


def embed_client() -> OpenAI:
    """A plain OpenAI-SDK client pointed at the embedding endpoint (Part 2)."""
    from openai import OpenAI

    cfg = embed_config()
    return OpenAI(base_url=cfg["base_url"], api_key=cfg["api_key"])


def chat_model(temperature: float = 0.1) -> ChatOpenAI:
    """A LangChain chat model — used by the LangGraph notebooks."""
    from langchain_openai import ChatOpenAI
    from pydantic import SecretStr

    cfg = llm_config()
    return ChatOpenAI(
        model=cfg["model"],
        base_url=cfg["base_url"],
        api_key=SecretStr(cfg["api_key"]),
        temperature=temperature,
        extra_body=EXTRA_BODY,
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
        max_tokens=64,
        extra_body=EXTRA_BODY,
    )
    content = reply.choices[0].message.content
    print(f"Reply    : {content.strip() if content else '(empty response)'}")
