import os
import praw

from src.qv_bot import QualityVoteBot

testee = QualityVoteBot(
    praw.Reddit(username=os.environ["reddit_username"],
                password=os.environ["reddit_password"],
                client_id=os.environ["reddit_client_id"],
                client_secret=os.environ["reddit_client_secret"],
                user_agent="desktop:com.halfdane.superstonk_qvbot:v0.0.2 (by u/half_dane)"))


def test_extract_config():
    text = "vote_comment: |-\n    **IMPORTANT POST LINKS**\n    \n    [What is GME and why should you consider " \
           "investing?](https://www.reddit.com/r/Superstonk/comments/qig65g" \
           "/welcome_rall_looking_to_catch_up_on_the_gme_saga/) || [What is DRS and why should you care?](" \
           "https://www.reddit.com/r/Superstonk/comments/ptvaka/when_you_wish_upon_a_star_a_complete_guide_to/) " \
           "|| [Low karma but still want to feed the DRS bot? Post on r/gmeorphans here](" \
           "https://www.reddit.com/r/GMEOrphans/comments/qlvour/welcome_to_gmeorphans_read_this_post/) ||\n\n    " \
           "------------------------------------------------------------------------\n    \n    Please help us " \
           "determine if this post deserves a place on /r/{{subreddit}}. [Learn more about this bot and why we " \
           "are using it here](" \
           "https://www.reddit.com/r/Superstonk/comments/poa6zy/introducing_uqualityvote_bot_a_democratic_tool_to" \
           "/)\n \n    If this post deserves a place on /r/{{subreddit}}, **UPVOTE** this comment!!\n \n    If " \
           "this post should not be here or or is a repost, **DOWNVOTE** This comment!\n \nignore_flairs: [" \
           "'7b24752e-85f9-11eb-b3c8-0e861167b641', '37ec242e-984f-11eb-94c6-0e8d0acce789', " \
           "'443477c2-9859-11eb-93e5-0e7222816149',\n '70f23bf8-95d6-11eb-a299-0e9b20cb9c43', " \
           "'02d4a642-a071-11eb-bf5d-0e4876509fbb',\n '33b1d54c-3445-11ec-953a-ceaf24437904']\nreport_threshold: " \
           "-7\nremove_threshold: -9999\nremoval_comment: /u/{{author}}, thank you for your submission. " \
           "Unfortunately, your post has been removed because it has been voted unsuitable for /r/{{subreddit}}. "

    config = testee.parse_config(text)

    assert config.ignore_flairs == ['7b24752e-85f9-11eb-b3c8-0e861167b641',
                                    '37ec242e-984f-11eb-94c6-0e8d0acce789',
                                    '443477c2-9859-11eb-93e5-0e7222816149',
                                    '70f23bf8-95d6-11eb-a299-0e9b20cb9c43',
                                    '02d4a642-a071-11eb-bf5d-0e4876509fbb',
                                    '33b1d54c-3445-11ec-953a-ceaf24437904']
    assert config.report_threshold == -7
    assert config.remove_threshold == -9999
    assert config.removal_comment == "/u/{{author}}, thank you for your submission. Unfortunately, your post " \
                                     "has been removed because it has been voted unsuitable for /r/{{" \
                                     "subreddit}}."


def test_read_config_from_wiki():
    assert testee.config is not None
    assert testee.config.report_threshold == -7
    print(testee.config.vote_comment)
