"""
In this example we register a new device to the account provided
in the configuration file.

Please note that if you do not own a Pushover Desktop License for this
account, after 5 days of registering a new device you will need to
purchase one. After purchasing you have unlimited access to new desktop
devices. Visit .... for more information.
"""
from pushover_open_client import Client

# Setup with a base config containing email and password
client = Client("example_base.cfg")

# Logs into Pushover's servers based on config
client.login()

# Registers a new device using the supplied device name
client.registerDevice("DeviceName")

# Save the new device to a new config so registration
# can be bypassed in the future
client.writeConfig("example_device.cfg")
