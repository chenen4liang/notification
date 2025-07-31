#!/usr/bin/env python3
"""
Check SEC Form 13F data availability and send Discord notifications
"""

import sys
import os
import argparse
import re
import subprocess
from datetime import datetime

# Import the check_for_month function from check_sec.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from check_sec import check_for_month
from send_discord_notification import send_discord_notification


def check_and_notify(year_month, silent=False, notify_only_if_available=False):
    """
    Check SEC data for a specific month and send Discord notification
    
    Args:
        year_month: String in format 'yyyy-mm' (e.g., '2025-06')
        silent: If True, suppress console output except for errors
        notify_only_if_available: If True, only send notification when data is available
    
    Returns:
        True if data is available, False otherwise
    """
    if not silent:
        print(f"Checking SEC Form 13F data for {year_month}...")
    
    # Check if data is available
    has_data = check_for_month(year_month)
    
    # Parse year and month for better formatting
    try:
        year, month = year_month.split('-')
        month_int = int(month)
        month_names = {
            1: 'January', 2: 'February', 3: 'March', 4: 'April',
            5: 'May', 6: 'June', 7: 'July', 8: 'August',
            9: 'September', 10: 'October', 11: 'November', 12: 'December'
        }
        month_name = month_names.get(month_int, month)
        formatted_month = f"{month_name} {year}"
    except:
        formatted_month = year_month
    
    # Prepare Discord notification
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    if has_data:
        emoji = "🟢"
        status = "**AVAILABLE**"
        color_text = "Data is now available"
        message = f"{emoji} **SEC Form 13F Data {status}**\n\n"
        message += f"✅ {color_text} for **{formatted_month}**\n"
        message += f"📊 Month checked: `{year_month}`\n"
        message += f"🕐 Checked at: {timestamp}\n\n"
        message += f"[View SEC Form 13F Data](https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets)"
    else:
        emoji = "🔴"
        status = "**NOT AVAILABLE**"
        color_text = "No data found"
        message = f"{emoji} **SEC Form 13F Data {status}**\n\n"
        message += f"❌ {color_text} for **{formatted_month}**\n"
        message += f"📊 Month checked: `{year_month}`\n"
        message += f"🕐 Checked at: {timestamp}\n\n"
        
        # Add helpful information about when data might be available
        try:
            quarter = (month_int - 1) // 3 + 1
            quarter_end_months = {1: "March", 2: "June", 3: "September", 4: "December"}
            quarter_end = quarter_end_months[quarter]
            message += f"ℹ️ **Note:** Form 13F data for Q{quarter} {year} (ending {quarter_end}) "
            message += f"typically becomes available 45 days after quarter end.\n\n"
        except:
            pass
            
        message += f"[Check SEC Form 13F Data](https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets)"
    
    # Send Discord notification based on settings
    notification_sent = False
    if not notify_only_if_available or has_data:
        notification_sent = send_discord_notification(message)
    
    if not silent:
        print(f"Data available: {has_data}")
        if notify_only_if_available and not has_data:
            print("ℹ️ No notification sent (data not available)")
        elif notification_sent:
            print("✅ Discord notification sent successfully")
        elif not notify_only_if_available or has_data:
            print("❌ Failed to send Discord notification")
    
    return has_data


def check_multiple_months(months, silent=False):
    """
    Check multiple months and send a summary notification
    
    Args:
        months: List of month strings in 'yyyy-mm' format
        silent: If True, suppress console output
    """
    results = {}
    for month in months:
        results[month] = check_for_month(month)
    
    # Prepare summary notification
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    message = "📊 **SEC Form 13F Data Availability Summary**\n\n"
    
    available_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    
    message += f"Checked **{total_count}** months - **{available_count}** have data available\n\n"
    
    # Sort months
    sorted_months = sorted(results.keys(), reverse=True)
    
    for month in sorted_months:
        has_data = results[month]
        emoji = "✅" if has_data else "❌"
        status = "Available" if has_data else "Not Available"
        message += f"{emoji} `{month}` - {status}\n"
    
    message += f"\n🕐 Checked at: {timestamp}\n"
    message += f"[View SEC Form 13F Data](https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets)"
    
    # Send Discord notification
    notification_sent = send_discord_notification(message)
    
    if not silent:
        print(f"\nSummary: {available_count}/{total_count} months have data available")
        if notification_sent:
            print("✅ Discord summary notification sent successfully")
        else:
            print("❌ Failed to send Discord notification")
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description='Check SEC Form 13F data and send Discord notifications',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python check_and_notify.py 2025-06                     # Check single month
  python check_and_notify.py 2025-06 2025-07 2025-08    # Check multiple months
  python check_and_notify.py --range 2025-01 2025-06    # Check range of months
  python check_and_notify.py 2025-06 --silent           # Suppress console output
  python check_and_notify.py --current-month            # Check current month
  python check_and_notify.py --current-month -n         # Only notify if data available
'''
    )
    
    parser.add_argument(
        'months',
        nargs='*',
        help='Month(s) to check in yyyy-mm format'
    )
    parser.add_argument(
        '--range',
        nargs=2,
        metavar=('START', 'END'),
        help='Check a range of months (inclusive)'
    )
    parser.add_argument(
        '--current-month',
        action='store_true',
        help='Check the current month'
    )
    parser.add_argument(
        '--silent', '-s',
        action='store_true',
        help='Suppress console output (only show errors)'
    )
    parser.add_argument(
        '--notify-only-if-available', '-n',
        action='store_true',
        help='Only send Discord notification if data is available'
    )
    
    args = parser.parse_args()
    
    # Determine which months to check
    months_to_check = []
    
    if args.current_month:
        # Get current month
        current_date = datetime.now()
        months_to_check.append(current_date.strftime("%Y-%m"))
    
    elif args.range:
        # Generate range of months
        start_year, start_month = map(int, args.range[0].split('-'))
        end_year, end_month = map(int, args.range[1].split('-'))
        
        current_year = start_year
        current_month = start_month
        
        while (current_year < end_year) or (current_year == end_year and current_month <= end_month):
            months_to_check.append(f"{current_year}-{current_month:02d}")
            current_month += 1
            if current_month > 12:
                current_month = 1
                current_year += 1
    
    elif args.months:
        months_to_check = args.months
    
    else:
        # Default to current month
        current_date = datetime.now()
        months_to_check = [current_date.strftime("%Y-%m")]
    
    # Validate month format
    for month in months_to_check:
        if not re.match(r'^\d{4}-\d{2}$', month):
            print(f"Error: Invalid month format '{month}'. Please use yyyy-mm format.")
            sys.exit(2)
    
    # Source bashrc to get environment variables
    bashrc_path = '/workspaces/notification/bashrc'
    if os.path.exists(bashrc_path):
        source_cmd = f'source {bashrc_path} && env'
        proc = subprocess.Popen(['bash', '-c', source_cmd], stdout=subprocess.PIPE)
        for line in proc.stdout:
            if line:
                key, _, value = line.decode('utf-8').partition('=')
                if key == 'discordChannel':
                    os.environ[key] = value.strip()
    
    # Check if we have Discord webhook
    if not os.environ.get('discordChannel'):
        print("Warning: discordChannel environment variable not set. Discord notifications will fail.")
        print("Set it with: export discordChannel='YOUR_WEBHOOK_URL'")
    
    # Process the checks
    if len(months_to_check) == 1:
        # Single month check
        has_data = check_and_notify(months_to_check[0], args.silent, args.notify_only_if_available)
        sys.exit(0 if has_data else 1)
    else:
        # Multiple months check
        results = check_multiple_months(months_to_check, args.silent)
        # Exit with 0 if any month has data, 1 if none have data
        sys.exit(0 if any(results.values()) else 1)


if __name__ == "__main__":
    main()