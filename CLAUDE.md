# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository stores Fusion 360 3D models. Fusion 360 files typically include:
- `.f3d` - Native Fusion 360 design files
- `.f3z` - Fusion 360 archive files (includes referenced data)
- Exported formats: `.step`, `.stl`, `.obj`, `.3mf` for sharing/printing

## Notes

Fusion 360 files are binary and cannot be meaningfully diffed in git. Consider exporting human-readable formats (STEP) or screenshots for documentation when tracking design changes.
