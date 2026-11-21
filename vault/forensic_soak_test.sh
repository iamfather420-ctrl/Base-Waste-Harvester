#!/data/data/com.termux/files/usr/bin/bash
set -u

LOG_FILE="$HOME/.agate_node/vault/consensus_memory.json"
ITERATIONS="${ITERATIONS:-50000}"
PORT=8888
mkdir -p "$HOME/.agate_node/vault" || exit 1

cleanup() {
    exec 3>&- 2>/dev/null || true
    termux-wake-unlock >/dev/null 2>&1 || true
}
trap 'cleanup; exit 130' INT TERM
trap cleanup EXIT

termux-wake-lock >/dev/null 2>&1 || true
echo "Initiating $ITERATIONS-cycle service-observation soak test (not an intrusion classifier)..."
exec 3>>"$LOG_FILE" || exit 1

for ((i=1; i<=ITERATIONS; i++)); do
    TIMESTAMP=$(date -Iseconds)
    HTTP_CODE=$(curl -sS -o /dev/null -w "%{http_code}" --connect-timeout 1 --max-time 2 "http://127.0.0.1:$PORT" 2>/dev/null)
    CURL_EXIT=$?

    if [ "$CURL_EXIT" -eq 0 ] && [ "$HTTP_CODE" = "200" ]; then
        STATUS="SUCCESS"
        EVENT="service_http_200"
    elif [ "$CURL_EXIT" -eq 0 ]; then
        STATUS="WARNING"
        EVENT="service_http_non_200"
    else
        STATUS="UNAVAILABLE"
        EVENT="service_connection_unavailable"
    fi

    printf '{"timestamp":"%s","id":%d,"status":"%s","event":"%s","http_code":"%s","curl_exit":%d}\n' \
        "$TIMESTAMP" "$i" "$STATUS" "$EVENT" "$HTTP_CODE" "$CURL_EXIT" >&3

    sleep 0.1
    if (( i % 1000 == 0 )); then
        echo "Audit Progress: $i / $ITERATIONS observations complete."
    fi
done

echo "Observation run complete. Network failures were recorded as UNAVAILABLE, not as verified intrusions."
