"""
GitHub Action Adapter for Autograder.

This module provides the entry point for the GitHub Action adapter that integrates
with the autograder workflow to process student submissions and generate feedback.
"""

import logging
import asyncio
from argparse import ArgumentParser
from autograder.another import AnotherOut
from .another import AnotherIn

logger = logging.getLogger(__name__)

parser = ArgumentParser(description="GitHub Action Adapter for Autograder")
parser.add_argument("--github-token", type=str, required=True, help="GitHub Token")
parser.add_argument(
    "--template-preset",
    type=str,
    required=True,
    help="The grading preset to use (e.g., api, html, python, etc.)",
)
parser.add_argument(
    "--student-name", type=str, required=True, help="The name of the student"
)
parser.add_argument(
    "--feedback-type",
    type=str,
    default="default",
    help="The type of feedback to provide (default or ai)",
)
parser.add_argument(
    "--custom-template",
    type=str,
    required=False,
    help="Test Files for the submission (in case of custom preset)",
)
parser.add_argument("--app-token", type=str, required=False, help="GitHub App Token")
parser.add_argument(
    "--openai-key",
    type=str,
    required=False,
    help="OpenAI API key for AI feedback (required only for AI feedback mode)",
)
parser.add_argument(
    "--include-feedback",
    type=str,
    required=False,
    help="Whether to include/generate feedback (true/false).",
)


async def main():
    """
    This is the entry point for the GitHub Action adapter.
    This makes the Adapter accessible to the GitHub Action workflow,
    that runs by entrypoint.sh script with all arguments passed to it.
    """
    try:
        print("Iniciou Main.py")
        AnotherIn()
        AnotherOut()
        args = parser.parse_args()
        print("Parsed arguments:")
        for key, value in vars(args).items():
            print(f"{key}: {value}")

        print("Encerrou Main.py")
    except ValueError as e:
        logger.error("Invalid value provided: %s", e)
        raise SystemExit(1) from e
    except SystemExit as e:
        logger.critical(e)
        raise SystemExit(1) from e
    except Exception as e:
        logger.error(e, exc_info=True)
        raise SystemExit(1) from e


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    asyncio.run(main())
