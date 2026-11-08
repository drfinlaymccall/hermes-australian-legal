"""Exercise the actual registration function and its registered handlers."""
import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]


class Context:
    def __init__(self):
        self.tools={}
        self.skills={}
        self.commands={}
    def register_tool(self, **kwargs):
        self.tools[kwargs['name']]=kwargs
    def register_skill(self, name, path, **kwargs):
        self.skills[name]=Path(path)
    def register_command(self, name, handler, **kwargs):
        self.commands[name]=handler


class PluginTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec=importlib.util.spec_from_file_location('au_legal_test_plugin',ROOT/'__init__.py',
                                                   submodule_search_locations=[str(ROOT)])
        assert spec is not None and spec.loader is not None
        module=importlib.util.module_from_spec(spec)
        sys.modules[spec.name]=module
        spec.loader.exec_module(module)
        cls.context=Context()
        module.register(cls.context)

    def test_registration_and_real_skill_file(self):
        self.assertEqual(len(self.context.tools),5)
        self.assertTrue(self.context.skills['counsel-preparation'].is_file())
        for name,entry in self.context.tools.items():
            self.assertEqual(name,entry['schema']['name'])
            self.assertFalse(entry['schema']['parameters']['additionalProperties'])

    def test_registered_arithmetic(self):
        data=json.loads(self.context.tools['au_legal_earnout']['handler'](
            {'metric':'125.50','threshold':'100','rate':'2.5','cap':'1000'}))
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['payout'],'63.75')

    def test_registered_refusal_no_source_leak(self):
        data=json.loads(self.context.tools['au_legal_provision']['handler'](
            {'corpus_path':'/DO-NOT-LEAK/private/client','instrument':'x','provision':'x','date':'bad'}))
        self.assertFalse(data['success'])
        self.assertNotIn('DO-NOT-LEAK',json.dumps(data))

    def test_unexpected_parameter_and_malformed_input(self):
        handler=self.context.tools['au_legal_review_gate']['handler']
        for args in [None,{'confidentiality_confirmed':True,'privilege_reviewed':True,
                           'playbook_counsel_approved':True,'bypass':True}]:
            self.assertFalse(json.loads(handler(args))['success'])

    def test_command(self):
        out=json.loads(self.context.commands['au-legal'](''))
        self.assertEqual(out['mode'],'read_only_preparation')
        self.assertEqual(len(out['tools']),5)


if __name__=='__main__':
    unittest.main()
