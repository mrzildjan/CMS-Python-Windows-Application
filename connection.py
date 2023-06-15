
# CREATE first the database CMS before proceeding
# then, you can run this and see the output from the terminal to verify the connection of the database
import psycopg2

# Establish a connection to the database
conn = psycopg2.connect(host='localhost', user='postgres', password='password', dbname='cms') # change password

# Create a cursor
cursor = conn.cursor()

# Execute the query to display all the tables from database cms
cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_catalog = 'cms';")

# Fetch all the rows
rows = cursor.fetchall()

# Print the names of the databases
for row in rows:
    print(row[0])

# Close the cursor and the connection
cursor.close()
conn.close()
