#!/usr/bin/env python3
"""Deck package contract tests, without game files or network access."""
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
import zipfile


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ROOT = Path(__file__).resolve().parents[2]
package = load("release_package", ROOT / "tools/release/package.py")
setup = load("installer_setup", ROOT / "tools/installer/setup.py")
guard = load("release_guard", ROOT / "tools/release/guard.py")


class DeckPackage(unittest.TestCase):
    def test_profile_requires_deck_architecture(self):
        with self.assertRaises(ValueError):
            package.deck_manifest("linux-aarch64")

    def test_defaults_are_editable_and_repair_preserves_user_settings(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = package.deck_manifest("linux-x86_64")
            setup.seed_package_settings(manifest, tmp)
            path = Path(tmp) / "user/settings.ini"
            settings = dict(line.split("=", 1) for line in path.read_text().splitlines()
                            if line and not line.startswith("#"))
            self.assertEqual(settings, {"fps60": "1", "resScale": "1",
                                        "vkPresentMode": "0", "drcMode": "pip"})
            chosen = b"# user settings\nfps60=0\ncustom=preserve\n"
            path.write_bytes(chosen)
            setup.seed_package_settings(manifest, tmp)
            self.assertEqual(path.read_bytes(), chosen)

    def test_legacy_package_does_not_seed_settings(self):
        with tempfile.TemporaryDirectory() as tmp:
            setup.seed_package_settings({}, tmp)
            self.assertFalse((Path(tmp) / "user").exists())

    def test_deck_instructions_pass_artifact_guard(self):
        problems = []
        guard.check_entry("START-HERE.txt", package.DECK_START.encode(), problems)
        self.assertEqual(problems, [])

    @unittest.skipIf(os.name == "nt", "POSIX executable bits are verified on the Linux runner")
    def test_zip_preserves_linux_launcher_permissions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "Deck package"
            root.mkdir()
            launcher = root / "wind-waker-hd"
            launcher.write_text("#!/bin/sh\nexit 0\n")
            launcher.chmod(0o755)
            package.make_zip(str(root), str(Path(tmp) / "deck.zip"))
            with zipfile.ZipFile(Path(tmp) / "deck.zip") as archive:
                mode = archive.getinfo("Deck package/wind-waker-hd").external_attr >> 16
                self.assertTrue(mode & 0o111)


if __name__ == "__main__":
    unittest.main()
