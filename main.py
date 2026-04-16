import pandas as pd
from dataql.parser import get_parser
from dataql.engine import DataQLEngine

def create_dummy_data():
    data = {
        "first_name": ["Alice", "Bob", "Charlie", "David", "Eve"],
        "department": ["Engineering", "Sales", "Engineering", "HR", "Sales"],
        "salary": [90000, 60000, 85000, 50000, 75000]
    }
    pd.DataFrame(data).to_csv("employees.csv", index=False)

if __name__ == "__main__":
    create_dummy_data()

    dsl_script = """
    LOAD "employees.csv";
    FILTER department == "Sales";
    COMPUTE bonus = salary * 0.15;
    COMPUTE total_comp = salary + bonus;
    """

    parser = get_parser()
    ast_tree = parser.parse(dsl_script)

    engine = DataQLEngine()
    engine.execute(ast_tree)

    print("\n--- Final Output DataFrame ---")
    print(engine.df)