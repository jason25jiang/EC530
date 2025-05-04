import openai
import os

def generate_sql_query(user_query, schema_info):
    """Generate SQL query using OpenAI based on user input."""
    openai.api_key = os.getenv("OPENAI_API_KEY")  # Fetch API key from environment variable
    
    prompt = f"""
    You are an AI assistant tasked with converting user queries into SQL statements.
    The database schema is as follows:
    {schema_info}
    User Query: "{user_query}"
    Your task is to generate the correct SQL query and explain what it does.
    """
    
    try:
        response = openai.Completion.create(
            model="gpt-4",  # or "gpt-3.5-turbo" depending on your use case
            prompt=prompt,
            max_tokens=150
        )
        sql_query = response.choices[0].text.strip()
        print(f"Generated SQL Query: {sql_query}")
    except Exception as e:
        print(f"Error generating SQL: {e}")

if __name__ == "__main__":
    schema_info = """
    Table: sales (sale_id INTEGER, product_id INTEGER, quantity INTEGER, sale_date TEXT, revenue REAL)
    Table: products (product_id INTEGER, product_name TEXT, category TEXT, price REAL)
    """
    
    user_query = input("Enter your SQL query (in plain language): ")
    generate_sql_query(user_query, schema_info)
