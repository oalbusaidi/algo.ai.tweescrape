import json
import asyncio
import codecs
from twscrape import API, gather

async def main() :
    api = API()
    json_file = open('tweets.json', 'w')

    q = "عمانتل"
    
    async for tweet in api.search(q, limit = 1):
        data = json.loads(tweet.json())
        json.dump(data, json_file, indent=4)


    json_file.close()


    json_file = open('tweets.json', 'r')

    content = json_file.read()

    print(content)
    json_file.close()



if __name__ == '__main__':
    asyncio.run(main())