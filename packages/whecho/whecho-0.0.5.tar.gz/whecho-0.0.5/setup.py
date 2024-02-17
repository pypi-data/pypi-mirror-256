# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['whecho']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1', 'setuptools>=40.6.3', 'toml>=0.6.0']

entry_points = \
{'console_scripts': ['whecho = whecho:whecho.main']}

setup_kwargs = {
    'name': 'whecho',
    'version': '0.0.5',
    'description': 'Linux echo with webhooks! ⚓',
    'long_description': '# whecho\nlinux echo but with webhooks! ⚓\n\nDon\'t guess when a job is finished! Have it message you!\n\n## requirements\n- python 3.6+\n\n## installation\n```\npip install whecho\n```\n\n## First Time Setup\n- obtain a webhook URL\n![discord_webhook_example](https://i.imgur.com/f9XnAew.png)\n- Currently supports:\n  - [discord](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)\n  - [slack](https://api.slack.com/messaging/webhooks)\n  - [webex](https://apphub.webex.com/applications/incoming-webhooks-cisco-systems-38054-23307-75252) (with markdown)\n- Initialize the `default_url`\n```\n$ whecho --init\nCurrent config:\n[1] default_url: None\n[2] user: craut\n[3] machine: craut-spectre\n\nPlease enter the number/name of the config option you would like to modify (empty or Q to exit): 1\nPlease enter the new value for default_url: <WEBHOOK_URL>\nSuccessfully modified default_url to <WEBHOOK_URL>!\nCurrent config:\n[1] default_url: <WEBHOOK_URL>\n[2] user: craut\n[3] machine: craut-spectre\n\nPlease enter the number/name of the config option you would like to modify (empty or Q to exit): q\nSuccessfully initialized whecho!\n```\n\n## general usage (from shell/console)\n```\n$ whecho "hello there"\n```\n![hello_there_discord](https://github.com/cvraut/whecho/blob/main/imgs/hello_there_discord.png?raw=true)\n\n## usage from python\n```\nfrom whecho.whecho import whecho_simple\nwhecho_simple("I\'m inside python 🐍")\n```\n![inside_python](https://github.com/cvraut/whecho/blob/main/imgs/inside_python.png?raw=true)\n\n## advanced usage\n```\n$ whecho --help\nusage: whecho [-h] [--version] [-m MSG] [--init] [-u URL] [-d] [MSG [MSG ...]]\n\nLinux echo with webhooks! ⚓\n\npositional arguments:\n  MSG                The message to echo.\n\noptional arguments:\n  -h, --help         show this help message and exit\n  --version          Prints the version of whecho and exits.\n  -m MSG, --msg MSG  The message to echo (same as 1st positional argument).\n  --init             Initializes whecho. Also used to change current config.\n  -u URL, --url URL  The webhook URL to send the message to.\n  -d, --debug        Whether to print debugging information.\n```',
    'author': 'Chinmay Raut',
    'author_email': None,
    'url': 'https://github.com/cvraut/whecho',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
