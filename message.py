import sqlite3 as lite
import sys

message = (
    ('Message Saved while creating DB.',),
    ('2nd message from db',)
)


con = lite.connect('message.db')

with con:

    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS msg")
    cur.execute("CREATE TABLE msg(msg_msg TEXT)")
    cur.executemany("INSERT INTO msg (msg_msg) VALUES (?)", message)
