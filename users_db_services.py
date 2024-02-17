import sqlite3

class UserDbServices:
    table_name = "twitter_user"
    table_fields = {
        "userid": "INTEGER",
        "username": "TEXT",
        "displayname": "TEXT",
        "created": "DATETIME",
        "followersCount": "INTEGER",
        "friendsCount": "INTEGER",
        "statusesCount": "INTEGER",
        "favouritesCount": "INTEGER",
        "listedCount": "INTEGER",
        "mediaCount": "INTEGER",
        "location": "TEXT",
        "verified": "INTEGER",
        "blue": "INTEGER"
    }

    def __init__(self):
        self.conn = sqlite3.connect("scraped_data.db")
        self.cursor = self.conn.cursor()
        columns = ', '.join([f'{field} {datatype}' if field != 'userid' else f'{field} {datatype} PRIMARY KEY' for field, datatype in self.table_fields.items()])
        create_table_query = f'CREATE TABLE IF NOT EXISTS {self.table_name} ({columns});'
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def user_exists(self, user_id):
        select_data_query = f'SELECT * FROM {self.table_name} WHERE userid=?;'
        self.cursor.execute(select_data_query, (user_id,))
        return self.cursor.fetchone() is not None

    def create_user(self, user_data):
        if not self.user_exists(user_data['userid']):
            insert_data_query = f'INSERT INTO {self.table_name} ({", ".join(self.table_fields.keys())}) VALUES ({", ".join(["?" for _ in self.table_fields.keys()])});'
            self.cursor.execute(insert_data_query, [user_data.get(field) for field in self.table_fields.keys()])
            self.conn.commit()
            return "User created successfully"
        else:
            return "User already exists"

    def read_user(self, user_id):
        select_data_query = f'SELECT * FROM {self.table_name} WHERE userid=?;'
        self.cursor.execute(select_data_query, (user_id,))
        user = self.cursor.fetchone()
        return user

    def update_user(self, user_id, updated_data):
        if self.user_exists(user_id):
            update_data_query = f'UPDATE {self.table_name} SET {", ".join([f"{field} = ?" for field in updated_data.keys()])} WHERE userid=?;'
            self.cursor.execute(update_data_query, list(updated_data.values()) + [user_id])
            self.conn.commit()
            return "User updated successfully"
        else:
            return "User does not exist"

    def delete_user(self, user_id):
        if self.user_exists(user_id):
            delete_data_query = f'DELETE FROM {self.table_name} WHERE userid=?;'
            self.cursor.execute(delete_data_query, (user_id,))
            self.conn.commit()
            return "User deleted successfully"
        else:
            return "User does not exist"
