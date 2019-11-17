from commands.command import Command
from utils.time import parse_time, format_seconds

class ChangeTimeCommand(Command):
	def is_command_authorized(self, permissions=None):
		return permissions and permissions.administrator

	def execute(self, current_server, current_time, message, author):
		parsed_time = parse_time(message[8:])

		if parsed_time >= 0:
			current_server.set_timeout(parsed_time)
			formatted_time = format_seconds(parsed_time)
			return "Cool, from now on I'll wait at least {} between alerts.".format(formatted_time)
		else:
			return "Sorry, I don't understand that formatting. I was expecting something like '!vtct hh:mm:ss'"