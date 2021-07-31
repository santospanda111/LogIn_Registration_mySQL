from pymysql import cursors
import pymysql
import datetime
from django.contrib.auth.hashers import make_password

class Coordinator():
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root1',
                             database='userregistration',
                             cursorclass=pymysql.cursors.DictCursor)

    def __init__(self):
        self.cursor= Coordinator.connection.cursor()

    def get_data_by_id(self,id):
        '''This function will return the user information by using user_id'''
        get_data_query="SELECT * FROM auth_user WHERE id=%s"
        self.cursor.execute(get_data_query,id)
        user= self.cursor.fetchall()
        return user

    def post_data(self,data):
        '''This function will check whether the username exists or not'''
        username=data.get('username')
        check_statement='SELECT EXISTS(SELECT * FROM auth_user WHERE username=%s)'
        self.cursor.execute(check_statement,username)
        checked_data= self.cursor.fetchall()
        return checked_data,username

    def post_insert_data(self,data):
        '''This function will get data from server and then insert into table.
            Return: email and user_id'''
        username=data.get('username')
        password=data.get('password')
        hashed_password=make_password(password)
        first_name=data.get('first_name')
        last_name=data.get('last_name')
        email=data.get('email')
        is_staff=0
        is_active=1
        is_superuser=0
        date_joined= datetime.datetime.now()
        insert_statement='INSERT INTO auth_user (first_name,last_name,email,username,password,is_staff,is_active,is_superuser,date_joined) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        insert_data=(first_name,last_name,email,username,hashed_password,is_staff,is_active,is_superuser,date_joined)
        self.cursor.execute(insert_statement,insert_data)
        id_statement= "SELECT id FROM auth_user WHERE username=%s"
        self.cursor.execute(id_statement,username)
        user_id=self.cursor.fetchone()
        return email,user_id

        
    def post_login_data(self,username):
        ''' This function will get the user_id and return it'''

        id_statement= "SELECT id FROM auth_user WHERE username=%s"
        self.cursor.execute(id_statement,username)
        user_id=self.cursor.fetchone()
        return user_id


    def get_verify_email(self,user_id,username):
        ''' this function will check the id and username then return the whole data'''
        
        verify_query="SELECT id,username FROM auth_user WHERE id=%s and username=%s"
        verify_data=(user_id,username)
        self.cursor.execute(verify_query,verify_data)
        data=self.cursor.fetchall()
        return data
