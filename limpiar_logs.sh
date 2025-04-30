#!/bin/bash
LOG_DIR="/var/log/miapp"
find $LOG_DIR -name "*.log" -type f -mtime +7 -exec rm -f {} \;
