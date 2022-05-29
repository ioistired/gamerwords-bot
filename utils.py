# Copyright 2020 io mintz <io@mintz.cc>

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

import asyncio

async def gather_or_cancel(*awaitables):
    """run the awaitables in the sequence concurrently. If any of them raise an exception,
    propagate the first exception raised and cancel all other awaitables.
    """
    gather_task = asyncio.gather(*awaitables)
    try:
        return await gather_task
    except asyncio.CancelledError:
        raise
    except:
        gather_task.cancel()
        raise
