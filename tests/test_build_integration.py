"""End-to-end Chromium builds and PDF text checks; use the pinned venv."""
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import pymupdf
from test_builder import ROOT, SK, fixture, sample


class BuildIntegrationTests(unittest.TestCase):
    def test_sample_and_verified_builds(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for mode in ('sample', 'verified'):
                out = root / mode
                data = SK / 'templates/trips_example.py'
                args = ['--allow-unverified'] if mode == 'sample' else []
                if mode == 'verified':
                    meta, trips = fixture()
                    # Synthetic test evidence only, generated at test time. Never a travel deliverable.
                    now = datetime.now(timezone.utc).isoformat()
                    for trip in trips:
                        fl = trip['flights']
                        fl['rate']['captured_at'] = now
                        for option in fl['options']: option[5]['captured_at'] = now
                        for hotel in trip['hotels'].values(): hotel['rate']['captured_at'] = now
                    data = root / 'fixture.py'
                    data.write_text(f'META = {meta!r}\nTRIPS = {trips!r}\n')
                result = subprocess.run([sys.executable, str(SK / 'scripts/build.py'), str(data), folder, str(out), *args], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                pdfs = sorted(out.glob('*.pdf'))
                self.assertEqual(len(pdfs), 3)
                for pdf in pdfs:
                    with pymupdf.open(pdf) as doc:
                        self.assertGreaterEqual(len(doc), 7)
                        self.assertTrue(all(abs(p.rect.width-595.28) < 1 and abs(p.rect.height-841.89) < 1 for p in doc))
                        text = ''.join(p.get_text() for p in doc)
                        for title in ('Your Itinerary', 'Flight Details', 'Day Wise Details', 'Cost Breakdown', 'CANCELLATION POLICIES'):
                            self.assertIn(title, text)
                        self.assertIn('Not verified for this fare/room rate', text)
                        self.assertNotIn('All listed fares are non-refundable', text)
                        self.assertNotIn('Both stays have free cancellation', text)
                        if mode == 'sample': self.assertIn('UNVERIFIED SAMPLE', text)
                        else: self.assertIn('Fixture provider', text)


if __name__ == '__main__':
    unittest.main()
