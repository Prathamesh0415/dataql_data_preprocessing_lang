# Project Report

## DataQL — A Domain-Specific Language for Data Preprocessing

---

**Subject:** Compiler Design Lab  
**Project Title:** DataQL — A Domain-Specific Language for CSV Data Preprocessing  
**Student Name:** Naresh Mahiya  
**Email:** nareshmahiya2017@gmail.com  
**Date:** April 2026  

---

## Table of Contents

1. [Abstract](#1-abstract)
2. [Introduction](#2-introduction)
3. [Objectives](#3-objectives)
4. [Background and Literature Review](#4-background-and-literature-review)
5. [System Design and Architecture](#5-system-design-and-architecture)
6. [Language Grammar Specification](#6-language-grammar-specification)
7. [Implementation Details](#7-implementation-details)
8. [Sample Execution and Output](#8-sample-execution-and-output)
9. [Tools and Technologies Used](#9-tools-and-technologies-used)
10. [Results and Discussion](#10-results-and-discussion)
11. [Conclusion](#11-conclusion)
12. [References](#12-references)

---

## 1. Abstract

DataQL is a Domain-Specific Language (DSL) designed to enable users to preprocess tabular data stored in CSV files using a simple, English-like syntax. The project implements all three classical phases of a language interpreter — lexical analysis, syntax analysis (parsing), and execution — making it a complete demonstration of compiler design principles. The language supports seven core data preprocessing operations: loading data, column selection, row filtering, sorting, column computation, data grouping with aggregation, and saving results. The lexer and parser are generated automatically from a formal grammar using the Lark library (LALR(1) parsing strategy), while the execution engine interprets the resulting Abstract Syntax Tree (AST) and applies operations to a pandas DataFrame. This project serves as a practical application of compiler construction theory in the context of real-world data preprocessing.

---

## 2. Introduction

### 2.1 Motivation

Data preprocessing is one of the most time-consuming steps in any data analysis or machine learning pipeline. Data analysts frequently need to clean raw CSV files — filtering rows, selecting columns, computing derived values, sorting records, and aggregating groups. Traditionally, this requires writing Python or SQL code, which is not always accessible to non-programmers.

DataQL addresses this by providing a simple, readable command language where a user can express preprocessing steps in plain English-like commands:

```
LOAD "sales_data.csv";
FILTER revenue > 10000;
SORT BY revenue DESC;
SAVE "high_revenue.csv";
```

From a compiler design perspective, DataQL is a complete interpreted language. It demonstrates the full pipeline from raw text input to program execution, encompassing lexical analysis, grammar-driven parsing, AST construction, and tree-walking interpretation.

### 2.2 Problem Statement

Design and implement a Domain-Specific Language (DSL) for data preprocessing that:

- Accepts a script written in a custom language syntax.
- Tokenizes the script using a lexer.
- Parses the token stream into an Abstract Syntax Tree using a formal grammar and parser.
- Interprets and executes the AST to transform a CSV dataset.

---

## 3. Objectives

1. Define a formal context-free grammar for a data preprocessing language.
2. Implement a lexer and LALR(1) parser using the Lark parsing toolkit.
3. Build an execution engine (interpreter) that walks the AST and performs data operations using pandas.
4. Support seven data preprocessing commands: LOAD, KEEP, FILTER, SORT, COMPUTE, GROUP, and SAVE.
5. Demonstrate the complete compiler pipeline — from source text to program output — on a sample dataset.

---

## 4. Background and Literature Review

### 4.1 Compiler Phases

A typical compiler or interpreter involves the following phases:

| Phase | Description |
|---|---|
| Lexical Analysis | Converts the raw source text into a flat stream of tokens (keywords, identifiers, literals, operators). |
| Syntax Analysis | Parses the token stream according to a formal grammar, producing an Abstract Syntax Tree (AST). |
| Semantic Analysis | Checks meaning-level correctness (type checking, scope resolution). |
| Code Generation / Interpretation | Generates target code or directly executes the AST. |

DataQL implements lexical analysis, syntax analysis, and direct interpretation (execution).

### 4.2 Domain-Specific Languages

A Domain-Specific Language (DSL) is a programming language or specification language dedicated to a particular problem domain. Unlike general-purpose languages (Python, Java), DSLs provide constructs and abstractions tailored to a specific task. Examples include SQL (database queries), HTML (document structure), and CSS (styling).

DataQL is an **internal interpreted DSL** — it is processed by a Python program that evaluates the language's constructs at runtime.

### 4.3 LALR(1) Parsing

LALR (Look-Ahead Left-to-Right Rightmost derivation) is a bottom-up parsing strategy. It reads input left to right, uses a look-ahead of one token to resolve parsing decisions, and builds the parse tree from leaves (tokens) up to the root. LALR(1) parsers are widely used in practice (they underlie tools like Yacc and Bison) because they are efficient (O(n) time complexity, linear in input length) and support a large class of practical grammars.

The Lark library used in this project generates an LALR(1) parser automatically from the grammar specification written in an EBNF-like notation.

### 4.4 Abstract Syntax Tree (AST)

An AST is a tree representation of the syntactic structure of a program. Unlike a raw parse tree (which includes every grammar rule including trivial ones), an AST retains only the semantically meaningful structure. Each node in the AST represents a construct in the source program. For example, parsing `FILTER salary > 50000;` produces:

```
filter_stmt
  └── condition
        ├── salary        (column name)
        ├── >             (operator)
        └── 50000         (value)
```

The execution engine walks this tree and uses the node data to filter the DataFrame.

---

## 5. System Design and Architecture

### 5.1 High-Level Architecture

The system follows a three-stage pipeline:

```
 ┌───────────────────────┐
 │   DataQL Script        │   (plain text source, e.g., "FILTER salary > 50000;")
 └──────────┬────────────┘
            │
            ▼
 ┌───────────────────────┐
 │      LEXER             │   Breaks text into tokens: FILTER, CNAME("salary"),
 │  (Lark / LALR)         │   OPERATOR(">"), NUMBER(50000), ";"
 └──────────┬────────────┘
            │
            ▼
 ┌───────────────────────┐
 │      PARSER            │   Matches token stream against grammar rules,
 │  (Lark / LALR)         │   produces an Abstract Syntax Tree (AST)
 └──────────┬────────────┘
            │
            ▼
 ┌───────────────────────┐
 │   EXECUTION ENGINE     │   Walks the AST node by node; for each statement
 │  (DataQLEngine class)  │   type calls the corresponding pandas operation
 └──────────┬────────────┘
            │
            ▼
 ┌───────────────────────┐
 │  Output DataFrame /    │   Modified dataset printed to console or saved
 │  CSV File              │   as a new CSV file
 └───────────────────────┘
```

### 5.2 Project File Structure

```
dataql_data_preprocessing_lang/
│
├── main.py                  # Entry point: creates sample data, runs the DSL script
├── requirements.txt         # Python dependencies (pandas, lark)
│
└── dataql/
    ├── __init__.py          # Package marker
    ├── parser.py            # Grammar definition and Lark parser factory
    └── engine.py            # AST-walking execution engine (DataQLEngine class)
```

### 5.3 Component Responsibilities

| Component | File | Responsibility |
|---|---|---|
| Grammar & Parser | `dataql/parser.py` | Defines the formal grammar; exposes `get_parser()` which returns a Lark LALR parser |
| Execution Engine | `dataql/engine.py` | `DataQLEngine.execute(tree)` walks the AST and performs pandas operations |
| Entry Point | `main.py` | Creates sample data, defines a demo script, invokes parser and engine |

---

## 6. Language Grammar Specification

The complete formal grammar of DataQL is defined in `dataql/parser.py` using Lark's EBNF-like notation:

```
start: statement+

?statement: load_stmt
          | keep_stmt
          | filter_stmt
          | sort_stmt
          | save_stmt
          | group_stmt
          | compute_stmt

load_stmt:    "LOAD" STRING ";"
keep_stmt:    "KEEP" CNAME ("," CNAME)* ";"
filter_stmt:  "FILTER" condition ("AND" condition)* ";"
sort_stmt:    "SORT" "BY" CNAME sort_order ";"
save_stmt:    "SAVE" STRING ";"
compute_stmt: "COMPUTE" CNAME "=" math_expr ";"
group_stmt:   "GROUP" "BY" CNAME "AGGREGATE" AGG_FUNC "(" CNAME ")" "AS" CNAME ";"

condition: CNAME OPERATOR value
OPERATOR: "==" | "!=" | ">" | "<" | ">=" | "<="

math_expr:    math_operand MATH_OP math_operand
MATH_OP:      "+" | "-" | "/" | "*"
AGG_FUNC:     "SUM" | "AVG" | "MAX" | "MIN" | "COUNT"

?math_operand: CNAME -> var | NUMBER -> num
?sort_order:   "ASC" -> asc | "DESC" -> desc
?value:        STRING | NUMBER

%import common.CNAME
%import common.ESCAPED_STRING -> STRING
%import common.SIGNED_NUMBER  -> NUMBER
%import common.WS
%ignore WS
```

### 6.1 Grammar Explanation

**Terminals (tokens produced by the Lexer):**

| Terminal | Meaning | Example |
|---|---|---|
| `CNAME` | Valid identifier — letters, digits, underscore | `salary`, `department`, `total_comp` |
| `STRING` | Double-quoted string literal | `"employees.csv"`, `"Sales"` |
| `NUMBER` | Signed integer or decimal number | `50000`, `0.15`, `-10` |
| `OPERATOR` | Comparison operator | `==`, `!=`, `>`, `<`, `>=`, `<=` |
| `MATH_OP` | Arithmetic operator | `+`, `-`, `*`, `/` |
| `AGG_FUNC` | Aggregation function keyword | `SUM`, `AVG`, `MAX`, `MIN`, `COUNT` |

**The `?` prefix** on a rule in Lark means the rule is "transparent" — if it has only one child, that child replaces the node in the tree, keeping the AST compact.

**The `->` alias** (e.g., `CNAME -> var`) renames the resulting tree node, allowing the engine to distinguish a column-name operand (`var`) from a numeric literal operand (`num`) in a `math_expr`.

**`%ignore WS`** instructs the lexer to discard all whitespace (spaces, tabs, newlines) between tokens.

---

## 7. Implementation Details

### 7.1 Parser (`dataql/parser.py`)

```python
from lark import Lark

def get_parser():
    return Lark(grammar, parser='lalr')
```

`get_parser()` is a factory function that instantiates and returns a Lark parser configured with the LALR(1) algorithm. The grammar string is passed directly. No manual tokenizer or parse-table construction is required — Lark derives both automatically from the grammar definition.

### 7.2 Execution Engine (`dataql/engine.py`)

The `DataQLEngine` class holds a single mutable state — `self.df` — which is the pandas DataFrame being transformed. The `execute(tree)` method iterates over the top-level children of the parsed AST (each corresponding to one statement) and dispatches to the appropriate handler using `stmt.data` (the node's rule name).

#### 7.2.1 LOAD Statement

```python
filename = stmt.children[0].value.strip('"')
self.df = pd.read_csv(filename)
```

Strips the surrounding double-quote characters from the parsed filename token and reads the CSV file into `self.df` using pandas.

#### 7.2.2 KEEP Statement

```python
columns = [child.value for child in stmt.children]
self.df = self.df[columns]
```

Extracts all column name tokens from the AST node and performs DataFrame column selection, dropping all other columns.

#### 7.2.3 FILTER Statement

```python
for condition in stmt.children:
    col = condition.children[0].value
    op  = condition.children[1].value
    val = condition.children[2].value
    if val.isdigit():
        val = float(val)
    else:
        val = val.strip('"')
    if op == '==': self.df = self.df[self.df[col] == val]
    elif op == '!=': self.df = self.df[self.df[col] != val]
    # ... (and so on for >, <, >=, <=)
```

Multiple `AND` conditions are processed sequentially — each iteration narrows `self.df`. The engine performs runtime type inference: if the value token is a digit string, it is cast to `float`; otherwise, surrounding quotes are stripped to get a string value. Filtering itself uses pandas **boolean indexing**, which is a vectorized O(n) operation.

#### 7.2.4 SORT Statement

```python
col = stmt.children[0].value
is_ascending = stmt.children[1].data == 'asc'
self.df = self.df.sort_values(by=col, ascending=is_ascending)
```

The sort direction is determined from the AST node name: `asc` or `desc` (set by the grammar alias `?sort_order: "ASC" -> asc | "DESC" -> desc`). `sort_values` is called on the DataFrame.

#### 7.2.5 SAVE Statement

```python
filename = stmt.children[0].value.strip('"')
self.df.to_csv(filename, index=False)
```

Writes the current state of `self.df` to a CSV file, without the row index column.

#### 7.2.6 COMPUTE Statement

```python
new_col    = stmt.children[0].value
math_expr  = stmt.children[1]
left_node  = math_expr.children[0]
op         = math_expr.children[1].value
right_node = math_expr.children[2]

def resolve_operand(node):
    if node.data == 'var':
        return self.df[node.children[0].value]   # pandas Series
    elif node.data == 'num':
        return float(node.children[0].value)      # scalar float

left_val  = resolve_operand(left_node)
right_val = resolve_operand(right_node)

if op == '+': self.df[new_col] = left_val + right_val
elif op == '-': self.df[new_col] = left_val - right_val
elif op == '*': self.df[new_col] = left_val * right_val
elif op == '/': self.df[new_col] = left_val / right_val
```

The `resolve_operand` helper returns either a pandas `Series` (for a column reference, node type `var`) or a Python `float` (for a numeric literal, node type `num`). When an operation is applied between a Series and a scalar, pandas **broadcasts** (vectorizes) the scalar across every row — no explicit loop is needed.

#### 7.2.7 GROUP Statement

```python
group_col  = stmt.children[0].value
agg_func   = stmt.children[1].value.upper()
target_col = stmt.children[2].value
alias      = stmt.children[3].value

func_map = {'SUM': 'sum', 'AVG': 'mean', 'MAX': 'max', 'MIN': 'min', 'COUNT': 'count'}
pd_func  = func_map.get(agg_func)

self.df = self.df.groupby(group_col)[target_col].agg(pd_func).reset_index(name=alias)
```

The `AGG_FUNC` terminal captures the aggregation keyword, which is mapped to the corresponding pandas aggregation string. `groupby(...).agg(...)` performs the group-and-aggregate operation. `reset_index(name=alias)` converts the result back to a flat DataFrame with the user-specified alias as the aggregated column name.

### 7.3 Entry Point (`main.py`)

```python
def create_dummy_data():
    data = {
        "first_name": ["Alice", "Bob", "Charlie", "David", "Eve"],
        "department": ["Engineering", "Sales", "Engineering", "HR", "Sales"],
        "salary":     [90000, 60000, 85000, 50000, 75000]
    }
    pd.DataFrame(data).to_csv("employees.csv", index=False)

dsl_script = """
    LOAD "employees.csv";
    FILTER department == "Sales";
    COMPUTE bonus = salary * 0.15;
    COMPUTE total_comp = salary + bonus;
"""

parser   = get_parser()
ast_tree = parser.parse(dsl_script)

engine = DataQLEngine()
engine.execute(ast_tree)

print("\n--- Final Output DataFrame ---")
print(engine.df)
```

`create_dummy_data()` generates a reproducible sample CSV. The DSL script string is then parsed into an AST and executed by the engine. The final DataFrame is printed to standard output.

---

## 8. Sample Execution and Output

### 8.1 Input CSV (`employees.csv`)

| first_name | department  | salary |
|---|---|---|
| Alice      | Engineering | 90000  |
| Bob        | Sales       | 60000  |
| Charlie    | Engineering | 85000  |
| David      | HR          | 50000  |
| Eve        | Sales       | 75000  |

### 8.2 DataQL Script

```
LOAD "employees.csv";
FILTER department == "Sales";
COMPUTE bonus = salary * 0.15;
COMPUTE total_comp = salary + bonus;
```

### 8.3 Step-by-Step Execution Trace

**Step 1 — LOAD**

The lexer produces tokens: `LOAD`, `"employees.csv"`, `;`

The parser matches rule `load_stmt` and builds the AST node. The engine calls `pd.read_csv("employees.csv")`. DataFrame now has 5 rows.

**Step 2 — FILTER department == "Sales"**

The lexer produces: `FILTER`, `department`, `==`, `"Sales"`, `;`

The parser builds a `filter_stmt` node containing one `condition` child. The engine evaluates `self.df['department'] == 'Sales'` (a boolean Series) and indexes the DataFrame with it.

DataFrame narrows to 2 rows: Bob and Eve.

**Step 3 — COMPUTE bonus = salary * 0.15**

The lexer produces: `COMPUTE`, `bonus`, `=`, `salary`, `*`, `0.15`, `;`

The parser builds a `compute_stmt` node with a `math_expr` child. The engine resolves `salary` as a pandas Series and `0.15` as a float scalar. The product `Series * scalar` is computed element-wise and stored as the new column `bonus`.

**Step 4 — COMPUTE total_comp = salary + bonus**

Similarly, `salary` and `bonus` are both resolved as pandas Series (columns in `self.df`). Their element-wise sum is stored as `total_comp`.

### 8.4 Console Output

```
[EXECUTED] LOADED data from employees.csv
[EXECUTED] FILTERED data
[EXECUTED] COMPUTED new column: bonus
[EXECUTED] COMPUTED new column: total_comp

--- Final Output DataFrame ---
  first_name department  salary    bonus  total_comp
1        Bob      Sales   60000   9000.0     69000.0
4        Eve      Sales   75000  11250.0     86250.0
```

### 8.5 AST Structure for the Demo Script

```
start
├── load_stmt
│     └── Token(STRING, '"employees.csv"')
├── filter_stmt
│     └── condition
│           ├── Token(CNAME, 'department')
│           ├── Token(OPERATOR, '==')
│           └── Token(STRING, '"Sales"')
├── compute_stmt
│     ├── Token(CNAME, 'bonus')
│     └── math_expr
│           ├── var
│           │     └── Token(CNAME, 'salary')
│           ├── Token(MATH_OP, '*')
│           └── num
│                 └── Token(NUMBER, '0.15')
└── compute_stmt
      ├── Token(CNAME, 'total_comp')
      └── math_expr
            ├── var
            │     └── Token(CNAME, 'salary')
            ├── Token(MATH_OP, '+')
            └── var
                  └── Token(CNAME, 'bonus')
```

---

## 9. Tools and Technologies Used

| Tool / Library | Version | Purpose |
|---|---|---|
| Python | 3.x | Implementation language |
| Lark | Latest | Grammar definition, automatic LALR(1) lexer and parser generation |
| Pandas | Latest | DataFrame operations within the execution engine |
| Git | — | Version control |

### 9.1 Why Lark?

Lark was chosen because:
- It accepts grammars written in a clean, readable EBNF-like notation.
- It supports LALR(1), LL(1), and Earley parsing strategies.
- It automatically generates both the lexer and the parser from a single grammar string.
- The resulting parse tree (Lark `Tree` and `Token` objects) is straightforward to traverse in Python.

### 9.2 Why Pandas?

Pandas provides efficient, vectorized operations over tabular data (DataFrames). Boolean indexing, `sort_values`, `groupby`, and column assignment are all implemented in optimized C/NumPy code under the hood, meaning DataQL operations run efficiently even on large CSV files.

---

## 10. Results and Discussion

### 10.1 Achievements

- A complete interpreted language pipeline was successfully implemented: lexing → parsing → AST construction → tree-walking execution.
- Seven data preprocessing commands are supported, covering the most common CSV transformation operations.
- The grammar is formal and unambiguous, enabling the LALR(1) parser to resolve every parsing decision with a single token of look-ahead.
- The execution engine correctly handles numeric and string values, column references, scalar literals, multi-condition filters (AND), sort direction, all four arithmetic operators, and five aggregation functions.

### 10.2 Compiler Design Concepts Demonstrated

| Concept | How It Appears in DataQL |
|---|---|
| Lexical Analysis | Lark's lexer tokenizes keywords (`LOAD`, `FILTER`, etc.), identifiers (`CNAME`), strings (`ESCAPED_STRING`), and numbers (`SIGNED_NUMBER`) |
| Context-Free Grammar | The grammar in `parser.py` is a context-free grammar in EBNF notation |
| LALR(1) Parsing | `Lark(grammar, parser='lalr')` generates and uses an LALR(1) parse table |
| Abstract Syntax Tree | Lark's `Tree` and `Token` objects form the AST traversed by the engine |
| Tree-Walking Interpreter | `DataQLEngine.execute()` implements the Interpreter design pattern on the AST |
| Type Inference | The engine detects numeric vs. string values at runtime from token content |
| Vectorized Execution | Pandas Series operations are applied element-wise without explicit loops |

### 10.3 Limitations and Future Work

| Limitation | Possible Extension |
|---|---|
| `COMPUTE` supports only a single binary operation (e.g., `a * b`) | Extend the grammar with recursive `math_expr` rules to support nested expressions (e.g., `(a + b) * c`) |
| `FILTER` supports only `AND` combinations | Add `OR` and parenthesized grouping to the filter grammar |
| No semantic error messages | Add type-checking and column-existence validation with informative error output |
| No interactive REPL | Add a read-eval-print loop so users can type and run commands one at a time |
| Only CSV input/output | Extend `LOAD`/`SAVE` to support JSON, Excel, and database sources |

---

## 11. Conclusion

DataQL successfully demonstrates the implementation of a complete language interpreter from first principles. The project applies core compiler design concepts — lexical analysis, formal grammar specification, LALR(1) parsing, and AST-based interpretation — to a practical problem in data preprocessing.

By writing a grammar-first language (defining syntax before implementation), the project follows sound language design methodology. The Lark library automates the most mechanically complex part (building parse tables), allowing focus to remain on the grammar design and execution semantics. The pandas library provides the high-performance data manipulation layer that makes the language practically useful.

The result is a readable, extensible DSL that allows data preprocessing pipelines to be expressed concisely, while the underlying system faithfully implements the three-phase compiler architecture studied in the course.

---

## 12. References

1. Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). *Compilers: Principles, Techniques, and Tools* (2nd ed.). Pearson Education.
2. Lark Documentation. *Lark — A Parsing Toolkit for Python*. https://lark-parser.readthedocs.io/
3. Pandas Documentation. *pandas — Python Data Analysis Library*. https://pandas.pydata.org/docs/
4. Fowler, M. (2010). *Domain-Specific Languages*. Addison-Wesley Professional.
5. Knuth, D. E. (1965). On the translation of languages from left to right. *Information and Control*, 8(6), 607–639.

---

*Report prepared for Compiler Design Lab — Academic Year 2025–2026*
