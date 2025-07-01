# database.py
import sqlite3
import datetime

def connect_db():
    """Creates or connects to the database and returns the connection and cursor."""
    conn = sqlite3.connect('bank_database.db')
    cursor = conn.cursor()
    return conn, cursor

def setup_database():
    """Sets up the database table if it doesn't exist."""
    conn, cursor = connect_db()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            account_number INTEGER PRIMARY KEY,
            full_name TEXT NOT NULL,
            gender TEXT NOT NULL,
            dob TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone_number TEXT UNIQUE NOT NULL,
            address TEXT NOT NULL,
            account_type TEXT NOT NULL,
            initial_deposit REAL NOT NULL,
            creation_date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def generate_account_number():
    """Generates a new, unique account number."""
    conn, cursor = connect_db()
    cursor.execute('SELECT MAX(account_number) FROM customers')
    last_account_number = cursor.fetchone()[0]
    conn.close()
    
    if last_account_number:
        return last_account_number + 1
    else:
        # Start with a base number if the table is empty
        return 100001 

def add_customer_to_db(customer_data):
    """Adds a new customer to the database."""
    conn, cursor = connect_db()
    
    # Generate a new account number
    acc_no = generate_account_number()
    
    # Get current date and time
    creation_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # The data to be inserted
    data_tuple = (
        acc_no,
        customer_data['full_name'],
        customer_data['gender'],
        customer_data['dob'],
        customer_data['email'],
        customer_data['phone_number'],
        customer_data['address'],
        customer_data['account_type'],
        customer_data['initial_deposit'],
        creation_date
    )

    # SQL query with placeholders to prevent SQL injection
    query = '''
        INSERT INTO customers (
            account_number, full_name, gender, dob, email, phone_number,
            address, account_type, initial_deposit, creation_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    
    try:
        cursor.execute(query, data_tuple)
        conn.commit()
        return acc_no # Return the new account number on success
    except sqlite3.IntegrityError as e:
        # This will catch errors if email or phone are not unique
        print(f"Database Error: {e}")
        return None
    finally:
        conn.close()
