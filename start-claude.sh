#!/usr/bin/env bash
#
# start-claude.sh — load an Anthropic API key from a .env file and launch Claude.
#
# Usage:
#   ./start-claude.sh                 # loads .env next to this script
#   ENV_FILE=/path/to/.env ./start-claude.sh
#   ./start-claude.sh --model opus    # extra args are passed through to claude
#
# Copy .env.example to .env and fill in your key before running.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${ENV_FILE:-${SCRIPT_DIR}/.env}"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "error: env file not found: $ENV_FILE" >&2
  echo "copy .env.example to .env and set ANTHROPIC_API_KEY" >&2
  exit 1
fi

# Load the .env file, exporting every variable it defines.
set -a
# shellcheck disable=SC1090
source "$ENV_FILE"
set +a

if [[ -z "${ANTHROPIC_API_KEY:-}" ]]; then
  echo "error: ANTHROPIC_API_KEY is not set in $ENV_FILE" >&2
  exit 1
fi

if ! command -v claude >/dev/null 2>&1; then
  echo "error: 'claude' CLI not found on PATH" >&2
  echo "install it from https://docs.claude.com/claude-code" >&2
  exit 1
fi

echo "Loaded ANTHROPIC_API_KEY from $ENV_FILE. Starting Claude..."
exec claude "$@"
