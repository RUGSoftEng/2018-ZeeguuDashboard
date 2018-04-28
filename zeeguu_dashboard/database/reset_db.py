import sys
import MySQLdb


def reset_cohort_db(cursor, database):
    cursor.execute("SELECT * FROM information_schema.COLUMNS "
                   "WHERE TABLE_SCHEMA = '" + database +
                   "' AND TABLE_NAME = 'cohort' "
                   "AND COLUMN_NAME = 'max_students'")
    result = cursor.fetchone()
    if result:
        cursor.execute("ALTER TABLE cohort "
                       "DROP COLUMN max_students")

    cursor.execute("SELECT * FROM information_schema.COLUMNS "
                   "WHERE TABLE_SCHEMA = '" + database +
                   "' AND TABLE_NAME = 'cohort' "
                   "AND COLUMN_NAME = 'language_id'")
    result = cursor.fetchone()
    if result:
        cursor.execute("ALTER TABLE cohort "
                       "DROP COLUMN language_id")

    cursor.execute("SELECT * FROM cohort "
                   "WHERE COLUMN_NAME = inv_code")
    result = cursor.fetchone()
    if result:
        cursor.execute("ALTER TABLE cohort "
                       "CHANGE inv_code invitation_code INT NOT NULL")


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
    #for now fixed code for the below information of database
    host = "localhost"
    user = "root"
    password = "12345678"
    database = 'zeeguu_chi'
    try:
        connection = MySQLdb.connect (host = host,
                                      user = user,
                                      passwd = password,
                                      db = database)
    except MySQLdb.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)

    cursor = connection.cursor()

    reset_cohort_db(cursor, database)
    get_cohort(cursor)

    disconnect_db(cursor, connection)


if __name__ == '__main__':
    main()