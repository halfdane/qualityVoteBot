# superstonkFlairChangeBot

A bot that supports mod-controlled flair granting.

While the bot runs, comment in Superstonk `!flairy:explain!`

To grant a flair, copy the user's request (something like `!FLAIRY!🚀Flair text🚀(red)`) into a response to their request.
The flairy bot will replace your comment with a cute confirmation message if everything went right,
otherwise it will be a humouros error message.

You will get a DM from the flairy containing the details of the change so you have a chance of 
reverting them in case something goes terribly wrong!


# Run

You have to export the following environment variables:

    export reddit_client_id="some-client-id"
    export reddit_client_secret="random gibberish"
    export reddit_username="half_dane"
    export reddit_password="very_secret"

    export target_subreddit="Superstonk or a test subreddit"

Afterwards execute

    make flairy

This sets up the venv for python and downloads the necessary dependencies before running the tests and starting the bot  

# Targets

    make flairy     # execute the bot 
    make clean      # clean up compile results and the venv
