import psycopg2

conn = psycopg2.connect(
    dbname="shoefit", user="nehanandhakumar", password="", host="localhost", port="5432"
)
cursor = conn.cursor()

# 1. Drop the old table so we start clean
cursor.execute("DROP TABLE IF EXISTS stride_logs;")

# 2. Create table with correct columns
cursor.execute("""
CREATE TABLE stride_logs (
    id SERIAL PRIMARY KEY,
    cadence INT,
    pronation_angle FLOAT,
    heel_impact_force INT,
    forefoot_impact_force INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

# 3. Insert sample stride data
cursor.execute("""
INSERT INTO stride_logs (cadence, pronation_angle, heel_impact_force, forefoot_impact_force)
VALUES 
    (158, 12.5, 820, 410),
    (162, 14.1, 850, 430),
    (160, 13.8, 810, 400),
    (155, 15.2, 890, 450);
""")

conn.commit()
cursor.close()
conn.close()

print("Sample gait data successfully inserted into 'shoefit' database!")