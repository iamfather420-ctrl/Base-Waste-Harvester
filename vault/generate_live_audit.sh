#!/data/data/com.termux/files/usr/bin/bash
set -u

LOG_FILE="$HOME/.agate_node/vault/consensus_memory.json"
PORT="8888"
TARGET_IP="127.0.0.1"
PARSER="$(dirname "$0")/parse_audit_log.py"

if ! command -v python3 >/dev/null 2>&1; then
    echo "BLOCKED: python3 is required to validate the audit log."
    exit 2
fi

METRICS=$(python3 "$PARSER" "$LOG_FILE") || {
    echo "AUDIT DATA INVALID OR UNAVAILABLE; no security verdict generated."
    exit 2
}
IFS=$'\t' read -r TOTAL_CYCLES BLOCK_COUNT SUCCESS_COUNT <<< "$METRICS"

if ping -c 1 -W 1 "$TARGET_IP" >/dev/null 2>&1; then
    PING_STATUS="HEARTBEAT_RESPONDED"
else
    PING_STATUS="HEARTBEAT_UNAVAILABLE"
fi

HTTP_CODE=$(curl -sS -o /dev/null -w "%{http_code}" --connect-timeout 1 --max-time 2 "http://$TARGET_IP:$PORT")
CURL_EXIT=$?
if [ "$CURL_EXIT" -eq 0 ]; then
    PORT_STATUS="SERVICE_REACHABLE_HTTP_$HTTP_CODE"
else
    PORT_STATUS="SERVICE_UNREACHABLE_OR_FILTERED_CURL_EXIT_$CURL_EXIT"
fi

echo "--- AGATE FORENSIC AUDIT: $(date -Iseconds) ---"
echo "VALIDATED EVENT RECORDS: $TOTAL_CYCLES"
echo "RECORDED FAILURES: $BLOCK_COUNT"
echo "RECORDED SUCCESSES: $SUCCESS_COUNT"
echo "CONNECTION HEARTBEAT: $PING_STATUS"
echo "PORT $PORT SERVICE STATUS: $PORT_STATUS"
echo "FIREWALL POLICY: NOT VERIFIED BY A FAILED CONNECTION"
if [ "$TOTAL_CYCLES" -gt 0 ]; then
    echo "RECORDED FAILURE RATE: $(( BLOCK_COUNT * 100 / TOTAL_CYCLES ))%"
else
    echo "RECORDED FAILURE RATE: NOT AVAILABLE (zero event records)"
fi
echo "RAW EVENT LOG TAIL (LAST 3):"
tail -n 3 "$LOG_FILE"
