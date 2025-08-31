from enum import Enum
import json
import re
from datetime import datetime

class Role(str, Enum):
    ADMIN = "ADMIN"
    EDITOR = "EDITOR"
    VIEWER = "VIEWER"

class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.name
        return super().default(obj)
    
user = {
    "oliver1234": {
        "password" : "1234",
        "name" : "Oliver",
        "bday" : "19970101",
        "role": Role.ADMIN
    },

    "bill1234" : {
        "password" : "qwer",
        "name" : "Bill",
        "bday" : "19990101",
        "role" : Role.EDITOR
    },
    
    "alice1234": {
        "password" : "asdf",
        "name" : "Alice",
        "bday" : "20000101",
        "role": Role.VIEWER
    }
}

def is_valid_password(password):
    """비밀번호 유효성 검사 함수"""
    return len(password) >= 5 and re.search(r"[!@#$%^&*()_+\-=\[\]{}|;:',./<>?`~]", password)

def is_valid_bday(bday):
    """생년월일 유효성 검사 함수"""
    if len(bday) != 8 or not bday.isdigit():
        return False, "Invalid format. Please enter 8 digits (YYYYMMDD)."
    try:
        birth_date = datetime.strptime(bday, '%Y%m%d')
        if birth_date > datetime.now():
            return False, "You cannot enter a future date of birth. Please try again."
        return True, ""
    except ValueError:
        return False, "The date of birth is not valid. Please try again."

def get_role_input():
    """역할 입력 함수"""
    while True:
        role_input = input("Please type your role ex) ADMIN, EDITOR, VIEWER: ").upper()
        if role_input in ["ADMIN", "EDITOR", "VIEWER"]:
            return getattr(Role, role_input)
        print("Role Value is wrong. Please enter ADMIN, EDITOR, or VIEWER.")

def print_all_users():
    """전체 사용자 목록을 보기 좋게 출력하는 함수"""
    print("\n" + "="*20)
    print(" Current User List ".center(20))
    print("="*20)
    print(json.dumps(user, indent=2, cls=EnumEncoder))
    print("="*20 + "\n")

# 초기 사용자 목록 출력
print_all_users()

while True:
    print("*"*20)
    print("1.Login, 2. Signing up, 3. Exit")
    print("*"*20)
    opt1 = input("Choose an option: ")
    
    if opt1 == "1":
        user_exist_id = input("Please type your ID: ")
        user_exist_ps = input("Please type your password: ")
        
        if user_exist_id in user and user[user_exist_id]["password"] == user_exist_ps:
            current_user_role = user[user_exist_id]["role"]
            print(f"Welcome back, {user[user_exist_id]['name']}! Your role is {current_user_role}.")
            
            while True:
                print("\n1. Edit My Info, 2. Delete Account, 3. Back")
                if current_user_role in [Role.ADMIN, Role.EDITOR]:
                    print("4. Edit Other User's Info")

                opt2 = input("Choose an option: ")

                if opt2 == "1":
                    target_id = user_exist_id
                    print(f"Editing info for user: {target_id}")

                    # 비밀번호 수정
                    new_password = input("Enter new password (press Enter to skip): ")
                    if new_password and is_valid_password(new_password):
                        user[target_id]["password"] = new_password
                        print("Password has been updated.")
                        print_all_users() # 사용자 목록 출력

                    # 이름 수정
                    new_name = input("Enter new name (press Enter to skip): ")
                    if new_name:
                        user[target_id]["name"] = new_name
                        print("Name has been updated.")
                        print_all_users() # 사용자 목록 출력
                    
                    # 생년월일 수정
                    new_bday_input = input("Enter new date of birth (press Enter to skip): ")
                    if new_bday_input:
                        valid, message = is_valid_bday(new_bday_input)
                        if valid:
                            user[target_id]["bday"] = new_bday_input
                            print("Date of birth has been updated.")
                            print_all_users() # 사용자 목록 출력
                        else:
                            print(f"Invalid date of birth: {message}")
                
                elif opt2 == "2":
                    # 계정 삭제 기능
                    if current_user_role == Role.ADMIN:
                        print("1. Delete My Account, 2. Delete Other Account")
                        delete_choice = input("Choose an option: ")
                        if delete_choice == "1":
                            confirm = input("Are you sure you want to delete your account? (yes/no): ").lower()
                            if confirm == "yes":
                                del user[user_exist_id]
                                print("Your account has been deleted.")
                                print_all_users() # 사용자 목록 출력
                                break
                            else:
                                print("Account deletion cancelled.")
                        elif delete_choice == "2":
                            target_id = input("Enter the ID of the user to delete: ")
                            if target_id not in user:
                                print("User not found.")
                            elif target_id == user_exist_id:
                                print("You cannot delete your own account with this option. Use '1' instead.")
                            else:
                                confirm = input(f"Are you sure you want to delete {target_id}'s account? (yes/no): ").lower()
                                if confirm == "yes":
                                    del user[target_id]
                                    print(f"Account for {target_id} has been deleted.")
                                    print_all_users() # 사용자 목록 출력
                                else:
                                    print("Account deletion cancelled.")
                        else:
                            print("Invalid option.")
                    else:
                        confirm = input("Are you sure you want to delete your account? (yes/no): ").lower()
                        if confirm == "yes":
                            del user[user_exist_id]
                            print("Your account has been deleted.")
                            print_all_users() # 사용자 목록 출력
                            break
                        else:
                            print("Account deletion cancelled.")
                        
                elif opt2 == "3":
                    break
                    
                elif opt2 == "4" and current_user_role in [Role.ADMIN, Role.EDITOR]:
                    # 다른 사용자 정보 수정 기능 (ADMIN, EDITOR 전용)
                    target_id = input("Enter the ID of the user you want to edit: ")
                    
                    if target_id not in user:
                        print("User not found.")
                        continue
                    
                    print(f"Editing info for user: {target_id}")
                    print(f"Current user info: {json.dumps(user[target_id], indent=2, cls=EnumEncoder)}")

                    while True:
                        print("\n1. Change Password, 2. Change Name, 3. Change Birthday, 4. Change Role, 5. Back")
                        edit_opt = input("Choose an option to edit: ")

                        if edit_opt == "1":
                            new_password = input("Enter new password: ")
                            if is_valid_password(new_password):
                                user[target_id]["password"] = new_password
                                print("Password has been updated.")
                                print_all_users() # 사용자 목록 출력
                            else:
                                print("Invalid new password. Password not updated.")
                        
                        elif edit_opt == "2":
                            new_name = input("Enter new name: ")
                            user[target_id]["name"] = new_name
                            print("Name has been updated.")
                            print_all_users() # 사용자 목록 출력
                            
                        elif edit_opt == "3":
                            while True:
                                new_bday_input = input("Enter new date of birth (ex: 19970616): ")
                                valid, message = is_valid_bday(new_bday_input)
                                if valid:
                                    user[target_id]["bday"] = new_bday_input
                                    print("Date of birth has been updated.")
                                    print_all_users() # 사용자 목록 출력
                                    break
                                print(message)
                        
                        elif edit_opt == "4":
                            if current_user_role == Role.EDITOR:
                                print("You don't have permission to change a user's role.")
                            else: # ADMIN
                                new_role = get_role_input()
                                user[target_id]["role"] = new_role
                                print(f"Role has been updated to {new_role}.")
                                print_all_users() # 사용자 목록 출력
                        
                        elif edit_opt == "5":
                            break
                        
                        else:
                            print("Invalid option.")

                else:
                    print("Invalid option.")
        else:
            print("Invalid ID or password.")

    elif opt1 == "2":
        # 회원가입 기능
        print("*"*20)
        print("Processing Sign Up")
        print("*"*20)
        new_user_id = input("Please type your ID: ")

        if new_user_id in user:
            print("The ID already exists. Please try another ID.")
            continue
        
        print("Password needs to be over 5 letters and include one special character.")
        while True:
            new_user_password = input("Please type your password: ")
            if is_valid_password(new_user_password):
                break
            print("Invalid password. Please follow the password rules.")

        new_user_name = input("Please type your name: ")
        
        while True:
            new_user_bday_input = input("Please type your date of birth (ex: 19970616): ")
            valid, message = is_valid_bday(new_user_bday_input)
            if valid:
                new_user_bday = new_user_bday_input
                break
            print(message)
        
        new_user_role = get_role_input()
        
        user[new_user_id] = {
            "password": new_user_password,
            "name": new_user_name,
            "bday": new_user_bday,
            "role": new_user_role
        }
        print(f"Welcome {user[new_user_id]['name']}! You have successfully signed up.")
        print_all_users() # 사용자 목록 출력

    elif opt1 == "3":
        print("Exiting the program.")
        break
    
    else:
        print("Invalid option. Please choose 1, 2, or 3.")
