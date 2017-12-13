import unittest
from app import dbmanager
from app import configreader

class DbManagerTest(unittest.TestCase):
    def setUp(self):
        config = configreader.ConfigReader()
        config.readconfig()
        self.dbman = dbmanager.DbManager(config.username, config.pw
                ,config.host ,config.db)
        self.assertEqual(0, self.dbman.connect())

        self.field = dbmanager.FieldDict()
        self.field['name'] = 'test'
        self.field['description'] = 'just a test'

        self.tag = dbmanager.TagDict()
        self.tag['name'] = 'test'
        self.tag['description'] = 'just a test'
        self.tag['fieldid'] = 'test'

        self.research = dbmanager.ResearchDict()
        self.research['title'] = 'test'
        self.research['tagid'] = 'test'

        self.author = dbmanager.AuthorDict()
        self.author['name'] = 'test'
        self.author['researchid'] = 'test'




    def test_returnNegative1WhenLoginFailed(self):
        config = configreader.ConfigReader()
        config.readconfig()
        dbman = dbmanager.DbManager("lala", config.pw
                ,config.host ,config.db)

        self.assertEqual(-1, dbman.connect())
        return


    def test_shouldNotAllowAdditionOfKeysForFieldDict(self):
        excep = 0;
        try:
            self.field['notAfield'] =  'test'
        except Exception as e:
            excep = e;

        self.assertEqual(KeyError, type(excep))
        return

    def test_shouldAllowSettingKeysForFieldDict(self):
        excep = 0;
        try:
            self.field['name'] =  'test'
        except Exception as e:
            excep = e;
        self.assertNotEqual(KeyError, type(excep))
        self.assertNotEqual(AttributeError, type(excep))
        return

    def test_shouldNotAllowAdditionOfKeysForTagDict(self):
        excep = 0;
        try:
            self.tag['notAfield'] =  'test'
        except Exception as e:
            excep = e;

        self.assertEqual(KeyError, type(excep))
        return

    def test_shouldNotAllowAdditionOfKeysForAuthorDict(self):
        excep = 0;
        try:
            self.author['notAfield'] =  'test'
        except Exception as e:
            excep = e;

        self.assertEqual(KeyError, type(excep))
        return

    def test_shouldNotAllowAdditionOfKeysForResearchDict(self):
        excep = 0;
        try:
            self.research['notAfield'] =  'test'
        except Exception as e:
            excep = e;

        self.assertEqual(KeyError, type(excep))
        return


    def test_ShouldRunCustomQuery(self):
        query = "show tables"
        self.assertEqual(0, self.dbman.executeCustomQuery(query)[0])
        return

    def test_ShouldAddToFields(self):
        self.assertEqual(1, self.dbman.AddToTable('field', self.field))
        self.assertEqual(1, self.dbman.deleteFromTable("field", "name", "test"))
        return

    def test_ShouldAddToTags(self):
        self.assertEqual(1, self.dbman.AddToTable('field', self.field))
        self.assertEqual(1, self.dbman.AddToTable('tag', self.tag))
        self.assertEqual(1, self.dbman.deleteFromTable('tag', "name", "test"))
        self.assertEqual(1, self.dbman.deleteFromTable('field', "name", "test"))
        return

    def test_ShouldAddToResearch(self):
        self.assertEqual(1, self.dbman.AddToTable('field', self.field))
        self.assertEqual(1, self.dbman.AddToTable('tag', self.tag))
        self.assertEqual(1, self.dbman.AddToTable('research', self.research))
        self.assertEqual(1, self.dbman.deleteFromTable('research', "title", "test"))
        self.assertEqual(1, self.dbman.deleteFromTable('tag', "name", "test"))
        self.assertEqual(1, self.dbman.deleteFromTable('field', "name", "test"))
        return

    def test_ShouldAddToAuthors(self):
        self.assertEqual(1, self.dbman.AddToTable('field', self.field))
        self.assertEqual(1, self.dbman.AddToTable('tag', self.tag))
        self.assertEqual(1, self.dbman.AddToTable('research', self.research))
        self.assertEqual(1, self.dbman.AddToTable('author', self.author))
        self.assertEqual(1, self.dbman.deleteFromTable('author', "name", "test"))
        self.assertEqual(1, self.dbman.deleteFromTable('research', "title", "test"))
        self.assertEqual(1, self.dbman.deleteFromTable('tag', "name", "test"))
        self.assertEqual(1, self.dbman.deleteFromTable('field', "name", "test"))
        return

    def test_ShouldNotAllowDupFields(self):
        self.assertEqual(1, self.dbman.AddToTable('field', self.field))
        self.assertEqual(-1, self.dbman.AddToTable('field', self.field))
        self.assertEqual(1, self.dbman.deleteFromTable('field', "name", "test"))
        return

    def test_ShouldDeleteFromTable(self):
        self.assertEqual(1, self.dbman.AddToTable('field', self.field))
        self.assertEqual(1, self.dbman.deleteFromTable('field', "name", "test"))
        return

    def test_ShouldUpdateFromDatabase(self):
        self.assertEqual(1, self.dbman.AddToTable('field', self.field))
        self.assertEqual(1, self.dbman.updateInTable('field', 'description', 'yey changed', 'name', 'test'))
        self.assertEqual(1, self.dbman.deleteFromTable("field", "name", "test"))
        return

    def test_retrieveItemsFromTable(self):
        field2 = dbmanager.FieldDict()
        field2['name'] = 'exam'
        field2['description'] = 'another test'
        self.assertEqual(1, self.dbman.AddToTable('field', self.field))
        self.assertEqual(1, self.dbman.AddToTable('field', field2))
        self.assertEqual(2, self.dbman.fetchFromTable('field')[0])
        self.assertEqual(1, self.dbman.deleteFromTable('field', "name", "test"))
        self.assertEqual(1, self.dbman.deleteFromTable('field', "name", "exam"))
        return

    def test_shouldAllInfoFromTable(self):
        field2 = dbmanager.FieldDict()
        field2['name'] = 'exam'
        field2['description'] = 'another test'
        self.assertEqual(1, self.dbman.AddToTable('field', self.field))
        self.assertEqual(1, self.dbman.AddToTable('field', field2))
        self.assertEqual('exam', self.dbman.selectFrom('field', {'name'}, "where name in ('test', 'exam')")[0]['name'])
        self.assertEqual(1, self.dbman.deleteFromTable('field', "name", "test"))
        self.assertEqual(1, self.dbman.deleteFromTable('field', "name", "exam"))
        return

    def test_shouldFromAllTable(self):
        self.assertEqual(1, self.dbman.AddToTable('field', self.field))
        self.assertEqual(1, self.dbman.AddToTable('tag', self.tag))
        self.assertEqual(1, self.dbman.AddToTable('research', self.research))
        self.assertEqual(1, self.dbman.AddToTable('author', self.author))
        self.assertEqual(type({}), type(self.dbman.getAll()[1][0]))
        self.assertEqual(1, self.dbman.deleteFromTable('author', "name", "test"))
        self.assertEqual(1, self.dbman.deleteFromTable('research', "title", "test"))
        self.assertEqual(1, self.dbman.deleteFromTable('tag', "name", "test"))
        self.assertEqual(1, self.dbman.deleteFromTable('field', "name", "test"))


if __name__ == "__main__":
    unittest.main()
