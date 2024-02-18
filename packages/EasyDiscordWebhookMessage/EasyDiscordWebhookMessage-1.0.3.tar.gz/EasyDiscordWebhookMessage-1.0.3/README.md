# Easy Discord Webhook Message

A Python package for easily sending messages through Discord webhooks.

## Installation

Install the package using pip:

```bash
pip install easy_discord_webhook_message
```

## Usage

```python
from easy_discord_webhook_message import Webhook

# Create an instance of the Webhook class
webhook_instance = Webhook()

# Define the webhook URL
webhook_instance.define_webhook_url("your_discord_webhook_url")

# Define mentions (optional)
webhook_instance.define_mentions(["userId1", "userId2"])

# Define content (optional)
webhook_instance.define_content("Hello @user1, check this out!")

# Send a message
webhook_instance.send(
    title="New Release",
    description="Version 1.0 is now available!",
    author="Your Bot",
    color="00FF00",
    url="https://github.com/yourusername/yourrepository/releases/tag/v1.0"
)
```