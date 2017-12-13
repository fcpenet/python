import unittest
from app import configreader

class ConfigReaderTest(unittest.TestCase):
    def test_returnNegative1WhenConfigFileDoesNotExist(self):
        config = configreader.ConfigReader()
        config.path = 'nonexistentfile'
        self.assertEqual(-1, config.readconfig())


    def test_shouldReturnDefaultValues(self):
        config = configreader.ConfigReader()
        config.readconfig()
        self.assertEqual('root', config.username)


if __name__ == "__main__":
    unittest.main()
