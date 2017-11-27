import logging
import time
import json
import argparse
from datetime import datetime

import dataset
import requests
from steem import Steem
from steem.post import Post

logger = logging.getLogger('utopian-support-bot')
logger.setLevel(logging.INFO)
logging.basicConfig()


def get_last_approved_posts(limit=20):
    r = requests.get(
        "https://api.utopian.io/api/posts?limit=%s" % limit).json()
    return r["results"]


def get_table(mysql_uri):
    db = dataset.connect(mysql_uri)
    return db["utopian_logs"]


def add_log(mysql_uri, post):
    get_table(mysql_uri).insert(dict(
        author=post["author"],
        permlink=post["permlink"],
        created_at=str(datetime.now()),
    ))


def already_voted(mysql_uri, post):
    return get_table(mysql_uri).find_one(
        author=post["author"], permlink=post["permlink"]
    )


def curate(mysql_uri, vote_caster, posting_key, weight=+50,
         self_vote=False, limit=20, apply_to_categories=None,
         vote_delay=+30, nodes=None):
    last_posts = get_last_approved_posts(limit)
    s = Steem(keys=[posting_key], nodes=nodes)
    for utopian_post in last_posts:

        if utopian_post["author"] == vote_caster and not self_vote:
            logger.info("Skipping %s. No self-vote.", post.identifier)
            continue

        post = Post(
            "@%s/%s" % (utopian_post["author"], utopian_post["permlink"]))

        elapsed_minutes = int(post.time_elapsed().seconds / 60)
        if elapsed_minutes < vote_delay:
            logger.info(
                "Skipping %s. I will wait until %s minutes.",
                post.identifier,
                vote_delay - elapsed_minutes
            )
            continue

        if already_voted(mysql_uri, post):
            logger.info("Skipping %s. Already voted.", post.identifier)
            continue

        if apply_to_categories:
            if utopian_post["json_metadata"]["type"] \
                    not in apply_to_categories:
                logger.info(
                    "Skipping %s, This posts category: %s",
                    post.identifier,
                    utopian_post["json_metadata"]["type"]
                )
                continue

        try:
            s.commit.vote(post.identifier, weight, account=vote_caster)
            add_log(mysql_uri, post)
            logger.info(
                "Casted vote on: %s with weight: %s", post.identifier, weight)
            time.sleep(3)
        except Exception as error:
            if 'already voted' in error.args[0]:
                add_log(mysql_uri, post)
            logger.error(error)
            continue


def scheduler(mysql_uri, vote_caster, posting_key, weight=+50,
        self_vote=False, limit=20, apply_to_categories=None,
        vote_delay=+30, check_frequency=30, nodes=None):

    while True:
        curate(
            mysql_uri,
            vote_caster,
            posting_key,
            weight=weight,
            self_vote=self_vote,
            limit=limit,
            apply_to_categories=apply_to_categories,
            vote_delay=vote_delay,
            nodes=nodes,
        )

        logger.info("Sleeping for %s seconds." % check_frequency)
        time.sleep(check_frequency)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Config file in JSON format")
    args = parser.parse_args()
    config = json.loads(open(args.config).read())

    scheduler(
        config["mysql_uri"],
        config["account"],
        config["posting_key"],
        weight=config.get("weight", +25),
        limit=config.get("limit", 20),
        apply_to_categories=config.get("apply_to_categories"),
        vote_delay=config.get("vote_delay", 30),
        check_frequency=config.get("check_frequency", 300),
        nodes=config.get("nodes"),
    )

if __name__ == '__main__':
    main()