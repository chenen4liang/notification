#!/usr/bin/env python3
"""
Use curl command via subprocess to check SEC data
Sometimes curl can bypass restrictions that Python libraries face
"""

import subprocess
import re
from datetime import datetime
import argparse
import sys


def check_for_month(year_month):
    """
    Check if SEC Form 13F page has data from a specific month
    Args:
        year_month: String in format 'yyyy-mm' (e.g., '2025-06')
    Returns True if data from this month is found, False otherwise
    """
    url = "https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets"
    
    # Curl command with various options to mimic a real browser
    curl_cmd = [
        'curl',
        '-s',  # Silent mode
        '-L',  # Follow redirects
        '--compressed',  # Accept compressed responses
        '-H', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        '-H', 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        '-H', 'Accept-Language: en-US,en;q=0.5',
        '-H', 'DNT: 1',
        '-H', 'Connection: keep-alive',
        '-H', 'Upgrade-Insecure-Requests: 1',
        '--max-time', '30',
        url
    ]
    
    try:
        # Execute curl command
        result = subprocess.run(curl_cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and len(result.stdout) > 100:
            html_content = result.stdout
            
            # Parse year and month
            try:
                year, month = year_month.split('-')
                month_int = int(month)
                year_int = int(year)
            except ValueError:
                return False
            
            # Map month numbers to names
            month_names = {
                1: ('January', 'Jan'), 2: ('February', 'Feb'), 3: ('March', 'Mar'),
                4: ('April', 'Apr'), 5: ('May', 'May'), 6: ('June', 'Jun'),
                7: ('July', 'Jul'), 8: ('August', 'Aug'), 9: ('September', 'Sep'),
                10: ('October', 'Oct'), 11: ('November', 'Nov'), 12: ('December', 'Dec')
            }
            
            if month_int not in month_names:
                return False
                
            full_name, short_name = month_names[month_int]
            
            # Determine which quarter this month belongs to
            quarter = (month_int - 1) // 3 + 1
            
            # Search patterns for the specified month
            month_patterns = [
                # Various date formats
                rf'{full_name}\s*{year}|{short_name}\s*{year}|{month}/{year}|{year}-{month}|{year}/{month}',
                rf'{full_name}\s*{year}|{short_name}\s*{year}|{month_int:02d}/{year}|{year}-{month_int:02d}|{year}/{month_int:02d}',
                # Quarter patterns
                rf'{year}Q{quarter}|Q{quarter}\s*{year}|{year}\s*Q{quarter}',
                # File patterns that might include this month
                rf'13F.*{year}[_-]?{month_int:02d}|{year}[_-]?{month_int:02d}.*13F',
                rf'13F.*{year}[_-]?{full_name}|{year}[_-]?{full_name}.*13F',
                rf'13F.*{year}[_-]?{short_name}|{year}[_-]?{short_name}.*13F',
                # Multi-month patterns - detect month within a range like "2024 December 2025 January February"
                rf'{year}\s+{full_name}',  # e.g. "2025 January"
                rf'{full_name}\s+{short_name}.*{year}|{year}\s+{full_name}\s+{short_name}',  # month names followed by year
                # Date range patterns that might include this month
                rf'\d{{2}}{short_name}{year}|\d{{2}}{full_name}{year}',  # e.g. "01jan2025" or "01january2025"
                rf'{month_int:02d}\w{{3}}{year[-2:]}',  # e.g. "01jan25"
            ]
            
            for pattern in month_patterns:
                if re.search(pattern, html_content, re.IGNORECASE):
                    return True
                    
            return False
            
        else:
            return False
            
    except:
        return False


def check_with_curl():
    """
    Use curl command to fetch SEC page
    """
    url = "https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets"
    
    print("Using curl to fetch SEC Form 13F page...")
    print("="*60)
    
    # Curl command with various options to mimic a real browser
    curl_cmd = [
        'curl',
        '-s',  # Silent mode
        '-L',  # Follow redirects
        '--compressed',  # Accept compressed responses
        '-H', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        '-H', 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        '-H', 'Accept-Language: en-US,en;q=0.5',
        '-H', 'DNT: 1',
        '-H', 'Connection: keep-alive',
        '-H', 'Upgrade-Insecure-Requests: 1',
        '--max-time', '30',
        url
    ]
    
    try:
        # Execute curl command
        result = subprocess.run(curl_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            html_content = result.stdout
            
            if len(html_content) > 100:
                print("✅ Successfully fetched page content with curl")
                
                # Search for 2025 references
                found_2025 = False
                found_items = []
                
                # Search patterns
                patterns = [
                    r'2025Q[1-4]',
                    r'Q[1-4]\s*2025',
                    r'href=["\'][^"\']*2025[^"\']*["\']',
                    r'>([^<]*2025[^<]*)<',
                    r'13F.*2025|2025.*13F'
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, html_content, re.IGNORECASE)
                    if matches:
                        found_2025 = True
                        for match in matches[:3]:  # Limit matches
                            found_items.append(f"Match: {match[:100]}...")
                
                print("\n" + "-"*60)
                print("RESULTS:")
                print("-"*60)
                
                if found_2025:
                    print("\n✅ FOUND 2025 DATA!")
                    print("\nMatches:")
                    for item in set(found_items):
                        print(f"  - {item}")
                else:
                    print("\n❌ No 2025 data found on the page")
                    
                    # Look for recent quarters
                    recent_quarters = re.findall(r'(20\d{2}Q[1-4])', html_content)
                    if recent_quarters:
                        print("\nMost recent quarters found:")
                        for q in sorted(set(recent_quarters), reverse=True)[:5]:
                            print(f"  - {q}")
                            
            else:
                print("❌ Page content is too short, might be an error page")
                print(f"Content preview: {html_content[:200]}")
                
        else:
            print(f"❌ Curl command failed with return code: {result.returncode}")
            if result.stderr:
                print(f"Error: {result.stderr}")
                
    except FileNotFoundError:
        print("❌ curl command not found. Please install curl:")
        print("  Ubuntu/Debian: sudo apt-get install curl")
        print("  MacOS: brew install curl")
        print("  Windows: Download from https://curl.se/windows/")
    except Exception as e:
        print(f"❌ Error running curl: {e}")


def check_edgar_api_with_curl():
    """
    Try SEC EDGAR API with curl
    """
    print("\n" + "="*60)
    print("Checking SEC EDGAR Search API with curl...")
    print("="*60)
    
    # EDGAR search API endpoint
    api_url = "https://efts.sec.gov/LATEST/search-index"
    
    # JSON payload for searching 13F forms in 2025
    json_data = '{"q":"13F","dateRange":"custom","startdt":"2025-01-01","enddt":"2025-12-31","forms":"13F-HR,13F-NT"}'
    
    curl_cmd = [
        'curl',
        '-s',
        '-X', 'POST',
        '-H', 'Content-Type: application/json',
        '-H', 'User-Agent: Mozilla/5.0 (compatible; SEC-Monitor/1.0)',  # Generic user agent
        '-H', 'Accept: application/json',
        '-d', json_data,
        '--max-time', '15',
        api_url
    ]
    
    try:
        result = subprocess.run(curl_cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and result.stdout:
            try:
                import json
                data = json.loads(result.stdout)
                hits = data.get('hits', {}).get('total', {}).get('value', 0)
                
                print(f"✅ API Response: Found {hits} Form 13F filings for 2025")
                
                if hits > 0:
                    print("\nSome 2025 Form 13F filings exist!")
                else:
                    print("\nNo 2025 Form 13F filings found yet")
                    
            except json.JSONDecodeError:
                print("Could not parse API response")
                print(f"Response preview: {result.stdout[:200]}")
        else:
            print(f"API request failed: {result.stderr if result.stderr else 'No response'}")
            
    except Exception as e:
        print(f"Error with API request: {e}")


def alternative_approaches():
    """
    Suggest alternative approaches
    """
    print("\n" + "="*60)
    print("Alternative Approaches to Get SEC 13F Data:")
    print("="*60)
    
    print("\n1. Use wget instead of curl:")
    print("   wget -qO- --user-agent='Mozilla/5.0' 'https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets'")
    
    print("\n2. Use lynx text browser:")
    print("   lynx -dump 'https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets'")
    
    print("\n3. Use a proxy service:")
    print("   - ScraperAPI, ProxyMesh, or similar services")
    print("   - They handle anti-bot measures automatically")
    
    print("\n4. SEC EDGAR Direct Downloads:")
    print("   - https://www.sec.gov/Archives/edgar/daily-index/")
    print("   - Look for index files that list all daily filings")
    
    print("\n5. Third-party APIs:")
    print("   - polygon.io - Financial data API")
    print("   - finnhub.io - Stock market API with SEC filings")
    print("   - sec-api.io - Dedicated SEC EDGAR API service")


def main(year_month=None):
    """
    Main function that returns True if data for the specified month is found
    Args:
        year_month: String in format 'yyyy-mm' (e.g., '2025-06')
                   If None, defaults to checking June/July/August 2025
    """
    # Check for specified month or default months
    if year_month:
        has_data = check_for_month(year_month)
        # Simple output when checking specific month
        print(str(has_data).lower())
    else:
        # Default: check for June, July, or August 2025
        has_data = any([
            check_for_month('2025-06'),
            check_for_month('2025-07'),
            check_for_month('2025-08')
        ])
        month_desc = "June/July/August 2025"
        
        # Verbose output for default mode
        print("="*60)
        print(f"SEC Form 13F Data Check for {month_desc}")
        print("="*60)
        print(f"Result: {has_data}")
        print("="*60)
        
        # Also run the original checks for more details
        check_with_curl()
        check_edgar_api_with_curl()
        alternative_approaches()
        
        print("\n" + "="*60)
        print("Note: Form 13F filings are due 45 days after each quarter ends.")
        print("Q1 2025 (Jan-Mar) filings would appear around mid-May 2025.")
        print("Q2 2025 (Apr-Jun) filings would appear around mid-August 2025.")
        print("Q3 2025 (Jul-Sep) filings would appear around mid-November 2025.")
        print("="*60)
    
    # Return the boolean result
    return has_data


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Check if SEC Form 13F data is available for a specific month',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python check_sec.py                    # Check for June/July/August 2025 (default)
  python check_sec.py 2025-06            # Check for June 2025
  python check_sec.py 2025-12            # Check for December 2025
  python check_sec.py 2024-03            # Check for March 2024
'''
    )
    parser.add_argument(
        'month',
        nargs='?',
        help='Month to check in yyyy-mm format (e.g., 2025-06)'
    )
    
    args = parser.parse_args()
    
    # Validate month format if provided
    if args.month:
        if not re.match(r'^\d{4}-\d{2}$', args.month):
            print(f"Error: Invalid month format '{args.month}'. Please use yyyy-mm format (e.g., 2025-06)")
            sys.exit(2)
    
    result = main(args.month)
    # Exit with 0 if True (data found), 1 if False (no data)
    sys.exit(0 if result else 1)