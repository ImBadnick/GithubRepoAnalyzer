import json
import mysql.connector
from mysql.connector import Error


f = open('../RepoData.json')
data = json.load(f)

try: 
    connection = mysql.connector.connect(host='host',
                                         database='db_name',
                                         user='user_name',
                                         password='user_password')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
  
        # Foreach repository take name, views and clones
        for repo in data['Repo']:
            name = repo['Name']
            views = []
            clones = []
            for single_view in repo['Stats']['views']:
                single_view_timestamp = single_view['timestamp']
                single_view_uniques_count = single_view['uniques']
                single_view_count = single_view['count']
                try:  
                    cursor.execute(f"""INSERT INTO Views (RepoName, view_timestamp, view_n_uniques_users, n_views) VALUES ('{name}','{single_view_timestamp}','{single_view_uniques_count}','{single_view_count}')""")
                except Error as e:
                    print(e)
            
            for single_clones in repo['Stats']['clones']:
                single_clones_timestamp = single_clones['timestamp']
                single_clones_uniques_count = single_clones['uniques']
                single_clones_count = single_clones['count']
                clones.append((name, single_clones_timestamp, single_clones_uniques_count, single_clones_count))
                try:  
                    cursor.execute(f"""INSERT INTO Clones (RepoName, clone_timestamp, clone_n_uniques_users, n_clones) VALUES ('{name}','{single_clones_timestamp}','{single_clones_uniques_count}','{single_clones_count}')""")
                except Error as e:
                    print(e)
            
        connection.commit()
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
except Error as e:
    print("Error while connecting to MySQL", e)
    



f.close()