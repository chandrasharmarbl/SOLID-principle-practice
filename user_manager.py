class UserManager:
    def __init__(self):
        self.users = []

    def add_user(self, name, email, user_type):
        if "@" not in email:
            print("Invalid email")
            return
        
        user = {"name": name, "email": email, "type": user_type}
        self.users.append(user)

        if user_type == "admin":
            print("Admin user added")
        elif user_type == "guest":
            print("Guest user added")

        f = open("users.txt", "a")
        f.write(name + "," + email + "," + user_type + "\n")
        f.close()

    def get_users(self):
        return self.users
    
if __name__ == "__main__":
    manager = UserManager()
    manager.add_user("Alice", "alice@example.com", "admin")
    manager.add_user("Bob", "bob@example.com", "guest")
    print(manager.get_users())