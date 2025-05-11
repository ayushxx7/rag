# rag
retrieval augment generation (rag) streamlit (st) based web app with chatbot support from Gemini

# setup and run
## install requirements
```bash
pip install -r requirements.txt
```

## run via streamlit
```bash
streamlit run rag.py
```

# about
- upload youtube_videos data of format (mentioned at the end).
- ask queries after local faiss index store is created.

# under the hood
- uses `sentence-transformers` from HuggingFace to embed queries and data
- uses `faiss` for creating vector store for querying
- uses `gemini` for good quality and scoped Q&A
- uses `streamlit` for the web interface

## codespace
https://animated-space-telegram-5g99vgrv9p624xjg.github.dev/?editSessionId=c882db15-890d-4101-b37d-3f4de152a243&continueOn=1

# sample queries
![IMG-20250511-WA0063](https://github.com/user-attachments/assets/179f43e4-ae3e-4ad1-ba7a-d5a724f2cf65)

![IMG-20250511-WA0062](https://github.com/user-attachments/assets/d682e79b-e61a-44e5-bb9f-2d30ff674769)

# data format
```json
{
    "videos": [
        {
            "video_id": "FZLadzn5i6Q",
            "title": "Uyi Amma - Azaad | Aaman D, Rasha Thadani| Madhubanti Bagchi,Amit Trivedi,Amitabh| Bosco| Abhishek K",
            "description": "👉🏻 SUBSCRIBE to Zee Music Company - https://bit.ly/2yPcBkS \n\nTo Stream & Download Full Song: \nSpotify - https://spoti.fi/3Po1CCU\nJioSaavn - https://bit.ly/40mPTLh\nGaana - https://bit.ly/4gFoWbi\niTunes - https://apple.co/3DHxyzy\nApple Music - https://apple.co/3DHxyzy\nAmazon Prime Music - https://amzn.to/40092RH\nHungama - https://bit.ly/3W1Lo6b\nYouTube Music - https://bit.ly/4a6CBp6\n\nSong: Uyi Amma\nSinger: Madhubanti Bagchi\nComposed by: Amit Trivedi\nLyrics by: Amitabh Bhattacharya\nChoreographer: Bosco Leslie Martis\nBacking Vocals: Rajiv Sundaresan, Rishikesh Kamerkar, Arun Kamath & Suhas Sawant\nCrew:-\nMusic Arranged and Produced by: Amit Trivedi & Rahul Tiwari\nElectric Guitar: Aryan Tiwari\nTrumpet: Robin Fargose\nShennai: Omkar Dhumal\nDholak & Dhol: Jayesh Kathak & Lalit Shankar\nAdditional Indian Percussion: Jayesh Kathak\nAssistant to Rahul Tiwari: Vipul Pednekar\nSound Engineer, AT Studios: Urmila Sutar & Chinmay Mestry\nAssistant Sound Engineer, AT Studios: Abhishek Vishnu Dandekar\nMixed & Mastered by: Shadab Rayeen at New Edge\nAssisted by: Anup, Prasad, Sohamm, Rupam & Kundan\nManager, AT Studios: Naveen\n\nRSVP & Guy In The Sky Pictures present \n#Azaad\n\nStarring: Ajay Devgn, Aaman Devgan, Rasha Thadani, Diana Penty, Mohit Malik & Piyush Mishra\nDirected by: Abhishek Kapoor\nProduced by: Ronnie Screwvala & Pragya Kapoor\nCo-produced by: Abhishek Nayyar & Abhishek Kapoor\nAssociate Producer: Pashan Jal\nWritten By: Ritesh Shah, Suresh Nair & Abhishek Kapoor\nCreative Producer: Nishant Kantharia, Maharsh Shah, Sanaya Irani\n\n\nMusic on Zee Music Company\n\nConnect with us on :\nSnapchat - https://bit.ly/3UIfICJ\nTwitter - https://www.twitter.com/ZeeMusicCompany\nFacebook - https://www.facebook.com/zeemusiccompany\nInstagram - https://www.instagram.com/zeemusiccompany\nYouTube - http://bit.ly/TYZMC",
            "published_at": "2025-01-04T14:54:39Z",
            "search_keyword": "hindi songs",
            "view_count": 260359258,
            "like_count": 1337731,
            "comment_count": 27287
        },
        {
            "video_id": "UdsO4SM4wKI",
            "title": "Mere Mehboob | Vicky Vidya Ka Woh Wala Video | Rajkummar | Triptii Dimri |Sachin-Jigar,Shilpa,Sachet",
            "description": "Turn up the heat with the sensational song \"Mere Mehboob\" from the film \"Vicky Vidya Ka Woh Wala Video\". \n\nStarring the Dynamic Duo Rajkummar Rao and Triptii Dimri. Sung by the Shilpa Rao and Sachet Tandon, Composed by the Incredible Duo, Sachin - Jigar and Penned by the Talented Priya Saraiya.\n\nGulshan Kumar, T-Series, Balaji Telefilms & Wakaoo Films Present\nin Association with Kathavachak Films\nA T-Series Films & Wakaoo Films Production\n\n\"Vicky Vidya Ka Woh Wala Video\"\n\nWritten & Directed by Raaj Shaandilyaa.\n\nReleasing in Cinemas with The Bang on 11th October 2024!\n\n#RajkummarRao #TriptiiDimri #VickyVIdyaKaWohWalaVideo #MereMehboob  \n\nMake Your #YTShorts😍on \"Mere Mehboob\" Now▶https://youtube.com/source/Z2hoXa--xvw/shorts\n\n♪Full Song Available on♪ \nJioSaavn: https://bit.ly/3zuyplk\nSpotify: https://spoti.fi/3XAvm32\nHungama: https://bit.ly/4ezOPro\nApple Music: https://bit.ly/3ZuFYmI\nGaana: https://bit.ly/3TDAYZi\nAmazon Prime Music: https://bit.ly/4dfjGZu\nWynk: https://bit.ly/4eBXidY\nYouTube Music: https://bit.ly/3zkHaP1\n\nSong Credits:\nMusic - Sachin-Jigar\nSinger - Shilpa Rao, Sachet Tandon\nLyrics- Priya Saraiya\nMix & Master - Eric Pillai @ Future Sound Of Bombay\nAssistant Mix Engineer- Michael Edwin Pillai\nChoreographer: Ganesh Acharya\nMusic Video Director-Mihir Gulati\nDOP -Siddharth Diwan\nChoreographer-Ganesh Acharya\nProject head (T- Series)- Pooja Singh Gujral\nProduction designer-Rajat Poddar\nProduction designer-parijat Poddar\nSteady cam- Sandeep Shetty\nJimmy jib- surender kumar J dulgach\nAssociate DOP- Sukesh Viswanath\nAssociate choreographers - Jayshree Kelkar, Sachin Poojary\nChief AD- Rishabh Dang\n1st AD-Hitesh Chandwani, PU Rohit\n2nd AD-Ankita Singh, Varun Gulati\nLine producer- Shivkumar Tiwari\nUPM- Naseem Shah\nProduction Manager-Pradhuman Deora, Abhijeet Jitendra Patil, Paresh Vaishnav\nProduction Assistant - Divyansh Vishwakarma\nProduction executive- Ravinder Rawat \nArt Director-ashutosh patnaik\nAssociate Art director- krishana swain, Mukesh chauhan\nAsst Choreographers-Mangesh Nikam, Sachin Howaldar, Meetali parmar, Shweta bombatkar\nChoreographer Manager - Ashish s Pandhari, Anna D’silva\nCostume designer Dancers- Jimmy\nEditor - Manoj magar\nColor studio - The Post Brothers\nDI Colorist -Ercan kucuk\nColor producer- ertug Ozturk      \n\nTriptii Dimri's Team:\nCelebrity managed by - Dharma Cornerstone Agency \nManager - Jui Pawar \nMake up - Simran Gidwani \nHair - Hrishikesh Naskar\nStyled by - Aastha Sharma \nStyling Team - Reann Moradian and Muskaan Matta\n\nRajkummar Rao's team\nManager : Mona Joshi\nHair : Vijay Raskar\nMakeup : nitin Purohit\nSpot : Anand Gautam\nSecurity : Sandeep Gajabhive\nDriver : Vidyanand Yadav\nCostume designer- Sonali R Patel\n\nFilm Credits:\nWritten & Directed by Raaj Shaandilyaa\nProduced by : Bhushan Kumar & Krishan Kumar \nProduced by : Shobha Kapoor & Ektaa R Kapoor\nProduced by : Vipul D Shah, Ashwin Varde, Rajesh Bahl \nProduced by : Raaj Shaandilyaa & Vimal Lahoti\nCo-Producer : Shiv Chanana   \nPresident (T-Series) : Neeraj Kalyan\nStory : Raaj Shaandilyaa, Yusuf Ali Khan \nDop : Aseem Mishra Isc\nScreenplay:  Raaj Shaandilyaa, Yusuf Ali Khan, Ishrat R Khan, Rajan Agarwal \nDialouges : Raaj Shaandilyaa\nDop : Aseem Mishra \nEditor : Prakash Chandra Sahoo \nSound Designer : Nihar Ranjan Samal \nProduction Design : Rajat Poddarr & Parijat Poddar\nCreative Director : Ishrat R Khan  \nExecutive  Producer : Kshitij Ravi Prasad \nProject Head (Wakaoo Films) : Barkha Thakur \nDA : Krishanu Singh Rathore  \nCostume Designer : Leepakshi Ellawadi \nAction Director : Manohar Verma \nMusic : Sachin - Jigar  \nLyrics : Priya Saraiya, Som \nBackground Music : Hitesh Sonik\nCasting Director : Paragg Mehta \nChoreographers : Ganesh Acharya, Raju Khan,  Vishnudeva, Sushma Sunam,  Piyush - Shazia\nProject Head (T-Series) : Meghha Chheda \nFilm & Content Team (T-Series) : Alok Kumar Shukla, Heett Savla, Shraddha Shrikant Ghanekar\nMarketing & Promotions (T-Series) : Shivam Chanana, Raj Chanana, Prashant Shetty, Mita Choudhary, Rahul Dubey, Amol Bhamare, Heett Savla\nDigital Team (T-Series) : Varun Arora, Juhi Singh, Praveen Sharma, Ratika Anand, Mohit Malik\nMusic on : T-Series  \nMusic Team  (T-Series)  : Raj Chanana, Shivam Chanana, Sonal Chawla, Sonu Srivastava, Vivin Sachdeva\nDi  : Prime Focus \nVfx : Cinegence Media \nDigital Marketing : White Rivers Media \nPublicity Design : Parass Kanani (house of Awe) \nVisual Promotions : Just Right Studioz Nx\n\n\nDownload Song Beat: https://bit.ly/3Cjh24R \n\n___________________________________\nEnjoy & stay connected with us!\n👉 Subscribe to T-Series: https://youtube.com/tseries\n👉 Like us on Facebook: https://www.facebook.com/tseriesmusic\n👉 Follow us on X: https://twitter.com/tseries\n👉 Follow us on Instagram: https://instagram.com/tseries.official",
            "published_at": "2024-09-23T15:00:08Z",
            "search_keyword": "hindi songs",
            "view_count": 235859450,
            "like_count": 1436965,
            "comment_count": 58099
        },
```
