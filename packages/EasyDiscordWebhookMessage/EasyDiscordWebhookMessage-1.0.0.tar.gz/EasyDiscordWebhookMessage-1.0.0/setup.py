from setuptools import setup, find_packages

setup(
    name='EasyDiscordWebhookMessage',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        "discord-webhook"
    ],
    author='Maengdok',
    author_email='maengdok@outlook.com',
    description='A Python package for easily sending messages through Discord webhooks',
    long_description="""
    # Easy Discord Webhook Message

    A Python package for easily sending messages through Discord webhooks.

    ## Installation

    Install the package using pip:

    ```bash
    pip install discord_webhook_easy_message
    ```

    ## Usage

    ```python
    from discord_webhook_easy_message import Webhook

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
    """,
    long_description_content_type='text/markdown',
    url='https://github.com/Axel-Pion-MDS/M2_Discord_Webhook',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)