import Client
import Events

client = Client.Client()

#Add commands & events here.
Events.Events(client.bot)
Events.Config(client.bot)
Events.Commands(client.bot)

client.RunBot()