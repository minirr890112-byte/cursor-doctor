# 🩺 Cursor Doctor

> **Diagnose and fix Cursor IDE when it gets dumb** — CLI tool that detects and repairs Cursor Editor performance issues.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green)]()
[![PyPI version](https://img.shields.io/pypi/v/cursor-doctor)](https://pypi.org/project/cursor-doctor/)

## Quick Install

```bash
pip install cursor-doctor
```

## What It Detects

Cursor Doctor scans for and fixes 28+ known issues that cause Cursor to slow down or behave incorrectly:

| Category | Signatures | Examples |
|----------|-----------|----------|
| **Performance** | 12 | Large index cache, bloated SQLite DBs, stale extensions |
| **Config** | 8 | Corrupted settings.json, conflicting keybindings |
| **Network** | 4 | Proxy misconfig, DNS timeouts, rate limiting |
| **Crash** | 4 | Corrupt workspaces, extension conflicts |

## Usage

```bash
# Full diagnosis
cursor-doctor diagnose

# List all known issue signatures
cursor-doctor list-signatures

# Filter by category
cursor-doctor list-signatures --category performance

# Auto-apply fixes for all detected issues
cursor-doctor diagnose --fix

# Pricing comparison (v1.2)
cursor-doctor pricing

# Migration guide between plans
cursor-doctor migrate
```

## Pricing Analysis (v1.2)

Compare Cursor pricing plans with rich terminal tables:

```bash
$ cursor-doctor pricing

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃     Cursor Plan Comparison       ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Plan          │ Price    │ Best For       │
├───────────────┼──────────┼────────────────┤
│ Free          │ $0       │ Casual use     │
│ Pro           │ $20/mo   │ Daily coding   │
│ Business      │ $40/mo   │ Teams          │
│ Enterprise    │ Custom   │ Large orgs     │
└───────────────┴──────────┴────────────────┘
```

## Why This Exists

Chinese developer communities (V2EX, CSDN) repeatedly report Cursor IDE "getting dumb" — slow completions, laggy UI, random crashes. Most fixes involve manually digging through config files and SQLite databases. **cursor-doctor** automates the diagnosis and repair.

## Supported Platforms

- macOS (primary)
- Linux
- Windows (via WSL)

## From the HermesMade Project

This tool was built from real V2EX/CSDN community pain points collected by the [HermesMade](https://github.com/minirr890112-byte) automated pain-point scanning pipeline. If Cursor slows down, this is the first thing to run.

## License

MIT
