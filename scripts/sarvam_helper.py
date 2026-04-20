#!/usr/bin/env python3
"""Generate Sarvam translation suggestions for changed Markdown files and comment on PRs."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
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
        # Ensure we only process existing .md files
        if candidate.endswith(".md") and Path(candidate).exists():
            files.append(Path(candidate))
    return files

def load_glossary(path: Path) -> Dict[str, str]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return {str(k): str(v) for k, v in data.items()}
    except Exception as e:
        print(f"Error loading glossary: {e}")
        return {}

def mask_markdown(text: str) -> Tuple[str, Dict[str, str]]:
    token_map: Dict[str, str] = {}
    patterns = [
        r"```[\s\S]*?```",  # fenced code blocks
        r"`[^`\n]+`",       # inline code
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

    # Mask Headers separately to keep them as single tokens
    lines = masked.splitlines()
    for i, line in enumerate(lines):
        if re.match(r"^\s{0,3}#{1,6}\s", line):
            token = f"{PLACEHOLDER_PREFIX}{len(token_map)}__"
            token_map[token] = line
            lines[i] = token
            
    return "\n".join(lines), token_map

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

def call_sarvam_api(text: str, config: dict) -> str:
    """Handles the actual API call with basic retry logic."""
    payload = {
        "input": text,
        "source_language_code": config['source_lang'],
        "target_language_code": config['target_lang'],
        "model": config['model'],
    }
    
    req = request.Request(
        config['api_url'],
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "api-subscription-key": config['api_key'],
        },
    )

    try:
        with request.urlopen(req, timeout=45) as resp:
            body = resp.read().decode("utf-8")
            parsed = json.loads(body)
            # Support multiple possible response keys from Sarvam API
            for key in ("translated_text", "translation", "output"):
                if key in parsed: return parsed[key]
                if "data" in parsed and key in parsed["data"]: return parsed["data"][key]
            
            raise ValueError(f"Unexpected response format: {body[:100]}")
    except error.HTTPError as e:
        if e.code == 429: # Rate limit
            time.sleep(2)
            return call_sarvam_api(text, config)
        raise

def translate_markdown(markdown: str, glossary: Dict[str, str], config: dict) -> str:
    masked, token_map = mask_markdown(markdown)
    glossary_applied = apply_glossary(masked, glossary)
    
    # Chunking: Split by double newline to avoid breaking sentences but keep chunks small
    chunks = glossary_applied.split("\n\n")
    translated_chunks = []
    
    for chunk in chunks:
        if not chunk.strip():
            translated_chunks.append("")
            continue
        try:
            translated_chunks.append(call_sarvam_api(chunk, config))
        except Exception as e:
            print(f"Chunk translation failed: {e}")
            translated_chunks.append(chunk) # Fallback to original for this chunk
            
    return unmask_markdown("\n\n".join(translated_chunks), token_map)

def parse_pr_number() -> int:
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path: raise RuntimeError("GITHUB_EVENT_PATH not found")
    payload = json.loads(Path(event_path).read_text(encoding="utf-8"))
    pr_number = payload.get("pull_request", {}).get("number")
    if not pr_number: raise RuntimeError("No PR number in event payload")
    return pr_number

def post_comment(repo: str, token: str, pr_number: int, body: str) -> None:
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    # GitHub limits comments to 65536 chars. We trim just in case.
    truncated_body = body[:65000]
    req = request.Request(
        url,
        data=json.dumps({"body": truncated_body}).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
        },
    )
    request.urlopen(req, timeout=30)

def build_comment(entries: Iterable[Tuple[Path, str]], target_lang: str) -> str:
    sections = [
        "## 🤖 Sarvam AI Translation Helper",
        f"Target Language: `{target_lang}`",
        "The following suggestions were generated using Sarvam AI. Please review for technical accuracy.",
        "---"
    ]
    for file_path, translation in entries:
        sections.extend([
            f"### 📄 `{file_path}`",
            "<details><summary>Click to view suggestion</summary>",
            "",
            "```markdown",
            translation,
            "```",
            "</details>",
            ""
        ])
    return "\n".join(sections)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--changed-files", default="changed_files.txt")
    parser.add_argument("--glossary", default="GLOSSARY.json")
    args = parser.parse_args()

    config = {
        'api_key': os.environ.get("SARVAM_API_KEY"),
        'api_url': os.environ.get("SARVAM_API_URL", "https://api.sarvam.ai/translate"),
        'model': os.environ.get("SARVAM_MODEL", "mayura-v1"), # Fixed to standard dash
        'source_lang': os.environ.get("SARVAM_SOURCE_LANG", "en-IN"),
        'target_lang': os.environ.get("SARVAM_TARGET_LANG", "hi-IN"),
    }

    github_token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")

    if not config['api_key'] or not github_token or not repo:
        print("Missing required Environment Variables. Check Secrets.")
        return 1

    files = load_changed_files(Path(args.changed_files))
    if not files:
        print("No markdown changes to process.")
        return 0

    glossary = load_glossary(Path(args.glossary))
    suggestions = []

    for file_path in files:
        print(f"Translating: {file_path}")
        content = file_path.read_text(encoding="utf-8")
        try:
            translation = translate_markdown(content, glossary, config)
            suggestions.append((file_path, translation))
        except Exception as e:
            print(f"Skipping {file_path} due to error: {e}")

    if suggestions:
        pr_number = parse_pr_number()
        comment_body = build_comment(suggestions, config['target_lang'])
        post_comment(repo, github_token, pr_number, comment_body)
        print("Success: Comment posted.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
