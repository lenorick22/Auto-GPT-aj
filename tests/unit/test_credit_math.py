import json
import os
import subprocess
import sys
import unittest


TOOL = os.path.join(
    os.path.dirname(__file__), "..", "..", "agents", "credit_repair", "tools", "credit_math.py"
)


class TestCreditMath(unittest.TestCase):
    def run_tool(self, *args):
        proc = subprocess.run(
            [sys.executable, TOOL, *args],
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(proc.stdout)

    def test_utilization_overall(self):
        data = self.run_tool(
            "utilization", "--cards", "visa:900:3000,amex:100:1000"
        )
        self.assertEqual(data["overall_balance"], 1000)
        self.assertEqual(data["overall_limit"], 4000)
        self.assertEqual(data["overall_utilization_pct"], 25.0)

    def test_target_paydown(self):
        data = self.run_tool(
            "target", "--balance", "1200", "--limit", "4000", "--target-pct", "10"
        )
        self.assertEqual(data["max_balance_for_target"], 400.0)
        self.assertEqual(data["pay_down_needed"], 800.0)

    def test_payoff_zero_apr(self):
        data = self.run_tool(
            "payoff", "--balance", "1000", "--apr", "0", "--payment", "250"
        )
        self.assertEqual(data["months"], 4)


if __name__ == "__main__":
    unittest.main()
