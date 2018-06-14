import Client
import DiscordEvents

client = Client.Client()

#Add commands & events here.
DiscordEvents.DiscordEvents(client.bot)
DiscordEvents.Config(client.bot)

client.RunBot()