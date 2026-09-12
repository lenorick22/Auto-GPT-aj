import os
import re
import unittest

import yaml


ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
KB = os.path.join(ROOT, "agents", "credit_repair", "knowledge")
YAML = os.path.join(ROOT, "agents", "credit_repair.yaml")


class TestCreditKnowledge(unittest.TestCase):
    def test_curriculum_files_exist(self):
        with open(os.path.join(KB, "INDEX.md"), encoding="utf-8") as fh:
            index = fh.read()
        mods = re.findall(r"`(\d{2}_[a-z0-9_]+\.md|INDEX\.md)`", index)
        self.assertTrue(mods)
        for name in set(mods):
            path = os.path.join(KB, name)
            self.assertTrue(os.path.isfile(path), msg=name)
            self.assertGreater(os.path.getsize(path), 200)

    def test_quick_reference_and_count(self):
        files = [f for f in os.listdir(KB) if f.endswith(".md")]
        self.assertIn("00_quick_reference.md", files)
        self.assertIn("INDEX.md", files)
        self.assertGreaterEqual(len(files), 15)

    def test_yaml_points_at_knowledge_dir(self):
        with open(YAML, encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        self.assertEqual(data.get("knowledge_dir") or data.get("knowledge_dir"), "agents/credit_repair/knowledge")

        def flat(items):
            out = []
            for item in items:
                if isinstance(item, dict):
                    out.extend(f"{k}: {v}" for k, v in item.items())
                else:
                    out.append(str(item))
            return " ".join(out)

        blob = flat(data["ai_goals"]) + " " + flat(data["operating_rules"])
        self.assertIn("INDEX.md", blob)
        self.assertIn("00_quick_reference.md", blob)
        self.assertIn("knowledge_brief.md", blob)
        for goal in data["ai_goals"]:
            self.assertIsInstance(goal, str)


if __name__ == "__main__":
    unittest.main()
