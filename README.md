# Reddit Scraping Subreddit Comparision README

### Problem Statement
I am using posts from two skincare subreddits (r/AsianBeauty and r/SkincareAddiction) in order to learn the skin concerns of two different groups of customers and what products/ingredients they are using to treat their issues to recommend to Sephora products and brands they should look into selling.

### Background Information

**Why Reddit Data**
Reddit is an incredibly popular website; it averages around 1.5 billion visits per [month](https://www.statista.com/statistics/443332/reddit-monthly-visitors/) and allows its users to create subreddits, or communities, based around whatever they want from topics as broad as news to niche interests such as whether some kid named Eric is wearing shorts [r/IsEricWearingShorts](https://www.reddit.com/r/IsEricWearingShorts/). On beauty subreddits like r/AsianBeauty and r/SkincareAddiction, members share their daily routines, favorite products, and general likes and dislikes. These posts contain an endless supply of information from incredibly knowledgeable individuals that Sephora can leverage in order to find new brands to carry and products containing the ingredients customers want.

**Accessing the Data with the Reddit API**
Since Reddit is such a rich source for text data, it has an API wrapper called [PRAW](https://praw.readthedocs.io/en/latest/) so you can access data from the site without having to scrape it. In order to use the wrapper, install it on your machine with pip, create an account with Reddit and sign up as a developer to receive API credits. Once you do so you have the ability to download up to 1000 posts from each subreddit and in addition to the title and text of the post you can also access information such as the number of comments, the upvote ratio, time posted, and even all of the comments on the post. 

### Data Dictionary

|Column Name |Data Type|Description|
|---|---|---|
| num_comments | <i>int</i> |  the number of comments on the post |
| post  | <i>object(string)</i>  | The body of the post  |
| time_utc|<i>float</i>| the time posted in epoch time |
| title | <i>object(string)</i> | the post title|
| upvote| <i>float</i>| the ratio of upvotes to downvotes where 1 is all upvotes and 0 is all downvotes|
| target| <i>int</i>| dummy, 1 if post from AsianBeauty, 0 from SkincareAddiction|
| title_word_count| <i>int</i>| number of words in title|
| post_word_count| <i>int</i>| number of words in post |
| post_isnull| <i>int</i> | dummy, 1 if no words in post, 0 otherwise |
|text |<i>object(string)</i>|the title column combined with the post column|
|text_word_count|<i>int</i>|total number of words in title and post|
|composite_sentiment|<i>float</i>|a score from -1 to 1 that measures how positive or negative the text is where -1 is completely negative and 1 is completely positive|

### EDA and The Model
I ran 7 scrapes each on the two subreddits, r/AsianBeauty and r/SkincareAddiction, and after dropping duplicate rows, I ended up with 6,207 posts. I then checked for null values, and created count variables and ran sentiment ananlysis on all of my text variables and built a function to output their histograms. I then ran my text column through CountVectorizer and turned the output into a dataframe in order to see the words from the posts. I ended up with more than 14,000 columns and I dug into the output to see if any of them were irrelevant words to add to my list of stop words. I filtered out http remnants, long numbers, and some words in Japanese and Korean using regex filters and added them to my list of stop words. Building the final list of stop words was an iterative process where I would run the model, see what irrelevant words rose to the top of the list for each subreddit, added those to the list and repeated. I ended up with 957 stop words in total. I built the model using a pipeline so I could grid search over different values of the CountVectorizer parameters, with the classification step done using a logistic regression function. This worked extremely well, with a training accuracy of 98.6% and a test accuracy of 94.2%. The model is slightly overfit, but changing the regularization levels in the logistic regression did not improve the accuracy scores. 

### Conclusions

Members of both subreddits discussed extensively how to deal with acne and what ingredients and products work to remove blemishes and reduce the appearance of scars. Also both subreddits strongly recommend wearing sunscreen daily. Skincare Addiction users seem to have more serious acne (or at least focus more of their discussions or dealing with it) and users tend to recommend the use of strong acids. Asian beauty users, on the other hand, are more focused on dealing with dry skin and using products to increase hydration and that proper hydration will also lead to a decrease in blemishes.

**Popular Brands and Ingredients on Asian Beauty:**

Brands: Innisfree, Klairs, Cosrx, Laneige, Sulwhasoo, A'peiu, Etude House, Kose, Skinfood, Krave, Pyunkang Yul, Neogen, Glow Recipe, Nature Republic, Shu Uemura, Shiseido
Ingredients: snail mucin, madecassoside, centella asiatica extract, royal honey, tamanu oil, green tea

**Popular Brands and Ingredients on Skincare Addiction:**

Brands: Neutrogena, Eucerin, Cetaphil, La Roche Posay, The Ordinary, CeraVe, Stratia, Paula's Choice, Pixi, Peter Thomas Roth, Clinique, Aztec Clay, Drunk Elephant
Ingredients: Glycolic acid, Azealic acid, placenta, hylauronic acid, BHA, benozyl peroxide, witch hazel, micellar water, AHA, coconut oil, aloe vera gel, lactic acid, tretonin, niacinamide, zinc

### Brands for Sephora to Investigate Selling
Sephora should look into carrying Stratia, Paula's Choice, Innisfree, Klairs, Sulwhasoo, and Nature Republic.

In addition to the above brands, Sephora already carries some Neogen products but Neogen's Green Tea stick face cleanser was referenced frequently in the AsianBeauty subreddit and should be added to their store. Also, Sephora should focus more on products that deal with acne prevention and contain hydrating ingredients like snail mucin and centella asiatica extract that Asian Beauty members like.

### Further Study
I would dig into the relevant terms from my scrapes, filter out the brand names, scrape Sephora's brands page, and compare which brands Sephora carries that are on my list and which they don't.
