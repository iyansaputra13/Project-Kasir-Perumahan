# migrasi_ke_supabase.py
import mysql.connector
from supabase import create_client, Client
from datetime import date, datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "Kasirperumahan133123!"),
    "database": os.getenv("MYSQL_DB", "kasir_perumahan")
}

# Initialize clients
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def serialize_value(value):
    """Handle all data type conversions"""
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    elif value is None:
        return None
    return str(value) if isinstance(value, (bytes, bytearray)) else value

def migrate_table(table_name, id_column="id"):
    try:
        print(f"\nMigrating {table_name}...")
        
        # Get existing IDs from Supabase
        existing_ids = set()
        try:
            existing = supabase.table(table_name).select(id_column).execute()
            existing_ids = {row[id_column] for row in existing.data}
        except Exception as e:
            print(f"Warning: Couldn't check existing data in {table_name} - {str(e)}")
        
        # Fetch data from MySQL
        mysql_cursor.execute(f"SELECT * FROM {table_name}")
        columns = [col[0] for col in mysql_cursor.description]
        new_data = []
        
        for row in mysql_cursor.fetchall():
            row_dict = dict(zip(columns, row))
            if row_dict.get(id_column) not in existing_ids:
                processed_row = {k: serialize_value(v) for k, v in row_dict.items()}
                new_data.append(processed_row)
        
        # Insert in batches
        batch_size = 100
        inserted_rows = 0
        
        for i in range(0, len(new_data), batch_size):
            batch = new_data[i:i + batch_size]
            try:
                response = supabase.table(table_name).insert(batch).execute()
                inserted_rows += len(batch)
                print(f"Inserted batch {i//batch_size + 1} for {table_name}")
            except Exception as e:
                print(f"Error inserting batch {i//batch_size + 1}: {str(e)}")
                # Try inserting row by row
                for row in batch:
                    try:
                        supabase.table(table_name).insert(row).execute()
                        inserted_rows += 1
                    except Exception as single_e:
                        print(f"Failed to insert row: {single_e}")
        
        print(f"Successfully migrated {inserted_rows}/{len(new_data)} rows to {table_name}")
        return True
        
    except Exception as e:
        print(f"Failed to migrate {table_name}: {str(e)}")
        return False

def main():
    try:
        # MySQL connection
        mysql_conn = mysql.connector.connect(**MYSQL_CONFIG)
        global mysql_cursor
        mysql_cursor = mysql_conn.cursor()
        
        # List of tables to migrate in order
        tables_to_migrate = [
            ('users', 'id'),          # Migrate users first
            ('transaksi', 'id'),      # Then transactions
            ('cicilan_dp', 'id'),     # Then installments
            ('pembayaran', 'id')      # Finally payments
        ]
        
        for table, id_col in tables_to_migrate:
            migrate_table(table, id_col)
            
    except Exception as e:
        print(f"Fatal error: {str(e)}")
    finally:
        if 'mysql_cursor' in globals():
            mysql_cursor.close()
        if 'mysql_conn' in locals():
            mysql_conn.close()

if __name__ == "__main__":
    print("Starting migration process...")
    main()
    print("\nMigration completed!")