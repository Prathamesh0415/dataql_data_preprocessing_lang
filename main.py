import pandas as pd
from dataql.parser import get_parser
from dataql.engine import DataQLEngine
import os

def create_test_data():
    # Ensure the data directory exists
    os.makedirs("data", exist_ok=True)
    
    data = {
        "first_name": ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy"],
        "last_name": ["Smith", "Jones", "Brown", "Williams", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson"],
        "department": ["Engineering", "Sales", "Engineering", "HR", "Sales", None, "Engineering", "HR", "Sales", "Engineering"],
        "salary": [90000, 60000, 85000, 50000, 75000, 80000, None, 52000, 62000, 95000],
        "age": [28, 35, None, 42, 29, 31, 26, 38, None, 45]
    }
    df = pd.DataFrame(data)
    df.to_csv("data/employees_raw.csv", index=False)
    print("--- 1. Generated 'data/employees_raw.csv' with intentional missing data ---\n")
    print(df)
    print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    create_test_data()
    parser = get_parser()
    engine = DataQLEngine()
    print("--- 2. RUNNING PIPELINE 1: Wrangling & Cleaning ---")
    
    pipeline_1_script = """
    LOAD "data/employees_raw.csv"; 
    FILLNULL age WITH 0;
    FILLNULL salary WITH 40000;
    DROPNULL; 
    RENAME first_name TO fname, last_name TO lname;
    COMPUTE bonus = salary * 0.12;
    COMPUTE total_comp = salary + bonus;
    FILTER total_comp > 60000;
    KEEP fname, lname, department, age, total_comp;
    SORT BY total_comp DESC;
    LIMIT 5;
    SAVE "data/top_5_earners.csv";
    """

    ast_1 = parser.parse(pipeline_1_script)
    engine.execute(ast_1)
    
    print("\n[RESULT] Pipeline 1 Output DataFrame:")
    print(engine.df)
    print("\n" + "="*50 + "\n")

    print("--- 3. RUNNING PIPELINE 2: Grouping & Aggregation ---")
    
    pipeline_2_script = """
    LOAD "data/employees_raw.csv";
    FILLNULL salary WITH 0;
    DROPNULL; 
    GROUP BY department AGGREGATE AVG(salary) AS avg_department_salary; 
    SORT BY avg_department_salary DESC;
    """
    
    ast_2 = parser.parse(pipeline_2_script)
    engine.execute(ast_2)
    
    print("\n[RESULT] Pipeline 2 Output DataFrame:")
    print(engine.df)
    print("\n" + "="*50 + "\n")