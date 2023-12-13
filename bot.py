import discord
import mysql.connector
from datetime import datetime

# MySQL database connection details
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
}


# Function to create the database and table
def create_database_and_table():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS discord")
        cursor.execute("USE discord")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                guild_id BIGINT,
                server_name VARCHAR(255),
                user_name VARCHAR(255),
                message TEXT,
                datetime DATETIME
            )
        """)

        print("Database and table created successfully!")

    except Exception as e:
        print(f"Error creating database and table: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# Function to insert log into the 'logs' table
def log_message(guild_id, server_name, user_name, message):
    try:
        connection = mysql.connector.connect(**db_config, database='discord')
        cursor = connection.cursor()

        # Insert log into 'logs' table
        query = "INSERT INTO logs (guild_id, server_name, user_name, message, datetime) VALUES (%s, %s, %s, %s, %s)"
        data = (guild_id, server_name, user_name, message, datetime.now())
        cursor.execute(query, data)

        connection.commit()

    except Exception as e:
        print(f"Error saving log entry: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def handle_response(message) -> str:
    p_message = message.lower()

    if p_message == '!hello' or '?hello':
        return 'Hello World!'


async def send_message(message, user_message, is_private):
    try:
        response = handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


async def on_message(message):
    if message.author == client.user:
        return

    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    guild_id = message.guild.id
    server_name = message.guild.name
    print(f"Hello World {server_name}.")
    log_message(guild_id, server_name, username, f"{username} said: {user_message} ({channel})")

    if user_message.startswith("?"):
        user_message = user_message[1:]
        await send_message(message, user_message, is_private=True)
    else:
        await send_message(message, user_message, is_private=False)

TOKEN = "(Add Your Bot Token Here)"

intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True

client = discord.Client(intents=intents)
client.event(on_message)


@client.event
async def on_ready():
    print(f'{client.user} is now running.')


create_database_and_table()
client.run(TOKEN)
