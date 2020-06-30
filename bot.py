#!/usr/bin/env python3

from bot_bin.bot import Bot

class Bot(Bot):
	startup_extensions = [
		'bot_bin.stats',
		'cogs.gamerwords',
		'jishaku',
	]

def main():
	import toml
	with open('config.toml') as f:
		bot = Bot(config=toml.load(f))
	bot.run()

if __name__ == '__main__':
	main()
