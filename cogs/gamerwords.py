# Copyright 2020 io mintz <io@mintz.cc>, StarrFox, Vex

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software
# is furnished to do so, subject to the following conditions:

# The above copyright notice, penisbird and this permission notice shall be included
# in all copies or substantial portions of the Software unmodified.

#                     _..._
#                  .-'     '-.
#                 /     _    _\
#                /':.  (o)  /__)
#               /':. .,_    |  |
#              |': ; /  \   /_/
#              /  ;  `"`"    }
#             ; ':.,         {
#            /      ;        }
#           ; '::.   ;\/\ /\ {
#          |.      ':. ;``"``\
#         / '::'::'    /      ;
#        |':::' '::'  /       |
#        \   '::' _.-`;       ;
#        /`-..--;` ;  |       |
#       ;  ;  ;  ;  ; |       |
#       ; ;  ;  ; ;  ;        /        ,--.........,
#       |; ;  ;  ;  ;/       ;       .'           -='.
#       | ;  ;  ; ; /       /       .\               '
#       |  ;   ;  /`      .\   _,=="  \             .'
#       \;  ; ; .'. _  ,_'\.\~"   //`. \          .'
#       |  ;  .___~' \ \- | |    /,\ `  \      ..'
#     ~ ; ; ;/  =="'' |`| | |       =="''\.==''
#     ~ /; ;/=""      |`| |`|   ==="`
#     ~..==`     \\   |`| / /=="`
#      ~` ~      /,\ / /= )")
#     ~ ~~         _')")
#     ~ ~   _,=~";`
#     ~  =~"|;  ;|       Penisbird
#      ~  ~ | ;  |       =========
#   ~ ~     |;|\ |
#           |/  \|

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR
# THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import random
import collections
import re
import asyncio
from string import ascii_letters

import discord
from discord.ext import commands
import unidecode

from utils import gather_or_cancel

GAMER_REGEX = r'(b+\s*r+\s*u+\s*h+)'

with open('data/catchphrases.txt') as f:
	CATCHPHRASES = list(map(str.rstrip, f))

class GamerReplacer:
	GAMER_WORD_PARTS = frozenset('ruh')

	def __init__(self, text):
		self.start_index = -1
		self.letter_check = [False] * 4
		self.match_length = 0
		self.spaces = 0
		self.closed = False
		self.text = text

	def reset(self):
		self.start_index = -1
		self.letter_check = [False] * 4
		self.match_length = 0
		self.spaces = 0

	def replace(self):
		if self.closed:
			raise RuntimeError('This replacer is closed')

		matches = []
		total_length = len(self.text)

		for index, char in enumerate(self.text):
			is_last_char = index + 1 == total_length
			decoded = unidecode.unidecode(char)

			# b is an end check
			if decoded.lower() in self.GAMER_WORD_PARTS:
				self.spaces = 0

			if decoded.lower() == 'b':
				if self.start_index == -1:
					self.start_index = index

				if self.start_index != -1 and sum(self.letter_check) == 4:
					if self.spaces:
						self.match_length -= self.spaces

					matches.append(self.text[self.start_index:self.start_index + self.match_length])
					self.match_length = len(char)
					self.letter_check = [True, False, False, False]
					self.start_index = index
					self.spaces = 0

				else:
					self.match_length += len(char)
					self.letter_check[0] = True
					self.spaces = 0

			elif decoded.lower() == 'r':
				self.match_length += len(char)
				self.letter_check[1] = True

			elif decoded.lower() == 'u':
				self.match_length += len(char)
				self.letter_check[2] = True

			elif decoded.lower() == 'h':
				self.match_length += len(char)
				self.letter_check[3] = True

			else:
				if self.start_index != -1 and sum(self.letter_check) == 4:
					if self.spaces:
						self.match_length -= self.spaces

					matches.append(self.text[self.start_index:self.start_index + self.match_length])
					self.reset()

				else:
					if decoded in ascii_letters:
						self.reset()

					else:
						if char.isspace():
							self.spaces += 1
						else:
							self.spaces = 0

						if self.start_index != -1:
							self.match_length += len(char)

			if self.start_index != -1 and sum(self.letter_check) == 4 and is_last_char:
				matches.append(self.text[self.start_index:self.start_index + self.match_length])

		match_indexes = []
		unsearched = self.text
		used = 0
		for match in sorted(matches, key=lambda l: len(l), reverse=True):
			start_pos = unsearched.find(match)
			end_pos = start_pos + len(match) - 1
			start = start_pos + used
			end = end_pos + used
			match_indexes.append((start, end))
			used += len(unsearched[:end_pos + 1])
			unsearched = unsearched[end_pos + 1:]

		seperated = [*self.text]
		offset = 0
		for start, end in match_indexes:
			start += offset
			end += offset

			replacement = random.choice(CATCHPHRASES)
			seperated[start:end + 1] = replacement

			replaced_len = len(replacement)
			offset += replaced_len - 4

		self.closed = True

		return ''.join(seperated)


class GamerWords(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.webhook_cache = collections.defaultdict(lambda: collections.defaultdict(list))
		# {guild:{channel:[webhook]}}
		bot.loop.create_task(self.populate_webhook_cache())
		bot.loop.create_task(self.clear_usernames())

	def has_gamer_words(self, string):
		string = unidecode.unidecode(string)
		match = re.search(GAMER_REGEX, string, flags=re.IGNORECASE)
		return match

	async def populate_webhook_cache(self):
		await self.bot.wait_until_ready()
		for guild in self.bot.guilds:
			for channel in guild.text_channels:
				try:
					webhooks = await channel.webhooks()
				except discord.HTTPException:
					continue

				for webhook in await channel.webhooks():
					if webhook.user == guild.me:
						self.webhook_cache[guild][webhook.channel].append(webhook)

	@commands.Cog.listener()
	async def on_webhooks_update(self, channel):
		webhooks = await channel.webhooks()
		webhooks = [webhook for webhook in webhooks if webhook.user == channel.guild.me]
		self.webhook_cache[channel.guild][channel] = webhooks

	async def get_webhook(self, channel):
		try:
			webhook = self.webhook_cache[channel.guild][channel][0]
			return webhook
		except (KeyError, IndexError):
			try:
				webhook = await channel.create_webhook(name='GamerHook')
				return webhook
			except discord.HTTPException:
				return None

	@commands.Cog.listener()
	async def on_message(self, message):
		if self.skip_if(message):
			return
		await self.handle_new_gamer_message(message)

	@commands.Cog.listener()
	async def on_message_edit(self, old_message, new_message):
		if self.skip_if(old_message):
			return
		await self.handle_new_gamer_message(new_message)

	@staticmethod
	def skip_if(message):
		return message.author.bot or not message.guild

	async def handle_new_gamer_message(self, message):
		text_match = self.has_gamer_words(message.content)
		file_match = any(self.has_gamer_words(attachment.filename) for attachment in message.attachments)
		if text_match or file_match:
			for attach in message.attachments:
				if attach.size >= getattr(message.guild, 'filesize_limit', 8 * 1024 ** 2):
					await message.delete(delay=0.2)
					return

			async def dl_attach(attach):
				file = await attach.to_file()
				if self.has_gamer_words(file.filename):
					file.filename = GamerReplacer(file.filename).replace()

				return file

			# download all attachments in parallel
			files = await gather_or_cancel(*map(dl_attach, message.attachments))

			try:
				# can't use delete(delay=) because we need to return on exceptions
				await asyncio.sleep(0.2)
				await message.delete()
			except discord.HTTPException:
				return

			if not message.channel.permissions_for(message.guild.me).manage_webhooks:
				return

			webhook = await self.get_webhook(message.channel)
			if not webhook:
				return

			author = message.author

			if message.channel.permissions_for(author).mention_everyone:
				allowed_mentions = discord.AllowedMentions(everyone=True, roles=True)
			else:
				allowed_mentions = discord.AllowedMentions(everyone=False, roles=False)

			await webhook.send(
				content=GamerReplacer(message.content).replace(),
				username=author.display_name,
				avatar_url=str(author.avatar_url),
				files=files,
				allowed_mentions=allowed_mentions
			)

	async def clear_usernames(self):
		await self.bot.wait_until_ready()
		for guild in self.bot.guilds:
			if not guild.me.guild_permissions.manage_nicknames:
				continue

			for member in guild.members:
				if member.top_role > guild.me.top_role:
					continue

				match = self.has_gamer_words(member.display_name)
				if match:
					new_content = GamerReplacer(member.display_name).replace()
					try:
						await member.edit(nick=new_content)
					except discord.Forbidden:
						# while iterating, we were denied Manage Nicknames
						continue

	@commands.Cog.listener()
	async def on_member_update(self, old_member, new_member):
		if old_member.display_name == new_member.display_name:
			return
		if old_member.top_role > old_member.guild.me.top_role:
			return
		guild = old_member.guild
		if not guild.me.guild_permissions.manage_nicknames:
			return

		match = self.has_gamer_words(new_member.display_name)
		if match:
			new_content = GamerReplacer(new_member.display_name).replace()
			await new_member.edit(nick=new_content)

def setup(bot):
	bot.add_cog(GamerWords(bot))
