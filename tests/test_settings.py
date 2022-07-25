import os

from unittest import TestCase, mock

from app.settings.settings import Settings


class TestSettings(TestCase):

    def test_default_settings(self):
        settings = Settings()
        self.assertTrue('localhost', settings.hostname)
        self.assertTrue(8000, settings.port)
        self.assertTrue('localhost', settings.database_host)
        self.assertTrue('db_habi', settings.database_name)
        self.assertTrue('dbuser', settings.database_user)
        self.assertTrue('dbpassword', settings.database_password)
        self.assertTrue(3306, settings.database_port)

    @mock.patch.dict(os.environ, {"DATABASE_NAME": "db_habi_prod"})
    def test_environment(self):
        settings = Settings
        self.assertTrue('db_habi_prod', settings.database_name)