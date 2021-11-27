import os
import werkzeug
get="ABCD123"
password=werkzeug.security.generate_password_hash(get, method='pbkdf2:sha256', salt_length=16)

password_to_check=input("Пароль:")




print(werkzeug.security.check_password_hash(password, password_to_check))
