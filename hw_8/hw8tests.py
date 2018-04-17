import unittest
import bibmanager
from pybtex.exceptions import PybtexError

class TestCases(unittest.TestCase):
	def test_author(self):
		self.assertEqual(bibmanager.parse_author('&Francis&, John'),'John Francis')

	def second_test(self):
		self.assertEqual(bibmanager.parse_author('&D.&, L. E.'),'L. E. D.')

	def error_testing(self):
		with self.assertRaises(PybtexError):
			bibmanager.add_to_database('fakefile.bib','Fake Collection')

if __name__ == '__main__':
	unittest.main()