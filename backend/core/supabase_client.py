import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", os.getenv("SUPABASE_ANON_KEY", ""))

if not SUPABASE_URL or "placeholder" in SUPABASE_URL or "your" in SUPABASE_URL:
    print("⚠️  [NOTE] Supabase is not configured. Falling back to Mock Client (Demo Mode).")
    class MockSupa:
        def __init__(self): self.auth = self
        def sign_in_with_password(self, p): raise Exception("Database not connected (Demo Mode). Please use 'Mock Google Login'.")
        def sign_up(self, p): raise Exception("Database not connected (Demo Mode).")
        def sign_in_with_oauth(self, *a, **kw): raise Exception("Database not connected")
        def exchange_code_for_session(self, *a, **kw): raise Exception("Database not connected")
        def table(self, *a, **kw): return self
        def select(self, *a, **kw): return self
        def execute(self, *a, **kw): return type('MockRes', (), {'data': []})()
    supabase = MockSupa()
    is_mock = True
else:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        is_mock = False
    except Exception as e:
        print(f"❌ Supabase Connection Error: {e}")
        class MockSupaFallback:
            def __init__(self): self.auth = self
            def sign_in_with_password(self, p): raise Exception(f"Database Error: {e}")
            def sign_up(self, p): raise Exception(f"Database Error: {e}")
            def sign_in_with_oauth(self, *a, **kw): raise Exception("Database Error")
            def exchange_code_for_session(self, *a, **kw): raise Exception("Database Error")
            def table(self, *a, **kw): return self
            def select(self, *a, **kw): return self
            def execute(self, *a, **kw): return type('MockRes', (), {'data': []})()
        supabase = MockSupaFallback()
        is_mock = True
