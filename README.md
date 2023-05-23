# News Aggregator for Geopolitical Topics

## Background and Problem Statement
In many of our work within public service, some of us are tasked to sense-make the current macro and micro-trends. However, to do so, there are a lot of manhours and time needed, and some departments even tried employing headcounts to do so. After that, they will send the news to all officers within their departments. But they cannot know what the readership is like. Hence, our team created a solution and is serving an alpha version to selected public officers as early users.

The goal of this project is to enhance the current application to expand to geopolitical-related news, which focused only on tech news. Users can pick their preferred topics (not keywords), before a set of 10 articles is sent to them ranked by their topic preferences and trendiness.

Why Geopolitics? This has been a recurring theme in our discussions with agencies. Also, there are a lot of movements happening such as the de-dollarization, that might be signals of a changing world order

## Methodology

#### Step 1: Name-entity extrations
1. 	Scrape data from reputable sources on international relations news (text first) 
		a. There is also a thought to see how to use a variety of data from commentaries on Video
2. Then, I need to clean the data - will explore using spaCy
3. Understand the similarity and differences based on the words that are in the text
4. Extract key words/phrases and entities to perform name-entity recognition, and group them by topic modelling using spaCy
5. I am thinking of using BERT to group them into three level of topics : L1 (Categories), L2 (Topics), and L3 (Keywords) with the key phrases
6. I will also use other transformer or large-language models such as GPT to compare the performance against BERT
7. The L1 and L2 Topics are exposed to users, and they can select the topics they want to read every morning

#### Step 2: Curate 10 articles to users
Besides users preference, I will use a few more factors as weights
1. Sources : based on the 'credibility' of the source
2. Hot-news/trends : based on how fresh the news is. By datetime, and by google trends
3. Geography : prioritize by countries maybe? But the hard part and depends on the entities we can abstract from the text

#### Step 3(a): Recommend to users
This is based on the users preference. Currently we only have 253 users, with 15 topics on tech. So there might be a cold-start problem

#### Step 3(b): Trend Analysis
This is tougher - what is the best way to show a particular topic trending over time? I need to do some research

## How to evaluate success
1. Number of clicks of articles recommended from their emails
2. Number of users increased through the addition of a geopolitical scope

## Potential Challenges
1. There might not be a lot of 'free' international journals; many are behind paywalls. So not all websites can be scraped? Need Shao Quan-fu
2. The scrapper might break over time when the way websites structure their contents change (which happens often)
3. During recognition of name-entity, it might be hard for the model to make sense of the importance by just the name of the country itself
4. If this is productionize, without man-in-the-loop, we might be sending controversial news to users, which is tough

