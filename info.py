import mysql.connector
import datetime

#this all the function that check the personal info and check the right password or not, function itself never return password but other can be return value

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
        return (passwordr==password)



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


#insert into the topup table record and transaction table record
def insert_topup(helper_username, bef_topup, after_topup, topup_amt, username):
        cursor = mydb.cursor()
        time = get_now()
        cursor.execute('INSERT INTO topup_history (username, bef_topup, after_topup, topup_amt, topup_time, user_topup) VALUES (%s, %s, %s, %s, %s, %s)',
                       (helper_username, bef_topup, after_topup, topup_amt, time , username))
        mydb.commit()
        cursor.execute('SELECT topup_id from topup_history WHERE username=%s AND topup_amt= %s AND topup_time= %s',
                (username, topup_amt, time,))
        transaction_id2 = cursor.fetchone()[0]

        topupcomment = "admin top up" if get_priv(username) == "admin" else "user top up"

        cursor.execute('INSERT INTO transaction(transaction_id2,user,amt_bef_transaction,amt_aft_transaction,total_amt_transaction, transaction_comment)VALUES(%s,%s,%s,%s,%s,%s)',
                (transaction_id2 ,helper_username, bef_topup, after_topup, topup_amt, topupcomment))
        mydb.commit()
        cursor.close()

def insert_slotmachine(username, bet_amount, symbols, winnings):
        cursor = mydb.cursor()
        cursor.execute(
        'INSERT INTO slot_machine_history (username, bet_amount, winnings, symbols, spin_time) VALUES (%s, %s, %s, %s, %s)',
        (username, bet_amount, winnings, ','.join(symbols), get_now()))
        mydb.commit()
        cursor.close()

