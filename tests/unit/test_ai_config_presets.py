import importlib.util
import os
import sys
import tempfile
import types
import unittest


def load_ai_config_module():
    path = os.path.join(
        os.path.dirname(__file__), "..", "..", "autogpt", "config", "ai_config.py"
    )
    spec = importlib.util.spec_from_file_location("ai_config_under_test", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class TestAIConfigPresets(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = load_ai_config_module()
        cls.AIConfig = cls.mod.AIConfig

    def test_load_credit_repair_preset(self):
        path = os.path.join(
            os.path.dirname(__file__), "..", "..", "agents", "credit_repair.yaml"
        )
        config = self.AIConfig.load(path)
        self.assertEqual(config.ai_name, "CreditFix-GPT")
        self.assertEqual(config.ai_language, "English")
        self.assertGreaterEqual(len(config.ai_goals), 5)
        self.assertGreaterEqual(len(config.ai_constraints), 5)
        self.assertGreaterEqual(len(config.operating_rules), 5)
        self.assertIn("lawful", config.prompt_preamble.lower())

    def test_construct_prompt_includes_language_and_rules(self):
        fake = types.ModuleType("autogpt.prompt")
        fake.get_prompt = lambda: "BASE_PROMPT"
        sys.modules["autogpt.prompt"] = fake

        config = self.AIConfig(
            ai_name="TestBot",
            ai_role="a tester",
            ai_goals=["Ship tests"],
            ai_constraints=["Stay in English"],
            ai_language="English",
            prompt_preamble="Be precise.",
            operating_rules=["Step one"],
        )
        text = config.construct_full_prompt()
        self.assertIn("TestBot", text)
        self.assertIn("OPERATING RULES", text)
        self.assertIn("PRESET CONSTRAINTS", text)
        self.assertIn("LANGUAGE:", text)
        self.assertIn("English", text)
        self.assertIn("BASE_PROMPT", text)
        self.assertIn("Be precise.", text)

    def test_save_roundtrip_optional_fields(self):
        config = self.AIConfig(
            ai_name="X",
            ai_role="role",
            ai_goals=["g1"],
            ai_constraints=["c1"],
            ai_language="English",
            prompt_preamble="P",
            operating_rules=["r1"],
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "settings.yaml")
            config.save(path)
            loaded = self.AIConfig.load(path)
            self.assertEqual(loaded.ai_name, "X")
            self.assertEqual(loaded.ai_constraints, ["c1"])
            self.assertEqual(loaded.ai_language, "English")
            self.assertEqual(loaded.prompt_preamble, "P")
            self.assertEqual(loaded.operating_rules, ["r1"])


if __name__ == "__main__":
    unittest.main()
