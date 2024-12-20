with open(".env", "w", encoding="utf-8") as f:
    f.write(f"""
    APP_NAME={input("APP_NAME: ")}
    SECRET_KEY={input("SECRET_KEY: ")}
    ALCHEMICAL_DATABASE_URL={input("ALCHEMICAL_DATABASE_URL: ")}
    """)

print("""
Run these:
python -m venv venv
venv\\Scripts\\activate or source venv/bin/activate
pip install -r requirements.txt
flask install
""")
