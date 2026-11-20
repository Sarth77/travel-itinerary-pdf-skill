"""Check the interpreter and installed distributions against the shipped pins."""
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
import platform
import sys

root = Path(__file__).resolve().parent.parent
errors = []
expected = (root / '.python-version').read_text().strip()
if platform.python_version() != expected:
    errors.append(f'Python {expected} required; found {platform.python_version()}')
for line in (root / 'requirements.txt').read_text().splitlines():
    if '==' not in line or line.lstrip().startswith('#'):
        continue
    name, expected = line.strip().split('==')
    try:
        actual = version(name)
    except PackageNotFoundError:
        actual = 'missing'
    if actual != expected:
        errors.append(f'{name}=={expected} required; found {actual}')
if errors:
    sys.exit('\n'.join(errors))
