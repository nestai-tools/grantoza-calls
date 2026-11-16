"""Verify absent-original references without relaxing checks for included source files."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools/grantoza/skills/grants/scripts'))
from source_integrity import source_matches
from public_catalog import validate_sources
from assessment_profile import verify_sources


class SourceReferenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.sha = hashlib.sha256(b'original source').hexdigest()
        self.doc = dict(id='SRC-test', plik='01-sources/originals/source.pdf', sha256=self.sha,
                        oryginal_w_pakiecie=False)

    def save_manifest(self):
        (self.root / 'documents.json').write_text(json.dumps(dict(dokumenty=[self.doc])))

    def test_declared_absent_original_passes_registry_and_profile(self):
        self.save_manifest()
        validate_sources(self.root)
        verify_sources(self.root, dict(zrodla_sha256={'SRC-test': self.sha}))

    def test_missing_file_needs_explicit_false(self):
        for value in (None, True, 0, 'false'):
            self.doc['oryginal_w_pakiecie'] = value
            self.assertFalse(source_matches(self.root, self.doc, self.sha))

    def test_only_original_paths_can_be_references(self):
        for path in ('03-application/form.md', '../source.pdf', '01-sources/text/source.md'):
            self.doc['plik'] = path
            self.assertFalse(source_matches(self.root, self.doc, self.sha))

    def test_reference_digest_must_match_profile(self):
        other = hashlib.sha256(b'another source').hexdigest()
        self.save_manifest()
        with self.assertRaises(ValueError):
            verify_sources(self.root, dict(zrodla_sha256={'SRC-test': other}))

    def test_included_file_is_always_hashed_even_if_false(self):
        path = self.root / self.doc['plik']
        path.parent.mkdir(parents=True)
        path.write_bytes(b'original source')
        self.assertTrue(source_matches(self.root, self.doc, self.sha))
        path.write_bytes(b'changed source')
        self.assertFalse(source_matches(self.root, self.doc, self.sha))
        self.save_manifest()
        with self.assertRaises(ValueError):
            validate_sources(self.root)
        with self.assertRaises(ValueError):
            verify_sources(self.root, dict(zrodla_sha256={'SRC-test': self.sha}))

    def test_invalid_digest_is_not_a_valid_reference(self):
        self.doc['sha256'] = 'invalid'
        self.assertFalse(source_matches(self.root, self.doc, 'invalid'))


if __name__ == '__main__':
    unittest.main()
