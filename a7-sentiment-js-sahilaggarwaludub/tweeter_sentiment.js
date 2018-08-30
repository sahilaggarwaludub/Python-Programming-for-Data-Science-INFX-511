'use strict';

//SENTIMENTS, EMOTIONS, and SAMPLE_TWEETS have already been "imported"

/* Your script goes here */
function split_tweet(text){
    // A function to split up the tweet's text (a string) into individual words (an array)
    var listWords = text.split(/\W+/);
    var listWords = listWords.map(function (item) {
        return item.toLowerCase();
    });
    var listOfWords = listWords.filter(function (item) {
        return (item.length > 1);
    });
    return listOfWords;
}

function word_with_emotion(listWords,emotion){
    // A function that filters an array of words to only get those words that contain a specific emotion.
    var sentiment = listWords.filter(function (n) {
        if (SENTIMENTS[n] != undefined && SENTIMENTS[n][emotion] != undefined) {
            return n;
        }
    });
    return sentiment;
}

function emotions(listWords){
    // A function that determines which words from an array have each emotion, returning an object that contains that information.
    var wordsEmotion = EMOTIONS.reduce(function (w, emotion) {
        if (!w[emotion]) {
            w[emotion] = [];
        }
        w[emotion].push(filterWordsForEmotion(listWords, emotion));
        return w;
    }, {});
    return wordsEmotion;
}

function common_words(listWords) {
    // A function that gets an array of the "most common" words in an array, ordered by their frequency.
    var dictWordCount = listWords.reduce(function (count, n) {
        if (!count[n]) {
            count[n] = 0;
        }
        count[n] = count[n] + 1;
        return count;
    }, {});

    var items = Object.keys(dictWordCount).map(function (key) {
        return [key, dictWordCount[key]];
    });

    items.sort(function (first, second) {
        return (second[1] - first[1]);
    });

    var listItems = [];
    items.forEach(function (item) {
        listItems.push(item[0]);
    });
    return listItems;
}
  
function getAllWords(tweets) {
    // takes in an array of tweet objects and returns an array of all the words included in those tweets.
    var list = tweets.reduce(function (listTweets, tweet) {
        listTweets = listTweets.concat(split_tweet(tweet['text']))
        return listTweets;
    }, []);
    return list;
}

function getEmotionHashtags(tweets, emotion) {
    // takes in two parameters: an array of tweet objects and a single emotion
    // This function will return a new array of all the hashtags that are used in tweets that have at least one word with that emotion.
    var t = tweets.filter(function (tweet) {
        var listWords = split_tweet(tweet['text']);
        var emotionDict = word_with_emotion(listWords, emotion)
        if (emotionDict.length > 0) {
            return tweet;
        }
    });
    var listHashtags = t.reduce(function (hashtag, tweet) {
        for (var i = 0; i < tweet['entities']['hashtags'].length; i++) {
            hashtag = hashtag.concat('#' + tweet['entities']['hashtags'][i]['text'].toLowerCase());
        }
        return hashtag;
    }, []);
    return listHashtags;
}

function analyzeTweets(tweets) {
    // function that takes in an array of tweets and returns an object containing the data of interest.
    var listWords = getAllWords(tweets);
    var dictEmotions = EMOTIONS.reduce(function (dict, emotion) {
        dict[emotion] = [];
        dict[emotion]['Hashtags'] = getEmotionHashtags(tweets, emotion);
        dict[emotion]['Example Words'] = word_with_emotion(listWords, emotion);
        dict[emotion]['%age Words'] = (dict[emotion]['Example Words'].length / listWords.length) * 100;
        return dict;
    }, {});
    var dsEmotions = EMOTIONS.reduce(function (dict, emotion) {
        dict[emotion]['Hashtags'] = common_words(dict[emotion]['Hashtags']);
        dict[emotion]['Example Words'] = common_words(dict[emotion]['Example Words']);
        return dict;
    }, dictEmotions);
    return dsEmotions;
}

function showEmotionData(obj1) {
    // The function takes as an argument the data structure returned from the analyzeTweets() function and displays the statisics
    var x = d3.select('#emotionsTableContent')
    x.html('');
    //sorting dictionary 
   var obj = Object.keys(obj1).sort(function(a, b){return obj1[b]['%age Words'] - obj1[a]['%age Words']});
    
    for (var emotion in obj){
        var one = obj[emotion];
        var two = (obj1[obj[emotion]]['%age Words']).toFixed(2) + '%';
        var three = obj1[obj[emotion]]['Example Words'].slice(0, 3).join(", ").toLowerCase();
        var four = obj1[obj[emotion]]['Hashtags'].slice(0, 3).join(", ").toLowerCase();
        var str_final = `<td>${one}</td><td>${two}</td><td>${three}</td><td>${four}</td>`
        x.append('tr').html(str_final);
    }
}


async function loadTweets(userName) {
    // takes in a Twitter username (as a string). This function then sends an AJAX request (an asynchronous HTTP request) for the user's timeline data, analyze that data (using your analyzeTweets() function), and then display the results (using your showEmotionData() function).
    var uri = '  https://faculty.washington.edu/joelross/proxy/twitter/timeline/?' + 'screen_name=' + userName;
    var tweets = await d3.json(uri);
    showEmotionData(analyzeTweets(tweets));
}

showEmotionData(analyzeTweets(SAMPLE_TWEETS));
var button = d3.select('#searchButton');
button.on('click', function(){
    var value = d3.select('#searchBox').property('value');
    loadTweets(value);
});

