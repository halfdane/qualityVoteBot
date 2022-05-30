++++++++++++++++++++++++++++++++++++++++++++++++++++


THIS PROJECT IS NOW RETIRED

The functionality of Superstonk's QV bot has moved into another place.

++++++++++++++++++++++++++++++++++++++++++++++++++++++

# qualityVoteBot

A mod bot that will sticky a comment on every new thread in your subreddit, just like [the original quality vote bot](https://old.reddit.com/r/QualityVote/comments/ji9kf6/introducing_qualityvote/)


# Run

You have to export the following environment variables:

    export reddit_client_id="some-client-id"
    export reddit_client_secret="random gibberish"
    export reddit_username="half_dane"
    export reddit_password="very_secret"

    export target_subreddit="Superstonk or a test subreddit"

Afterwards execute

    make

This sets up the venv for python and downloads the necessary dependencies before running the tests and starting the bot  

