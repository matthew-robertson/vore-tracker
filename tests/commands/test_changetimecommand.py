import unittest
from unittest.mock import patch, Mock
import discord
import datetime

from commands import ChangeTimeCommand
from serverobjects.server import DiscordServer

class TestChangeTimeCommand(unittest.TestCase):
	def setUp(self):
		self.command = ChangeTimeCommand()
		self.time = datetime.datetime.now()
		self.server_json = {
			'server_id' : 1,
			'awake' : True,
			'timeout_duration_seconds': 1800,
			'banned_words': [{
				'rowid': 1,
				'server_id': 1,
				'banned_word': 'vore',
				'infracted_at': (self.time - datetime.timedelta(minutes=20)).strftime("%Y-%m-%d %H:%M:%S"),
				'calledout_at': (self.time - datetime.timedelta(minutes=20)).strftime("%Y-%m-%d %H:%M:%S")
			}]
		}

	def test_is_command_authorized__no_permissions_disallowed(self):
		result = self.command.is_command_authorized()
		self.assertFalse(result)

	def test_is_command_authorized__non_admin_disallowed(self):
		permissions = discord.Permissions()
		result = self.command.is_command_authorized(permissions)
		self.assertFalse(result)

	def test_is_command_authorized__admin_allowed(self):
		permissions = discord.Permissions.all()
		result = self.command.is_command_authorized(permissions)
		self.assertTrue(result)

	@patch('serverobjects.server.DiscordServer.set_timeout')
	def test_execute__change_full_time_valid(self, time_patch):
		message = Mock(**{
      'server': Mock(**{
        'id': 1
      }),
      'content': "!vtdelay 1:1:1",
      'author': Mock(**{
        'id': 2,
        'mention': "@test",
        'bot': False
      }),
    })
		server = DiscordServer(self.server_json, self.time, None)
		self.command.execute(server, self.time, message.content, message.author)
		time_patch.assert_called_with(1+1*60+1*60*60)
		self.assertTrue(time_patch.called)

	@patch('serverobjects.server.DiscordServer.set_timeout')
	def test_execute__change_second_time_valid(self, time_patch):
		message = Mock(**{
      'server': Mock(**{
        'id': 1
      }),
      'content': "!vtdelay 999",
      'author': Mock(**{
        'id': 2,
        'mention': "@test",
        'bot': False
      }),
    })
		server = DiscordServer(self.server_json, self.time, None)
		self.command.execute(server, self.time, message.content, message.author)
		time_patch.assert_called_with(999)
		self.assertTrue(time_patch.called)

	@patch('serverobjects.server.DiscordServer.set_timeout')
	def test_execute__change_extra_invalid(self, time_patch):
		message = Mock(**{
      'server': Mock(**{
        'id': 1
      }),
      'content': "!vtdelay 1:1:1:1",
      'author': Mock(**{
        'id': 2,
        'mention': "@test",
        'bot': False
      }),
    })
		server = DiscordServer(self.server_json, self.time, None)
		self.command.execute(server, self.time, message.content, message.author)
		self.assertFalse(time_patch.called)

	@patch('serverobjects.server.DiscordServer.set_timeout')
	def test_execute__change_no_time_invalid(self, time_patch):
		message = Mock(**{
      'server': Mock(**{
        'id': 1
      }),
      'content': "!vtdelay",
      'author': Mock(**{
        'id': 2,
        'mention': "@test",
        'bot': False
      }),
    })
		server = DiscordServer(self.server_json, self.time, None)
		self.command.execute(server, self.time, message.content, message.author)
		self.assertFalse(time_patch.called)