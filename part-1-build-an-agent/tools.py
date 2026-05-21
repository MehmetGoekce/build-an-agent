# pyright: strict
"""
Commerce tools for the shopping-assistant agent.

These are plain Python functions. A "tool" is nothing more than a function
the model is allowed to call — these are deliberately ordinary so you can
see that for yourself. Both notebooks in this folder import them:

  * 01-raw-agent.ipynb        describes them with a hand-written JSON schema
  * 02-langgraph-agent.ipynb  wraps them with the @tool decorator

Same functions, two ways of handing them to a model.
"""
import json
from pathlib import Path
from typing import TypedDict


class Product(TypedDict):
    """One row of the product catalogue (see products.json)."""

    product_id: str
    name: str
    category: str
    price_chf: float
    tags: list[str]
    in_stock: bool
    rating: float
    description: str


_CATALOG: list[Product] = json.loads(
    (Path(__file__).parent / "products.json").read_text()
)


def search_products(query: str) -> str:
    """Search the product catalogue by keyword.

    Returns a JSON list of matching products (id, name, price, category).
    """
    q = query.lower().strip()
    hits = [p for p in _CATALOG if _matches(p, q)]

    # Fall back to per-word matching so "warm jacket" still finds "jacket".
    if not hits:
        words = [w for w in q.split() if len(w) > 2]
        hits = [p for p in _CATALOG if any(_matches(p, w) for w in words)]

    return json.dumps(
        [
            {
                "product_id": p["product_id"],
                "name": p["name"],
                "price_chf": p["price_chf"],
                "category": p["category"],
                "in_stock": p["in_stock"],
            }
            for p in hits[:5]
        ]
    )


def get_product_details(product_id: str) -> str:
    """Return the full record for one product, by its product_id, as JSON."""
    for p in _CATALOG:
        if p["product_id"].lower() == product_id.lower().strip():
            return json.dumps(p)
    return json.dumps({"error": f"No product found with id '{product_id}'"})


def _matches(product: Product, term: str) -> bool:
    """True if `term` appears anywhere in a product's searchable text."""
    haystack = " ".join(
        [product["name"], product["category"], " ".join(product["tags"])]
    ).lower()
    return term in haystack
