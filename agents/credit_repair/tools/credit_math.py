#!/usr/bin/env python3
"""Credit utilization and payoff helpers for CreditFix-GPT.

Examples:
  python agents/credit_repair/tools/credit_math.py utilization --balance 1200 --limit 4000
  python agents/credit_repair/tools/credit_math.py utilization --cards 'visa:900:3000,amex:400:1000'
  python agents/credit_repair/tools/credit_math.py target --limit 4000 --target-pct 10
  python agents/credit_repair/tools/credit_math.py payoff --balance 2500 --apr 22.9 --payment 200
  python agents/credit_repair/tools/credit_math.py snowball --debts 'cardA:900:19,cardB:400:24,loan:2500:11' --budget 350
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from typing import Iterable, List


@dataclass
class Card:
    name: str
    balance: float
    limit: float

    @property
    def utilization(self) -> float:
        if self.limit <= 0:
            return 0.0
        return (self.balance / self.limit) * 100.0


@dataclass
class Debt:
    name: str
    balance: float
    apr: float  # percent


def parse_cards(raw: str) -> List[Card]:
    cards: List[Card] = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        name, balance, limit = part.split(":")
        cards.append(Card(name.strip(), float(balance), float(limit)))
    return cards


def parse_debts(raw: str) -> List[Debt]:
    debts: List[Debt] = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        name, balance, apr = part.split(":")
        debts.append(Debt(name.strip(), float(balance), float(apr)))
    return debts


def cmd_utilization(args: argparse.Namespace) -> int:
    if args.cards:
        cards = parse_cards(args.cards)
        total_bal = sum(c.balance for c in cards)
        total_lim = sum(c.limit for c in cards)
        overall = (total_bal / total_lim * 100.0) if total_lim else 0.0
        rows = [
            {
                "name": c.name,
                "balance": round(c.balance, 2),
                "limit": round(c.limit, 2),
                "utilization_pct": round(c.utilization, 2),
                "flag": "HIGH" if c.utilization > 30 else ("OK" if c.utilization <= 10 else "WATCH"),
            }
            for c in cards
        ]
        result = {
            "cards": rows,
            "overall_balance": round(total_bal, 2),
            "overall_limit": round(total_lim, 2),
            "overall_utilization_pct": round(overall, 2),
            "guidance": (
                "Aim under 30% overall; many people target under 10% before statement close."
            ),
        }
    else:
        if args.limit <= 0:
            print("limit must be > 0", file=sys.stderr)
            return 2
        util = args.balance / args.limit * 100.0
        result = {
            "balance": args.balance,
            "limit": args.limit,
            "utilization_pct": round(util, 2),
            "flag": "HIGH" if util > 30 else ("OK" if util <= 10 else "WATCH"),
        }
    print(json.dumps(result, indent=2))
    return 0


def cmd_target(args: argparse.Namespace) -> int:
    if args.limit <= 0:
        print("limit must be > 0", file=sys.stderr)
        return 2
    max_balance = args.limit * (args.target_pct / 100.0)
    pay_down = max(0.0, args.balance - max_balance)
    result = {
        "limit": args.limit,
        "current_balance": args.balance,
        "target_pct": args.target_pct,
        "max_balance_for_target": round(max_balance, 2),
        "pay_down_needed": round(pay_down, 2),
    }
    print(json.dumps(result, indent=2))
    return 0


def months_to_payoff(balance: float, apr: float, payment: float) -> dict:
    if payment <= 0:
        return {"error": "payment must be > 0"}
    monthly_rate = (apr / 100.0) / 12.0
    if monthly_rate == 0:
        months = math.ceil(balance / payment)
        interest = 0.0
    else:
        # payment must cover interest
        min_interest = balance * monthly_rate
        if payment <= min_interest:
            return {
                "error": "payment too low to cover monthly interest",
                "minimum_interest_only": round(min_interest, 2),
            }
        months = 0
        interest = 0.0
        principal = balance
        # Cap runaway loops
        while principal > 0 and months < 1200:
            interest_part = principal * monthly_rate
            principal = principal + interest_part - payment
            interest += interest_part
            months += 1
            if principal < 0:
                interest += principal  # last payment overshoot adjustment
                principal = 0
    return {
        "balance": round(balance, 2),
        "apr_pct": apr,
        "payment": payment,
        "months": months,
        "total_interest": round(max(interest, 0.0), 2),
        "total_paid": round(balance + max(interest, 0.0), 2),
    }


def cmd_payoff(args: argparse.Namespace) -> int:
    result = months_to_payoff(args.balance, args.apr, args.payment)
    print(json.dumps(result, indent=2))
    return 0 if "error" not in result else 2


def allocate_snowball(debts: List[Debt], budget: float, method: str) -> dict:
    debts = [Debt(d.name, d.balance, d.apr) for d in debts if d.balance > 0]
    if method == "avalanche":
        debts.sort(key=lambda d: (-d.apr, d.balance))
    else:
        debts.sort(key=lambda d: (d.balance, -d.apr))

    schedule = []
    month = 0
    working = debts
    while working and month < 1200:
        month += 1
        # minimums approximated as interest + 1% principal (simple model)
        mins = {}
        for d in working:
            interest = d.balance * (d.apr / 100.0) / 12.0
            mins[d.name] = max(25.0, interest + d.balance * 0.01)
        min_total = sum(mins.values())
        if budget < min_total:
            return {
                "error": "budget below estimated minimums",
                "estimated_minimums_total": round(min_total, 2),
                "minimums": {k: round(v, 2) for k, v in mins.items()},
            }
        extra = budget - min_total
        # apply mins
        for d in working:
            pay = mins[d.name]
            interest = d.balance * (d.apr / 100.0) / 12.0
            d.balance = d.balance + interest - pay
        # dump extra on first target
        target = working[0]
        target.balance -= extra
        paid_off = []
        still = []
        for d in working:
            if d.balance <= 0.01:
                paid_off.append(d.name)
            else:
                still.append(d)
        schedule.append(
            {
                "month": month,
                "focus": target.name,
                "paid_off_this_month": paid_off,
                "remaining_balances": {d.name: round(max(d.balance, 0), 2) for d in still},
            }
        )
        working = still
        if method == "avalanche":
            working.sort(key=lambda d: (-d.apr, d.balance))
        else:
            working.sort(key=lambda d: (d.balance, -d.apr))

    return {
        "method": method,
        "months_to_debt_free": month,
        "schedule_preview": schedule[:6],
        "schedule_length": len(schedule),
        "note": "Educational model using simplified minimums; replace with real statement minimums.",
    }


def cmd_snowball(args: argparse.Namespace) -> int:
    debts = parse_debts(args.debts)
    result = allocate_snowball(debts, args.budget, args.method)
    print(json.dumps(result, indent=2))
    return 0 if "error" not in result else 2


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="CreditFix math utilities")
    sub = p.add_subparsers(dest="cmd", required=True)

    u = sub.add_parser("utilization", help="Compute utilization")
    u.add_argument("--balance", type=float, default=0.0)
    u.add_argument("--limit", type=float, default=0.0)
    u.add_argument("--cards", type=str, default="", help="name:balance:limit,...")
    u.set_defaults(func=cmd_utilization)

    t = sub.add_parser("target", help="Paydown needed for a utilization target")
    t.add_argument("--balance", type=float, required=True)
    t.add_argument("--limit", type=float, required=True)
    t.add_argument("--target-pct", type=float, default=10.0)
    t.set_defaults(func=cmd_target)

    pay = sub.add_parser("payoff", help="Months/interest to pay off one debt")
    pay.add_argument("--balance", type=float, required=True)
    pay.add_argument("--apr", type=float, required=True)
    pay.add_argument("--payment", type=float, required=True)
    pay.set_defaults(func=cmd_payoff)

    s = sub.add_parser("snowball", help="Snowball/avalanche schedule preview")
    s.add_argument("--debts", required=True, help="name:balance:apr,...")
    s.add_argument("--budget", type=float, required=True)
    s.add_argument("--method", choices=["snowball", "avalanche"], default="snowball")
    s.set_defaults(func=cmd_snowball)
    return p


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
