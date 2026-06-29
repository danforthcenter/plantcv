#!/usr/bin/env bash
# Auto-approve Read tool calls for any file within the plantcv project.
set -euo pipefail

input=$(cat)
file_path=$(printf '%s' "$input" | jq -r '.tool_input.file_path // empty')

if [[ -n "$file_path" && "$file_path" == /home/josh/plantcv/* ]]; then
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"allow"}}'
fi
