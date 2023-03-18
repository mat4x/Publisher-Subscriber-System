import datetime
dt = datetime.datetime

past_posts = {
    "slyplt" : (
        (dt.timestamp(dt(2022, 12, 10)),
        '''Hello guys welcome to our channel. This is Abhyudaya and Gautami, together we make fun articles on millennial friendly topics. SUBSCRIBE and hit the bell icon! FOLLOW US ON SOCIAL MEDIA. Business enquiries :- slayypointofficial@gmail.com'''),
        (dt.timestamp(dt(2023, 1, 10)),
        '''Hey Slayy Fam! The Mivi Big Bang Sale is here! The best deals on Mivi's entire collection. Also have you seen the new colours of the Mivi Roam? Get the BEST audio at crazy deals. SHOP NOW'''),
        (dt.timestamp(dt(2023, 3, 5)),
        '''So close to 1M!! Jaldi se subscribe kar do.''')
        ),

    "cblt" : (
        (dt.timestamp(dt(2022, 11, 30)),
        '''Just an idiot with a computer science degree trying his best.'''),
        (dt.timestamp(dt(2022, 12, 20)),
        '''Merry Christmas everyone. So I hear you guys like puzzles, you've got 25 days to solve it: B64 Pzg1Njk3ZWZkMWI5OGQ0MzJmYmZmNmI0MWYzYmUwMjJm'''),
        ),

    "cptrphl":(
        (dt.timestamp(dt(2022, 10, 31)),
        '''Brady John Haran OAM (born 18 June 1976) is an Australian-British independent filmmaker and video journalist who produces educational videos and documentary films for his YouTube channels, the most notable being Periodic Videos and Numberphile. Haran is also the co-host of the Hello Internet podcast along with fellow educational YouTuber CGP Grey. On 22 August 2017, Haran launched his second podcast, called The Unmade Podcast, and on 11 November 2018, he launched his third podcast, The Numberphile Podcast, based on his mathematics-centered channel of the same name.'''),
        (dt.timestamp(dt(2023, 2, 25)),
        '''I SOLVED IT. Base64 decode to MD5 HASH => "I like myself"''')
        )
    }

for channel in ["slyplt", "cblt", "cptrphl"]:
    with open(f"{channel}.csv", 'w') as file:
       for pair in past_posts[channel]:
        file.write(str(pair[0]) + ',' + pair[1].replace(',', ';') + '\n')
