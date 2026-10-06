#!/usr/bin/env python3
import hashlib
from pathlib import Path
import subprocess
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "build-cache"
OUTPUT = ROOT / "output/CtsOverlay.apk"
REF = "39bd3a09640efb81234cdbd8ab98ab71541d5d46"
TOOLS = {
    "build/apktool/apktool_3.0.2.jar": "eee4669a704a14e0623407e6701b0b91887e61e1e4049cb7a82833e14ae8b5fd",
    "build/sign/apksigner.jar": "925fb5189d62fea563eaa24636108cb28a7281c05b63f3478f6c53e7768c7d3b",
    "build/sign/testkey.pk8": "495675d32e89a149d5abe191f4e9c0e218b9068714e9b53a7c91e164a0741a23",
    "build/sign/testkey.x509.pem": "a4384ba815b9499a5ce349b4e33c1755278873fe2eac150a068823f526e6dbde",
}


def tool(source):
    CACHE.mkdir(exist_ok=True)
    dest = CACHE / Path(source).name
    if not dest.exists():
        url = f"https://raw.githubusercontent.com/MindTheGapps/vendor_gapps/{REF}/{source}"
        with urllib.request.urlopen(url, timeout=60) as response:
            dest.write_bytes(response.read())
    with dest.open("rb") as file:
        actual_hash = hashlib.file_digest(file, "sha256").hexdigest()
    if actual_hash != TOOLS[source]:
        raise RuntimeError(f"Unexpected tool hash: {dest}")
    return dest


def run(*args):
    subprocess.run([str(arg) for arg in args], check=True)


def main():
    apktool = tool("build/apktool/apktool_3.0.2.jar")
    signer = tool("build/sign/apksigner.jar")
    key = tool("build/sign/testkey.pk8")
    cert = tool("build/sign/testkey.x509.pem")
    unsigned = CACHE / "CtsOverlay-unsigned.apk"
    aligned = CACHE / "CtsOverlay-aligned.apk"
    signed = CACHE / "CtsOverlay.apk"

    run("java", "-jar", apktool, "b", ROOT / "overlay", "-o", unsigned)
    run("zipalign", "-p", "-f", "4", unsigned, aligned)
    run("java", "-jar", signer, "sign", "--key", key, "--cert", cert,
        "--v4-signing-enabled", "false", "--out", signed, aligned)
    run("java", "-jar", signer, "verify", signed)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(signed.read_bytes())
    print(f"Built {OUTPUT}")


if __name__ == "__main__":
    main()
