import random
import mysql.connector
import string
import datetime
from flask import Flask,flash, render_template, request, redirect, url_for, session, jsonify, abort

#this all the function that check the personal info and check the right password or not, function itself never return password but other can be return

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="casino")

def get_priv(username):
        cursor = mydb.cursor()
        cursor.execute('SELECT priv FROM user WHERE username = %s', (username,))
        result = cursor.fetchone()
        priv = result[0] if result else None
        return priv

def get_balance(username):
        cursor = mydb.cursor()
        cursor.execute('SELECT balance FROM user WHERE username = %s', (username,))
        result = cursor.fetchone()
        balance = result[0] if result else None
        return balance

def get_status(username):
        cursor = mydb.cursor()
        cursor.execute('SELECT status FROM user WHERE username = %s', (username,))
        result = cursor.fetchone()
        status = result[0] if result else None
        return status

def get_login_logout(username):
        cursor = mydb.cursor()
        cursor.execute('SELECT last_login,last_logout FROM user WHERE username = %s', (username,))
        result = cursor.fetchone()
        l_login = result[0] if result else None
        l_logout = result[1] if result else None
        return l_login,l_logout

def check_username(username):
        cursor = mydb.cursor()
        cursor.execute('SELECT username FROM user WHERE username = %s', (username,))
        result = cursor.fetchone()
        if (result is not None):
                return True
        else:
                return False

def check_password(username,password):
        cursor = mydb.cursor()
        cursor.execute('SELECT password FROM user WHERE username = %s', (username,))
        result = cursor.fetchone()
        passwordr = result[0] if result else None
        if (passwordr==password):
                return True
        else:
                return False


def get_now():
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

#update script
def update_logout(username,now):
        cursor = mydb.cursor()
        cursor.execute("UPDATE user SET last_logout = %s WHERE username = %s", (now, username))
        mydb.commit()
        cursor.close()

def update_balance(username,new_balance):        
        cursor = mydb.cursor()
        cursor.execute('UPDATE user SET balance = %s WHERE username = %s', (new_balance, username))
        mydb.commit()
        cursor.close()


