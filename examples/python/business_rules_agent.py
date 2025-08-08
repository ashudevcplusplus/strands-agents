from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any

from strands import Agent, tool
from strands.models.ollama import OllamaModel

RUN_DIR = os.path.join("runlogs", "business_rules")


def _ensure_parent(path: str) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)


@dataclass
class OrderDecision:
    discount_percent: float
    free_shipping: bool
    require_manual_review: bool
    notes: list[str]
    rationale: str


def _safe_get(obj: dict[str, Any], key: str, default: Any = None) -> Any:
    value = obj.get(key, default)
    return value


@tool
def evaluate_order_rules(order_json: str) -> str:
    """Evaluate business rules for an order.

    The input must be a JSON object with keys:
    - customer_tier: one of "Gold" | "Silver" | "Bronze"
    - order_total: number (USD)
    - new_customer: boolean
    - item_category: e.g., "electronics", "apparel", "groceries"
    - stock_level: integer (units available)
    - region: e.g., "US", "EU"

    Returns a JSON string with fields: discount_percent, free_shipping,
    require_manual_review, notes, rationale.
    """
    try:
        order = json.loads(order_json)
    except json.JSONDecodeError as exc:
        return json.dumps({"error": f"invalid JSON: {exc}"})

    customer_tier = str(_safe_get(order, "customer_tier", "Bronze")).title()
    order_total = float(_safe_get(order, "order_total", 0.0))
    new_customer = bool(_safe_get(order, "new_customer", False))
    item_category = str(_safe_get(order, "item_category", "misc")).lower()
    stock_level = int(_safe_get(order, "stock_level", 0))
    region = str(_safe_get(order, "region", "US")).upper()

    notes: list[str] = []
    discount = 0.0

    # Tier-based base discount
    if customer_tier == "Gold":
        discount += 10.0
        notes.append("Gold base discount 10%")
    elif customer_tier == "Silver":
        discount += 5.0
        notes.append("Silver base discount 5%")
    else:
        notes.append("Bronze/no tier base discount 0%")

    # High-value order bonus
    if order_total > 1000:
        discount += 3.0
        notes.append("High-value order bonus +3% (> $1000)")

    # New customer welcome
    if new_customer and order_total >= 100:
        discount += 2.0
        notes.append("New customer welcome +2% (>= $100)")

    # Category-specific constraints
    if item_category == "electronics":
        # Risk/return constraints cap discounts for electronics
        if discount > 10.0:
            notes.append("Electronics discount capped at 10%")
        discount = min(discount, 10.0)
    elif item_category == "groceries":
        # Groceries excluded from discounts
        if discount > 0:
            notes.append("Groceries not discount-eligible — reset to 0%")
        discount = 0.0

    # Stock and risk checks
    require_manual_review = stock_level < 5 and order_total > 500
    if require_manual_review:
        notes.append("Low stock (<5) and high order value (> $500) — manual review required")

    # Region-specific compliance note (illustrative)
    if region == "EU":
        notes.append("EU region — ensure VAT invoice details are present")

    # Shipping policy
    free_shipping = order_total >= 200 or customer_tier == "Gold"
    if free_shipping:
        notes.append("Eligible for free shipping (tier or threshold)")

    decision = OrderDecision(
        discount_percent=round(discount, 2),
        free_shipping=free_shipping,
        require_manual_review=require_manual_review,
        notes=notes,
        rationale="; ".join(notes) if notes else "Standard rules applied",
    )

    return json.dumps(asdict(decision), ensure_ascii=False)


@tool
def log_decision(name: str, decision_json: str) -> str:
    """Append a timestamped business decision record to runlogs/business_rules/{name}.log.

    Args:
        name: logical identifier for the log file (e.g., order id)
        decision_json: JSON string from evaluate_order_rules
    """
    os.makedirs(RUN_DIR, exist_ok=True)
    ts = datetime.utcnow().isoformat() + "Z"
    path = os.path.join(RUN_DIR, f"{name}.log")
    _ensure_parent(path)
    try:
        # Normalize JSON for readability
        parsed = json.loads(decision_json)
        normalized = json.dumps(parsed, ensure_ascii=False, separators=(",", ":"))
    except Exception:
        normalized = decision_json
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {normalized}\n")
    return f"Appended decision entry to {path}"


def build_model() -> OllamaModel:
    model_tag = os.getenv("OLLAMA_MODEL", "qwen3:8b")
    return OllamaModel(host="http://localhost:11434", model_id=model_tag)


def build_business_rules_agent(model: OllamaModel) -> Agent:
    return Agent(
        model=model,
        system_prompt=(
            "You are a business rules agent.\n"
            "- Always compute decisions using evaluate_order_rules with a structured JSON input.\n"
            "- After deciding, summarize succinctly and record using log_decision.\n"
            "- Keep outputs concise and structured."
        ),
        tools=[evaluate_order_rules, log_decision],
    )


def _example_orders() -> list[dict[str, Any]]:
    return [
        {
            "id": "ORD-1001",
            "customer_tier": "Gold",
            "order_total": 1450.75,
            "new_customer": False,
            "item_category": "electronics",
            "stock_level": 3,
            "region": "US",
        },
        {
            "id": "ORD-1002",
            "customer_tier": "Silver",
            "order_total": 220.0,
            "new_customer": True,
            "item_category": "apparel",
            "stock_level": 25,
            "region": "EU",
        },
    ]


def main() -> None:
    if os.getenv("NO_LLM") == "1":
        # Deterministic fallback: call tools directly, no model required
        print("=== Business Rules Agent Demo (NO_LLM mode) ===")
        for order in _example_orders():
            print(f"\n-- {order['id']} --")
            decision = evaluate_order_rules(json.dumps(order, ensure_ascii=False))
            print(decision)
            print(log_decision(order["id"], decision))
        return

    model = build_model()
    agent = build_business_rules_agent(model)

    print("=== Business Rules Agent Demo ===")
    for order in _example_orders():
        prompt = (
            "Evaluate this order against business rules, then log the decision under its id.\n"
            f"Order JSON: {json.dumps(order, ensure_ascii=False)}\n"
            f"Use log id: {order['id']}"
        )
        print(f"\n-- {order['id']} --")
        print(agent(prompt))


if __name__ == "__main__":
    main()
