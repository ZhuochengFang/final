# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ZJU ISEE (School of Information & Electronics Engineering) 2026 bachelor thesis LaTeX template, based on [cyc-987/zju-isee3in1-bachelor-thesis-template](https://github.com/cyc-987/zju-isee3in1-bachelor-thesis-template). The thesis topic is low-power high-precision sensing interface design using dynamic amplifiers and correlated level shifting (CLS). All thesis content is written in Chinese.

## Build Commands

The project compiles with XeLaTeX + BibTeX. Run from the `latex/` directory:

```bash
# Full build (xelatex → bibtex → xelatex × 2)
cd latex
xelatex -interaction=nonstopmode -halt-on-error main.tex
# Run bibtex on each .aux that contains \bibdata references:
for f in doc_thesis/contents/*.aux doc_3in1/contents/*.aux; do
  [ -f "$f" ] && grep -qE '\\bibdata\{|\\bibstyle\{' "$f" && bibtex "${f%.aux}"
done
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex
```

A VS Code build task is configured in `latex/.vscode/tasks.json` (PowerShell-based, label: "LaTeX: 一键编译(main)").

## Compilation Modes

Controlled via `\documentclass` options in `latex/main.tex`:

- `thesisonly` — compile thesis only (current setting)
- `final` — compile full document (thesis + 三合一: literature review, proposal, translation)
- `blind` / `noblind` — toggle blind review (hides student/supervisor info)

## Architecture

- **`latex/main.tex`** — entry point; defines student/supervisor metadata and includes all content files
- **`latex/iseebachelor.cls`** — custom document class built on `ctexart`; defines fonts (STFangsong/SimHei/SimSun from `assets/fonts/`), page geometry, headers/footers, section formatting, and all custom commands
- **`latex/doc_thesis/`** — thesis content
  - `contents/04_Main.tex` aggregates the main body chapters (`04-1_Introduction.tex`, `04-2_MainBody.tex`, `04-3_Conclution.tex`, `04-4_Appendix.tex`)
  - `refs/MainReference.bib` — thesis bibliography
  - `figs/` — thesis figures
- **`latex/doc_3in1/`** — 三合一 supplementary documents (literature review, proposal, foreign language translation) with its own `contents/`, `refs/`, and `figs/`
- **`schematic/`** — EasyEDA circuit schematics (`.eprj2` format, not editable as text)
- **`latex/script/`** — utility scripts (e.g., MATLAB gain calculations)

## Important Notes

- All paths in `.tex` files are relative to `latex/` (the compilation root). For example, figures use `doc_thesis/figs/...` and bibliographies use `doc_thesis/refs/...`.
- When moving content between thesis and 3-in-1 sections, all `\bibliography{}` and `\includegraphics{}` paths must be updated to reflect the new prefix (`doc_thesis/` vs `doc_3in1/`).
- The `.cls` file loads specific font files from `assets/fonts/` by filename — font changes require updating both the font files and the cls configuration.
- Citation style uses `gbt7714` (Chinese national standard GB/T 7714).

## request
- 请使用简体中文来回答问题和编辑tex文档的文本部分。