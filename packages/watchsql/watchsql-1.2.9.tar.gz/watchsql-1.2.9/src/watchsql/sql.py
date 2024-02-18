from dataclasses import dataclass, field
from time import perf_counter
from datetime import datetime
from threading import Thread
import MySQLdb
import MySQLdb.cursors

class QueryNotAllowed(Exception):
    def __init__(self, query: str, position: tuple):
        msg = f"Query not allowed:\n{query}\n"
        msg += (" " * position[0]) + ("^" * (position[1]-position[0]))
        super().__init__(msg)

@dataclass
class QueryOptions:
    db_host: str
    db_user: str | None
    db_pass: str | None
    db_base: str | None
    db_port: int | None
    query: str

    def __post_init__(self):
        self.query = self.query.strip()

        allowed_first_words = ["SELECT", "DESC", "SHOW"]
        banned_query_words  = ["INTO"]
        if self.query.split(" ")[0].upper() not in allowed_first_words:
            raise QueryNotAllowed(self.query, (0, self.query.find(" ")))
        for x in banned_query_words:
            if (n := self.query.find(x)) > -1:
                raise QueryNotAllowed(self.query, (n, n+len(x)))

@dataclass
class Result:
    time: datetime
    result: dict
    query_time: float

class QueryWatcher:

    def __init__(self, options: QueryOptions):
        self.options = options
        self.db = DBConnection(self.options)
        self.th = Thread(target=self._watch)

        self.running = False
        self.last_run = datetime.now()
        self.results = list()

    def query(self):
        th = Thread(target=self._watch)
        th.start()
        th.join()
        #self.th.start()

    def _watch(self):
        self.running = True
        self.last_run = datetime.now()
        self.last_command_run_s = perf_counter()

        try:
            t1 = perf_counter()
            self.db.cur.execute(self.options.query)
            result = self.db.cur.fetchall()
            self.db.cnx.rollback()
            self.results.append(Result(
                time = datetime.now(),
                result = result,
                query_time = perf_counter() - t1
            ))
            self.query_had_error = False
        except Exception as e:
            self.query_error = str(e)
            self.query_had_error = True

        self.running = False
        self.screen_change_pending = True

class DBConnection:
    """ Context manager, that CAN be used "manually" with the open and close methods. """

    def __init__(self, queryOptions: QueryOptions, cursorclass=MySQLdb.cursors.DictCursor, **params):
        self.cursorclass = cursorclass
        self.connect_params = {
            "host": queryOptions.db_host,
            "user": queryOptions.db_user,
            "passwd": queryOptions.db_pass,
            "db": queryOptions.db_base,
            "port": queryOptions.db_port,
            "charset": "latin1",
            "use_unicode": True
        }
        for key, value in params.items(): self.connect_params[key] = value
        if open: self.open()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        """ This should run even if a exception is raised somewhere. """
        self.close()

    def open(self):
        self.cnx = MySQLdb.connect(**self.connect_params)
        self.cur = self.cnx.cursor(self.cursorclass)

    def close(self):
        if hasattr(self, "cur") and hasattr(self, "cnx") and self.cnx.open:
            self.cur.close()
            self.cnx.close()
