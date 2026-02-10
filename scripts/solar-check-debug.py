#!/usr/bin/env python3
"""
Solar System Monitor for Huntsville Cabin - Debug Version
"""

import sys
import re
import subprocess
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import time
from datetime import datetime

print("Starting solar check...", flush=True)

def extract_value(text, pattern, flags=0):
    """Extract a value using regex"""
    match = re.search(pattern, text, flags)
    return match.group(1) if match else "N/A"

def get_weather(location):
    """Fetch weather from wttr.in"""
    try:
        result = subprocess.run(
            ['curl', '-s', f'wttr.in/{location}?format=%l:+%c+%t+%h+%w'],
            capture_output=True,
            text=True,
            timeout=20
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        return f"{location}: (unavailable)"
    except Exception as e:
        print(f"Weather fetch error for {location}: {e}", file=sys.stderr, flush=True)
        return f"{location}: (error)"

def get_hitch_status():
    """Calculate days remaining on current hitch"""
    from datetime import datetime, timezone, timedelta
    
    central = timezone(timedelta(hours=-6))
    now_central = datetime.now(central)
    today_central = now_central.date()
    
    hitch_end = datetime(2026, 2, 3).date()
    days_remaining = (hitch_end - today_central).days + 1
    
    if days_remaining < 0:
        return "🏠 OFF HITCH"
    elif days_remaining == 0:
        return "🏠 OFF HITCH"
    elif days_remaining == 1:
        return "🏠 LAST DAY OF HITCH"
    else:
        return f"⏰ {days_remaining} days left on hitch"

def check_solar():
    """Log in and fetch solar system data"""
    
    print("Launching browser...", flush=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()
        
        try:
            print("Navigating to login page...", flush=True)
            page.goto("https://www.opticsre.com/login", wait_until='domcontentloaded', timeout=30000)
            time.sleep(2)
            
            print("Checking for popup...", flush=True)
            try:
                close_btn = page.locator('button:has-text("CLOSE")').first
                close_btn.click(timeout=3000)
                time.sleep(1)
            except:
                pass
            
            print("Filling login form...", flush=True)
            email_input = page.locator('input[type="email"], input[type="text"]').first
            email_input.fill('trentperry149@yahoo.com')
            
            password_input = page.locator('input[type="password"]').first
            password_input.fill('AydenZP1109!')
            
            print("Submitting login...", flush=True)
            submit_btn = page.locator('button[type="submit"]').first
            submit_btn.click()
            
            print("Waiting for navigation...", flush=True)
            try:
                page.wait_for_load_state('networkidle', timeout=15000)
            except PlaywrightTimeout:
                pass
            
            time.sleep(3)
            
            print("Extracting data...", flush=True)
            text = page.inner_text('body')
            
            # Extract system status
            system_time = extract_value(text, r'CURRENT SYSTEM TIME\s*:\s*(\d+/\d+/\d+\s+\d+:\d+)')
            system_state = extract_value(text, r'Right Now, You are\s+(\w+)')
            
            # Extract current readings
            solar_now = extract_value(text, r'Solar\s+([\d.]+)kW')
            load_now = extract_value(text, r'Load\s+([\d.]+)kW')
            gen_now = extract_value(text, r'Generator\s+([\d.]+)kW')
            voltage = extract_value(text, r'Voltage\s+([\d.]+)V')
            battery_temp = extract_value(text, r'([\d.]+)\s*°F')
            
            print("Navigating to yesterday...", flush=True)
            try:
                selectors = [
                    'button:has-text("<")',
                    'button:has-text("‹")',
                    'button[aria-label*="previous"]',
                    'button[aria-label*="Previous"]',
                    'i.fa-chevron-left',
                    '[class*="chevron-left"]',
                    '[class*="arrow-left"]',
                ]
                
                clicked = False
                for selector in selectors:
                    try:
                        arrow = page.locator(selector).first
                        arrow.click(timeout=3000)
                        clicked = True
                        time.sleep(2)
                        break
                    except:
                        continue
                
                if not clicked:
                    page.mouse.click(26, 59)
                    time.sleep(2)
                    
            except Exception as e:
                print(f"Could not click left arrow: {e}", file=sys.stderr, flush=True)
            
            print("Extracting yesterday's data...", flush=True)
            yesterday_text = page.inner_text('body')
            solar_yesterday = extract_value(yesterday_text, r'Solar\s+([\d.]+)kWh')
            gen_yesterday = extract_value(yesterday_text, r'From Gen\s+([\d.]+)kWh')
            load_yesterday = extract_value(yesterday_text, r'To Load\s+([\d.]+)kWh')
            
            print("Formatting output...", flush=True)
            print()
            print("☀️  HUNTSVILLE CABIN SOLAR SYSTEM")
            print(f"📅 System Time: {system_time}")
            print(f"🔋 Status: {system_state}")
            print(f"🛢️  {get_hitch_status()}")
            print()
            print("⚡ CURRENT READINGS")
            print(f"  Solar:     {solar_now} kW")
            print(f"  Load:      {load_now} kW")
            print(f"  Generator: {gen_now} kW {'🔴 RUNNING' if float(gen_now) > 0 else '⚪ OFF'}")
            print(f"  Battery:   {voltage} V @ {battery_temp}°F")
            print()
            print("📊 YESTERDAY'S TOTALS")
            print(f"  Solar Production:     {solar_yesterday} kWh")
            print(f"  Generator Production: {gen_yesterday} kWh")
            print(f"  Load Consumption:     {load_yesterday} kWh")
            print()
            
            gen_kw = float(gen_now) if gen_now != "N/A" else 0
            gen_kwh_yesterday = float(gen_yesterday) if gen_yesterday != "N/A" else 0
            
            if gen_kw > 0:
                print("⚠️  GENERATOR IS CURRENTLY RUNNING")
            elif gen_kwh_yesterday > 0:
                print(f"ℹ️  Generator ran yesterday: {gen_kwh_yesterday} kWh produced")
            else:
                print("✅ Generator did not run yesterday")
            
            print()
            print("🌤️  WEATHER")
            locations = [
                "Huntsville,Utah",
                "Johnson+City,Texas", 
                "Jal,New+Mexico"
            ]
            for i, loc in enumerate(locations):
                weather = get_weather(loc)
                print(f"  {weather}")
                if i < len(locations) - 1:
                    time.sleep(2)
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}", file=sys.stderr, flush=True)
            import traceback
            traceback.print_exc()
            try:
                page.screenshot(path='/home/ubuntu/clawd/scripts/solar-error.png')
            except:
                pass
            raise
        finally:
            print("Closing browser...", flush=True)
            browser.close()

if __name__ == "__main__":
    check_solar()
    print("Done!", flush=True)
