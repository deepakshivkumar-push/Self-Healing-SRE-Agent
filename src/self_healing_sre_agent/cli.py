from __future__ import annotations

import argparse
import logging

from .config import load_settings
from .service import run_service


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Self-Healing SRE Agent")
    parser.add_argument(
        "--iterations",
        type=int,
        default=None,
        help="Override MAX_ITERATIONS for local demo runs",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    settings = load_settings()
    if args.iterations is not None:
        settings.max_iterations = args.iterations

    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    run_service(settings)


if __name__ == "__main__":
    main()
