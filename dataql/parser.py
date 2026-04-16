from lark import Lark

grammar = """
    start: statement+

    ?statement: load_stmt
              | keep_stmt
              | filter_stmt
              | sort_stmt
              | save_stmt
              | group_stmt 
              | compute_stmt

    load_stmt: "LOAD" STRING ";"
    keep_stmt: "KEEP" CNAME ("," CNAME)* ";"
    filter_stmt: "FILTER" condition ("AND" condition)* ";"
    sort_stmt: "SORT" "BY" CNAME sort_order ";"
    save_stmt: "SAVE" STRING ";"
    
    compute_stmt: "COMPUTE" CNAME "=" math_expr ";"
    math_expr: math_operand MATH_OP math_operand

    group_stmt: "GROUP" "BY" CNAME "AGGREGATE" AGG_FUNC "(" CNAME ")" "AS" CNAME ";"

    
    condition: CNAME OPERATOR value
    OPERATOR: "==" | "!=" | ">" | "<" | ">=" | "<="

    MATH_OP: "+" | "-" | "/" | "*"
    AGG_FUNC: "SUM" | "AVG" | "MAX" | "MIN" | "COUNT"
    
    ?math_operand: CNAME -> var | NUMBER -> num
    ?sort_order: "ASC" -> asc | "DESC" -> desc
    ?value: STRING | NUMBER

    %import common.CNAME
    %import common.ESCAPED_STRING -> STRING
    %import common.SIGNED_NUMBER -> NUMBER
    %import common.WS
    %ignore WS
"""

def get_parser():
    return Lark(grammar, parser='lalr')