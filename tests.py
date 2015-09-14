import unittest
from database import SimpleDB


class TestSimpleDatabase(unittest.TestCase):
    def setUp(self):
        self.db = SimpleDB()

    def test_set(self):
        self.db.set('one', 1)

    def test_get(self):
        self.db.set('thumb', 'tack')
        self.assertEqual(self.db.get('thumb'), 'tack')

    def test_unset(self):
        self.db.set('thumb', 'tack')
        self.db.unset('thumb')
        self.assertEqual(self.db.get('thumb'), 'NULL')

    def test_num_equal_to(self):
        self.assertEqual(self.db.num_equal_to('thumb'), 0)
        self.db.set('thumb', 'tack')
        self.assertEqual(self.db.num_equal_to('tack'), 1)
        self.db.set('tick', 'tack')
        self.assertEqual(self.db.num_equal_to('tack'), 2)
        self.db.set('tick', 'toe')
        self.assertEqual(self.db.num_equal_to('tack'), 1)

    def test_begin(self):
        self.db._begin()
        self.db.set('a', '30')
        self.assertEqual(self.db.get('a'), '30')

    def test_rollback(self):
        self.db._begin()
        self.db.set('a', '10')
        self.db._begin()
        self.db.set('a', '20')
        self.assertEqual(self.db.get('a'), '20')
        self.db._rollback()
        self.assertEqual(self.db.get('a'), 10)
        self.db._rollback()
        self.assertEqual(self.db.get('a'), 'NULL')

    def test_commit(self):
        self.db._begin()
        self.db.set('a', '30')
        self.db._begin()
        self.db.set('a', 40)
        self.db._commit()
        self.assertEqual(self.db._rollback(), 'NO TRANSACTION')


if __name__ == '__main__':
    unittest.main()
