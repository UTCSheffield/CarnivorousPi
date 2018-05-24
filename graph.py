import pandas as pd
import sqlite3

conn = sqlite3.connect("Logging.db")
df = pd.read_sql_query("SELECT * FROM Logging_Table LIMIT 120;", conn)

df.plot.line()