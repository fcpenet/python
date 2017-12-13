import pymysql

class FieldDict(dict):
    _keys = {'name':'varchar(20)', 'description':'varchar(20)'}
    def __init__(self, *args):
        return

    def __setitem__(self, key, val):
        if key not in self._keys:
            raise KeyError
        dict.__setitem__(self, key, val)
        return

class ResearchDict(dict):
    _keys = {'title':'varchar(30)', 'tagid':'varchar(10)'}
    def __init__(self, *args):
        return

    def __setitem__(self, key, val):
        if key not in self._keys:
            raise KeyError
        dict.__setitem__(self, key, val)
        return

class TagDict(dict):
    _keys = {'name':'varchar(10)', 'description':'varchar(20)', 'fieldid':'varchar(10)'}
    def __init__(self, *args):
        return

    def __setitem__(self, key, val):
        if key not in self._keys:
            raise KeyError
        dict.__setitem__(self, key, val)
        return

class AuthorDict(dict):
    _keys = {'name':'varchar(30)', 'researchid':'varchar(30)'}
    def __init__(self,*args):
        return

    def __setitem__(self, key, val):
        if key not in self._keys:
            raise KeyError
        dict.__setitem__(self, key, val)
        return

class DbManager:
    _cx = 0
    _isConnected = False
    def __enter__(self):
        return self

    def __exit__(self):
        self._cx.close()
    def __init__(self, un, pw, host, db):
        self.un =  un
        self.pw = pw
        self.host = host
        self.db = db

        '''
            Create table first at the start
        '''

        startQuery  = "CREATE TABLE IF NOT EXISTS "
        return;

    def connect(self):
        if (self._isConnected == False):
            try:
                self._cx = pymysql.connect(user=self.un, password=self.pw,
                        host=self.host , database=self.db)
                self._isConnected = True
                return 0
            except pymysql.Error as err:
                if err.args[0]== 1045: #wrong un pw
                    print("Something is wrong with your user name or password")
                elif err.args[0]== 1049: #non-existent db
                    print("Database does not exist")
                else:
                    print(err)
                return -1


    def executeCustomQuery(self, query):
        if (self._isConnected == True):
            with self._cx.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                print(result)
                self._cx.commit()

                return (cursor.rowcount, result)
        else:
            print("Not connected to DB!")
            return (-1, ())

    def selectFrom(self, table, column={'*'}, where=''):
        if (self._isConnected == True):
            with self._cx.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "select {}  from {} {}" \
                    .format(",".join("{}".format(key) for key in column) \
                        , table \
                        ,where)

                cursor.execute(sql)
                result = cursor.fetchall()
                self._cx.commit()

                return result
        else:
            print("Not connected to DB!")
            return -1

    def getAll(self, orderby=''):
        if (self._isConnected == True):
            with self._cx.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "select r.title as Title, a.name as Author, t.name as Tag, f.name as Field from \
                        author a \
                        left join research r \
                        on a.researchid=r.title \
                        left join tag t  \
                        on r.tagid=t.name \
                        left join field f  \
                        on t.fieldid=f.name \
                        {}".format(orderby)
                cursor.execute(sql)
                result = cursor.fetchall()
                self._cx.commit()

                return (cursor.rowcount, result)
        else:
            print("Not connected to DB!")
            return (-1, ())

    def getAllWhere(self, where):
        if (self._isConnected == True):
            with self._cx.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "select * from (select r.title as Title, a.name as Author, t.name as Tag, f.name as Field from \
                        author a \
                        left join research r \
                        on a.researchid=r.title \
                        left join tag t  \
                        on r.tagid=t.name \
                        left join field f  \
                        on t.fieldid=f.name) as T\
                        where  {}".format(where)
                cursor.execute(sql)
                result = cursor.fetchall()
                self._cx.commit()

                return (cursor.rowcount, result)
        else:
            print("Not connected to DB!")
            return (-1,())

    def AddToTable(self, table, item):
        if (self._isConnected == True):
            try:
                with self._cx.cursor() as cursor:
                    sql = "INSERT INTO {} ({}) VALUES ( {} )" \
                        .format(table \
                            , ",".join("{}".format(key) for key,val in item.items()) \
                            , ",".join("\"{}\"".format(val) for key, val in item.items()))

                    cursor.execute(sql)
                    self._cx.commit()

                return cursor.rowcount
            except pymysql.err.IntegrityError as err:
                print("Insertion failed: ", err)
                return -1
        return 0

    def deleteFromTable(self, table, column, value):
        if (self._isConnected == True):
            try:
                with self._cx.cursor() as cursor:
                    sql = "delete from {} where {} = \"{}\"".format(table, column, value)
                    cursor.execute(sql)
                    self._cx.commit()

                return (cursor.rowcount, "")
            except pymysql.err.IntegrityError as err:
                print("Deletion failed: ", err)
                if (1451 == err.args[0]):
                    return(-1, "Cannot delete! {} from {} is in use.".format(value, table))
                return (-1, "Error!")
        return (-1, "Error!")

    def updateInTable(self, table, column, value, cond_col, cond_value):
        if (self._isConnected == True):
            try:
                with self._cx.cursor() as cursor:
                    sql = "update {} set {}=\"{}\" where {} = \"{}\"".format(table, column, value, cond_col, cond_value)
                    cursor.execute(sql)
                    self._cx.commit()

                return cursor.rowcount
            except pymysql.err.IntegrityError as err:
                print("Insertion failed: ", err)
                return -1
        return -1

    def fetchFromTable(self, table):
        if (self._isConnected == True):
            try:
                with self._cx.cursor(pymysql.cursors.DictCursor) as cursor:
                    sql = "select * from {}".format(table)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    self._cx.commit()
                    print(result)
                    return (cursor.rowcount, result)
            except pymysql.err.IntegrityError as err:
                print("Insertion failed: ", err)
                return (-1, ())
        return (-1,())

    def populatedb(self):
        field2 = FieldDict()
        field2['name'] = 'exam'
        field2['description'] = 'another test'
        self.AddToTable('field', field2)
        field2['name'] = 'exam1'
        self.AddToTable('field', field2)
        field2['name'] = 'exam2'
        self.AddToTable('field', field2)
        field2['name'] = 'exam3'
        self.AddToTable('field', field2)
        field2['name'] = 'exam4'
        self.AddToTable('field', field2)

        tag = TagDict()
        tag['name'] = 'tag'
        tag['description'] = 'just another tag'
        tag['fieldid'] = 'exam'
        self.AddToTable('tag', tag)
        tag['name'] = 'tag1'
        tag['fieldid'] = 'exam'
        self.AddToTable('tag', tag)
        tag['name'] = 'tag2'
        tag['fieldid'] = 'exam3'
        self.AddToTable('tag', tag)
        tag['name'] = 'tag3'
        tag['fieldid'] = 'exam3'
        self.AddToTable('tag', tag)
        tag['name'] = 'tag4'
        tag['fieldid'] = 'exam4'
        self.AddToTable('tag', tag)
        tag['name'] = 'tag5'
        tag['fieldid'] = 'exam4'
        self.AddToTable('tag', tag)

        research = ResearchDict()
        research['title'] = 'A study of'
        research['tagid'] = 'tag1'
        self.AddToTable('research', research)
        research['title'] = 'A study of stars'
        research['tagid'] = 'tag3'
        self.AddToTable('research', research)
        research['title'] = 'A study of water'
        research['tagid'] = 'tag3'
        self.AddToTable('research', research)
        research['title'] = 'A study of earth'
        research['tagid'] = 'tag4'
        self.AddToTable('research', research)
        research['title'] = 'A study of human'
        research['tagid'] = 'tag5'
        self.AddToTable('research', research)
        research['title'] = 'A look at life'
        research['tagid'] = 'tag5'
        self.AddToTable('research', research)

        author = AuthorDict()
        author['name'] = 'kiko'
        author['researchid'] = 'a study of'
        self.AddToTable('author',author)
        author['name'] = 'kiko'
        author['researchid'] = 'a study of stars'
        self.AddToTable('author',author)
        author['name'] = 'joana'
        author['researchid'] = 'a study of water'
        self.AddToTable('author',author)
        author['name'] = 'irah'
        author['researchid'] = 'a study of earth'
        self.AddToTable('author',author)
        author['name'] = 'joana'
        author['researchid'] = 'a study of human'
        self.AddToTable('author',author)
        author['name'] = 'kiko'
        author['researchid'] = 'a look at life'
        self.AddToTable('author',author)
