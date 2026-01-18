"""Minimal logging utilities for FIGARO-NAM scripts."""
import logging
import sys

def setup_logging(name: str, level: int = logging.INFO) -> logging.Logger:
    """Configure compact logging for a script."""
    log = logging.getLogger(name)
    log.setLevel(level)
    if not log.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        log.addHandler(handler)
    return log
