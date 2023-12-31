import sqlite3
from CHAT_LLM_log import LOG

def initialize_db():
    conn = sqlite3.connect('shm.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS session
                 (uid text, session_id text, data text)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS conversion
             (uid text, session_id text, conversion_id text, data1 text, data2 text)''')

    conn.commit()
    conn.close()


#这个函数用于连接到名为'shm.db'的SQLite数据库，并打印每个表的名称、列名和最近的5条记录。
def test_db():
    conn = sqlite3.connect('shm.db')
    c = conn.cursor()

    tables = c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    for table in tables:
        print("Table name:", table[0])
        columns = c.execute("PRAGMA table_info({})".format(table[0])).fetchall()
        for column in columns:
            print("Column name:", column[1])
        records = c.execute("SELECT * FROM {} ORDER BY rowid DESC LIMIT 5".format(table[0])).fetchall()
        print("Last 5 records:", records)

    conn.close()

#给数据库添加测试数据，session表中添加5条数据，conversion表中增加25条数据。
def init_test_data():
    conn = sqlite3.connect('shm.db')
    c = conn.cursor()
    # Add test data to the session table
    c.execute("INSERT INTO session (uid, session_id, data) VALUES (?, ?, ?)", ("uid{}".format(1), "session_id{}".format(1), "data{}".format("session1")))
    c.execute("INSERT INTO session (uid, session_id, data) VALUES (?, ?, ?)", ("uid{}".format(1), "session_id{}".format(2), "data{}".format("session2")))
    c.execute("INSERT INTO session (uid, session_id, data) VALUES (?, ?, ?)", ("uid{}".format(1), "session_id{}".format(3), "data{}".format("session3")))
    c.execute("INSERT INTO session (uid, session_id, data) VALUES (?, ?, ?)", ("uid{}".format(1), "session_id{}".format(4), "data{}".format("session4")))
    c.execute("INSERT INTO session (uid, session_id, data) VALUES (?, ?, ?)", ("uid{}".format(1), "session_id{}".format(5), "data{}".format("session50000")))

    # Add test data to the conversion table
    c.execute("INSERT INTO conversion (uid, session_id,conversion_id,  data1, data2) VALUES (?, ?, ?, ?, ?)", ("uid{}".format(1),  "session_id{}".format(1), "conversion_id{}".format(1), "data1{}".format("conversion1"), "data2{}".format("conversion1")))
    c.execute("INSERT INTO conversion (uid, session_id,conversion_id,  data1, data2) VALUES (?, ?, ?, ?, ?)", ("uid{}".format(1),  "session_id{}".format(1), "conversion_id{}".format(1), "data1{}".format("conversion2"), "data2{}".format("conversion2")))
    c.execute("INSERT INTO conversion (uid, session_id,conversion_id,  data1, data2) VALUES (?, ?, ?, ?, ?)", ("uid{}".format(1),  "session_id{}".format(1), "conversion_id{}".format(1), "data1{}".format("conversion3"), "data2{}".format("conversion3")))
    c.execute("INSERT INTO conversion (uid, session_id,conversion_id,  data1, data2) VALUES (?, ?, ?, ?, ?)", ("uid{}".format(1),  "session_id{}".format(1), "conversion_id{}".format(1), "data1{}".format("conversion4"), "data2{}".format("conversion4")))
    c.execute("INSERT INTO conversion (uid, session_id,conversion_id,  data1, data2) VALUES (?, ?, ?, ?, ?)", ("uid{}".format(1),  "session_id{}".format(1), "conversion_id{}".format(1), "data1{}".format("conversion5"), "data2{}".format("conversion5")))
    c.execute("INSERT INTO conversion (uid, session_id,conversion_id,  data1, data2) VALUES (?, ?, ?, ?, ?)", ("uid{}".format(1),  "session_id{}".format(1), "conversion_id{}".format(1), "data1{}".format("conversion6"), "data2{}".format("conversion60000")))
    
    c.execute("INSERT INTO conversion (uid, session_id,conversion_id,  data1, data2) VALUES (?, ?, ?, ?, ?)", ("uid{}".format(1),  "session_id{}".format(5), "conversion_id{}".format(1), "data1{}".format("conversion1"), "data2{}".format("conversion1")))
    c.execute("INSERT INTO conversion (uid, session_id,conversion_id,  data1, data2) VALUES (?, ?, ?, ?, ?)", ("uid{}".format(1),  "session_id{}".format(5), "conversion_id{}".format(1), "data1{}".format("conversion2"), "data2{}".format("conversion2")))
    c.execute("INSERT INTO conversion (uid, session_id,conversion_id,  data1, data2) VALUES (?, ?, ?, ?, ?)", ("uid{}".format(1),  "session_id{}".format(5), "conversion_id{}".format(1), "data1{}".format("conversion3"), "data2{}".format("conversion3")))
    c.execute("INSERT INTO conversion (uid, session_id,conversion_id,  data1, data2) VALUES (?, ?, ?, ?, ?)", ("uid{}".format(1),  "session_id{}".format(5), "conversion_id{}".format(1), "data1{}".format("conversion4"), "data2{}".format("conversion4")))
    c.execute("INSERT INTO conversion (uid, session_id,conversion_id,  data1, data2) VALUES (?, ?, ?, ?, ?)", ("uid{}".format(1),  "session_id{}".format(5), "conversion_id{}".format(1), "data1{}".format("conversion5"), "data2{}".format("conversion5")))
    c.execute("INSERT INTO conversion (uid, session_id,conversion_id,  data1, data2) VALUES (?, ?, ?, ?, ?)", ("uid{}".format(1),  "session_id{}".format(5), "conversion_id{}".format(1), "data1{}".format("conversion6"), "data2{}".format("conversion60000")))
    
    
    conn.commit()
    conn.close()


#从session表中查询最近30条数据
def query_recent_session_data_by_uid(uid):
    conn = sqlite3.connect('shm.db')
    c = conn.cursor()
    records = c.execute("SELECT * FROM session WHERE uid=? ORDER BY rowid DESC LIMIT 30", (uid,)).fetchall()
    conn.close()
    LOG(records)
    return records


#从conversion表中查询最近30条数据
def query_recent_conversion_data_by_uid_and_session_id(uid, session_id):
    conn = sqlite3.connect('shm.db')
    c = conn.cursor()
    records = c.execute("SELECT * FROM conversion WHERE uid=? AND session_id=? ORDER BY rowid ASC LIMIT 30", (uid, session_id)).fetchall()
    conn.close()
    LOG(records)
    return records


if __name__ == '__main__':
    initialize_db()
    init_test_data()
    test_db()
    test_db()
