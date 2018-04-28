import sys
import MySQLdb


def update_cohort_db(cursor, database):
    # change name to class_name
    cursor.execute("SELECT * FROM information_schema.COLUMNS "
                   "WHERE TABLE_SCHEMA = '" + database +
                   "' AND TABLE_NAME = 'cohort' "
                   "AND COLUMN_NAME = 'class_name'")
    result = cursor.fetchall()
    if not result:
        cursor.execute("ALTER TABLE cohort "
                       "Change name class_name char(50)")

    # add inv_code column
    cursor.execute("SELECT * FROM information_schema.COLUMNS "
                   "WHERE TABLE_SCHEMA = '" + database +
                   "' AND TABLE_NAME = 'cohort' "
                   "AND COLUMN_NAME = 'inv_code'")
    result = cursor.fetchall()
    if not result:
        cursor.execute("ALTER TABLE cohort "
                       "ADD inv_code char(50)")
        cursor.execute("ALTER TABLE cohort "
                       "ADD UNIQUE (inv_code) ")
        cursor.execute("SELECT id, class_name FROM cohort")
        rows = cursor.fetchall()
        for row in rows:
            cursor.execute("UPDATE cohort SET inv_code = '" + row[1] + "' WHERE id = '" + str(row[0]) + "'")

    # add column max_students
    cursor.execute("SELECT * FROM information_schema.COLUMNS "
                   "WHERE TABLE_SCHEMA = '" + database +
                   "' AND TABLE_NAME = 'cohort' "
                   "AND COLUMN_NAME = 'max_students'")
    result = cursor.fetchall()
    if not result:
        cursor.execute("ALTER TABLE cohort "
                       "ADD max_students int NOT NULL DEFAULT 30")

    # add cur_students column
    cursor.execute("SELECT * FROM information_schema.COLUMNS "
                   "WHERE TABLE_SCHEMA = '" + database +
                   "'AND TABLE_NAME = 'cohort' "
                   "AND COLUMN_NAME = 'cur_students'")
    result = cursor.fetchall()
    if not result:
        cursor.execute("ALTER TABLE cohort "
                       "ADD cur_students int NOT NULL DEFAULT 0")

    # add class_lange_id column
    cursor.execute("SELECT * FROM information_schema.COLUMNS "
                   "WHERE TABLE_SCHEMA = '" + database +
                   "' AND TABLE_NAME = 'cohort' "
                   "AND COLUMN_NAME = 'class_language_id'")
    result = cursor.fetchall()
    if not result:
        cursor.execute("ALTER TABLE cohort "
                       "ADD class_language_id int NOT NULL DEFAULT 4")


def get_cohort(cursor):
    query = "SELECT * FROM cohort "
    cursor.execute(query)
    print('''SELECT * FROM cohort:''')
    result = cursor.fetchall()
    for r in result:
        print(r)
    return result


def disconnect_db(cursor, connection):
    cursor.close()
    connection.close()


def main():
    host = "localhost"
    user = "root"
    password = "12345678"
    database = 'zeeguu_chi'
    try:
        connection = MySQLdb.connect(host=host,
                                     user=user,
                                     passwd=password,
                                     db=database)
    except MySQLdb.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)

    cursor = connection.cursor()

    update_cohort_db(cursor, database)
    get_cohort(cursor)

    disconnect_db(cursor, connection)


if __name__ == '__main__':
    main()
