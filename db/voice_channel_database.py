import aiosqlite


# Function to set up the database and create the necessary table
async def setup_db(db_path):
    # Connect to the SQLite database
    async with aiosqlite.connect(db_path) as db:
        # Execute SQL command to create a table for storing voice states
        await db.execute('''
            CREATE TABLE IF NOT EXISTS voice_states (
                guild_id INTEGER PRIMARY KEY,
                channel_id INTEGER
            )
        ''')
        # Commit the changes to the database
        await db.commit()


# Function to save the current voice channel state to the database
async def save_state(db_path, guild_id, channel_id):
    # Connect to the database
    async with aiosqlite.connect(db_path) as db:
        # Replace or insert the new state into the database
        await db.execute('REPLACE INTO voice_states (guild_id, channel_id) VALUES (?, ?)', (guild_id, channel_id))
        # Commit the changes
        await db.commit()


# Function to remove a guild's voice channel state from the database
async def remove_state(db_path, guild_id):
    # Connect to the database
    async with aiosqlite.connect(db_path) as db:
        # Delete the state for the specified guild
        await db.execute('DELETE FROM voice_states WHERE guild_id = ?', (guild_id,))
        # Commit the changes
        await db.commit()


# Function to retrieve the initial voice channel states from the database
async def get_initial_channels(db_path, limit=100):
    # List to store the channel information
    channels = []
    # Connect to the database
    async with aiosqlite.connect(db_path) as db:
        # Execute a query to select all voice states
        async with db.execute('SELECT guild_id, channel_id FROM voice_states LIMIT ?', (limit,)) as cursor:
            # Iterate over the results and add them to the channels list
            async for row in cursor:
                channels.append((row[0], row[1]))
    # Return the list of channel states
    return channels
