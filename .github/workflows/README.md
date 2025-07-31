# GitHub Actions Setup for SEC Data Monitoring

This directory contains GitHub Actions workflows for automatically checking SEC Form 13F data availability.

## Workflows

### 1. check-sec-data.yml (Simple)
- Runs every hour
- Checks July 2025 data
- Only sends Discord notification if data becomes available

### 2. check-sec-data-advanced.yml (Advanced)
- Runs every hour at minute 15
- Supports manual triggering with custom month
- Option to always send notifications (for testing)

## Setup Instructions

### 1. Add Discord Webhook as GitHub Secret

1. Go to your GitHub repository
2. Navigate to Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add a secret named `DISCORD_WEBHOOK`
5. Paste your Discord webhook URL as the value
   - Format: `https://discord.com/api/webhooks/[ID]/[TOKEN]`

### 2. Enable GitHub Actions

1. Go to the Actions tab in your repository
2. Enable workflows if prompted

### 3. Customize the Workflow

To check a different month by default, edit the workflow file:
- Change `2025-07` to your desired month in `yyyy-mm` format

To change the schedule:
- Modify the cron expression (currently `0 * * * *` for hourly)
- Examples:
  - `0 */2 * * *` - Every 2 hours
  - `0 9,17 * * *` - At 9 AM and 5 PM daily
  - `0 9 * * 1-5` - At 9 AM on weekdays only

## Manual Triggering

You can manually run the advanced workflow:
1. Go to Actions tab
2. Select "SEC Form 13F Data Monitor"
3. Click "Run workflow"
4. Choose options:
   - Month to check (default: 2025-07)
   - Whether to always notify (default: only if data available)

## Monitoring

- Check the Actions tab to see workflow runs
- Green checkmark = successful run
- If data becomes available, you'll receive a Discord notification
- Failed runs will show a red X - check logs for errors

## Troubleshooting

If notifications aren't working:
1. Verify the `DISCORD_WEBHOOK` secret is set correctly
2. Check workflow logs for errors
3. Test manually with "Run workflow" button
4. Ensure the Discord webhook is active and not deleted