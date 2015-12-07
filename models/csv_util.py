import csv
import os

def csv_to_dict():
    print os.getcwd()
    with open('applications/liub/uploads/2013.csv', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        new_user_dict = []
        header = next(spamreader)
        for row in spamreader:
            entry = {}
            for id, val in enumerate(row):
                entry[header[id]] = val
            new_user_dict.append(entry)
    print new_user_dict
    return new_user_dict