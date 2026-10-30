"""Package WordCraft and audited project resources; never include user settings."""

import argparse
import hashlib
import os
from pathlib import Path
import plistlib
import shutil
import subprocess
import tempfile
import zipfile


def package(args):
    root = Path(__file__).resolve().parents[1]
    source = root / "wordcraft"
    version = args.version
    if not version or any(c not in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-" for c in version):
        raise SystemExit("Invalid package version")
    binary_input = args.binary.resolve()
    if not binary_input.is_file():
        raise SystemExit("The compiled WordCraft binary does not exist")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    archive = output / f"WordCraft-{version}-{args.platform}.zip"
    if archive.exists():
        raise SystemExit(f"Refusing to overwrite existing package: {archive}")

    with tempfile.TemporaryDirectory(prefix="wordcraft-api-package-") as temporary:
        temporary = Path(temporary)
        if args.platform == "macos-arm64":
            bundle = temporary / "WordCraft.app"
            binary = bundle / "Contents/MacOS/WordCraft"
            destination = bundle / "Contents/Resources"
            binary.parent.mkdir(parents=True)
            destination.mkdir()
            shutil.copyfile(binary_input, binary)
            os.chmod(binary, 0o755)
            commit = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=root, check=True, capture_output=True, text=True
            ).stdout.strip()
            template = (source / "packaging/macos/Info.plist.in").read_text()
            template = template.replace("@SHORT_VERSION@", "0.11.0").replace("@VERSION@", version).replace("@BUILD_SHA@", commit)
            info = plistlib.loads(template.encode())
            info["WordCraftLocalPatch"] = "API Edition 20261030.2; saved API credential fix; optional Windows PDF printing; 798 PCB terms"
            (bundle / "Contents/Info.plist").write_bytes(plistlib.dumps(info))
            (bundle / "Contents/PkgInfo").write_bytes(b"APPL????")
            shutil.copyfile(source / "assets/app-icon/wordcraft.icns", destination / "WordCraft.icns")
        else:
            bundle = temporary / f"WordCraft-{version}-Win64"
            bundle.mkdir()
            shutil.copyfile(binary_input, bundle / "WordCraft.exe")
            destination = bundle

        for filename in ("LICENSE-MIT", "LICENSE-APACHE", "NOTICE", "ATTRIBUTION.md"):
            shutil.copyfile(source / filename, destination / filename)
            shutil.copyfile(root / "third-party/craft-libs-shared" / filename, destination / ("craft-libs-" + filename))
        for filename in ("LICENSE-MIT", "LICENSE-APACHE", "ATTRIBUTION.md"):
            shutil.copyfile(root / "craft-i18n" / filename, destination / ("craft-i18n-" + filename))
        shutil.copytree(root / "third-party/wordcraft-craft-libs-1774443", destination / "wordcraft-craft-libs-1774443")
        shutil.copyfile(root / "README.md", destination / "使用说明.md")
        shutil.copyfile(source / "assets/pcb-glossary-public.json", destination / "pcb-glossary-public.json")
        for path in (source / "docs").glob("local-*.md"):
            shutil.copyfile(path, destination / path.name)
        for path in (source / "assets/fonts").glob("OFL-*.txt"):
            shutil.copyfile(path, destination / path.name)
        fonts_dir = os.environ.get("CRAFT_FONTS_DIR")
        if not fonts_dir and os.environ.get("CRAFT_FONTS_REQUIRED"):
            raise SystemExit("CRAFT_FONTS_DIR is required for the release package and font licenses")
        if fonts_dir:
            fonts = Path(fonts_dir)
            shutil.copyfile(fonts / "ATTRIBUTION.md", destination / "craft-fonts-ATTRIBUTION.md")
            licenses = sorted((fonts / "fonts").glob("*/OFL.txt"))
            if not licenses:
                raise SystemExit("craft-fonts has no OFL licenses")
            for license_path in licenses:
                # Do not collide with bundled OFL-Inter.txt on case-insensitive
                # macOS/Windows filesystems: craft-fonts also has fonts/inter/.
                shutil.copyfile(license_path, destination / ("craft-fonts-OFL-" + license_path.parent.name + ".txt"))

        if args.platform == "macos-arm64":
            subprocess.run(["xattr", "-cr", str(bundle)], check=True)
            subprocess.run(["codesign", "--force", "--deep", "--sign", "-", str(bundle)], check=True)
            subprocess.run(["codesign", "--verify", "--deep", "--strict", str(bundle)], check=True)
            subprocess.run(["ditto", "-c", "-k", "--keepParent", "--norsrc", "--noextattr", str(bundle), str(archive)], check=True)
        else:
            with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zipped:
                for path in sorted(bundle.rglob("*")):
                    if path.is_file():
                        zipped.write(path, str(path.relative_to(temporary)))

    with zipfile.ZipFile(archive) as zipped:
        if zipped.testzip() is not None:
            raise SystemExit("Archive CRC check failed")
    digest = hashlib.sha256()
    with archive.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    checksum = digest.hexdigest()
    (output / (archive.name + ".sha256")).write_text(checksum + "  " + archive.name + "\n")
    print(archive)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--platform", choices=("macos-arm64", "win64"), required=True)
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--output", type=Path, required=True)
    package(parser.parse_args())
