import unittest
from app import db
from unittest.mock import patch
from app.tasks import get_author_id


class Model_test(unittest.TestCase):
    @patch('app.models.Author')
    @patch('app.db')
    def test_models(self):
        from app.model.author import Author


        new_author=mock_author(name='')
        mock_db.session.add(new_author)
        qry=mock_db.session.query(mock_author).all().limit(1)
        print(qry.name)


if __name__ == '__main__':
    unittest.main()
