# Embedded file name: lib.coginvasion.distributed.CogInvasionErrorCodes
"""

  Filename: CogInvasionErrorCodes.py
  Created by: blach (25Jan15)

"""
EC_MULTIPLE_LOGINS = 110
EC_BAD_TOKEN = 111
EC_INVALID_ACCOUNT = 112
EC_NON_EXISTENT_AV = 113
EC_OCCUPIED_SLOT_CREATION_ATTEMPT = 114
UnknownErrorMsg = 'An unexpected problem has occured. (Error code %s) Your connection has been lost, but you should be able to connect again and go right back into the game.'
ErrorCode2ErrorMsg = {EC_MULTIPLE_LOGINS: 'You have been disconnected because someone has logged into your account on another computer.',
 EC_BAD_TOKEN: 'You have been disconnected because your login token is invalid.',
 EC_INVALID_ACCOUNT: 'You have been disconnected because your account is invalid.',
 EC_NON_EXISTENT_AV: 'You have been disconnected because you tried to do something to a non-existent Toon.',
 EC_OCCUPIED_SLOT_CREATION_ATTEMPT: 'You have been disconnected because you tried to create a Toon on an occupied slot.'}