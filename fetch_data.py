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

#to create node relations:
def create_bmi_relationships(tx):
    tx.run("""
    MATCH (p1:Patient), (p2:Patient)
    WHERE abs(toFloat(p1.bmi) - toFloat(p2.bmi)) < 2 AND p1 <> p2
    MERGE (p1)-[:SIMILAR_BMI]->(p2)
    """)

with driver.session() as session:
    session.write_transaction(create_bmi_relationships)

print("Created BMI relationships!")

def create_glucose_relationships(tx):
    tx.run("""
    MATCH (p1:Patient), (p2:Patient)
    WHERE abs(toInteger(p1.glucose) - toInteger(p2.glucose)) < 10 AND p1 <> p2
    MERGE (p1)-[:SIMILAR_GLUCOSE]->(p2)
    """)

with driver.session() as session:
    session.write_transaction(create_glucose_relationships)

print("Created Glucose relationships!")

def create_pregnancy_relationships(tx):
    tx.run("""
    MATCH (p1:Patient), (p2:Patient)
    WHERE abs(toInteger(p1.pregnancies) - toInteger(p2.pregnancies)) <= 1 AND p1 <> p2
    MERGE (p1)-[:SIMILAR_PREGNANCIES]->(p2)
    """)

with driver.session() as session:
    session.write_transaction(create_pregnancy_relationships)

print("Created Pregnancy relationships!")
