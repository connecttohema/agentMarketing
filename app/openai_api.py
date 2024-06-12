import openai
import os

# Set your OpenAI API key from an environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_sql_query(prompt, table_schema):
    detailed_prompt = f"""
    You are an SQL expert. Write an SQL query for the database tables based on the following request: {prompt}

    {table_schema}

    Use SQLite syntax for date calculations. Ensure to select all columns from the relevant tables.
    """
    #Uncomment the following code to use the OpenAI API
# response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are an SQL expert."},
#             {"role": "user", "content": detailed_prompt}
#         ],
#         max_tokens=150,
#         temperature=0.5,
#     )

    response_text = response['choices'][0]['message']['content'].strip()
    sql_start = response_text.find("```sql")
    sql_end = response_text.find("```", sql_start + 1)

    if sql_start != -1 and sql_end != -1:
        sql_query = response_text[sql_start + len("```sql"):sql_end].strip()
    else:
        sql_query = response_text

    return sql_query

def generate_query(customer_id):
    prompt = f"Generate a SQL query to fetch the CustomerId, FirstName, LastName, EmailAddress, PhoneNumber, MailingAddress, DateOfBirth, and AgentId of a customer with ID '{customer_id}' from the 'customers' table."
    
    table_schema = """
    Table: customers
    Columns: CustomerId, FirstName, LastName, EmailAddress, PhoneNumber, MailingAddress, DateOfBirth, AgentId
    """
    
    query = generate_sql_query(prompt, table_schema)
    return query

def generate_letter_content(customer, prompt_type):
    detailed_prompt = f"""
    Write a personalized marketing letter for the following customer based on the prompt type: {prompt_type}.
    
    Customer Details:
    - CustomerId: {customer['CustomerId']}
    - FirstName: {customer['FirstName']}
    - LastName: {customer['LastName']}
    - EmailAddress: {customer['EmailAddress']}
    - PhoneNumber: {customer['PhoneNumber']}
    - MailingAddress: {customer['MailingAddress']}
    - DateOfBirth: {customer['DateOfBirth']}
    - AgentId: {customer['AgentId']}
    
    Prompt Type: {prompt_type}
    """
  #Uncomment the following code to use the OpenAI API
  # response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are an expert marketing letter writer."},
#             {"role": "user", "content": detailed_prompt}
#         ],
#         max_tokens=300,
#         temperature=0.7,
#     )
    return response['choices'][0]['message']['content'].strip()
