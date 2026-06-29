#!/usr/bin/env bash
# PostToolUse: marks AI-edited sections in Python files; blocks try/except/finally additions.
set -euo pipefail

input=$(cat)
file_path=$(printf '%s' "$input" | jq -r '.tool_input.file_path // empty')

# Only process existing Python files
[[ -n "$file_path" && "$file_path" == *.py ]] || exit 0
[[ -f "$file_path" ]] || exit 0

# Resolve the git root
git_root=$(git -C "$(dirname "$(realpath "$file_path")")" rev-parse --show-toplevel 2>/dev/null) || exit 0

# Get diff: tracked files vs HEAD; untracked files as full addition
if git -C "$git_root" ls-files --error-unmatch "$file_path" &>/dev/null; then
    diff_output=$(git -C "$git_root" diff HEAD -- "$file_path" 2>/dev/null)
else
    diff_output=$(git diff --no-index -- /dev/null "$file_path" 2>/dev/null || true)
fi
[[ -n "$diff_output" ]] || exit 0

# Block if any added line introduces try / except / finally.
# Use -E on the grep -v step to avoid BRE \+ interpretation issues (ugrep compat).
if printf '%s\n' "$diff_output" \
       | grep -E '^\+' | grep -Ev '^\+{3}' \
       | grep -qE '^\+[[:space:]]*(try|except|finally)([[:space:]]|:)'; then
    printf '{"decision":"block","reason":"Only human editors should add Try/Catch/Finally logic. Remove the try/except/finally statement before saving."}'
    exit 2
fi

# Write the diff to a temp file for Python to read cleanly
diff_tmp=$(mktemp)
trap 'rm -f "$diff_tmp"' EXIT
printf '%s\n' "$diff_output" > "$diff_tmp"

# Parse the diff and annotate changed sections with # START AI EDIT / # END AI EDIT
python3 - "$file_path" "$diff_tmp" << 'PYEOF'
import sys, re

file_path = sys.argv[1]
diff_file  = sys.argv[2]

with open(diff_file) as f:
    diff_lines = f.read().splitlines()

with open(file_path) as f:
    raw = f.read()
source_lines = raw.splitlines()
trailing_newline = raw.endswith('\n')

# Find contiguous change blocks (runs of + and/or - lines, broken by context lines).
# Each block's annotation span = first..last line number of its + lines (1-based).
sections = []
current_new = 0   # next new-file line number (1-based, per hunk header)
block_first = None
block_last  = None

for line in diff_lines:
    m = re.match(r'^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@', line)
    if m:
        if block_first is not None:
            sections.append((block_first, block_last))
            block_first = block_last = None
        current_new = int(m.group(1))
        continue
    if line.startswith('---') or line.startswith('+++'):
        continue
    if line.startswith('+'):
        if block_first is None:
            block_first = current_new
        block_last = current_new
        current_new += 1
    elif line.startswith('-'):
        pass  # removed line: no new-file line number consumed
    else:
        # Context line: close any open block
        if block_first is not None:
            sections.append((block_first, block_last))
            block_first = block_last = None
        current_new += 1

if block_first is not None:
    sections.append((block_first, block_last))

START = '  # START AI EDIT'
END   = '  # END AI EDIT'

for first, last in sections:
    si, ei = first - 1, last - 1
    if si < 0 or ei >= len(source_lines):
        continue
    if si == ei:
        source_lines[si] = source_lines[si].rstrip() + START + END
    else:
        source_lines[si] = source_lines[si].rstrip() + START
        source_lines[ei] = source_lines[ei].rstrip() + END

with open(file_path, 'w') as f:
    f.write('\n'.join(source_lines))
    if trailing_newline:
        f.write('\n')
PYEOF
