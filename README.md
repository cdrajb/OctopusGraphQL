# OctopusGraphQL
IOG_CD.py is code to download Intelligent Octopus Go (IOG) completedDispatches and save to a logfile.  
You'll need to edit it with your Octopus account number and api key, and to select logfile location.
(I think I may have based it on code I found elsewhere, so apologies if you recognise it! Let me know and I'll credit you)

IOG_check_rates.py will check the half-hour periods between specific start and end times, and report whether they are to be charged at peak or off-peak rate.
(Note that it may take a while, sometimes a few days, before the rates are updated to reflect IOG dispatches)

octo_account.py uses the Octopus API (not GraphQL) to report your account details

For octo_account.py and IOG_check_rates.py - create a subfolder called include, and in that subfolder create a file called creds.py, with definitions as follows:

apikey="sk_live_...." # Your Octopus API Key
accountNumber="A-A....." # Your Octopus Account Number
propertyId='nnnnnn'	# Your property id (if you don't know this, run octo_account.py to find it)
