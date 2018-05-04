import re
import sys
import codecs
import math


def get_probability_parameters():
    global prior_probabilities, true_probability, fake_probability, positive_probability, negative_probability
    nb_model_file = codecs.open('nbmodel.txt', 'r', encoding='utf-8')
    line_no = 0
    for line in nb_model_file:
        if line_no == 1:
            prior_probabilities = eval(line)
        elif line_no == 3:
            true_probability = eval(line)
        elif line_no == 5:
            fake_probability = eval(line)
        elif line_no == 7:
            positive_probability = eval(line)
        elif line_no == 9:
            negative_probability = eval(line)

        line_no += 1


def classify_review():
    nb_output_file = codecs.open("nboutput.txt", "w", encoding='utf-8')

    pattern_regex = r'[~@#$%&.?\-"/;:,!(){}*^+=|<>_]+'

    for line in lines:
        true = math.log(prior_probabilities["True"])
        fake = math.log(prior_probabilities["Fake"])
        pos = math.log(prior_probabilities["Pos"])
        neg = math.log(prior_probabilities["Neg"])

        reviews = line.rstrip().split(" ", 1)
        reviews[1] = reviews[1].lower()
        patterns_list = re.findall(pattern_regex, reviews[1])

        for pattern in patterns_list:
            reviews[1] = reviews[1].replace(pattern, " ")

        reviews[1] = reviews[1].replace("[", " ").replace("]", " ")

        word = filter(None, reviews[1].split(" "))
        for token in word:
            if token in true_probability:
                true += math.log(true_probability[token])
            if token in fake_probability:
                fake += math.log(fake_probability[token])
            if token in positive_probability:
                pos += math.log(positive_probability[token])
            if token in negative_probability:
                neg += math.log(negative_probability[token])

        if true > fake:
            nb_output_file.write(str(reviews[0]) + " True ")
        else:
            nb_output_file.write(str(reviews[0]) + " Fake ")

        if pos > neg:
            nb_output_file.write("Pos\n")
        else:
            nb_output_file.write("Neg\n")

    nb_output_file.close()


'''Main'''
prior_probabilities = dict()
true_probability = dict()
fake_probability = dict()
positive_probability = dict()
negative_probability = dict()

get_probability_parameters()

dev_text_file = codecs.open('dev-text.txt', 'r', encoding='utf-8')

lines = dev_text_file.readlines()
classify_review()
