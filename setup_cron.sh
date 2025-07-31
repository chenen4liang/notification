#!/bin/bash

# Script to set up hourly cron job for SEC monitoring

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Create a cron script
cat > "$SCRIPT_DIR/run_sec_check.sh" << 'EOF'
#!/bin/bash
# Load Discord webhook from bashrc or environment
export discordChannel="${discordChannel:-YOUR_DISCORD_WEBHOOK_HERE}"

# Change to script directory
cd "$(dirname "$0")"

# Run the check
/usr/bin/python3 check_and_notify.py 2025-07 --notify-only-if-available >> sec_check.log 2>&1
EOF

# Make the script executable
chmod +x "$SCRIPT_DIR/run_sec_check.sh"

# Add to crontab (runs every hour at minute 5)
(crontab -l 2>/dev/null; echo "5 * * * * $SCRIPT_DIR/run_sec_check.sh") | crontab -

echo "✅ Cron job set up successfully!"
echo "📅 Will run every hour at minute 5"
echo "📝 Logs will be saved to: $SCRIPT_DIR/sec_check.log"
echo ""
echo "⚠️  Don't forget to:"
echo "1. Edit run_sec_check.sh and replace YOUR_DISCORD_WEBHOOK_HERE with your actual webhook"
echo "2. Or set the discordChannel environment variable"
echo ""
echo "To view current cron jobs: crontab -l"
echo "To remove this cron job: crontab -e (and delete the line)"