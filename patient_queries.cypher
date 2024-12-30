MATCH (p:Patient) RETURN p LIMIT 10

MATCH (p:Patient)
RETURN COUNT(p) AS NumberOfPatients

MATCH (p:Patient)
WHERE toInteger(p.age) > 50 AND toInteger(p.outcome) = 1
RETURN p.age, p.glucose, p.bmi, p.outcome

MATCH (p:Patient)
RETURN AVG(toFloat(p.bmi)) AS AverageBMI

MATCH (p:Patient)
RETURN FLOOR(toInteger(p.age) / 10) * 10 AS AgeGroup, COUNT(p) AS Count
ORDER BY AgeGroup

MATCH (p:Patient)
WHERE toInteger(p.pregnancies) > 3 AND toInteger(p.outcome) = 1
RETURN p.pregnancies, p.age, p.glucose, p.bmi

MATCH (p:Patient)
WHERE toInteger(p.insulin) < 50 OR toInteger(p.insulin) > 200
RETURN p.age, p.insulin, p.outcome

MATCH (p:Patient)
RETURN p.age, p.bmi,
       CASE
         WHEN toFloat(p.bmi) < 18.5 THEN "Underweight"
         WHEN toFloat(p.bmi) >= 18.5 AND toFloat(p.bmi) <= 24.9 THEN "Normal"
         WHEN toFloat(p.bmi) >= 25 AND toFloat(p.bmi) <= 29.9 THEN "Overweight"
         ELSE "Obese"
       END AS BMICategory

MATCH (p:Patient)
WITH p.glucose AS glucose, p.bmi AS bmi
MERGE (g:GlucoseLevel {level: glucose})
MERGE (b:BMI {level: bmi})
MERGE (g)-[:HAS_BMI]->(b)
RETURN g.level AS GlucoseLevel, b.level AS BMILevel

MATCH (p1:Patient)-[r]->(p2:Patient)
RETURN p1, r, p2 LIMIT 25

MATCH (p1:Patient)-[r:SIMILAR_PREGNANCIES]->(p2:Patient)
RETURN p1, r, p2 LIMIT 25
