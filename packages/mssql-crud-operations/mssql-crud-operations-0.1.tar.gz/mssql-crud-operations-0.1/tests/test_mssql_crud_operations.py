import pyodbc

class MSSQLCrudOperations:
    def __init__(self, server, port, database, table_name):
        self.conn_str = f'DRIVER={{SQL Server}};SERVER={server},{port};DATABASE={database};Trusted_Connection=yes;'
        self.table_name = table_name

    def create_connection(self):
        conn = pyodbc.connect(self.conn_str)
        return conn

    def execute_query(self, query, values=None):
        try:
            conn = self.create_connection()
            cursor = conn.cursor()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)

            conn.commit()
            print("Sorgu başarıyla çalıştırıldı.")
            return True

        except Exception as e:
            conn.rollback()
            print(f'Hata: {e}')
            return False

        finally:
            conn.close()

    def insert_data(self, **kwargs):
        try:
            columns = ', '.join(f"{key}" for key in kwargs.keys() if key != 'ID')
            values = ', '.join('?' for key in kwargs.keys() if key != 'ID')
            insert_query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({values})"
            values = tuple(value for key, value in kwargs.items() if key != 'ID')

            if self.execute_query(insert_query, values):
                last_inserted_id = self.get_last_inserted_id()
                return last_inserted_id
            else:
                return False

        except Exception as e:
            return str(e)

    def get_last_inserted_id(self):
        try:
            query = f"SELECT TOP 1 ID FROM {self.table_name} ORDER BY ID DESC;"
            conn = self.create_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            last_inserted_id = cursor.fetchone()
            return int(last_inserted_id[0]) if last_inserted_id else None

        except Exception as e:
            print(f'Hata: {e}')
            return None

        finally:
            conn.close()

    def update_data(self, **kwargs):
        try:
            update_columns = ', '.join(f"{key} = ?" for key in kwargs.keys() if key != 'ID')
            update_query = f"UPDATE {self.table_name} SET {update_columns} WHERE ID = ?"
            values = tuple(kwargs.values())
            if self.execute_query(update_query, values):
                return True
            else:
                return False
        except Exception as e:
            return str(e)

    def update_or_insert_data(self, **kwargs):
        try:
            record_id = kwargs.get('ID')

            if self.record_exists(record_id):
                if self.update_data(**kwargs):
                    return f"Record with ID {record_id} updated successfully"

            else:
                insert_result = self.insert_data(**kwargs)
                if insert_result:
                    return insert_result

        except Exception as e:
            return str(e)

    def record_exists(self, record_id):
        search_query = f"SELECT * FROM {self.table_name} WHERE ID = ?"
        values = (record_id,)
        try:
            conn = self.create_connection()
            cursor = conn.cursor()
            cursor.execute(search_query, values)
            row = cursor.fetchone()
            return row is not None

        except Exception as e:
            print(f'Hata: {e}')
            return str(e)
        finally:
            conn.close()

    def delete_data(self, record_id):
        try:
            delete_query = f"DELETE FROM {self.table_name} WHERE ID = ?"
            self.execute_query(delete_query, (record_id,))
        except Exception as e:
            return str(e)

    def search_data(self, **kwargs):
        if not kwargs:
            search_query = f"SELECT * FROM {self.table_name}"
            values = None
        else:
            conditions = ' AND '.join(f"{key} = ?" for key in kwargs.keys() if kwargs[key])
            if conditions:
                search_query = f"SELECT * FROM {self.table_name} WHERE {conditions}"
                values = tuple(value for value in kwargs.values() if value)
            else:
                search_query = f"SELECT * FROM {self.table_name}"
                values = None

        try:
            conn = self.create_connection()
            cursor = conn.cursor()
            if values:
                cursor.execute(search_query, values)
            else:
                cursor.execute(search_query)

            rows = cursor.fetchall()

            if rows:
                result = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

                return result
            else:
                return []

        except Exception as e:
            print(f'Hata: {e}')
            return str(e)

        finally:
            conn.close()
