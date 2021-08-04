from pymysql import cursors
import pymysql

class Coordinator():
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root1',
                             database='userregistration',
                             cursorclass=pymysql.cursors.DictCursor)

    def __init__(self):
        self.cursor= Coordinator.connection.cursor()

    def get_note(self,data):
        '''This function will return the notes information by using user_id'''
        id=data.get('id')
        get_data_query="SELECT * FROM note_notes WHERE user_note_id=%s"
        self.cursor.execute(get_data_query,id)
        user_note= self.cursor.fetchall()
        return user_note

    def post_note(self,data):
        '''This function will get data from server and then insert into table.'''
        id=data.get('id')
        title=data.get('title')
        description=data.get('description')
        insert_statement='INSERT INTO note_notes (user_note_id,title,description) VALUES(%s,%s,%s)'
        insert_data=(id,title,description)
        self.cursor.execute(insert_statement,insert_data)
        inserted_data=self.cursor.execute('SELECT * FROM note_notes WHERE user_note_id=%s',id)
        return inserted_data

    def put_note(self,data):
        '''This function will get data from server and update the note'''
        id=data.get('id')
        title=data.get('title')
        description=data.get('description')
        update_query='UPDATE note_notes SET title = %s, description= %s WHERE user_note_id = %s'
        update_data=(title,description,id)
        self.cursor.execute(update_query,update_data)
        return True

    def delete_note(self,data):
        '''This function will delete note data according to the user_id'''
        id=data.get('id')
        delete_query='DELETE FROM note_notes WHERE user_note_id=%s'
        self.cursor.execute(delete_query,id)
        return True