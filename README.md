# Bollywood Hungama Chatbot 🎬✨

A Retrieval Augmented Generation (RAG) Streamlit web app that lets you chat with a fun Bollywood-themed bot about YouTube videos! Uses Gemini (Google Generative AI), HuggingFace embeddings, FAISS vector store, and a stylish Bollywood UI.

---

## Features

- **Bollywood-themed chatbot UI** with random quotes and fun loading messages.
- **Gemini (Google Generative AI)** for high-quality, context-aware answers.
- **HuggingFace sentence-transformers** for embedding video data and queries.
- **FAISS** for fast vector search and retrieval.
- **Streamlit** for a modern, interactive web interface.
- **Chat history** with Bollywood flair.
- **Automatic FAISS index creation** from your YouTube video JSON data.

---

## Setup & Run

### 1. Install requirements

```bash
pip install -r requirements.txt
```

### 2. Prepare your data

- Place your YouTube video data in a file named `youtube_videos.json` in the project root.
- See [Data Format](#data-format) below for the required structure.

### 3. Run the app

```bash
streamlit run rag.py
```

---

## Usage

- The app will load your `youtube_videos.json`, create a FAISS vector store, and launch the chatbot.
- Ask any question about the videos (e.g., "Which video has the most views?", "Tell me about the song Uyi Amma").
- Enjoy Bollywood quotes and themed responses!

---

## Under the Hood

- **Embeddings:** Uses `sentence-transformers/all-MiniLM-L6-v2` from HuggingFace for text embeddings.
- **Vector Store:** Uses `faiss` for fast similarity search.
- **LLM:** Uses Gemini (`gemini-1.5-pro`) via Google Generative AI for generating answers.
- **UI:** Built with Streamlit, styled with Bollywood colors, emojis, and quotes.

---

## Sample Queries

- "Which video is the most popular?"
- "Tell me about the song Uyi Amma."
- "Who are the singers in Mere Mehboob?"

---

## Data Format

Your `youtube_videos.json` should look like this:

```json
{
    "videos": [
        {
            "video_id": "FZLadzn5i6Q",
            "title": "Uyi Amma - Azaad | Aaman D, Rasha Thadani| Madhubanti Bagchi,Amit Trivedi,Amitabh| Bosco| Abhishek K",
            "description": "👉🏻 SUBSCRIBE to Zee Music Company ...",
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
        }
    ]
}
```

---

## Credits

- Made with ❤️ for Bollywood fans.
- Follow [Zee Music on Instagram](https://www.instagram.com/zeemusiccompany/).

---

## Codespace

[Open in Codespace](https://animated-space-telegram-5g99vgrv9p624xjg.github.dev/?editSessionId=c882db15-890d-4101-b37d-3f4de152a243&continueOn=1)
