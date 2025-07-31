#!/usr/bin/env python3
"""
Send notifications to Discord webhook
"""

import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime


def send_discord_notification(message, webhook_url=None):
    """
    Send a notification message to Discord webhook
    
    Args:
        message: The message to send
        webhook_url: Discord webhook URL (if not provided, uses discordChannel env var)
    
    Returns:
        True if successful, False otherwise
    """
    if not webhook_url:
        webhook_url = os.environ.get('discordChannel')
    
    if not webhook_url:
        print("Error: No Discord webhook URL provided and discordChannel environment variable not set")
        return False
    
    # Prepare the payload
    payload = {
        "content": message,
        "username": "SEC Data Monitor",
        "avatar_url": "https://www.sec.gov/themes/custom/uswds_sec/dist/images/logos/SEC_Logo.png"
    }
    
    # Convert to JSON
    json_data = json.dumps(payload).encode('utf-8')
    
    # Create the request
    req = urllib.request.Request(
        webhook_url,
        data=json_data,
        headers={
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    )
    
    try:
        # Send the request
        with urllib.request.urlopen(req) as response:
            if response.status == 204:
                print("✅ Notification sent successfully to Discord")
                return True
            else:
                print(f"❌ Unexpected response code: {response.status}")
                return False
                
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error: {e.code} - {e.reason}")
        if e.code == 400:
            print("Bad request - check your webhook URL and message format")
        elif e.code == 401:
            print("Unauthorized - invalid webhook URL")
        elif e.code == 404:
            print("Not found - webhook URL might be incorrect")
        elif e.code == 429:
            print("Rate limited - too many requests")
        return False
        
    except urllib.error.URLError as e:
        print(f"❌ URL Error: {e.reason}")
        return False
        
    except Exception as e:
        print(f"❌ Error sending notification: {e}")
        return False


def send_sec_data_notification(month_year, has_data):
    """
    Send a notification about SEC Form 13F data availability
    
    Args:
        month_year: The month being checked (e.g., '2025-06')
        has_data: Boolean indicating if data is available
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    if has_data:
        message = f"🟢 **SEC Form 13F Data Available**\n\n"
        message += f"Data for **{month_year}** is now available!\n"
        message += f"Checked at: {timestamp}"
    else:
        message = f"🔴 **SEC Form 13F Data Not Available**\n\n"
        message += f"No data found for **{month_year}**\n"
        message += f"Checked at: {timestamp}"
    
    return send_discord_notification(message)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Send Discord notifications')
    parser.add_argument('message', nargs='?', help='Message to send')
    parser.add_argument('--month', help='Month to report on (yyyy-mm format)')
    parser.add_argument('--has-data', action='store_true', help='Indicates data is available')
    parser.add_argument('--webhook', help='Discord webhook URL (overrides env variable)')
    
    args = parser.parse_args()
    
    if args.month:
        # Send SEC data notification
        success = send_sec_data_notification(args.month, args.has_data)
    elif args.message:
        # Send custom message
        success = send_discord_notification(args.message, args.webhook)
    else:
        # Send test message
        test_message = "🔔 Test notification from SEC Data Monitor"
        success = send_discord_notification(test_message, args.webhook)
    
    sys.exit(0 if success else 1)