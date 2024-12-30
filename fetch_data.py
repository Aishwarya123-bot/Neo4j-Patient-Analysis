from neo4j import GraphDatabase
import pandas as pd

# Connect to Neo4j
uri = "bolt://localhost:7687"  # Your database URI
username = "neo4j"             # Your username
password = "Aishwarya@29"      # Your password

driver = GraphDatabase.driver(uri, auth=(username, password))

# Function to create nodes and relationships
def create_data(tx):
    tx.run("""
    LOAD CSV WITH HEADERS FROM 'file:///diabetes.csv' AS row
    CREATE (:Patient {
        pregnancies: row.Pregnancies,
        glucose: row.Glucose,
        blood_pressure: row.BloodPressure,
        skin_thickness: row.SkinThickness,
        insulin: row.Insulin,
        bmi: row.BMI,
        diabetes_pedigree_function: row.DiabetesPedigreeFunction,
        age: row.Age,
        outcome: row.Outcome
    })
    """)

# Create the database and import data
with driver.session() as session:
    session.execute_write(create_data)  # Use execute_write for compatibility with new versions

print("Data has been added to Neo4j!")

# Close the connection
driver.close()
