"""Export dbo.sample_data from a Microsoft Fabric lakehouse SQL analytics endpoint to CSV.

Usage:
  set FABRIC_SQL_ENDPOINT=<your-endpoint>.datawarehouse.fabric.microsoft.com
  python scripts/fetch_sample.py data/sample_data.csv

Optional: FABRIC_DATABASE names the lakehouse (default: Playground_Datalake).
Sign-in happens in your browser with Microsoft Entra ID; no secrets are stored.
"""
import csv
import os
import struct
import sys

import mssql_python
from azure.identity import InteractiveBrowserCredential

SERVER = os.environ.get("FABRIC_SQL_ENDPOINT")
DB = os.environ.get("FABRIC_DATABASE", "Playground_Datalake")
if not SERVER or len(sys.argv) < 2:
    raise SystemExit(__doc__)
OUT = sys.argv[1]
MAX_ROWS = 200000

token = InteractiveBrowserCredential().get_token("https://database.windows.net/.default").token
tb = token.encode("utf-16-le")
conn = mssql_python.connect(
    f"Server={SERVER};Database={DB};Encrypt=yes;",
    attrs_before={1256: struct.pack(f"<I{len(tb)}s", len(tb), tb)},
)
cur = conn.cursor()

cur.execute("SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS "
            "WHERE TABLE_SCHEMA='dbo' AND TABLE_NAME='sample_data' ORDER BY ORDINAL_POSITION")
cols = cur.fetchall()
print("COLUMNS:")
for c in cols:
    print(f"  {c[0]}: {c[1]}")

cur.execute("SELECT COUNT_BIG(*) FROM dbo.sample_data")
n = cur.fetchone()[0]
print("ROWS:", n)

cur.execute(f"SELECT TOP {MAX_ROWS} * FROM dbo.sample_data")
names = [d[0] for d in cur.description]
rows = cur.fetchall()
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(names)
    for r in rows:
        w.writerow(["" if v is None else v for v in r])
print("WROTE", len(rows), "rows,", os.path.getsize(OUT), "bytes")
print("SAMPLE:")
for r in rows[:5]:
    print("  ", list(r))
