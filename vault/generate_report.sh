#!/data/data/com.termux/files/usr/bin/bash
set -u

LOG_FILE="$HOME/.agate_node/vault/consensus_memory.json"
REPORT_FILE="$HOME/.agate_node/vault/forensic_summary.txt"
PARSER="$(dirname "$0")/parse_audit_log.py"

if ! command -v python3 >/dev/null 2>&1; then
    echo "BLOCKED: python3 is required to validate the audit log."
    exit 2
fi
METRICS=$(python3 "$PARSER" "$LOG_FILE") || {
    echo "AUDIT DATA INVALID OR UNAVAILABLE; refusing to generate a verified report."
    exit 2
}
IFS=$'\t' read -r TOTAL_ATTEMPTS FAILED_ATTEMPTS SUCCESS_ATTEMPTS <<< "$METRICS"
TIMESTAMP=$(date -Iseconds)

{
    echo "--- AGATE FORENSIC AUDIT: $TIMESTAMP ---"
    echo "Evidence status: JSONL records validated."
    echo "Event records: $TOTAL_ATTEMPTS."
    echo "Recorded failures: $FAILED_ATTEMPTS."
    echo "Recorded successful responses: $SUCCESS_ATTEMPTS."
    echo "Security posture: NOT ASSESSED BY THIS LOG."
    echo "Firewall enforcement: NOT VERIFIED."
    echo "Note: connection failures are service-availability observations, not proof of intrusion or firewall blocking."
    echo "--- END LOG ---"
} > "$REPORT_FILE"

cat "$REPORT_FILE"
