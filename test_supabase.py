from config.supabase_config import supabase

def test():
    result = supabase.table("transaksi").select("*").limit(1).execute()
    print(result)

if __name__ == "__main__":
    test()
