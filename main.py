import time
import psycopg2

# --- CONFIGURATION ---
SIMULATION_MODE = True  
DB_NAME = "shoefit"
DB_USER = "nehanandhakumar"  

def connect_db():
    """Establishes connection to your local PostgreSQL instance with a timeout."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            host="localhost",
            port="5432",
            connect_timeout=3  
        )
        return conn
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None

def analyze_gait(roll_time):
    """Evaluates the stride timing and returns classification + recommendation."""
    if roll_time < 120:
        classification = "RAPID_STRIKE"
        rec = "Needs stiff, rockered geometry platform shoes to smooth transition."
    elif roll_time > 350:
        classification = "PROLONGED_HEEL"
        rec = "Needs plush cushioning with reinforced heel crash pads."
    else:
        classification = "IDEAL"
        rec = "Standard neutral support daily trainers."
    return classification, rec

def log_stride(user_id, roll_time, classification, recommendation):
    """Inserts a calculated step directly into the PostgreSQL stride_logs table."""
    conn = connect_db()
    if not conn:
        return
    
    try:
        cur = conn.cursor()
        query = """
            INSERT INTO stride_logs (user_id, roll_time_ms, gait_classification, recommended_shoe_type)
            VALUES (%s, %s, %s, %s);
        """
        cur.execute(query, (user_id, roll_time, classification, recommendation))
        conn.commit()
        print(f"💾 Step logged successfully! ({roll_time} ms -> {classification})")
        cur.close()
    except Exception as e:
        print(f"❌ Failed to write to database: {e}")
    finally:
        conn.close()

def main():
    print("--- Shoe Fit Data Processor Active ---")
    
    conn = connect_db()
    if not conn:
        print("❌ Cannot proceed without a database connection.")
        return
        
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO users (user_id, name) VALUES (1, 'Neha') ON CONFLICT DO NOTHING;")
        conn.commit()
        cur.close()
    except Exception as e:
        print(f"⚠️ Warning creating test user: {e}")
    finally:
        conn.close()

    current_user_id = 1 
    
    if SIMULATION_MODE:
        print("🤖 Running in SIMULATION MODE. Generating test footsteps...")
        mock_steps = [80, 250, 420, 260] 
        
        for step_time in mock_steps:
            time.sleep(1.0) 
            print(f"\n[STEP DETECTED] Processing a foot roll of {step_time} ms...")
            
            gait_class, shoe_rec = analyze_gait(step_time)
            log_stride(current_user_id, step_time, gait_class, shoe_rec)
            
        print("\n🏁 Finished processing simulated steps.")

if __name__ == "__main__":
    main()