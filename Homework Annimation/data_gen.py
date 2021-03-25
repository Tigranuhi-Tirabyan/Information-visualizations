import sqlite3
import numpy as np
import time


connection = sqlite3.connect('data_db.db')
c = connection.cursor()

c.execute("DROP TABLE IF EXISTS dice_results")

c.execute("CREATE TABLE dice_results (Id int, value1 int, value2 int, value3 int, value4 int, value5 int, value6 int, value7 int)")



i = 0
while i < 100:
    i += 1
    value1 = np.random.randint(1,7)
    value2 = np.random.randint(1,7)
    value3 = np.random.randint(1,7)
    value4 = np.random.randint(1,7)
    value5 = np.random.randint(1,7)
    value6 = np.random.randint(1,7)
    value7 = np.random.randint(1,7)
    c.execute("INSERT INTO dice_results values ({},{},{},{},{},{},{},{})".format(i,value1, value2, value3, value4, value5, value6, value7))
    connection.commit()

    time.sleep(0.5)
