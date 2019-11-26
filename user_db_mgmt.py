import argparse
import sqlite3
import pandas as pd


def insert_user(db_path, username, first, last, email, has_password=0):
    """
    Inserts a user into the user database. Will throw an error is the user
    already exists.

    Args:
        db_path: path to the user database
        username: username of the user
        first: users first name
        last: users last name
        email: user email including address
        has_password: indicates if they have a password in the users table
            should be 0 in almost every situation.
        
    Returns:
        None: updates user database
    """
    conn = sqlite3.connect(db_path)

    new_user = pd.DataFrame(
        [[username, first, last, email, has_password]],
        columns=["username", "first_name", "last_name", "email", "has_password"],
    )
    new_user.to_sql("usernames", conn, if_exists="append", index=False)

    conn.commit()
    conn.close()

    return "User inserted"


def delete_user(db_path, username):
    """
    Deletes a user from the user database. 

    Args:
        db_path: path to the user database
        username: username of the user
        
    Returns:
        None: updates user database
    """
    conn = sqlite3.connect(db_path)

    query_user = """DELETE FROM user WHERE username=?;"""
    query_usernames = """DELETE FROM usernames WHERE username=?;"""

    c = conn.cursor()
    c.execute(query_user, (username,))
    c.execute(query_usernames, (username,))

    conn.commit()
    conn.close()

    return "User deleted"


def update_from_csv(user_db, csv_path):
    """
    Updates usernames table in the users database using the usernames csv

    Args:
        db_path: path to the user database
        csv_path: path of the csv to use to update the database
        
    Returns:
        None: updates user database
    """
    usernames = pd.read_csv(csv_path)

    conn = sqlite3.connect(user_db)
    c = conn.cursor()

    usernames.to_sql("temp", conn, if_exists="append", index=False)
    c.execute(
        f"""
            INSERT INTO usernames (username, first_name, last_name, email, has_password)
            SELECT username, first_name, last_name, email, has_password FROM temp t
            WHERE NOT EXISTS
                (SELECT * from usernames f
                WHERE f.username = t.username);
            """
    )
    conn.commit()
    conn.close()
    return "Users updated"


def create_from_csv(db_path, csv_path):
    """
    Creates a users database for the dashboard from
    a provided csv file

    Args:
        db_path(str): path to the database - if just the name
            it will be created in this folder
        csv_path(str): path to the csv
            that contains the csv of users
            Columns of username, first_name, last_name, email, has_password
    """
    usernames = pd.read_csv(csv_path)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    q = """CREATE TABLE user (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password NOT NULL
            );
            """

    c.execute(q)
    conn.commit()

    q = """CREATE TABLE usernames (
            username TEXT NOT NULL UNIQUE PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            has_password INT NOT NULL
            );
        """
    c.execute(q)

    usernames.to_sql("usernames", conn, if_exists="append", index=False)
    conn.commit()
    conn.close()

    return "User database created"


def main(action, db_path, csv_path, username, first, last, email, has_password=0):
    user_func = {
        "delete user": (delete_user, [db_path, username]),
        "add user": (
            insert_user,
            [db_path, username, first, last, email, int(has_password)],
        ),
        "update from csv": (update_from_csv, [db_path, csv_path]),
        "create from csv": (create_from_csv, [db_path, csv_path]),
    }

    db_action, args = user_func[action]

    return db_action(**args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "action",
        type=str,
        help="Action to perform on the database. Can be delete user, add user, update from csv, and create from csv.",
    )
    parser.add_argument("db_path", type=str, help="path to database (include .db)")
    parser.add_argument(
        "csv_path",
        type=str,
        default=None,
        help="path to username csv file (include filename and .csv. Only needs to be included for update or create from csv actions.",
    )
    parser.add_argument(
        "username",
        type=str,
        default=None,
        help="user name to be inserted or deleted. Not needed for csv related actions.",
    )
    parser.add_argument(
        "first",
        type=str,
        default=None,
        help="first name of user to be inserted. Not needed for deletion of user or csv related actions.",
    )
    parser.add_argument(
        "last",
        type=str,
        default=None,
        help="last name of user to be inserted. Not needed for deletion of user or csv related actions.",
    )
    parser.add_argument(
        "email",
        type=str,
        default=None,
        help="email of user to be inserted (including address). Not needed for deletion of user or csv related actions.",
    )
    parser.add_argument(
        "has_password",
        type=str,
        default=None,
        help="Does the user have a password in the users table? 1 if they do, 0 if they do not. Not needed for deletion of user or csv related actions.",
    )
    arguments = parser.parse_args()
    main(**vars(arguments))
