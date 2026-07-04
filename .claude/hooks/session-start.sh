#!/bin/bash
set -euo pipefail

# Only relevant on Claude Code on the web, where each session gets a fresh
# container and locally-added MCP servers (claude mcp add) don't persist.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

MCP_NAME="novamira-wordpress-125475"

if [ -z "${WP_API_URL:-}" ] || [ -z "${WP_API_USERNAME:-}" ] || [ -z "${WP_API_PASSWORD:-}" ]; then
  echo "session-start.sh: WP_API_URL / WP_API_USERNAME / WP_API_PASSWORD not set in this environment's" \
       "config — skipping Novamira WordPress MCP setup. Add them under the environment's" \
       "environment-variable settings to enable it." >&2
  exit 0
fi

# Idempotent: drop any stale registration, then (re)add fresh.
claude mcp remove "$MCP_NAME" -s local >/dev/null 2>&1 || true

claude mcp add "$MCP_NAME" \
  -s local \
  -e WP_API_URL="$WP_API_URL" \
  -e WP_API_USERNAME="$WP_API_USERNAME" \
  -e WP_API_PASSWORD="$WP_API_PASSWORD" \
  -- npx -y @automattic/mcp-wordpress-remote@latest >&2
