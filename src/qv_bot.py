import logging
import os
import threading
import time

import chevron
import praw
import yaml


class DotDict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class QualityVoteBot:
    logger = logging.getLogger(__name__)

    default_config = {
            'report_reason': 'Score of stickied comment has dropped below threshold',
        }

    def __init__(self, reddit):
        self.reddit = reddit
        self.subreddit = self.reddit.subreddit(os.environ["target_subreddit"])
        self.config = None
        self.fetch_config_from_wiki()

    def run_threaded(self, interval, job_func):
        def repeat():
            while True:
                try:
                    job_func()
                except Exception as e:
                    self.logger.error(e)
                self.logger.debug(f"starting to sleep")
                time.sleep(interval)

        job_thread = threading.Thread(target=repeat, name=job_func.__name__.upper())
        job_thread.start()

    def run(self):
        self.run_threaded(360, self.add_comments_to_posts)
        self.run_threaded(360, self.check_recent_comments)
        self.run_threaded(360, self.fetch_config_from_wiki)

    def add_comments_to_posts(self, ):
        for submission in self.subreddit.stream.submissions():
            if not self.__has_stickied_comment(submission) \
                    and submission.link_flair_template_id not in self.config['ignore_flairs']:
                self.logger.info(f"https://www.reddit.com{submission.permalink}")
                sticky = submission.reply(self.config['vote_comment'])
                sticky.mod.distinguish(how="yes", sticky=True)
            else:
                self.logger.debug(f"Ignoring https://www.reddit.com{submission.permalink}")

    def check_recent_comments(self, ):
        self.logger.info("checking comments")
        count = 0
        for comment in self.reddit.user.me().comments.new(limit=None):
            count += 1
            if not self.__is_removed(comment.parent()) and comment.score <= self.config['report_threshold']:
                model: dict = self.config.copy()
                model.update(comment.parent().__dict__)
                comment.parent().report(chevron.render(self.config['report_reason'], model))
        self.logger.info(f"looked at {count} comments")

    def fetch_config_from_wiki(self):
        wiki_config_text = self.subreddit.wiki['qualityvote'].content_md
        wiki_config = yaml.safe_load(wiki_config_text)
        updated_config: dict = self.default_config.copy()
        updated_config.update(wiki_config)
        updated_config['vote_comment'] = chevron.render(updated_config['vote_comment'], self.__dict__)
        self.config = updated_config
        self.logger.info(f"reloaded config")
        self.logger.debug(self.config)

    def __has_stickied_comment(self, submission):
        return len(submission.comments) > 0 and submission.comments[0].stickied

    def __is_removed(self, s):
        try:
            author = str(s.author.name)
        except:
            author = '[Deleted]'
        if s.banned_by is not None or author != '[Deleted]':
            return True
        else:
            return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(threadName)s %(message)s')
    aReddit = praw.Reddit(username=os.environ["reddit_username"],
                         password=os.environ["reddit_password"],
                         client_id=os.environ["reddit_client_id"],
                         client_secret=os.environ["reddit_client_secret"],
                         user_agent="desktop:com.halfdane.superstonk_qvbot:v0.0.3 (by u/half_dane)")

    aReddit.validate_on_submit = True
    logging.info(f'working as {aReddit.user.me()}')
    QualityVoteBot(aReddit).run()
