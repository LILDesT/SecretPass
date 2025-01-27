import os
import random
import string
from cryptography.fernet import Fernet

class Def_generate:
    @staticmethod
    def generate_password(length=12):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        return password

    @staticmethod
    def load_or_create_key(key_file="secret.key"):
        if not os.path.exists(key_file):
            key = Fernet.generate_key()
            with open(key_file, "wb") as file:
                file.write(key)
            print(f"Ключ шифрования создан и сохранён в {key_file}.")
        else:
            print(f"Ключ шифрования загружен из {key_file}.")
        with open(key_file, "rb") as file:
            return file.read()

    @staticmethod
    def encrypt_text(text, key):
        cipher = Fernet(key)
        encrypted_text = cipher.encrypt(text.encode())
        return encrypted_text

    @staticmethod
    def decrypt_text(encrypted_text, key):
        cipher = Fernet(key)
        decrypted_text = cipher.decrypt(encrypted_text).decode()
        return decrypted_text

    @staticmethod
    def save_password(file_name, description, password, key):
        encrypted_password = Def_generate.encrypt_text(password, key)
        with open(file_name, "ab") as file:
            file.write(f"{description}: ".encode() + encrypted_password + b"\n")
        print(f"Пароль для '{description}' сохранён (зашифрован).")

    @staticmethod
    def view_passwords(file_name, key, sort=False):
        if not os.path.exists(file_name):
            print("Файл с паролями пока не создан.")
            return []
        passwords = []
        with open(file_name, "rb") as file:
            for line in file:
                try:
                    description, encrypted_password = line.split(b": ", 1)
                    decrypted_password = Def_generate.decrypt_text(encrypted_password.strip(), key)
                    passwords.append({"description": description.decode(), "password": decrypted_password})
                except Exception as e:
                    print(f"Ошибка при расшифровке строки: {line}. Причина: {e}")
        if sort:
            passwords = sorted(passwords, key=lambda x: x["description"])
        for entry in passwords:
            print(f"{entry['description']}: {entry['password']}")
        return passwords

    @staticmethod
    def delete_password(file_name, description, key):
        if not os.path.exists(file_name):
            print("Файл с паролями пока не создан.")
            return
        updated_lines = []
        password_deleted = False
        with open(file_name, "rb") as file:
            for line in file:
                desc, encrypted_password = line.split(b": ", 1)
                if desc.decode() == description:
                    password_deleted = True
                else:
                    updated_lines.append(line)
        if not password_deleted:
            print(f"Пароль с описанием '{description}' не найден.")
        else:
            with open(file_name, "wb") as file:
                file.writelines(updated_lines)
            print(f"Пароль с описанием '{description}' успешно удалён.")

def main():
    file_name = "passwords.enc"
    key_file = "secret.key"
    key = Def_generate.load_or_create_key(key_file)

    while True:
        print("\nМеню:")
        print("1. Сгенерировать пароль")
        print("2. Добавить существующий пароль")
        print("3. Просмотреть сохранённые пароли")
        print("4. Удалить пароль")
        print("5. Выйти")
        choice = input("Выберите действие: ")

        if choice == "1":
            description = input("Введите описание для пароля: ")
            length = int(input("Введите длину пароля (по умолчанию 12): ") or 12)
            password = Def_generate.generate_password(length)
            print(f"Сгенерированный пароль: {password}")
            Def_generate.save_password(file_name, description, password, key)
        elif choice == "2":
            description = input("Введите описание для пароля: ")
            password = input("Введите существующий пароль: ")
            Def_generate.save_password(file_name, description, password, key)
        elif choice == "3":
            sort = input("Отсортировать по алфавиту? (y/n): ").lower() == "y"
            Def_generate.view_passwords(file_name, key, sort=sort)
        elif choice == "4":
            description = input("Введите описание для пароля, который нужно удалить: ")
            Def_generate.delete_password(file_name, description, key)
        elif choice == "5":
            print("Выход из программы.")
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
