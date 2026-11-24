import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

STUDIO = Path(__file__).resolve().with_name("studio.py")

class SecurityTests(unittest.TestCase):
    def run_cli(self, source, target):
        return subprocess.run([sys.executable, str(STUDIO), str(source), "--output", str(target)], capture_output=True, text=True, timeout=10)

    def test_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "input.txt"
            target = Path(folder) / "output.srt"
            source.write_text("Private narration", encoding="utf-8")
            target.write_text("original", encoding="utf-8")
            self.assertNotEqual(self.run_cli(source, target).returncode, 0)
            self.assertEqual(target.read_text(), "original")

    def test_private_text_not_printed(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "input.txt"
            target = Path(folder) / "output.srt"
            source.write_text("Private narration", encoding="utf-8")
            result = self.run_cli(source, target)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn("Private narration", result.stdout)
            self.assertIn("Private narration", target.read_text(encoding="utf-8"))

    def test_oversized_input_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "input.txt"
            target = Path(folder) / "output.srt"
            source.write_bytes(b"x" * 1048577)
            self.assertNotEqual(self.run_cli(source, target).returncode, 0)
            self.assertFalse(target.exists())

if __name__ == "__main__":
    unittest.main()
