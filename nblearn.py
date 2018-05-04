import sys
import codecs
import re


def initial_counts():
    global true, fake, positive, negative
    global true_list, fake_list, positive_list, negative_list

    pattern_regex = r'[~@#$%&.?\-"/;:,!(){}*^+=|<>_]+'

    for line in lines:
        words = line.rstrip().split(" ", 3)
        words[3] = words[3].lower()
        patterns_list = re.findall(pattern_regex, words[3])

        for pattern in patterns_list:
            words[3] = words[3].replace(pattern, " ")

        words[3] = words[3].replace("[", " ").replace("]", " ")

        if words[1] == "True":
            true += 1
            true_list.append(words[3])
        else:
            fake += 1
            fake_list.append(words[3])

        if words[2] == "Pos":
            positive += 1
            positive_list.append(words[3])
        else:
            negative += 1
            negative_list.append(words[3])


def count_features():
    global tokens
    global true_dict, fake_dict, positive_dict, negative_dict

    for reviews in true_list:
        flag = False
        if reviews in positive_list:
            flag = True
        w = filter(None, reviews.split(" "))
        for token in w:
            if token not in tokens:
                if token not in stopwords:
                    tokens.append(token)
                    true_dict[token] = 1
                    if flag:
                        positive_dict[token] = 1
                    else:
                        negative_dict[token] = 1
            else:
                if token in true_dict:
                    true_dict[token] += 1
                else:
                    true_dict[token] = 1

                if flag:
                    if token in positive_dict:
                        positive_dict[token] += 1
                    else:
                        positive_dict[token] = 1
                else:
                    if token in negative_dict:
                        negative_dict[token] += 1
                    else:
                        negative_dict[token] = 1

    for reviews in fake_list:
        flag = False
        if reviews in positive_list:
            flag = True
        w = filter(None, reviews.split(" "))
        for token in w:
            if token not in tokens:
                if token not in stopwords:
                    tokens.append(token)
                    fake_dict[token] = 1
                    if flag:
                        positive_dict[token] = 1
                    else:
                        negative_dict[token] = 1
            else:
                if token in fake_dict:
                    fake_dict[token] += 1
                else:
                    fake_dict[token] = 1

                if flag:
                    if token in positive_dict:
                        positive_dict[token] += 1
                    else:
                        positive_dict[token] = 1
                else:
                    if token in negative_dict:
                        negative_dict[token] += 1
                    else:
                        negative_dict[token] = 1


def laplace_smoothing():
    global true_total, fake_total, positive_total, negative_total

    for feature in tokens:
        if feature in true_dict:
            true_dict[feature] += 1
        else:
            true_dict[feature] = 1
        true_total += true_dict[feature]

        if feature in fake_dict:
            fake_dict[feature] += 1
        else:
            fake_dict[feature] = 1
        fake_total += fake_dict[feature]

        if feature in positive_dict:
            positive_dict[feature] += 1
        else:
            positive_dict[feature] = 1
        positive_total += positive_dict[feature]

        if feature in negative_dict:
            negative_dict[feature] += 1
        else:
            negative_dict[feature] = 1
        negative_total += negative_dict[feature]


def calculate_probability():
    global prior_probability

    prior_probability["True"] = (1.0 * true) / len(lines)
    prior_probability["Fake"] = (1.0 * fake) / len(lines)
    prior_probability["Pos"] = (1.0 * positive) / len(lines)
    prior_probability["Neg"] = (1.0 * negative) / len(lines)

    for feature in tokens:
        true_dict[feature] = (1.0 * true_dict[feature])/true_total
        fake_dict[feature] = (1.0 * fake_dict[feature])/fake_total
        positive_dict[feature] = (1.0 * positive_dict[feature])/positive_total
        negative_dict[feature] = (1.0 * negative_dict[feature])/negative_total


'''Main'''
true = 0
fake = 0
positive = 0
negative = 0

true_list = []
fake_list = []
positive_list = []
negative_list = []

true_dict = dict()
fake_dict = dict()
positive_dict = dict()
negative_dict = dict()

true_total = 0
fake_total = 0
positive_total = 0
negative_total = 0

tokens = []

stopwords = ["a", "a's", "able", "about", "above", "across", "after", "again", "against", "ain", "ain't", "all",
             "almost", "along", "also", "am", "among", "amongst", "an", "and", "any", "anyhow", "anyone", "anyway",
             "anyways", "appear", "are", "aren", "aren't", "around", "as", "aside", "ask", "asking", "at", "away", "be",
             "became", "because", "become", "becomes", "becoming", "been", "before", "behind", "being", "below",
             "beside", "besides", "between", "beyond", "both", "brief", "but", "by", "came", "can", "come", "comes",
             "consider", "considering", "corresponding", "could", "couldn", "couldn't", "d", "did", "didn", "didn't",
             "do", "does", "doesn", "doesn't", "doing", "don", "don't", "done", "down", "downwards", "during", "each",
             "edu", "eg", "eight", "either", "else", "elsewhere", "etc", "even", "ever", "every", "ex", "few",
             "followed", "following", "follows", "for", "former", "formerly", "from", "further", "furthermore", "get",
             "gets", "getting", "given", "gives", "go", "goes", "going", "gone", "got", "gotten", "had", "hadn",
             "hadn't", "happens", "has", "hasn", "hasn't", "have", "haven", "haven't", "having", "he", "he's", "hed",
             "hence", "her", "here", "here's", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "hi",
             "him", "himself", "his", "how", "hows", "i", "i'd", "i'll", "i'm", "i've", "ie", "if", "in", "inc",
             "indeed", "into", "inward", "is", "isn", "isn't", "it", "it'd", "it'll", "it's", "its", "itself", "just",
             "keep", "keeps", "kept", "know", "known", "knows", "lately", "later", "latter", "latterly", "lest", "let",
             "let's", "ll", "looking", "looks", "ltd", "m", "ma", "may", "maybe", "me", "mean", "meanwhile", "might",
             "mightn", "mightn't", "more", "most", "mustn", "mustn't", "my", "myself", "name", "namely", "nd", "near",
             "nearly", "need", "needn", "needn't", "needs", "neither", "next", "nine", "no", "non", "nor", "not", "now",
             "nowhere", "o", "of", "off", "often", "oh", "ok", "okay", "old", "on", "once", "one", "ones", "only",
             "onto", "or", "other", "others", "ought", "our", "ours", "ourselves", "out", "over", "own", "per",
             "placed", "que", "quite", "re", "regarding", "s", "said", "same", "saw", "say", "saying", "says",
             "second", "secondly", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves",
             "sensible", "sent", "seven", "several", "shan", "shan't", "she", "she'd", "she'll", "she's", "should",
             "should've", "shouldn", "shouldn't", "since", "six", "so", "some", "somebody", "somehow", "someone",
             "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "specified", "specify",
             "specifying", "still", "sub", "such", "sup", "sure", "t", "t's", "take", "taken", "tell", "tends", "th",
             "than", "that", "that'll", "that's", "thats", "the", "their", "theirs", "them", "themselves", "then",
             "thence", "there", "there's", "thereafter", "thereby", "therefore", "therein", "theres", "thereupon",
             "these", "they", "they'd", "they'll", "they're", "they've", "think", "third", "this", "those", "though",
             "three", "through", "thru", "thus", "to", "together", "too", "took", "toward", "towards", "tried", "tries",
             "truly", "try", "trying", "twice", "two", "un", "under", "until", "up", "upon", "us", "use", "used",
             "uses", "using", "usually", "value", "various", "ve", "very", "via", "viz", "vs", "want", "wants", "was",
             "wasn", "wasn't", "way", "we", "we'd", "we'll", "we're", "we've", "went", "were", "weren", "weren't",
             "what", "what's", "whatever", "when", "when's", "whence", "whenever", "where", "where's", "whereafter",
             "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who",
             "who's", "whoever", "whole", "whom", "whose", "why", "why's", "will", "willing", "wish", "with", "within",
             "without", "won", "won't", "would", "wouldn", "wouldn't", "y", "yes", "yet", "you", "you'd", "you'll",
             "you're", "you've", "your", "yours", "yourself", "yourselves", "ull"]

prior_probability = dict()

training_data = codecs.open('train-labeled.txt', 'r', encoding='utf-8')

lines = training_data.readlines()

initial_counts()
count_features()
laplace_smoothing()
calculate_probability()

nb_model_file = codecs.open("nbmodel.txt", "w", encoding='utf-8')
nb_model_file.write("Prior Probabilities\n" + str(prior_probability) + "\n")
nb_model_file.write("True\n" + str(true_dict) + "\n")
nb_model_file.write("Fake\n" + str(fake_dict) + "\n")
nb_model_file.write("Pos\n" + str(positive_dict) + "\n")
nb_model_file.write("Neg\n" + str(negative_dict))
nb_model_file.close()
