import sys
import MySQLdb


def main():
    """
    for now fixed code for the below information of database
    """
    host = "localhost"
    user = "root"
    password = "12345678"
    database = 'zeeguu_test'
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


def reset_cohort_db(cursor, database):

    """drop max_students"""
    cursor.execute("SELECT * FROM information_schema.COLUMNS "
                   "WHERE TABLE_SCHEMA = '" + database +
                   "' AND TABLE_NAME = 'cohort' "
                   "AND COLUMN_NAME = 'max_students'")
    result = cursor.fetchone()
    if result:
        cursor.execute("ALTER TABLE cohort "
                       "DROP COLUMN max_students")

    """drop language_id and remove foreign key"""
    cursor.execute("SELECT * FROM information_schema.COLUMNS "
                   "WHERE TABLE_SCHEMA = '" + database +
                   "' AND TABLE_NAME = 'cohort' "
                   "AND COLUMN_NAME = 'language_id'")
    result = cursor.fetchone()
    if result:
        cursor.execute("ALTER TABLE cohort DROP FOREIGN KEY cohort_ibfk_1")
        cursor.execute("ALTER TABLE cohort "
                       "DROP COLUMN language_id")

    """change inv_code back to invitation_code"""
    cursor.execute("SELECT * FROM information_schema.COLUMNS "
                   "WHERE TABLE_SCHEMA = '" + database +
                   "' AND TABLE_NAME = 'cohort' "
                   "AND COLUMN_NAME = 'inv_code'")
    result = cursor.fetchone()
    if result:
        cursor.execute("ALTER TABLE cohort "
                       "Change inv_code invitation_code char(50) NOT NULL")


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


if __name__ == '__main__':
    main()