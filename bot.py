#!/usr/bin/env python3

# Copyright 2020 io mintz <io@mintz.cc>
# Copyright 2020 Vex

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

import discord
from bot_bin.bot import Bot

class Bot(Bot):
	startup_extensions = [
		'bot_bin.stats',
		'cogs.gamerwords',
		'jishaku',
	]
	def __init__(self, *args, **kwargs):
		super().__init__(
			intents=discord.Intents(
				# avatar/nickname caching
				members=True,
				guilds=True,
				webhooks=True,
				messages=True,
				# needed for jishaku pagination
				reactions=True,
			),
			*args,
			**kwargs,
		)

def main():
	import toml
	with open('config.toml') as f:
		bot = Bot(config=toml.load(f))
	bot.run()

if __name__ == '__main__':
	main()
