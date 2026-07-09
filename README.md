# bankroll-sim

![status](https://img.shields.io/badge/status-active-brightgreen) ![python](https://img.shields.io/badge/python-3.10%2B-blue) ![license](https://img.shields.io/badge/license-MIT-lightgrey)

Compare **flat stake**, **proportional**, and **Kelly-ish** sizing on synthetic win/loss sequences.

Educational risk-of-ruin lab for DS students.

## Install

```bash
pip install -e ".[dev]"
```

## CLI

```bash
bankroll-sim run --p 0.55 --odds 2.0 --bankroll 1000 --n 300 --mode flat --stake 20 --seed 1
bankroll-sim run --p 0.55 --odds 2.0 --bankroll 1000 --n 300 --mode prop --frac 0.02 --seed 1
bankroll-sim compare --p 0.55 --odds 2.0 --bankroll 1000 --n 200 --seed 42
```
