"""
Mission Control — Show full Notion workspace tree.
Run: python scripts/notion_tree.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
sys.stdout.reconfigure(encoding='utf-8')
from skills.builtin.notion_util import print_tree
print_tree()
