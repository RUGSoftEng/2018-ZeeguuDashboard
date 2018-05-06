import sys
import MySQLdb


"""
This file contains the scripts for migrating the old Zeeguu database to the new version for this project.
"""


def update_cohort_db(cursor, database):
    """

    :param cursor:
    :param database:
    :return:
    """

    """rename invitation_code to inv_code column"""
    cursor.execute("SELECT * FROM information_schema.COLUMNS "
                   "WHERE TABLE_SCHEMA = '" + database +
                   "' AND TABLE_NAME = 'cohort' "
                   "AND COLUMN_NAME = 'inv_code'")
    result = cursor.fetchall()
    if not result:
        cursor.execute("ALTER TABLE cohort "
                       "Change invitation_code inv_code char(50) NOT NULL")
        cursor.execute("ALTER TABLE cohort "
                       "ADD UNIQUE (inv_code) ")
        cursor.execute("SELECT id, name, inv_code FROM cohort")
        rows = cursor.fetchall()
        for row in rows:
            """if no the class has no inv_code, set the name as same as inv_code"""
            if row[2] is None:
                cursor.execute("UPDATE cohort SET inv_code = '" + row[1] + "' WHERE id = '" + str(row[0]) + "'")

    """add column max_students"""
    cursor.execute("SELECT * FROM information_schema.COLUMNS "
                   "WHERE TABLE_SCHEMA = '" + database +
                   "' AND TABLE_NAME = 'cohort' "
                   "AND COLUMN_NAME = 'max_students'")
    result = cursor.fetchall()
    if not result:
        cursor.execute("ALTER TABLE cohort "
                       "ADD max_students int NOT NULL DEFAULT 30")

    """add class_language_id column"""
    cursor.execute("SELECT * FROM information_schema.COLUMNS "
                   "WHERE TABLE_SCHEMA = '" + database +
                   "' AND TABLE_NAME = 'cohort' "
                   "AND COLUMN_NAME = 'language_id'")
    result = cursor.fetchall()
    if not result:
        cursor.execute("ALTER TABLE cohort "
                       "ADD language_id int NOT NULL DEFAULT 4")


def get_cohort(cursor):
    """

    :param cursor:
    :return:
    """
    query = "SELECT * FROM cohort "
    cursor.execute(query)
    print('''SELECT * FROM cohort:''')
    result = cursor.fetchall()
    for r in result:
        print(r)
    return result


def disconnect_db(cursor, connection):
    """

    :param cursor:
    :param connection:
    :return:
    """
    cursor.close()
    connection.close()


def main():
    """

    :return:
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

    update_cohort_db(cursor, database)

    """this doesn't do anything but it is good to see if we update db correctly"""
    get_cohort(cursor)

    disconnect_db(cursor, connection)


if __name__ == '__main__':
    main()
