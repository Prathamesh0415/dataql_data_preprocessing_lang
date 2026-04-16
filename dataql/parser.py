from lark import Lark

grammar = """
    start: statement+

    ?statement: load_stmt
              | keep_stmt
              | filter_stmt
              | sort_stmt
              | save_stmt
              | group_stmt 

    load_stmt: "LOAD" STRING ";"
    keep_stmt: "KEEP" CNAME ("," CNAME)* ";"
    filter_stmt: "FILTER" condition ("AND" condition)* ";"
    sort_stmt: "SORT" "BY" CNAME sort_order ";"
    save_stmt: "SAVE" STRING ";"
    
    group_stmt: "GROUP" "BY" CNAME "AGGREGATE" AGG_FUNC "(" CNAME ")" "AS" CNAME ";"

    condition: CNAME OPERATOR value
    OPERATOR: "==" | "!=" | ">" | "<" | ">=" | "<="
    
    AGG_FUNC: "SUM" | "AVG" | "MAX" | "MIN" | "COUNT"
    
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