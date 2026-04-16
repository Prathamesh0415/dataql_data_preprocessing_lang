import pandas as pd
from dataql.parser import get_parser
from dataql.engine import DataQLEngine

def create_dummy_data():
    data = {
        "first_name": ["Alice", "Bob", "Charlie", "David", "Eve", "Frank"],
        "department": ["Engineering", "Sales", "Engineering", "HR", "Engineering", "Sales"],
        "salary": [90000, 60000, 85000, 50000, 110000, 75000]
    }
    pd.DataFrame(data).to_csv("data/employees.csv", index=False)

if __name__ == "__main__":
    create_dummy_data()

    dsl_script = """
    LOAD "data/employees.csv";
    GROUP BY department AGGREGATE AVG(salary) AS average_salary;
    SORT BY average_salary DESC;
    """

    parser = get_parser()
    ast_tree = parser.parse(dsl_script)

    engine = DataQLEngine()
    engine.execute(ast_tree)

    print("\n--- Final Output DataFrame ---")
    print(engine.df)