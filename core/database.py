import mysql.connector
from mysql.connector import errorcode
import pandas as pd

WEATHER_DATA = pd.read_csv("../data/data.csv")

try:
    my_db = mysql.connector.connect(
        host="localhost",
        port=3000,
        user="root",
        password="2002",
        database="cloud_oracle",
    )

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your username or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist.")
    else:
        print(err)


def insert_record(connection, weather_records):
    cursor = connection.cursor()
    query = """
                INSERT INTO weather_data(month, day, date, lowest_temperature, highest_temperature) VALUES(%s, %s, %s, %s, %s);
             """

    for row in weather_records.itertuples(index=False):
        cursor.execute(
            query,
            (
                row.month,
                row.day,
                row.date,
                int(row.lowest_temperature),
                int(row.highest_temperature),
            ),
        )

    connection.commit()

    query_d = """
            SELECT * FROM Weather_data;
            """
    cursor.execute(query_d)
    results = cursor.fetchall()
    cursor.close()
    return results


if my_db.is_connected():
    data = insert_record(my_db, WEATHER_DATA)
    print(data)
    my_db.close()
