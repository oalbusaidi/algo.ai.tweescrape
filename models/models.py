class UserModel: 
    def __init__(self, obj : dict):
        self.dataDict = {
            "userid"          : obj['id'],
            "username"        : obj['username'],
            "displayname"     : obj['displayname'],
            "created"         : obj['created'],
            "followersCount"  : obj['followersCount'],
            "friendsCount"    : obj['friendsCount'],
            "statusesCount"   : obj['statusesCount'],
            "favouritesCount" : obj['favouritesCount'],
            "listedCount"     : obj['listedCount'],
            "mediaCount"      : obj['mediaCount'],
            "location"        : obj['location'],
            "verified"        : obj['verified'],
            "blue"            : obj['blue'],
        }

        self.userid          = obj['id']
        self.username        = obj['username']
        self.displayname     = obj['displayname']
        self.created         = obj['created']
        self.followersCount  = obj['followersCount']
        self.friendsCount    = obj['friendsCount']
        self.statusesCount   = obj['statusesCount']
        self.favouritesCount = obj['favouritesCount']
        self.listedCount     = obj['listedCount']
        self.mediaCount      = obj['mediaCount']
        self.location        = obj['location']
        self.verified        = obj['verified']
        self.blue            = obj['blue']



    

class TweetModel: 
    def __init__(self, obj : dict):
        self.dataDict = {
            "tweetid"        :  obj['id'],
            "userid"         :  obj['user']['id'],
            "conversationid" :  obj['conversationId'],
            "url"            :  obj['url'],
            "date"           :  obj['date'],
            "lang"           :  obj['lang'],
            "rawContent"     :  obj['rawContent'],
            "replyCount"     :  obj['replyCount'],
            "retweetCount"   :  obj['retweetCount'],
            "likeCount"      :  obj['likeCount'],
            "quoteCount"     :  obj['quoteCount'],
            "viewCount"      :  obj['viewCount']
        }

        self.tweetid         = obj['id']
        self.userid          = obj['user']['id']
        self.conversationid  = obj['conversationId']
        self.url             = obj['url']
        self.date            = obj['date']
        self.lang            = obj['lang']
        self.rawContent      = obj['rawContent']
        self.replyCount      = obj['replyCount']
        self.retweetCount    = obj['retweetCount']
        self.likeCount       = obj['likeCount']
        self.quoteCount      = obj['quoteCount']
        self.viewCount       = obj['viewCount']

    