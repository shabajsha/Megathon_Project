#!/usr/bin/env python3
"""
Run the fraud pipeline located in the local `fraud/` subfolder.

Usage:
  python run_fraud.py path/to/image.jpg

This will print a single integer (0-100) — the fraud percentage.
"""
import sys
import os
root = os.path.dirname(os.path.abspath(__file__))
fraud_dir = os.path.join(root, 'fraud')
# Ensure we run with working directory inside fraud/ so pipeline_check finds its data files
os.chdir(fraud_dir)
sys.path.insert(0, fraud_dir)

try:
  from pipeline_check import aggregate_decision
except Exception as e:
  print(f"Error importing pipeline: {e}")
  sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python run_fraud.py path/to/image.jpg')
        sys.exit(1)
    img = sys.argv[1]
    res = aggregate_decision(img)
    pct = int(round(res.get('fraud_confidence', 0.0) * 100.0))
    print(pct)
