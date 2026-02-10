#!/usr/bin/env python3
"""
Update usage statistics for Wingman Dashboard
Extracts session data and calculates costs
"""

import json
import subprocess
import re
from datetime import datetime, timedelta
from pathlib import Path

def get_session_stats():
    """Get session statistics from openclaw sessions command"""
    try:
        result = subprocess.run(
            ['openclaw', 'sessions', '--format', 'json'],
            capture_output=True,
            text=True,
            cwd='/home/ubuntu/clawd'
        )
        
        output = result.stdout
        
        # Parse the text output for main session
        lines = output.split('\n')
        main_session = None
        
        for line in lines:
            if 'agent:main:main' in line and 'direct' in line:
                # Extract context percentage
                match = re.search(r'\((\d+)%\)', line)
                if match:
                    context_pct = int(match.group(1))
                    
                    # Extract tokens (e.g., "96k/131k")
                    token_match = re.search(r'(\d+)k/(\d+)k', line)
                    if token_match:
                        used_tokens = int(token_match.group(1)) * 1000
                        max_tokens = int(token_match.group(2)) * 1000
                        
                        # Extract model
                        model_match = re.search(r'(claude-sonnet-4-5|grok-4-1-fast-reasoning|claude-opus-4-5)', line)
                        model = model_match.group(1) if model_match else 'unknown'
                        
                        main_session = {
                            'context_pct': context_pct,
                            'used_tokens': used_tokens,
                            'max_tokens': max_tokens,
                            'model': model
                        }
                        break
        
        return main_session
    except Exception as e:
        print(f"Error getting session stats: {e}")
        return None

def get_compaction_count():
    """Count compaction events from memory files"""
    memory_dir = Path('/home/ubuntu/.openclaw/memory')
    compaction_count = 0
    
    try:
        # Check memory files for compaction references
        if memory_dir.exists():
            for file in memory_dir.glob('*.json'):
                try:
                    with open(file) as f:
                        data = json.load(f)
                        if isinstance(data, dict):
                            # Count compaction-related entries
                            content = json.dumps(data).lower()
                            compaction_count += content.count('compact')
                except:
                    pass
    except Exception as e:
        print(f"Error counting compactions: {e}")
    
    return compaction_count

def calculate_costs(used_tokens, model):
    """Calculate estimated costs based on token usage and model"""
    # Cost per million tokens (input/output average)
    cost_per_mtok = {
        'claude-sonnet-4-5': 3.0,  # $3 input, $15 output - using average
        'grok-4-1-fast-reasoning': 10.0,  # $5 input, $15 output
        'claude-opus-4-5': 15.0,   # $15 input, $75 output
    }
    
    rate = cost_per_mtok.get(model, 5.0)
    
    # Estimate daily usage (assuming 20 sessions per day)
    daily_tokens = used_tokens * 20
    weekly_tokens = daily_tokens * 7
    monthly_tokens = daily_tokens * 30
    
    return {
        'daily': round((daily_tokens / 1_000_000) * rate, 2),
        'weekly': round((weekly_tokens / 1_000_000) * rate, 2),
        'monthly': round((monthly_tokens / 1_000_000) * rate, 2),
        'rate_per_mtok': rate
    }

def main():
    print("Updating usage statistics...")
    
    # Get session stats
    session = get_session_stats()
    if not session:
        print("Could not retrieve session stats")
        session = {
            'context_pct': 0,
            'used_tokens': 0,
            'max_tokens': 131072,
            'model': 'unknown'
        }
    
    # Get compaction count
    compaction_count = get_compaction_count()
    
    # Calculate costs
    costs = calculate_costs(session['used_tokens'], session['model'])
    
    # Build usage data
    usage_data = {
        'updated_at': datetime.utcnow().isoformat() + 'Z',
        'context': {
            'percentage': session['context_pct'],
            'used_tokens': session['used_tokens'],
            'max_tokens': session['max_tokens'],
            'tokens_display': f"{session['used_tokens']//1000}k/{session['max_tokens']//1000}k"
        },
        'compaction': {
            'count': compaction_count,
            'last_date': datetime.utcnow().strftime('%Y-%m-%d')
        },
        'costs': costs,
        'model': session['model']
    }
    
    # Write to JSON file
    output_path = Path('/home/ubuntu/clawd/wingman-dashboard/usage.json')
    with open(output_path, 'w') as f:
        json.dump(usage_data, f, indent=2)
    
    print(f"✓ Usage stats updated: {session['context_pct']}% context, {compaction_count} compactions")
    print(f"✓ Estimated costs: ${costs['daily']}/day, ${costs['weekly']}/week, ${costs['monthly']}/month")
    print(f"✓ Written to {output_path}")

if __name__ == '__main__':
    main()
