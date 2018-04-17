import unittest
import bibmanager

class TestHelper(unittest.TestCase):
	def test_author(self):
		self.assertEqual(bibmanager.parse_author('&Francis&, John'),'John Francis')

	def second_test(self):
		self.assertEqual(bibmanager.parse_author('&D.&, L. E.'),'L. E. D.')

if __name__ == '__main__':
	unittest.main()