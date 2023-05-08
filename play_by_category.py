from redbot.core import commands
import random
import os

path_cog = "C:/Users/nonadmin-main/Documents/MyCogs/play_by_category/"
path_cats = path_cog + "tracks/"
path_hist = path_cog + "history/"


def add_to_history(cat, track):
    path_file = path_hist + cat + ".txt"

    # append track fo history
    with open(path_file, "a") as file:
        file.write(track + "\n")

    # get num of file lines
    with open(path_file, "r+") as file:
        len_file = len(file.readlines())

    # get num of tracks in category
    len_cat = len([t.name for t in os.scandir(path_cats + cat)])

    # if all available tracks recorded, reset history
    if len_cat <= len_file:
        with open(path_file, 'w'):
            pass


def track_in_history(cat, track):
    path_file = path_hist + cat + ".txt"

    # create file if it doesn't exist
    if not os.path.isfile(path_file):
        with open(path_file, 'w'):
            pass

    with open(path_file, "r") as file:
        return track + "\n" in file.readlines()


def get_track(cat):
    cat_tracks = [t.name for t in os.scandir(path_cats + cat)]
    while True:
        random.shuffle(cat_tracks)
        track = cat_tracks.pop()

        if not track_in_history(cat, track):
            break

    add_to_history(cat, track)

    return track


class PlayByCategory(commands.Cog):
    """cat as in category"""

    # TODO: get prefix from redbot code

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        await ctx.send("h")

    @commands.command()
    async def playcat(self, ctx, cat):
        """play any track fromm user selected category"""

        # if folder doesn't exist
        if not os.path.isdir(path_cats + cat):
            await ctx.send("Category not found")
            return

        # if folder doesn't have files
        if not any(os.scandir(path_cats + cat)):
            await ctx.send("Category has no tracks")
            return

        # get (recently unplayed) random track in category
        track = get_track(cat)

        # otherwise, track will wait in queue,
        # and previous track shouldn't be in queue anymore
        await ctx.invoke(self.bot.get_command("stop"))

        # play track
        await ctx.invoke(self.bot.get_command("play"),
                         query=os.path.join(path_cats, cat, track))

    @commands.command()
    async def helpcat(self, ctx):
        """lets user know what they can do"""
        await ctx.send("?playcat <category>"
                       "?printcat - print available categories")

    @commands.command()
    async def printcat(self, ctx):
        """Get and print all category names in cog working directory.
        Folder names are category names."""

        # get folder names (excluding empty folders)
        cats = [c.name for c in os.scandir(path_cats)
                if any(os.scandir(path_cats + c.name))]

        # if list, join items to str
        if not isinstance(cats, str):
            cats = ", ".join(cats)

        await ctx.send("Available categories:  " + cats)
