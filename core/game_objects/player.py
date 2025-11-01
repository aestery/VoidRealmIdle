

class Player:
    def __init__(self, pool):
        self.pool = pool
        
    async def get(self, user_id):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow("SELECT * FROM player WHERE player_id=$1", user_id)

    async def create(self, user_id, initial_lvl=1, strength=1, player_xp=0):
        async with self.pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO player (player_id, playerlvl, playerstrength, player_xp) VALUES ($1, $2, $3, $4) "
                "ON CONFLICT (player_id) DO NOTHING;",
                user_id, initial_lvl, strength, player_xp
            )

    async def update_hp(self, user_id, hp):
        async with self.pool.acquire() as conn:
            await conn.execute(
                "UPDATE player SET hp=$1 WHERE player_id=$2", hp, user_id
            )

    async def add_xp(self, user_id, xp):
        async with self.pool.acquire() as conn:
            await conn.execute(
                "UPDATE player SET player_xp = player_xp + $1 WHERE player_id=$2",
                xp, user_id
            )