import argparse
from getpass import getpass
from watchsql.sql import QueryWatcher, QueryOptions, QueryNotAllowed
import sys

class GLOBALS:
    QUERY: QueryWatcher

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", "-H", type=str, help="database host [localhost]", default="127.0.0.1")
    parser.add_argument("--port", "-P", type=int, help="database port [3306]", default=3306)
    parser.add_argument("--user", "-u", type=str, help="database user", default=None)
    parser.add_argument("--database", "-d", type=str, help="database", default=None)
    parser.add_argument("--password", "-p", action="store_true", help="get database password from command line", default=False)

    parser.add_argument("--timeout", "-n", type=int, metavar='seconds', help="Update interval [2]", default=2)
    parser.add_argument("--graph-values", "-g", type=str, help="The column to use for graphing", default=None)
    parser.add_argument("--graph-column", "-c", type=str, help="The column to use for graphing labels", default=None)
    parser.add_argument("--graph-max-samples", type=int, help="How many samples to save before starting to scroll [1000]", default=1000)
    parser.add_argument("--vertical", "-v", action="store_true", help="Show rows vertically instead of in a table", default=False)

    parser.add_argument("query", metavar="QUERY", type=str, nargs="+", help="The query to watch")

    args = parser.parse_args()

    password = None
    if args.password:
        password = getpass("Password: ")

    try:
        q1 = QueryWatcher(QueryOptions(
            db_host = args.host,
            db_user = args.user,
            db_pass = password,
            db_base = args.database,
            db_port = args.port,
            query = " ".join(args.query)
        ))
    except QueryNotAllowed as e:
        print(f"\u001b[31m{e}\u001b[0m")
        sys.exit(1)

    q1.query()
    q1.query()
    print(q1.results)
        
