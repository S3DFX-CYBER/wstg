#!/usr/bin/env python3
"""Generate Sarvam translation suggestions for changed Markdown files and comment on PRs."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Tuple
from urllib import error, request

PLACEHOLDER_PREFIX = "__WSTG_TOKEN_"


def load_changed_files(path: Path) -> List[Path]:
    if not path.exists():
        return []

    files: List[Path] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        candidate = line.strip()
        if candidate.endswith(".md") and Path(candidate).exists():
            files.append(Path(candidate))
    return files


def load_glossary(path: Path) -> Dict[str, str]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {str(k): str(v) for k, v in data.items()}


def mask_markdown(text: str) -> Tuple[str, Dict[str, str]]:
    """Mask Markdown segments that should not be translated."""
    token_map: Dict[str, str] = {}

    patterns = [
        r"```[\s\S]*?```",  # fenced code blocks
        r"`[^`\n]+`",  # inline code
        r"!\[[^\]]*\]\([^\)]+\)",  # images
        r"\[[^\]]+\]\([^\)]+\)",  # links
    ]

    def replacer(match: re.Match[str]) -> str:
        token = f"{PLACEHOLDER_PREFIX}{len(token_map)}__"
        token_map[token] = match.group(0)
        return token

    masked = text
    for pattern in patterns:
        masked = re.sub(pattern, replacer, masked)

    preserved_lines: List[str] = []
    for line in masked.splitlines():
        if re.match(r"^\s{0,3}#{1,6}\s", line):
            token = f"{PLACEHOLDER_PREFIX}{len(token_map)}__"
            token_map[token] = line
            preserved_lines.append(token)
        else:
            preserved_lines.append(line)

    return "\n".join(preserved_lines), token_map


def unmask_markdown(text: str, token_map: Dict[str, str]) -> str:
    restored = text
    for token, value in token_map.items():
        restored = restored.replace(token, value)
    return restored


def apply_glossary(text: str, glossary: Dict[str, str]) -> str:
    for source_term, target_term in glossary.items():
        pattern = re.compile(rf"\b{re.escape(source_term)}\b", re.IGNORECASE)
        text = pattern.sub(target_term, text)
    return text


def call_sarvam_api(
    text: str,
    api_key: str,
    source_lang: str,
    target_lang: str,
    model: str,
    api_url: str,
) -> str:
    payload = {
        "input": text,
        "source_language_code": source_lang,
        "target_language_code": target_lang,
        "model": model,
    }
    req = request.Request(
        api_url,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "api-subscription-key": api_key,
        },
    )
    with request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode("utf-8")

    parsed = json.loads(body)
    if isinstance(parsed, dict):
        if isinstance(parsed.get("translated_text"), str):
            return parsed["translated_text"]
        if isinstance(parsed.get("translation"), str):
            return parsed["translation"]
        if isinstance(parsed.get("output"), str):
            return parsed["output"]
        data = parsed.get("data")
        if isinstance(data, dict):
            for key in ("translated_text", "translation", "output"):
                if isinstance(data.get(key), str):
                    return data[key]

    raise ValueError("Unable to parse Sarvam response for translated text")


def translate_markdown(
    markdown: str,
    glossary: Dict[str, str],
    api_key: str,
    source_lang: str,
    target_lang: str,
    model: str,
    api_url: str,
) -> str:
    masked, token_map = mask_markdown(markdown)
    glossary_applied = apply_glossary(masked, glossary)
    translated = call_sarvam_api(
        text=glossary_applied,
        api_key=api_key,
        source_lang=source_lang,
        target_lang=target_lang,
        model=model,
        api_url=api_url,
    )
    return unmask_markdown(translated, token_map)


def parse_pr_number() -> int:
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        raise RuntimeError("GITHUB_EVENT_PATH is not set")

    payload = json.loads(Path(event_path).read_text(encoding="utf-8"))
    pr_number = payload.get("pull_request", {}).get("number")
    if not isinstance(pr_number, int):
        raise RuntimeError("Unable to determine pull request number")
    return pr_number


def post_comment(repo: str, token: str, pr_number: int, body: str) -> None:
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    req = request.Request(
        url,
        data=json.dumps({"body": body}).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
        },
    )
    with request.urlopen(req, timeout=30) as _resp:
        return


def build_comment(entries: Iterable[Tuple[Path, str]], target_lang: str) -> str:
    sections = [
        "## 🤖 Sarvam Translation Suggestions",
        f"Target language: `{target_lang}`",
        "",
        "These are machine-generated suggestions for review by human translators.",
    ]

    for file_path, translation in entries:
        sections.extend(
            [
                "",
                f"### `{file_path}`",
                "```markdown",
                translation[:3500],
                "```",
            ]
        )

    return "\n".join(sections)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--changed-files", default="changed_files.txt")
    parser.add_argument("--glossary", default="GLOSSARY.json")
    args = parser.parse_args()

    sarvam_api_key = os.environ.get("SARVAM_API_KEY")
    github_token = os.environ.get("GITHUB_TOKEN")
    github_repository = os.environ.get("GITHUB_REPOSITORY", "")

    if not sarvam_api_key:
        print("SARVAM_API_KEY is not configured. Skipping translation helper.")
        return 0

    if not github_token:
        print("GITHUB_TOKEN is not configured. Skipping comment creation.")
        return 0

    if not github_repository:
        print("GITHUB_REPOSITORY is not configured. Skipping comment creation.")
        return 0

    source_lang = os.environ.get("SARVAM_SOURCE_LANG", "en-IN")
    target_lang = os.environ.get("SARVAM_TARGET_LANG", "hi-IN")
    model = os.environ.get("SARVAM_MODEL", "mayura:v1")
    api_url = os.environ.get("SARVAM_API_URL", "https://api.sarvam.ai/translate")

    files = load_changed_files(Path(args.changed_files))
    if not files:
        print("No changed markdown files found. Skipping translation helper.")
        return 0

    glossary = load_glossary(Path(args.glossary))
    suggestions: List[Tuple[Path, str]] = []

    for file_path in files:
        content = file_path.read_text(encoding="utf-8")
        try:
            translation = translate_markdown(
                markdown=content,
                glossary=glossary,
                api_key=sarvam_api_key,
                source_lang=source_lang,
                target_lang=target_lang,
                model=model,
                api_url=api_url,
            )
            suggestions.append((file_path, translation))
        except (error.URLError, TimeoutError, ValueError) as exc:
            print(f"Failed to translate {file_path}: {exc}")

    if not suggestions:
        print("No translation suggestions were generated.")
        return 0

    pr_number = parse_pr_number()
    comment_body = build_comment(suggestions, target_lang)
    post_comment(github_repository, github_token, pr_number, comment_body)
    print(f"Posted translation suggestions to PR #{pr_number}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
