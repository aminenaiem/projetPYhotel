import pymysql

ports = [3306, 3307, 2555, 33060]
found = False

for p in ports:
    print(f"Testing port {p}...")
    try:
        conn = pymysql.connect(
            host='127.0.0.1', 
            user='root', 
            password='', 
            port=p, 
            connect_timeout=2
        )
        print(f"SUCCESS: Connected to MySQL on port {p}!")
        with conn.cursor() as cursor:
            cursor.execute("SHOW DATABASES")
            dbs = [db[0] for db in cursor.fetchall()]
            print(f"Databases: {dbs}")
        conn.close()
        found = True
        break
    except Exception as e:
        print(f"FAILED on port {p}: {e}")

if not found:
    print("Could not connect to MySQL on any typical port.")
