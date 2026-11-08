"""Synthetic contract checks; no legal merits evaluation."""
import unittest
from au_legal.workflow import review_gate, earnout, check_finding


class WorkflowTests(unittest.TestCase):
    def test_no_consent_blocks(self):
        out = review_gate(confidentiality_confirmed=False, privilege_reviewed=True,
                          playbook_counsel_approved=True)
        self.assertEqual(out['status'], 'blocked')
        self.assertFalse(out['can_grade'])

    def test_no_playbook_is_ungraded(self):
        out = review_gate(confidentiality_confirmed=True, privilege_reviewed=True,
                          playbook_counsel_approved=False)
        self.assertEqual(out['status'], 'ungraded')
        self.assertFalse(out['can_grade'])

    def test_strings_are_not_consent(self):
        with self.assertRaises(ValueError):
            review_gate(confidentiality_confirmed='false', privilege_reviewed=True,
                        playbook_counsel_approved=True)

    def test_attestation_not_verified_authority(self):
        out = review_gate(confidentiality_confirmed=True, privilege_reviewed=True,
                          playbook_counsel_approved=True)
        self.assertTrue(out['can_grade'])
        self.assertEqual(out['authority'], 'user_attested_not_independently_verified')
        self.assertFalse(out['can_send_or_file'])

    def test_decimal_scenario(self):
        out = earnout(metric='125.50', threshold='100', rate='2.5', cap='1000')
        self.assertEqual(out['payout'], '63.75')
        self.assertEqual(out['formula'], 'min(cap, max(0, metric - threshold) * rate)')

    def test_rounding_is_explicit_not_host_context(self):
        from decimal import localcontext, ROUND_UP
        with localcontext() as context:
            context.rounding=ROUND_UP
            out=earnout(metric='0.005',threshold='0',rate='1',cap='1')
        self.assertEqual(out['payout'],'0.00')

    def test_cap_and_floor(self):
        self.assertEqual(earnout(metric='1',threshold='2',rate='3',cap='4')['payout'],'0.00')
        self.assertEqual(earnout(metric='100',threshold='2',rate='3',cap='4')['payout'],'4.00')

    def test_reject_unsafe_numbers(self):
        for value in ['NaN','Infinity','-1','1e999999',True,{},'1,000']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                earnout(metric=value,threshold='2',rate='3',cap='4')

    def test_source_quote_and_caveat(self):
        source={'text':'FICTIONAL TEST ONLY: example words.', 'date':'2026-01-01',
                'caveats':['Incomplete fictional record'], 'corpus_commit':'a'*40,
                'compilation_commit':'b'*40,'compilation_tag':'sample/2026-01-01'}
        out=check_finding(clause_text='Sample clause',clause_quote='Sample clause',
                          source=source,source_quote='example words',date='2026-01-01')
        self.assertEqual(out['status'],'quote_match_only')
        self.assertEqual(out['caveats'],source['caveats'])
        self.assertFalse(out['legal_correctness_verified'])

    def test_sha256_source_handles(self):
        source={'text':'synthetic words','date':'2026-01-01','caveats':[],
                'corpus_commit':'a'*64,'compilation_commit':'b'*64}
        out=check_finding(clause_text='A',clause_quote='A',source=source,
                          source_quote='synthetic words',date='2026-01-01')
        self.assertEqual(out['status'],'quote_match_only')
        self.assertFalse(out['source_authenticity_verified'])

    def test_source_text_must_be_string(self):
        source={'text':['synthetic words'],'date':'2026-01-01','caveats':[],
                'corpus_commit':'a'*40,'compilation_commit':'b'*40}
        with self.assertRaises(ValueError):
            check_finding(clause_text='A',clause_quote='A',source=source,
                          source_quote='synthetic words',date='2026-01-01')

    def test_hallucinated_quote_blocked(self):
        with self.assertRaises(ValueError):
            check_finding(clause_text='A',clause_quote='B',source={},source_quote='x',date='2026-01-01')

    def test_date_mismatch_blocks(self):
        with self.assertRaises(ValueError):
            check_finding(clause_text='A',clause_quote='A',
                          source={'text':'x','date':'2025-01-01'},source_quote='x',date='2026-01-01')


if __name__=='__main__':
    unittest.main()
