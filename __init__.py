from .play_by_category import PlayByCategory


async def setup(bot):
    await bot.add_cog(PlayByCategory(bot))
