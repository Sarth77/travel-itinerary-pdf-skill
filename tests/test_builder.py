import copy
from datetime import datetime, timedelta, timezone
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SK = ROOT / 'travel-itinerary-pdf'
sys.path.insert(0, str(SK / 'scripts'))
import build
from rates import (validate_rates, flight_context, hotel_context, policy_text,
                   evidence_error, UNKNOWN_POLICY)
spec = importlib.util.spec_from_file_location('sample', SK / 'templates/trips_example.py')
sample = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sample)
NOW = datetime(2026, 11, 20, 12, tzinfo=timezone.utc)


def evidence(amount, context, now=NOW):
    return dict(source='Fixture provider', url='https://example.com/search?quote=test',
                captured_at=now.isoformat(), currency='INR', amount=amount, context=context)


def fixture():
    meta, trips = copy.deepcopy(sample.META), copy.deepcopy(sample.TRIPS)
    for trip in trips:
        fl = trip['flights']
        fl['rate'] = evidence(fl['price'], flight_context(meta, fl))
        fl['options'] = [(*o, evidence(o[3], flight_context(meta, fl, o))) for o in fl['options']]
        for hotel in trip['hotels'].values():
            hotel['rate'] = evidence(hotel['price'], hotel_context(meta, hotel))
    return meta, trips


class RateTests(unittest.TestCase):
    def setUp(self):
        self.meta, self.trips = fixture()

    def test_valid_quotes(self):
        self.assertEqual(validate_rates(self.meta, self.trips, NOW), [])

    def test_every_quote_requires_evidence(self):
        for target in ('selected', 'option', 'hotel'):
            with self.subTest(target=target):
                meta, trips = fixture()
                fl = trips[0]['flights']
                if target == 'selected': fl.pop('rate')
                elif target == 'option': fl['options'][1] = fl['options'][1][:5]
                else: next(iter(trips[0]['hotels'].values())).pop('rate')
                self.assertEqual(len(validate_rates(meta, trips, NOW)), 1)

    def test_bad_evidence(self):
        ev = self.trips[0]['flights']['rate']
        changes = [dict(source=''), dict(url='file:///tmp/quote'), dict(url='https://'),
                   dict(captured_at='garbage'), dict(captured_at='2026-11-20T12:00:00'),
                   dict(captured_at=(NOW+timedelta(seconds=1)).isoformat()),
                   dict(captured_at=(NOW-timedelta(hours=24, seconds=1)).isoformat()),
                   dict(amount=True), dict(amount=0), dict(currency='USD'), dict(context={})]
        for change in changes:
            with self.subTest(change=change):
                self.assertIsNotNone(evidence_error(ev | change, ev['amount'], ev['context'], NOW))
        self.assertIsNone(evidence_error(ev | {'captured_at': (NOW-timedelta(hours=24)).isoformat()}, ev['amount'], ev['context'], NOW))

    def test_context_mismatch(self):
        for key, value in [('origin_code', 'BOM'), ('departure_date', '2027-01-01'), ('pax', '3 Adults'), ('rooms', '2 rooms')]:
            with self.subTest(key=key):
                self.assertTrue(validate_rates(self.meta | {key: value}, self.trips, NOW))
        hotel = next(iter(self.trips[0]['hotels'].values()))
        hotel['room'] = 'Different room'
        self.assertTrue(validate_rates(self.meta, self.trips, NOW))

    def test_invalid_prices(self):
        for amount in (-1, float('nan'), float('inf'), True, '123'):
            with self.subTest(amount=amount):
                self.trips[0]['flights']['price'] = amount
                self.assertTrue(validate_rates(self.meta, self.trips, NOW))

    def test_policy_needs_rate_specific_fresh_evidence(self):
        fl = self.trips[0]['flights']
        context = flight_context(self.meta, fl)
        fl['policy'] = 'Free cancellation'  # legacy claims never count
        self.assertEqual(policy_text(fl, fl['price'], context, NOW), UNKNOWN_POLICY)
        fl['cancellation'] = dict(text='Outbound refundable until 18:00 IST; return non-refundable.', evidence=copy.deepcopy(fl['rate']))
        self.assertIn('Outbound refundable', policy_text(fl, fl['price'], context, NOW))
        fl['cancellation']['evidence']['context'] = {}
        self.assertEqual(policy_text(fl, fl['price'], context, NOW), UNKNOWN_POLICY)
        hotel = next(iter(self.trips[0]['hotels'].values()))
        hotel['cancellation'] = dict(text='Free until 21 Nov 12:00 IST; then full stay charge.', evidence=copy.deepcopy(hotel['rate']))
        self.assertIn('Free until', policy_text(hotel, hotel['price'], hotel_context(self.meta, hotel), NOW))
        hotel['cancellation']['evidence']['captured_at'] = (NOW-timedelta(days=2)).isoformat()
        self.assertEqual(policy_text(hotel, hotel['price'], hotel_context(self.meta, hotel), NOW), UNKNOWN_POLICY)

    def test_origin_totals_and_design(self):
        self.meta.update(origin_short='Mumbai', origin_city='Mumbai', origin_code='BOM')
        # This test exercises sample mode so changing the origin doesn't invent quote evidence.
        build.configure(self.meta, self.trips, '.', '.', True, NOW)
        totals = []
        for trip in self.trips:
            html, total = build.build(trip)
            totals.append(total)
            self.assertIn('Mumbai to ', html)
            self.assertNotIn('Delhi to ', html)
            self.assertIn('UNVERIFIED SAMPLE', html)
            self.assertNotIn('Live fare', html)
            self.assertNotIn('today\'s live', html)
            self.assertIn('CANCELLATION POLICIES', html)
            self.assertIn('class="meter"', html)
            self.assertIn('class="hero"', html)
            self.assertIn('class="summ"', html)
            self.assertIn('class="pill', html)
        self.assertEqual(totals, [64218, 50588, 50780])

    def test_validation_precedes_output(self):
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder) / 'not-created'
            result = subprocess.run([sys.executable, str(SK / 'scripts/build.py'), str(SK / 'templates/trips_example.py'), folder, str(out)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn('missing evidence', result.stderr)
            self.assertFalse(out.exists())

    def test_verified_sources_rendered_and_escaped(self):
        fl = self.trips[0]['flights']
        fl['rate']['source'] = '<provider>'
        build.configure(self.meta, self.trips, '.', '.', now=NOW)
        html, _ = build.build(self.trips[0])
        self.assertIn('&lt;provider&gt;', html)
        self.assertIn(fl['rate']['url'], html)
        self.assertIn('Within 24h', html)
        self.assertNotIn('All listed fares are non-refundable', html)


if __name__ == '__main__':
    unittest.main()
