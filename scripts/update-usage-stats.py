#!/usr/bin/env python3
"""
Update usage statistics for Wingman Dashboard
Extracts session data and calculates costs PER MODEL
"""

import json
import subprocess
import re
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

def get_all_sessions():
    """Get all session statistics from openclaw sessions command"""
    try:
        result = subprocess.run(
            ['openclaw', 'sessions', '--json'],
            capture_output=True,
            text=True,
            cwd='/home/ubuntu/clawd'
        )
        
        if result.returncode != 0:
            print(f"Error getting sessions: {result.stderr}")
            return None
            
        data = json.loads(result.stdout)
        return data.get('sessions', [])
    except Exception as e:
        print(f"Error getting session stats: {e}")
        return None

def normalize_model_name(model):
    """Normalize model names for grouping"""
    if not model:
        return 'unknown'
    
    model = model.lower()
    
    # Group Claude models
    if 'claude' in model:
        if 'haiku' in model:
            return 'claude-haiku'
        elif 'sonnet' in model:
            return 'claude-sonnet'
        elif 'opus' in model:
            return 'claude-opus'
    
    # Group Grok models
    if 'grok' in model:
        return 'grok'
    
    # Group Gemini models
    if 'gemini' in model:
        return 'gemini'
    
    # Group GPT models
    if 'gpt' in model or 'o1' in model:
        if '4o' in model:
            return 'gpt-4o'
        elif 'o1' in model:
            return 'gpt-o1'
        return 'gpt'
    
    # DALL-E
    if 'dall-e' in model or 'dalle' in model:
        return 'dall-e'
    
    return model

def get_model_display_name(model_key):
    """Get friendly display name for model"""
    names = {
        'claude-haiku': 'Claude Haiku',
        'claude-sonnet': 'Claude Sonnet',
        'claude-opus': 'Claude Opus',
        'grok': 'Grok',
        'gemini': 'Gemini',
        'gpt-4o': 'GPT-4o',
        'gpt-o1': 'GPT-o1',
        'gpt': 'GPT',
        'dall-e': 'DALL-E',
        'unknown': 'Unknown'
    }
    return names.get(model_key, model_key.upper())

def get_model_cost_rate(model_key):
    """Get cost per million tokens (average of input/output)"""
    rates = {
        'claude-haiku': 0.4,      # $0.25 input, $1.25 output
        'claude-sonnet': 3.0,     # $3 input, $15 output
        'claude-opus': 15.0,      # $15 input, $75 output
        'grok': 10.0,             # $5 input, $15 output (estimate)
        'gemini': 2.5,            # Varies by tier, using mid-range
        'gpt-4o': 5.0,            # $2.50 input, $10 output
        'gpt-o1': 30.0,           # Higher tier reasoning model
        'gpt': 5.0,               # Generic GPT
        'dall-e': 20.0,           # Image generation (per 1M equivalent tokens)
        'unknown': 5.0
    }
    return rates.get(model_key, 5.0)

def aggregate_model_usage(sessions):
    """Aggregate token usage and costs by model"""
    model_stats = defaultdict(lambda: {
        'total_tokens': 0,
        'input_tokens': 0,
        'output_tokens': 0,
        'session_count': 0
    })
    
    main_session_info = None
    
    for session in sessions:
        model = session.get('model', 'unknown')
        normalized = normalize_model_name(model)
        
        total = session.get('totalTokens', 0)
        input_tok = session.get('inputTokens', 0)
        output_tok = session.get('outputTokens', 0)
        
        model_stats[normalized]['total_tokens'] += total
        model_stats[normalized]['input_tokens'] += input_tok
        model_stats[normalized]['output_tokens'] += output_tok
        model_stats[normalized]['session_count'] += 1
        
        # Capture main session info
        if session.get('key') == 'agent:main:main':
            main_session_info = {
                'context_pct': int((total / session.get('contextTokens', 1)) * 100) if session.get('contextTokens') else 0,
                'used_tokens': total,
                'max_tokens': session.get('contextTokens', 131072),
                'model': model
            }
    
    # Calculate costs for each model
    model_breakdown = []
    total_cost_daily = 0
    total_cost_weekly = 0
    total_cost_monthly = 0
    
    for model_key, stats in model_stats.items():
        rate = get_model_cost_rate(model_key)
        
        # Estimate daily usage based on current session totals
        # Assuming these represent cumulative usage, scale to daily estimate
        daily_tokens = stats['total_tokens'] * 0.1  # Conservative 10% daily churn
        weekly_tokens = daily_tokens * 7
        monthly_tokens = daily_tokens * 30
        
        daily_cost = (daily_tokens / 1_000_000) * rate
        weekly_cost = (weekly_tokens / 1_000_000) * rate
        monthly_cost = (monthly_tokens / 1_000_000) * rate
        
        total_cost_daily += daily_cost
        total_cost_weekly += weekly_cost
        total_cost_monthly += monthly_cost
        
        model_breakdown.append({
            'model': model_key,
            'display_name': get_model_display_name(model_key),
            'total_tokens': stats['total_tokens'],
            'input_tokens': stats['input_tokens'],
            'output_tokens': stats['output_tokens'],
            'session_count': stats['session_count'],
            'cost_rate': rate,
            'costs': {
                'daily': round(daily_cost, 2),
                'weekly': round(weekly_cost, 2),
                'monthly': round(monthly_cost, 2)
            }
        })
    
    # Sort by total tokens (most used first)
    model_breakdown.sort(key=lambda x: x['total_tokens'], reverse=True)
    
    return model_breakdown, main_session_info, {
        'daily': round(total_cost_daily, 2),
        'weekly': round(total_cost_weekly, 2),
        'monthly': round(total_cost_monthly, 2)
    }

def get_compaction_count():
    """Count compaction events from memory files"""
    memory_dir = Path('/home/ubuntu/.openclaw/memory')
    compaction_count = 0
    
    try:
        if memory_dir.exists():
            for file in memory_dir.glob('*.json'):
                try:
                    with open(file) as f:
                        data = json.load(f)
                        if isinstance(data, dict):
                            content = json.dumps(data).lower()
                            compaction_count += content.count('compact')
                except:
                    pass
    except Exception as e:
        print(f"Error counting compactions: {e}")
    
    return compaction_count

def main():
    print("Updating usage statistics with model breakdown...")
    
    # Get all sessions
    sessions = get_all_sessions()
    if not sessions:
        print("Could not retrieve session data")
        return
    
    # Aggregate by model
    model_breakdown, main_session, total_costs = aggregate_model_usage(sessions)
    
    # Get compaction count
    compaction_count = get_compaction_count()
    
    # Build usage data
    usage_data = {
        'updated_at': datetime.utcnow().isoformat() + 'Z',
        'context': {
            'percentage': main_session['context_pct'] if main_session else 0,
            'used_tokens': main_session['used_tokens'] if main_session else 0,
            'max_tokens': main_session['max_tokens'] if main_session else 131072,
            'tokens_display': f"{(main_session['used_tokens']//1000) if main_session else 0}k/{(main_session['max_tokens']//1000) if main_session else 131}k"
        },
        'compaction': {
            'count': compaction_count,
            'last_date': datetime.utcnow().strftime('%Y-%m-%d')
        },
        'costs': total_costs,
        'model': main_session['model'] if main_session else 'unknown',
        'model_breakdown': model_breakdown,
        'total_sessions': len(sessions)
    }
    
    # Write to JSON file
    output_path = Path('/home/ubuntu/clawd/wingman-dashboard/usage.json')
    with open(output_path, 'w') as f:
        json.dump(usage_data, f, indent=2)
    
    print(f"✓ Usage stats updated: {len(model_breakdown)} models tracked")
    print(f"✓ Total costs: ${total_costs['daily']:.2f}/day, ${total_costs['weekly']:.2f}/week, ${total_costs['monthly']:.2f}/month")
    
    for model in model_breakdown[:5]:  # Show top 5
        print(f"  • {model['display_name']}: {model['total_tokens']:,} tokens, ${model['costs']['monthly']:.2f}/mo")
    
    print(f"✓ Written to {output_path}")

if __name__ == '__main__':
    main()
