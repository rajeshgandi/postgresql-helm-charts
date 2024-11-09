import psycopg2
from faker import Faker
import sys

# Initialize Faker and database connection
fake = Faker()
conn = psycopg2.connect(
    host="localhost",  # Use localhost when port-forwarding
    database="postgres",
    user="postgres",
    password="postgres"
)
cursor = conn.cursor()

# Define the number of records to insert
num_authors = 1000
num_books = 100000
batch_size = 5000  # Commit every 1000 records

# Insert authors with progress reporting
print("Inserting authors...")
author_ids = []  # List to store the generated author IDs
for i in range(num_authors):
    cursor.execute("INSERT INTO authors (name) VALUES (%s) RETURNING author_id", (fake.name(),))  # Use your actual primary key name
    author_id = cursor.fetchone()[0]  # Get the generated author ID
    author_ids.append(author_id)  # Store it in the list

    if (i + 1) % batch_size == 0:
        conn.commit()  # Commit every batch_size authors
        print(f"{i + 1} authors inserted...")

# Final commit for authors
conn.commit()
print(f"Total authors inserted: {num_authors}")

# Insert books with progress reporting
print("Inserting books...")
for i in range(num_books):
    # Use a valid author_id from the list
    random_author_id = fake.random.choice(author_ids)  # Pick a random author ID from the list
    cursor.execute("INSERT INTO books (title, author_id) VALUES (%s, %s)", (fake.sentence(), random_author_id))

    if (i + 1) % batch_size == 0:
        conn.commit()  # Commit every batch_size books
        print(f"{i + 1} books inserted...")

# Final commit for books
conn.commit()
print(f"Total books inserted: {num_books}")

# Clean up
cursor.close()
conn.close()
print("Data insertion completed.")

