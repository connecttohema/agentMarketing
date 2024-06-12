from flask import Blueprint, request, jsonify, send_from_directory
import json
import sqlite3
import os
from .openai_api import generate_sql_query, generate_query, generate_letter_content
from .pdf_generator import generate_pdf

bp = Blueprint('routes', __name__)

@bp.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    prompt = data.get('prompt')
    print("Received query prompt:", prompt)  # Debugging log

    # Define the table schema
    table_schema = """
    Table: agents
    Columns:
    - AgentId (TEXT)
    - State (TEXT)
    - AgentCode (INTEGER)
    - StateCode (INTEGER)
    - BookOfBusinessId (TEXT)

    Table: customers
    Columns:
    - CustomerId (TEXT)
    - FirstName (TEXT)
    - LastName (TEXT)
    - EmailAddress (TEXT)
    - PhoneNumber (TEXT)
    - MailingAddress (TEXT)
    - DateOfBirth (DATE)
    - AgentId (TEXT)

    Table: do_not_solicit
    Columns:
    - CustomerId (TEXT)
    - DoNotSolicit (BOOLEAN)

    Table: policies
    Columns:
    - PolicyId (TEXT)
    - CustomerId (TEXT)
    - LineOfBusiness (TEXT)
    - PolicyTermStartDate (DATE)
    - PolicyTermEndDate (DATE)
    - CoverageDetails (TEXT)
    - MonthlyPaymentAmount (REAL)
    - Premium (REAL)
    - RenewalDate (DATE)
    - PaymentPlan (TEXT)
    - DueDate (DATE)
    - PolicyStatus (TEXT)

    Table: vendor
    Columns:
    - CustomerId (TEXT)
    - FirstName (TEXT)
    - LastName (TEXT)
    - VehicleBought (TEXT)
    - VehicleModel (TEXT)
    - DatePurchased (DATE)
    """

    sql_query = generate_sql_query(prompt, table_schema)

    # Connect to the SQLite database and execute the query
    conn = sqlite3.connect('internal_db.db')
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()

        # Get column names
        column_names = [description[0] for description in cursor.description]

        # Format the results as a list of dictionaries
        formatted_results = [dict(zip(column_names, row)) for row in results]

        # Save the results to result.json
        with open('result.json', 'w') as f:
            json.dump({"results": formatted_results}, f, indent=4)

        conn.close()
        return jsonify({"message": "Query executed successfully.", "results": formatted_results})
    except sqlite3.Error as e:
        conn.close()
        return jsonify({"error": str(e)}), 500

@bp.route('/create_letter', methods=['POST'])
def create_letter():
    data = request.get_json()
    customer_id = data.get('customer_id')
    prompt_type = data.get('prompt_type')
    print("Received customer ID(s):", customer_id)  # Debugging log

    if not customer_id:
        return jsonify({"error": "Customer ID is required"}), 400

    # Generate SQL query using GPT-3.5
    query = generate_query(customer_id)

    # Fetch customer details using the generated query
    conn = sqlite3.connect('internal_db.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        customer_details = cursor.fetchone()
        conn.close()

        if not customer_details:
            return jsonify({"error": "Customer not found"}), 404

        customer = {
            "CustomerId": customer_details[0],
            "FirstName": customer_details[1],
            "LastName": customer_details[2],
            "EmailAddress": customer_details[3],
            "PhoneNumber": customer_details[4],
            "MailingAddress": customer_details[5],
            "DateOfBirth": customer_details[6],
            "AgentId": customer_details[7]
        }

        # Generate letter content using GPT-3.5
        letter_content = generate_letter_content(customer, prompt_type)
        
        # Create the PDF
        pdf_file_name = generate_pdf(customer, letter_content)

        # Ensure the static directory exists
        static_dir = os.path.join(os.getcwd(), 'static')
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)

        # Move the PDF file to the static directory
        pdf_path = os.path.join(static_dir, pdf_file_name)
        
        # If the file already exists, remove it
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        
        os.rename(pdf_file_name, pdf_path)
        print("PDF file created and moved to:", pdf_path)  # Debugging log

        return jsonify({"message": "Marketing letter created successfully.", "pdf_file": pdf_file_name})
    except sqlite3.Error as e:
        conn.close()
        print("Error during database operation:", e)  # Debugging log
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print("General error:", e)  # Debugging log
        return jsonify({"error": str(e)}), 500

# Serve the PDF file
@bp.route('/static/<path:filename>', methods=['GET'])
def serve_static(filename):
    print("Serving PDF file:", filename)  # Debugging log
    return send_from_directory('static', filename)
