#!/bin/bash
# Debug wrapper to instrument latexmk runs and log to /Users/xichen/Documents/hithesis-master/.cursor/debug-eee92d.log
# Hypothesis A: Is $max_repeat=2 too aggressive for the doc?
# Hypothesis B: How many xelatex passes does latexmk actually run?
# Hypothesis C: Citation resolution cycle length
# Hypothesis D: splitindex/glossary invocation
# Hypothesis E: Forward reference cycles

set -u
LOG=/Users/xichen/Documents/hithesis-master/.cursor/debug-eee92d.log
WS=/Users/xichen/Documents/hithesis-master
STDERR_LOG=$WS/.cursor/latexmk-stderr.log

# Helper to write NDJSON log (one line per call)
ndjson_log() {
  local hypothesis="$1"
  local location="$2"
  local message="$3"
  local data="$4"
  local id="log_$(date +%s)_$$_$RANDOM"
  printf '{"sessionId":"eee92d","id":"%s","timestamp":%s,"location":"%s","message":"%s","data":%s,"runId":"debug-1","hypothesisId":"%s"}\n' \
    "$id" "$(date +%s)000" "$location" "$message" "$data" "$hypothesis" >> "$LOG"
}

# Ensure log file exists & clear
: > "$LOG"
ndjson_log "A" "tmp/debug-build.sh:start" "Wrapper starting" "{\"ws\":\"$WS\"}"

# Capture pre-state
PRE_AUX_COUNT=$(find "$WS" -name "*.aux" 2>/dev/null | wc -l | tr -d ' ')
ndjson_log "A" "tmp/debug-build.sh:pre" "Before latexmk: aux file count" "{\"aux_files\":$PRE_AUX_COUNT}"

PRE_BIB_COUNT=$(find "$WS" -name "*.bbl" 2>/dev/null | wc -l | tr -d ' ')
ndjson_log "D" "tmp/debug-build.sh:pre" "Before latexmk: bbl file count" "{\"bbl_files\":$PRE_BIB_COUNT}"

# Hypothesis A: check the .latexmkrc override
if [ -f "$WS/.latexmkrc" ]; then
  MAXREPEAT=$(grep -E '^\$max_repeat' "$WS/.latexmkrc" | head -1)
  ndjson_log "A" "tmp/debug-build.sh:rcfile" "Detected .latexmkrc override" "{\"max_repeat_line\":\"$MAXREPEAT\"}"
else
  ndjson_log "A" "tmp/debug-build.sh:rcfile" "No .latexmkrc override found" "{}"
fi

# Look at the workspace latexmkrc (full one) — hypothesis D
if [ -f "$WS/latexmkrc" ]; then
  HAS_SPLITINDEX=$(grep -c "splitindex" "$WS/latexmkrc")
  HAS_BIBTEX_USE=$(grep -c "^\$bibtex_use" "$WS/latexmkrc")
  ndjson_log "D" "tmp/debug-build.sh:rcfile" "Workspace latexmkrc (non-hidden) state" "{\"has_splitindex\":$HAS_SPLITINDEX,\"has_bibtex_use\":$HAS_BIBTEX_USE}"
fi

# Hypothesis B/D: Run latexmk with -gg (very verbose) to log every tool invocation
START_TIME=$(date +%s)
ndjson_log "B" "tmp/debug-build.sh:start" "Running latexmk -gg -xelatex" "{\"start_time\":$START_TIME}"

cd "$WS"
latexmk -gg -xelatex thesis.tex > "$STDERR_LOG" 2>&1
RC=$?
END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))
ndjson_log "A" "tmp/debug-build.sh:done" "latexmk finished" "{\"exit_code\":$RC,\"elapsed_sec\":$ELAPSED}"

# Count tool invocations
XELATEX_RUNS=$(grep -c "Run number .* of rule 'xelatex'" "$STDERR_LOG" 2>/dev/null || echo 0)
BIBTEX_RUNS=$(grep -c "Run number .* of rule 'bibtex'" "$STDERR_LOG" 2>/dev/null || echo 0)
SPLITINDEX_RUNS=$(grep -c "Run number .* of rule 'splitindex'" "$STDERR_LOG" 2>/dev/null || echo 0)
MAKEINDEX_RUNS=$(grep -c "Run number .* of rule 'makeindex'" "$STDERR_LOG" 2>/dev/null || echo 0)
ndjson_log "B" "tmp/debug-build.sh:summary" "Tool invocation counts" "{\"xelatex_runs\":$XELATEX_RUNS,\"bibtex_runs\":$BIBTEX_RUNS,\"splitindex_runs\":$SPLITINDEX_RUNS,\"makeindex_runs\":$MAKEINDEX_RUNS}"

# Hypothesis A: did latexmk hit max_repeat?
UNSTABLE=$(grep -c "Maximum runs of xelatex reached" "$STDERR_LOG" 2>/dev/null || echo 0)
ndjson_log "A" "tmp/debug-build.sh:summary" "Did latexmk hit max_repeat" "{\"hit_max\":$UNSTABLE}"

# Hypothesis E: forward-reference cycles
UNDEFINED_REFS=$(grep -c "LaTeX Warning: Reference.*undefined" "$STDERR_LOG" 2>/dev/null || echo 0)
ndjson_log "E" "tmp/debug-build.sh:summary" "Undefined ref warnings (forward refs)" "{\"undefined_refs\":$UNDEFINED_REFS}"

# Hypothesis C: citation cycle
UNDEFINED_CITES=$(grep -c "Package natbib Warning: Citation.*undefined" "$STDERR_LOG" 2>/dev/null || echo 0)
ndjson_log "C" "tmp/debug-build.sh:summary" "Undefined citation warnings" "{\"undefined_cites\":$UNDEFINED_CITES}"

# Did bibtex re-run (sign of a cite-key cycle)?
BIBTEX_INVOCATIONS=$(grep -c "This is BibTeX" "$STDERR_LOG" 2>/dev/null || echo 0)
ndjson_log "C" "tmp/debug-build.sh:summary" "BibTeX process invocations" "{\"bibtex_invocations\":$BIBTEX_INVOCATIONS}"

# Look at the LAST aux file content for chap3 (the one we edited) — to see what unresolved labels it has
if [ -f "$WS/body/chap3.aux" ]; then
  NEW_LABELS=$(grep -c "newlabel" "$WS/body/chap3.aux" 2>/dev/null || echo 0)
  ndjson_log "E" "tmp/debug-build.sh:post" "chap3.aux newlabel count" "{\"newlabels\":$NEW_LABELS}"
fi

ndjson_log "B" "tmp/debug-build.sh:done" "Wrapper finished" "{}"
echo "DEBUG: log written to $LOG"
echo "DEBUG: stderr-capture at $STDERR_LOG"
exit $RC
