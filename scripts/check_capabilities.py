from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def find_command(names: list[str]) -> str | None:
    for name in names:
        found = shutil.which(name)
        if found:
            return found
    return None


def existing_path(paths: list[Path]) -> str | None:
    for path in paths:
        if path.exists():
            return str(path)
    return None


def try_command(args: list[str], timeout: int = 12) -> tuple[bool, str]:
    try:
        proc = subprocess.run(args, capture_output=True, text=True, timeout=timeout, check=False)
    except Exception as exc:
        return False, str(exc)
    output = (proc.stdout or proc.stderr or "").strip().splitlines()
    return proc.returncode == 0, output[0] if output else f"exit code {proc.returncode}"


def find_browser() -> str | None:
    env_browser = os.environ.get("BROWSER")
    if env_browser and " " not in env_browser.strip():
        value = env_browser.strip()
        path = Path(value).expanduser()
        if path.exists():
            return str(path)
        found = shutil.which(value)
        if found:
            return found

    home = Path.home()
    return existing_path(
        [
            Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
            Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
            Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
            Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
            home / "AppData/Local/Google/Chrome/Application/chrome.exe",
            home / "AppData/Local/Microsoft/Edge/Application/msedge.exe",
            Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
            Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"),
        ]
    ) or find_command(["chrome", "google-chrome", "chromium", "chromium-browser", "msedge", "firefox"])


def python_package(name: str) -> tuple[bool, str]:
    spec = importlib.util.find_spec(name)
    return bool(spec), spec.origin if spec and spec.origin else "not installed"


def node_package(name: str) -> tuple[bool, str]:
    node = find_command(["node", "node.exe"])
    if not node:
        return False, "node not found"
    script = f"require.resolve('{name}');"
    ok, detail = try_command([node, "-e", script], timeout=8)
    return ok, detail if ok else f"{name} not resolvable from current environment"


def collect() -> dict[str, object]:
    ffmpeg = find_command(["ffmpeg", "ffmpeg.exe"])
    ffprobe = find_command(["ffprobe", "ffprobe.exe"])
    node = find_command(["node", "node.exe"])
    npm = find_command(["npm", "npm.cmd"])
    npx = find_command(["npx", "npx.cmd"])
    browser = find_browser()

    ffmpeg_ok, ffmpeg_detail = try_command([ffmpeg, "-version"]) if ffmpeg else (False, "not found")
    ffprobe_ok, ffprobe_detail = try_command([ffprobe, "-version"]) if ffprobe else (False, "not found")
    node_ok, node_detail = try_command([node, "--version"]) if node else (False, "not found")
    npm_ok, npm_detail = try_command([npm, "--version"]) if npm else (False, "not found")
    npx_ok, npx_detail = try_command([npx, "--version"]) if npx else (False, "not found")
    playwright_ok, playwright_detail = node_package("playwright")
    whisper_ok, whisper_detail = python_package("faster_whisper")

    tools = [
        {
            "name": "FFmpeg",
            "available": ffmpeg_ok,
            "detail": ffmpeg_detail,
            "use": "读取/抽帧/提取音频/生成联系图，是本地视频分析的基础。",
            "fix": "Windows: winget install Gyan.FFmpeg；macOS: brew install ffmpeg。",
        },
        {
            "name": "ffprobe",
            "available": ffprobe_ok,
            "detail": ffprobe_detail,
            "use": "读取视频时长、分辨率、编码和音轨。",
            "fix": "随 FFmpeg 一起安装；安装后重开终端再检查。",
        },
        {
            "name": "Node.js",
            "available": node_ok,
            "detail": node_detail,
            "use": "运行网页视频真实播放脚本。",
            "fix": "安装 Node.js LTS，然后在 skill 目录运行 npm install。",
        },
        {
            "name": "npm/npx",
            "available": npm_ok and npx_ok,
            "detail": f"npm={npm_detail}; npx={npx_detail}",
            "use": "安装 Playwright 并运行浏览器自动化。",
            "fix": "随 Node.js LTS 一起安装。",
        },
        {
            "name": "Playwright",
            "available": playwright_ok,
            "detail": playwright_detail,
            "use": "打开网页链接、播放视频、截图关键时间点。",
            "fix": "在 skill 目录运行 npm install && npx playwright install chromium。",
        },
        {
            "name": "Chrome/Edge",
            "available": bool(browser),
            "detail": browser or "not found",
            "use": "作为真实网页视频播放浏览器；没有也可用 Playwright bundled Chromium。",
            "fix": "安装 Chrome 或 Edge，或运行 npx playwright install chromium。",
        },
        {
            "name": "faster-whisper",
            "available": whisper_ok,
            "detail": whisper_detail,
            "use": "本地转写口播，生成 TXT/SRT/JSON 时间线。",
            "fix": "在 skill 目录运行 python -m pip install -r requirements.txt。",
        },
        {
            "name": "Codex Browser plugin",
            "available": None,
            "detail": "cannot be detected from this standalone script",
            "use": "让 Codex 直接看本地网页、截图和交互式预览。",
            "fix": "在 Codex 中启用 Browser 插件；安装 skill 本身不会自动安装插件。",
        },
    ]

    available = {tool["name"]: tool["available"] for tool in tools}
    if available["FFmpeg"] and available["ffprobe"] and available["Playwright"] and available["faster-whisper"] and (
        available["Chrome/Edge"] or available["Playwright"]
    ):
        level = "full"
    elif available["FFmpeg"] and available["ffprobe"]:
        level = "recommended"
    else:
        level = "minimal"

    return {"level": level, "tools": tools}


def print_human(report: dict[str, object]) -> None:
    print(f"Current watch-video capability level: {report['level']}")
    print("\nAvailable / missing:")
    for tool in report["tools"]:
        state = "unknown" if tool["available"] is None else ("ok" if tool["available"] else "missing")
        print(f"- {tool['name']}: {state}")
        print(f"  use: {tool['use']}")
        print(f"  detail: {tool['detail']}")
        if tool["available"] is not True:
            print(f"  fix: {tool['fix']}")

    print("\nFast path to full:")
    print("1. Install FFmpeg and make ffmpeg/ffprobe available on PATH.")
    print("2. In this skill folder, run: python -m pip install -r requirements.txt")
    print("3. In this skill folder, run: npm install && npx playwright install chromium")
    print("4. Restart Codex after installing or updating skills/plugins.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check whether this computer can run watch-video at full quality.")
    parser.add_argument("--json", action="store_true", help="Print JSON only.")
    args = parser.parse_args()
    report = collect()
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_human(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
