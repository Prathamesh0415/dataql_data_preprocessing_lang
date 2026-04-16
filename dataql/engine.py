import pandas as pd

class DataQLEngine:
    def __init__(self):
        self.df = None

    def execute(self, tree):
        for stmt in tree.children:
            if stmt.data == 'load_stmt':
                filename = stmt.children[0].value.strip('"')
                self.df = pd.read_csv(filename)
                print(f"[EXECUTED] LOADED data from {filename}")

            elif stmt.data == 'keep_stmt':
                columns = [child.value for child in stmt.children]

                self.df = self.df[columns]

                print(f"[EXECUTED] KEPT columns: {columns}")

                

            elif stmt.data == 'filter_stmt':
                for condition in stmt.children:
                    col = condition.children[0].value
                    op = condition.children[1].value
                    val = condition.children[2].value
                    if val.isdigit():
                        val = float(val)
                    else:
                        val = val.strip('"')
                    if op == '==': self.df = self.df[self.df[col] == val]
                    elif op == '!=': self.df = self.df[self.df[col] != val]
                    elif op == '>': self.df = self.df[self.df[col] > val]
                    elif op == '<': self.df = self.df[self.df[col] < val]
                    elif op == '>=': self.df = self.df[self.df[col] >= val]
                    elif op == '<=': self.df = self.df[self.df[col] <= val]
                print(f"[EXECUTED] FILTERED data")

            elif stmt.data == 'sort_stmt':
                col = stmt.children[0].value
                is_ascending = stmt.children[1].data == 'asc'
                self.df = self.df.sort_values(by=col, ascending=is_ascending)
                order_str = "ASC" if is_ascending else "DESC"
                print(f"[EXECUTED] SORTED BY {col} {order_str}")


            elif stmt.data == 'save_stmt':
                filename = stmt.children[0].value.strip('"')
                self.df.to_csv(filename, index=False)
                print(f"[EXECUTED] SAVED results to {filename}") 

            elif stmt.data == 'group_stmt':
                group_col = stmt.children[0].value
                agg_func = stmt.children[1].value.upper()
                target_col = stmt.children[2].value
                alias = stmt.children[3].value
                func_map = {
                    'SUM': 'sum',
                    'AVG': 'mean',
                    'MAX': 'max',
                    'MIN': 'min',
                    'COUNT': 'count'
                }
                pd_func = func_map.get(agg_func)
                if pd_func:
                    self.df = self.df.groupby(group_col)[target_col].agg(pd_func).reset_index(name=alias)
                    print(f"[EXECUTED] GROUPED BY {group_col}, AGGREGATED {agg_func}({target_col}) AS {alias}")
                else:
                    print(f"[ERROR] Unsupported aggregate function: {agg_func}")

            elif stmt.data == 'compute_stmt':
                new_col = stmt.children[0].value
                math_expr = stmt.children[1]
                left_node = math_expr.children[0]
                op = math_expr.children[1].value
                right_node = math_expr.children[2]
                def resolve_operand(node):
                    if node.data == 'var':
                        return self.df[node.children[0].value]
                    elif node.data == 'num':
                        return float(node.children[0].value)
                left_val = resolve_operand(left_node)
                right_val = resolve_operand(right_node)
                if op == '+':
                    self.df[new_col] = left_val + right_val
                elif op == '-':
                    self.df[new_col] = left_val - right_val
                elif op == '*':
                    self.df[new_col] = left_val * right_val
                elif op == '/':
                    self.df[new_col] = left_val / right_val

                print(f"[EXECUTED] COMPUTED new column: {new_col}")