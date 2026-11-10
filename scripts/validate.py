#!/usr/bin/env python3
from pathlib import Path
import sys
root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / 'tools/grantoza/skills/grants/scripts'))
from public_catalog import validate_repository
index = validate_repository(root)
print('Validated calls:', len(index['calls']))
