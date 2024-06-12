import pandas as pd
import sqlite3

def load_csv_to_db():
    # Connect to SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect('internal_db.db')
    cursor = conn.cursor()

    # Load and process agents.csv
    agents_df = pd.read_csv('agents.csv')
    agents_df.to_sql('agents', conn, if_exists='replace', index=False)

    # Load and process customers.csv
    customers_df = pd.read_csv('customers.csv')
    customers_df['DateOfBirth'] = pd.to_datetime(customers_df['DateOfBirth'], format='%Y-%m-%d')
    customers_df.to_sql('customers', conn, if_exists='replace', index=False)

    # Load and process do_not_solicit.csv
    do_not_solicit_df = pd.read_csv('do_not_solicit.csv')
    do_not_solicit_df.to_sql('do_not_solicit', conn, if_exists='replace', index=False)

    # Load and process policies.csv
    policies_df = pd.read_csv('policies.csv')
    policies_df['PolicyTermEndDate'] = pd.to_datetime(policies_df['PolicyTermEndDate'], format='%Y-%m-%d %H:%M:%S.%f')
    policies_df['PolicyTermStartDate'] = pd.to_datetime(policies_df['PolicyTermStartDate'], format='%Y-%m-%d')
    policies_df['RenewalDate'] = pd.to_datetime(policies_df['RenewalDate'], format='%Y-%m-%d')
    policies_df['DueDate'] = pd.to_datetime(policies_df['DueDate'], format='%Y-%m-%d')
    policies_df.to_sql('policies', conn, if_exists='replace', index=False)

    # Load and process vendor.csv
    vendor_df = pd.read_csv('vendor.csv')
    vendor_df['DatePurchased'] = pd.to_datetime(vendor_df['DatePurchased'], format='%Y-%m-%d')
    vendor_df.to_sql('vendor', conn, if_exists='replace', index=False)

    conn.commit()
    conn.close()

def execute_query(query):
    conn = sqlite3.connect('internal_db.db')
    cursor = conn.cursor()

    cursor.execute(query)
    result = cursor.fetchone()

    conn.close()

    if result:
        return {
            "CustomerId": result[0],
            "FirstName": result[1],
            "LastName": result[2],
            "EmailAddress": result[3],
            "PhoneNumber": result[4],
            "MailingAddress": result[5],
            "DateOfBirth": result[6],
            "AgentId": result[7]
        }
    else:
        return None
