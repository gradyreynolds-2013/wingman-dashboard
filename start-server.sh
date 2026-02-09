#!/bin/bash

# Wingman Dashboard Keep-Alive Script
# Auto-restarts HTTP server if it crashes

LOG_FILE="/tmp/wingman-dashboard.log"
PIDFILE="/tmp/wingman-dashboard.pid"
PORT=8080
DIR="/home/ubuntu/clawd/wingman-dashboard"

echo "Starting Wingman Dashboard server..." >> $LOG_FILE
echo "$(date): Starting..." >> $LOG_FILE

while true; do
    # Check if process is running
    if [ -f "$PIDFILE" ] && kill -0 $(cat $PIDFILE) 2>/dev/null; then
        sleep 10
        continue
    fi
    
    # Start server
    cd $DIR
    python3 -m http.server $PORT --bind 0.0.0.0 >> $LOG_FILE 2>&1 &
    
    PID=$!
    echo $PID > $PIDFILE
    echo "$(date): Server started with PID $PID" >> $LOG_FILE
    
    # Wait for process
    wait $PID
    
    # If we get here, process died
    echo "$(date): Server crashed with PID $PID, restarting in 5 seconds..." >> $LOG_FILE
    sleep 5
done
