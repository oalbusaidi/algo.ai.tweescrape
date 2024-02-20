import json
import asyncio
from twscrape import API
from tweet_db_services import TweetDbServices
from users_db_services import UserDbServices
from models import UserModel, TweetModel


async def main() :
    api = API()
    userDbServices = UserDbServices()
    tweetDbServices = TweetDbServices()
    
    # json_file = open('tweets.json', 'w', encoding='utf-8')

    q = "#مدينة_السلطان_هيثم"

    count  = 0    
    async for tweet in api.search(q, limit = 2000):
        data = json.loads(tweet.json())
        tweet = TweetModel(data)
        user = UserModel(data['user'])
        userDbServices.create_user(user.dataDict)
        tweetDbServices.create_tweet(tweet.dataDict)
        # json.dump(data, json_file, ensure_ascii=False, indent=4)
        count += 1
    print(count)

    # json_file.close()


if __name__ == '__main__':
    asyncio.run(main())