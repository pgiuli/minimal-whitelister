#Purpose: Handle the database of users and uses the pterodactyl API to whitelist or remove players from the server.
#Does this make unnecessary calls to the database? Yes. Do I care? No.


import sqlite3
import os
import pterodactyl

#Create a database if it doesn't exist
def create_database():
    if not os.path.exists('database.db'):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE users (discord_id text, minecraft_username text)''')
        conn.commit()
        conn.close()
        print("Created database")

def clear_database():
    if os.path.exists('database.db'):
        os.remove('database.db')
        print("Deleted database")
    create_database()
#Add a user to the database
def add_user(discord_id, minecraft_username):
    #Check if the user already exists, if so, replace their minecraft username
    if user_exists(discord_id):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("UPDATE users SET minecraft_username=? WHERE discord_id=?", (minecraft_username, discord_id))
        conn.commit()
        conn.close()
        print(f"Updated user {discord_id} with minecraft username to {minecraft_username}")
    #Otherwise, add them to the database
    else:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES (?, ?)", (discord_id, minecraft_username))
        conn.commit()
        conn.close()
        print(f"Added user {discord_id} with minecraft username {minecraft_username}")

#Remove a user from the database
def remove_user(discord_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE discord_id=?", (discord_id,))
    conn.commit()
    conn.close()

#Get a user's minecraft username from their discord ID
def get_minecraft_username(discord_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT minecraft_username FROM users WHERE discord_id=?", (discord_id,))
    result = c.fetchone()
    conn.close()
    return result[0]

#Get a user's discord ID from their minecraft username
def get_discord_id(minecraft_username):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT discord_id FROM users WHERE minecraft_username=?", (minecraft_username,))
    result = c.fetchone()
    conn.close()
    if result == None:
        return None
    return result[0]

#Check if a user is in the database
def user_exists(discord_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE discord_id=?", (discord_id,))
    result = c.fetchone()
    conn.close()
    return result != None



#Flow: Check if username is in database, if it is, check if it belongs to the discord user. If it does, add it to the whitelist. If it doesn't, return an error. If it isn't in the database, add it to the database and whitelist it.
def whitelist(discord_id, minecraft_username):
    print(f"discord_id: {discord_id}, minecraft_username: {minecraft_username}")
    #Is there a user with this minecraft username?
    if get_discord_id(minecraft_username) != None:
        #If another player is already whitelisted with that username, quit
        #Get the user's discord ID
        username_owner_id = get_discord_id(minecraft_username)
        print(f"username_owner_id: {username_owner_id}")
        if str(username_owner_id) != str(discord_id):
            return "Username already in use by another player!"
    #Is there a user with this discord ID?
    if user_exists(discord_id):
        #Get the user's minecraft username
        old_username = get_minecraft_username(discord_id)
        print(f"old_username: {old_username}")
        #If the user's minecraft username is different, remove the old one from the whitelist
        if str(old_username) != str(minecraft_username):
            print("ITS DIFERENT")
            remove_user(discord_id)
            add_user(discord_id, minecraft_username)
            pterodactyl.remove_whitelist(old_username)
            print(f"Removed {old_username} from the whitelist")
        #Add the new minecraft username to the whitelist
        pterodactyl.add_whitelist(minecraft_username)
        print(f"Added {minecraft_username} to the whitelist")
        return f"Removed {old_username} from the whitelist and added {minecraft_username} to the whitelist."
    else:
        #If the user isn't in the database and no other user is using that username, add them to the database and whitelist them
        add_user(discord_id, minecraft_username)
        pterodactyl.add_whitelist(minecraft_username)
        print(f"Added {minecraft_username} to the whitelist")
        return f"Added {minecraft_username} to the whitelist."

def unwhitelist(discord_id):
    #Is there a user with this discord ID?
    if user_exists(discord_id):
        #Get the user's minecraft username
        minecraft_username = get_minecraft_username(discord_id)
        #Remove the user from the database
        remove_user(discord_id)
        #Remove the user from the whitelist
        pterodactyl.remove_whitelist(minecraft_username)
        print(f"Removed {minecraft_username} from the whitelist")
        return f"Removed {minecraft_username} from the whitelist"
    else:
        return "You are not whitelisted! use /whitelist <minecraft username> to whitelist yourself."


create_database()