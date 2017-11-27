
Utopy, is a CLI app to curate content on **approved** contributions shared via utopian.io. 

with Utopy,

* You can support contributions directly with your votes
* You can front-run utopian.io bot for better curation rewards.

I believe, this is a win-win situation. I know there is a curation trail on the works, but I don't like curation trails personally. I do like the option to customize curation for utopian.io posts.

<img src="https://i.hizliresim.com/7yJ8DN.png">
***

#### Installation

You need python3.6 or greater.

```
$ (sudo) pip install utopy
```

#### Running

```
$ utopy_bot /path/to/config.json
```

#### Configuration (config.json file)

```
{
  "posting_key": "private_posting_key",
  "account": "caster_account",
  "mysql_uri": "mysql+pymysql://user:pass@localhost/utopian",
  "nodes": ["https://rpc.buildteam.io"],
  "weight": 10,
  "limit": 50,
  "apply_to_categories": ["development", "tutorials"],
  "vote_delay": 30,
  "check_frequency": 300
}

```

**apply_to_categories**

You can only vote for selected contribution categories. For example, I vote for development and tutorials categories.

**vote_delay**

This is for voting N minutes after the creation time of post. Default is 30.

**account**

vote caster account

**mysql_uri**

MySQL connection URI. You need to create a database and fill this accordingly. mySQL is needed to put logs of upvotes.

**limit**

Utopy checks last N approved posts in the utopian. This is the **N**. Default is 20.

**weight**

Vote weight percentage. Default is 25.

**check_frequency**

Wait time between utopy cycles to fetch new posts. Default is 300 seconds.

**nodes**

List of steem public nodes.

***

Feel free to comment about the usage/features. 

Github URL: [http://github.com/emre/utopy](http://github.com/emre/utopy)





