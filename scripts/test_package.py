"""Synthetic packaging checks: no app launch, API calls or user configuration."""

import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile


class PackageTests(unittest.TestCase):
    def test_windows_resources_and_checksums(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory(prefix="wordcraft-package-test-") as temporary:
            temporary = Path(temporary)
            binary = temporary / "synthetic.exe"
            binary.write_bytes(b"Synthetic package fixture; not an executable")
            output = temporary / "dist"
            command = [sys.executable, str(root / "scripts/package.py"), "--platform", "win64", "--binary", str(binary), "--version", "0.11.0-test.1", "--output", str(output)]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            archive = output / "WordCraft-0.11.0-test.1-win64.zip"
            self.assertTrue(archive.is_file())
            with zipfile.ZipFile(archive) as zipped:
                self.assertIsNone(zipped.testzip())
                names = zipped.namelist()
                self.assertTrue(any(name.endswith("/WordCraft.exe") for name in names))
                for required in ("LICENSE-MIT", "NOTICE", "craft-i18n-LICENSE-MIT", "craft-libs-LICENSE-APACHE", "wordcraft-craft-libs-1774443/NOTICE", "使用说明.md", "local-api-assistant.md"):
                    self.assertTrue(any(name.endswith("/" + required) for name in names), required)
                self.assertFalse(any(name.endswith(("ai-api.json", "prefs.json", ".env")) for name in names))
                self.assertFalse(any("GridCraft.exe" in name for name in names))
                self.assertIn("WordCraft API Edition", zipped.read(next(name for name in names if name.endswith("/使用说明.md"))).decode())
            expected = hashlib.sha256(archive.read_bytes()).hexdigest()
            self.assertEqual((output / (archive.name + ".sha256")).read_text().split()[0], expected)
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Refusing to overwrite", result.stderr)

    def test_reject_unsafe_version(self):
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run([sys.executable, str(root / "scripts/package.py"), "--platform", "win64", "--binary", __file__, "--version", "../invalid", "--output", "dist"], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Invalid package version", result.stderr)


if __name__ == "__main__":
    unittest.main()
