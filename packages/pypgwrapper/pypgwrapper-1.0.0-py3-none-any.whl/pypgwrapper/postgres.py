import psycopg2
from psycopg2 import sql, extras, extensions
from tabulate import tabulate


class Postgres:
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.connection = None
        self.query = None

    def connect(self, database=None, _print_message=True):
        try:
            database = database or self.current_database
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=database,
            )
            self.connection.autocommit = True  # Disable transactions
            if _print_message:
                print(f"Connected to database '{database}' as user '{self.user}'")
        except psycopg2.Error as e:
            print(
                f"Error connecting to database '{database}' as user '{self.user}': {e}"
            )

    def disconnect(self, _print_message=True):
        if self.connection:
            self.connection.close()
            if _print_message:
                print("Disconnected from database.")

    def select(self, table, columns="*"):
        self.query = self._build_query(columns=columns, table=table)
        return self

    def where(self, conditions):
        self.query += self._build_where_clause(conditions)
        return self

    def order(self, columns, asc=False):
        self.query += self._build_order_by_clause(columns, asc)
        return self

    def groupby(self, columns):
        self.query += self._build_group_by_clause(columns)
        return self

    def execute(self):
        if self.query:
            self.sql(self.query)
        else:
            print("No query to execute.")

    # Other methods...

    def _build_query(
        self, columns="*", table=None, conditions=None, order_by=None, group_by=None
    ):
        query_template = "SELECT {columns} FROM {table}{where_clause}{group_by_clause}{order_by_clause}"
        where_clause = self._build_where_clause(conditions) if conditions else ""
        group_by_clause = self._build_group_by_clause(group_by) if group_by else ""
        order_by_clause = self._build_order_by_clause(order_by) if order_by else ""
        return query_template.format(
            columns=columns,
            table=table,
            where_clause=where_clause,
            group_by_clause=group_by_clause,
            order_by_clause=order_by_clause,
        )

    def _build_where_clause(self, conditions):
        return f" WHERE {conditions}" if conditions else ""

    def _build_order_by_clause(self, columns, asc=False):
        order_direction = "ASC" if asc else "DESC"
        return f" ORDER BY {columns} {order_direction}" if columns else ""

    def _build_group_by_clause(self, columns):
        return f" GROUP BY {columns}" if columns else ""

    def sql(self, query, commit=False):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                if commit:
                    self.connection.commit()
                else:
                    if cursor.description is not None:
                        columns = [desc[0] for desc in cursor.description]
                        result = cursor.fetchall()
                        if result:
                            print(tabulate(result, headers=columns, tablefmt="psql"))
                        else:
                            print("No results found.")
        except psycopg2.Error as e:
            print(f"Error executing query: {e}")

    def create_database(self, new_database):
        if self.connection.get_dsn_parameters()["dbname"] != "postgres":
            current_database = self.connection.get_dsn_parameters()["dbname"]
            self.connect(database="postgres")
        query = sql.SQL("CREATE DATABASE {}").format(sql.Identifier(new_database))
        self.sql(query)
        self.connect(
            database=current_database, _print_message=False
        )  # Connect to the new database
        print(f"Database '{new_database}' created")

    def execute(self):
        if self.query:
            self.sql(self.query)
        else:
            print("No query to execute.")

    def delete_database(self, database_to_delete):
        try:
            current_database = self.connection.get_dsn_parameters()["dbname"]
            self.connect(database="postgres", _print_message=False)
            query = sql.SQL("DROP DATABASE IF EXISTS {}").format(
                sql.Identifier(database_to_delete)
            )
            self.sql(query)
            print(f"Database '{database_to_delete}' deleted")
            self.connect(database=current_database, _print_message=False)
        except psycopg2.Error as e:
            print(f"Error deleting database '{database_to_delete}': {e}")

    def delete_user(self, username):
        query = sql.SQL("DROP USER IF EXISTS {}").format(sql.Identifier(username))
        if self.sql(query, commit=True):
            print(f"User '{username}' deleted")

    def create_user(self, username, password, is_superuser=False):
        query = sql.SQL("CREATE USER {} WITH PASSWORD {}").format(
            sql.Identifier(username), sql.Literal(password)
        )
        if is_superuser:
            query += sql.SQL(" SUPERUSER")
        if self.sql(query, commit=True):
            print(f"User '{username}' created")

    def switch_user(self, user, password):
        try:
            current_database = self.connection.get_dsn_parameters()["dbname"]
            self.disconnect(_print_message=False)
            self.user = user
            self.password = password
            self.connect(database=current_database, _print_message=False)
            print(f"Switched to user '{user}'")
        except psycopg2.Error as e:
            print(f"Error switching to user '{user}': {e}")

    def get_connection_details(self):
        if self.connection:
            print(
                f"Connected to database '{self.connection.get_dsn_parameters()['dbname']}' as user '{self.user}'"
            )
        else:
            print("Not connected to any database.")


# Example usage:
if __name__ == "__main__":
    db = Postgres(host="localhost", port="5432", user="postgres", password="password")

    db.connect(database="market_data")

    db.delete_database("test_db")
    db.create_database("test_db")

    db.get_connection_details()

    db.delete_user("test_user")

    # Creating a new user
    db.create_user(username="test_user", password="test_password", is_superuser=True)

    db.switch_user(user="test_user", password="test_password")

    # db.connect(database="market_data")

    # Example query building
    db.select(table="stock_data.gainers", columns="symbol, price").where(
        "symbol = 'HOLO'"
    ).order("symbol", asc=True).execute()

    db.sql("SELECT symbol, price FROM stock_data.gainers LIMIT 5")
