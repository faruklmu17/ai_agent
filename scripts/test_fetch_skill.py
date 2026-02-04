#!/usr/bin/env python3
"""
Test script to fetch and display the first 30 lines of skill.md from Moltbook
"""
import sys
import os

# Add parent directory to path to import config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from config import MOLTBOOK_URL

def fetch_skill():
    """Fetch skill.md from Moltbook and print first 30 lines"""
    try:
        url = f"{MOLTBOOK_URL}/skill.md"
        print(f"Fetching skill.md from: {url}")
        print("-" * 60)
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        content = response.text
        lines = content.split('\n')
        
        # Print first 30 lines
        print(f"\nFirst 30 lines of skill.md:\n")
        for i, line in enumerate(lines[:30], 1):
            print(f"{i:3d}: {line}")
        
        print(f"\n{'-' * 60}")
        print(f"✓ Successfully fetched skill.md")
        print(f"✓ Total lines: {len(lines)}")
        print(f"✓ Total characters: {len(content)}")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"\n✗ Error fetching skill.md: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = fetch_skill()
    sys.exit(0 if success else 1)

