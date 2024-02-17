import sqlite3

class TweetDbServices:
    table_name = "twitter_tweet"
    table_fields = {
        "tweetid": "INTEGER",
        "userid": "INTEGER",
        "conversationid": "INTEGER",
        "url": "TEXT",
        "date": "DATETIME",
        "lang": "TEXT",
        "rawContent": "TEXT",
        "replyCount": "INTEGER",
        "retweetCount": "INTEGER",
        "likeCount": "INTEGER",
        "quoteCount": "INTEGER",
        "viewCount": "INTEGER",
    }

    def __init__(self):
        self.conn = sqlite3.connect("scraped_data.db")
        self.cursor = self.conn.cursor()
        columns = ', '.join([f'{field} {datatype}' if field != 'tweetid' else f'{field} {datatype} PRIMARY KEY' for field, datatype in self.table_fields.items()])
        create_table_query = f'CREATE TABLE IF NOT EXISTS {self.table_name} ({columns});'
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def tweet_exists(self, tweet_id):
        select_data_query = f'SELECT * FROM {self.table_name} WHERE tweetid=?;'
        self.cursor.execute(select_data_query, (tweet_id,))
        return self.cursor.fetchone() is not None

    def create_tweet(self, tweet_data):
        if not self.tweet_exists(tweet_data['tweetid']):
            insert_data_query = f'INSERT INTO {self.table_name} ({", ".join(self.table_fields.keys())}) VALUES ({", ".join(["?" for _ in self.table_fields.keys()])});'
            self.cursor.execute(insert_data_query, [tweet_data.get(field) for field in self.table_fields.keys()])
            self.conn.commit()
            return "Tweet created successfully"
        else:
            return "Tweet already exists"

    def read_tweet(self, tweet_id):
        select_data_query = f'SELECT * FROM {self.table_name} WHERE tweetid=?;'
        self.cursor.execute(select_data_query, (tweet_id,))
        tweet = self.cursor.fetchone()
        return tweet

    def update_tweet(self, tweet_id, updated_data):
        if self.tweet_exists(tweet_id):
            update_data_query = f'UPDATE {self.table_name} SET {", ".join([f"{field} = ?" for field in updated_data.keys()])} WHERE tweetid=?;'
            self.cursor.execute(update_data_query, list(updated_data.values()) + [tweet_id])
            self.conn.commit()
            return "Tweet updated successfully"
        else:
            return "Tweet does not exist"

    def delete_tweet(self, tweet_id):
        if self.tweet_exists(tweet_id):
            delete_data_query = f'DELETE FROM {self.table_name} WHERE tweetid=?;'
            self.cursor.execute(delete_data_query, (tweet_id,))
            self.conn.commit()
            return "Tweet deleted successfully"
        else:
            return "Tweet does not exist"
