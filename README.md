# SEC Form 13F Data Monitor

Automated monitoring system for SEC Form 13F data availability with Discord notifications.

## Overview

This project provides Python scripts to check the SEC website for Form 13F data availability and send notifications to Discord when new data becomes available. It includes GitHub Actions workflows for automated hourly checks.

## Features

- 🔍 Check SEC Form 13F data availability for specific months
- 📊 Support for single month or multiple months checking
- 🔔 Discord webhook notifications
- 🤖 GitHub Actions automation for hourly checks
- 🔕 Option to only notify when data becomes available (no spam)
- 📅 Flexible date range checking

## Quick Start

### 1. Prerequisites

- Python 3.7+
- Discord webhook URL ([How to create a Discord webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks))
- Git and GitHub account (for automated checks)

### 2. Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/notification.git
   cd notification
   ```

2. Set your Discord webhook URL:
   ```bash
   export discordChannel="https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_TOKEN"
   ```

### 3. Basic Usage

Check specific month:
```bash
python check_sec.py 2025-06
```

Check and send Discord notification:
```bash
python check_and_notify.py 2025-06
```

Check current month with notification only if data is available:
```bash
python check_and_notify.py --current-month --notify-only-if-available
```

## Scripts

### check_sec.py
Core script that checks SEC website for Form 13F data.

```bash
# Check specific month
python check_sec.py 2025-06

# Returns: true/false
```

### check_and_notify.py
Enhanced script that checks data and sends Discord notifications.

```bash
# Check single month
python check_and_notify.py 2025-06

# Check multiple months
python check_and_notify.py 2025-01 2025-02 2025-03

# Check range of months
python check_and_notify.py --range 2025-01 2025-06

# Check current month
python check_and_notify.py --current-month

# Only notify if data is available
python check_and_notify.py --current-month --notify-only-if-available
```

### send_discord_notification.py
Utility script for sending Discord notifications.

```bash
# Send custom message
python send_discord_notification.py "Your message here"

# Send SEC data notification
python send_discord_notification.py --month 2025-06 --has-data
```

## GitHub Actions Automation

The project includes workflows for automated checking:

### Setup GitHub Actions

1. Fork/clone this repository to your GitHub account

2. Add Discord webhook as a secret:
   - Go to Settings → Secrets and variables → Actions
   - Add secret named `DISCORD_WEBHOOK` with your webhook URL

3. Enable GitHub Actions in the repository

### Available Workflows

- **check-sec-data.yml**: Simple hourly check for July 2025
- **check-sec-data-advanced.yml**: Advanced workflow with manual triggers and options

The workflows run automatically every hour and only send notifications when new data becomes available.

## Environment Variables

- `discordChannel`: Discord webhook URL for notifications

## Data Availability Timeline

SEC Form 13F data is typically published according to this schedule:
- Q1 (Jan-Mar): Available around mid-May
- Q2 (Apr-Jun): Available around mid-August  
- Q3 (Jul-Sep): Available around mid-November
- Q4 (Oct-Dec): Available around mid-February

## Troubleshooting

1. **No Discord notifications:**
   - Verify `discordChannel` environment variable is set
   - Check webhook URL is valid and active
   - Test with: `python send_discord_notification.py "Test"`

2. **GitHub Actions not running:**
   - Ensure Actions are enabled in repository settings
   - Check workflow files are in `.github/workflows/`
   - Verify `DISCORD_WEBHOOK` secret is set

3. **Script returns false for known available data:**
   - SEC website structure may have changed
   - Try running with verbose output to debug

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is provided as-is for educational and monitoring purposes.