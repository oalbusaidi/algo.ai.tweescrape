import sqlite3

class SearchTermDbServices:
    
    table_name = "search_term"
    table_fields = {
        "termid": "INTEGER PRIMARY KEY",
        "term": "TEXT",
        "uid": "INTEGER FOREIGN KEY REFERENCES algouser(userid)", 
    }

    def __init__(self):
        
        self.conn = sqlite3.connect("search_data.db")
        self.cursor = self.conn.cursor()

        columns = ", ".join(
            [f"{field} {datatype}" for field, datatype in self.table_fields.items()]
        )
        create_table_query = f"CREATE TABLE IF NOT EXISTS {self.table_name} ({columns});"
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def term_exists(self, term_id):
       

        select_data_query = f"SELECT * FROM {self.table_name} WHERE termid=?;"
        self.cursor.execute(select_data_query, (term_id,))
        return self.cursor.fetchone() is not None

    def create_term(self, term_data):
        if not self.term_exists(term_data["termid"]):
            insert_data_query = f'INSERT INTO {self.table_name} ({", ".join(self.table_fields.keys())}) VALUES ({", ".join(["?" for _ in self.table_fields.keys()])});'
            self.cursor.execute(insert_data_query, list(term_data.values()))
            self.conn.commit()
            return "Search term created successfully"
        else:
            return "Search term already exists"

    def read_term(self, term_id):
        select_data_query = f"SELECT * FROM {self.table_name} WHERE termid=?;"
        self.cursor.execute(select_data_query, (term_id,))
        return self.cursor.fetchone()

    def update_term(self, term_id, updated_data):
        if self.term_exists(term_id):
            update_data_query = f'UPDATE {self.table_name} SET {", ".join([f"{field} = ?" for field in updated_data.keys()])} WHERE termid=?;'
            self.cursor.execute(update_data_query, list(updated_data.values()) + [term_id])
            self.conn.commit()
            return "Search term updated successfully"
        else:
            return "Search term does not exist"

    def delete_term(self, term_id):
        if self.term_exists(term_id):
            delete_data_query = f"DELETE FROM {self.table_name} WHERE termid=?;"
            self.cursor.execute(delete_data_query, (term_id,))
            self.conn.commit()
            return "Search term deleted successfully"
        else:
            return "Search term does not exist"