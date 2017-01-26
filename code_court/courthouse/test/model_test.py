import os
import unittest
import tempfile

import web

from web import app, model

class ModelsTestCase(unittest.TestCase):
    """
    Contains tests for the database model
    """
    def setUp(self):
        self.db_fd, self.dbfile = tempfile.mkstemp()
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + self.dbfile
        app.config['TESTING'] = True
        app.app_context().push()
        self.app = app.test_client()
        with app.app_context():
            web.setup_database(app)

    def test_language(self):
        init_results = model.Language.query.filter_by(name="python").all()

        # create and add python lang
        python = model.Language("python", True)
        model.db.session.add(python)
        model.db.session.commit()

        # fetch python lang
        results = model.Language.query.filter_by(name="python").all()

        self.assertGreater(len(results), len(init_results))

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.dbfile)

if __name__ == '__main__':
    unittest.main()