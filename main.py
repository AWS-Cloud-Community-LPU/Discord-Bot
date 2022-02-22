"""
MIT License
Copyright (c) 2022 AWS Cloud Community LPU
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


import configparser
import discord
import functions as F


log_message = f"Bot Started at {F.get_time()}\n"
print(log_message)
F.print_logs(log_message)


# Discord authentication
client = discord.Client()
config = configparser.ConfigParser()
config.read("secrets.ini")


@client.event
async def on_message(message):
    """
    Function Invoked when a message is sent on Discord Server.
    """
    if message.author == client.user:
        return

    if message.content.startswith("$events"):
        log_text = f"User: {message.author}\n"
        log_text = log_text + f"Time: {F.get_time()}\n"
        log_text = log_text + "Command: $events\n"
        F.print_logs(log_text)
        await message.channel.send(F.get_events())


client.run(config["KEYS"]["API_KEY"])
