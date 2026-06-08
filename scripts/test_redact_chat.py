import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("redact_chat.py")
SPEC = importlib.util.spec_from_file_location("redact_chat", MODULE_PATH)
assert SPEC and SPEC.loader
redact_chat = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(redact_chat)


class RedactChatTests(unittest.TestCase):
    def test_redacts_labeled_secret(self):
        source = "账号: demo\n密码: Example123!\n"
        result = redact_chat.redact(source)
        self.assertIn("账号: demo", result)
        self.assertIn("密码: [REDACTED]", result)
        self.assertNotIn("Example123!", result)

    def test_redacts_unlabeled_server_bundle(self):
        source = "服务器地址\n192.0.2.10\ndemo\nExample123!\n代码在 /srv/app\n"
        result = redact_chat.redact(source)
        self.assertIn("[REDACTED_HOST]", result)
        self.assertIn("[REDACTED_USERNAME]", result)
        self.assertIn("[REDACTED_SECRET]", result)
        self.assertNotIn("192.0.2.10", result)
        self.assertNotIn("Example123!", result)

    def test_personal_level_masks_contact_data(self):
        source = "联系 13800138000 或 test@example.com，主机 10.0.0.8"
        result = redact_chat.redact(source, "personal")
        self.assertNotIn("13800138000", result)
        self.assertNotIn("test@example.com", result)
        self.assertNotIn("10.0.0.8", result)

    def test_does_not_redact_normal_chat(self):
        source = "周五中午过去，下午部署前端和后端。"
        self.assertEqual(source, redact_chat.redact(source))

    def test_secret_prefix_is_not_treated_as_a_label(self):
        source = "Secret123!\n"
        self.assertEqual(source, redact_chat.redact(source))


if __name__ == "__main__":
    unittest.main()
