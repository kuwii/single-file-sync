import unittest
import sfsync

class SingleFileSyncTest(unittest.TestCase):
    def test_merge_simple(self):
        a = { 'key1': 'value1', 'key2': 'value2', 'key3': 'value3' }
        b = { 'key1': 'newValue1', 'key2': 'newValue2' }
        sfsync.merge_content(a, b)
        self.assertEqual(a['key1'], 'newValue1')
        self.assertEqual(a['key2'], 'newValue2')
        self.assertEqual(a['key3'], 'value3')
        self.assertEqual(len(a), 3)
    
    def test_merge_append(self):
        a = { 'key1': 'value1' }
        b = { 'key2': 'value2' }
        sfsync.merge_content(a, b)
        self.assertEqual(a['key2'], 'value2')
        self.assertEqual(len(a), 2)

    def test_merge_embedded(self):
        a = { 'key1': 'value1', 'key2': { 'subKey1': 'subValue1', 'subKey2': 'subValue2' } }
        b = { 'key2': { 'subKey2': 'newSubValue2' } }
        sfsync.merge_content(a, b)
        self.assertEqual(a['key1'], 'value1')
        self.assertEqual(a['key2']['subKey1'], 'subValue1')
        self.assertEqual(a['key2']['subKey2'], 'newSubValue2')
    
    def test_merge_override(self):
        a = { 'key1': 'value1', 'key2': { 'subKey1': 'subValue1', 'subKey2': 'subValue2' } }
        b = { 'key2': 'newValue2' }
        sfsync.merge_content(a, b)
        self.assertEqual(a['key2'], 'newValue2')


if __name__ == '__main__':
    unittest.main()
