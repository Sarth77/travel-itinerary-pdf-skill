import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PreflightTests(unittest.TestCase):
    def run_check(self, mode, fix=False):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            scripts = root / 'skill/scripts'
            scripts.mkdir(parents=True)
            (scripts / 'preflight.sh').write_bytes((ROOT / 'travel-itinerary-pdf/scripts/preflight.sh').read_bytes())
            (root / 'skill/.python-version').write_text('3.12.13')
            work = root / 'working folder'
            (work / 'venv/bin').mkdir(parents=True)
            bins = root / 'bin'; bins.mkdir()
            def executable(path, text):
                path.write_text('#!/bin/bash\n' + text); path.chmod(0o755)
            executable(bins / 'jq', 'exit 0\n')
            executable(bins / 'curl', 'if [ "$MODE" = network ]; then printf 000; exit 7; fi; printf 200\n')
            executable(work / 'venv/bin/python', '''if [[ "${1:-}" == *check_toolchain.py ]]; then
  [ "$MODE" != drift ]; exit $?
fi
cat >/dev/null
[ "$MODE" != chromium ]
''')
            if mode == 'missing': (work / 'venv/bin/python').unlink()
            executable(scripts / 'setup_env.sh', '[ "$MODE" != setup ]\n')
            env = os.environ | {'MODE': mode, 'PATH': str(bins) + ':/usr/bin:/bin'}
            return subprocess.run(['/bin/bash', str(scripts / 'preflight.sh'), str(work)] + (['--fix'] if fix else []), env=env, capture_output=True, text=True)

    def test_success(self):
        self.assertEqual(self.run_check('ok').returncode, 0)

    def test_failures_nonzero(self):
        for mode in ('network', 'drift', 'chromium', 'missing', 'setup'):
            with self.subTest(mode=mode):
                result = self.run_check(mode, fix=mode == 'setup')
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertNotIn('SUMMARY 0 issue(s)', result.stdout)


if __name__ == '__main__':
    unittest.main()
