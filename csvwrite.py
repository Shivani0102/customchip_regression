import csv
from pathlib import Path

file = Path(r"C:\Users\Fleek\PycharmProjects\customchip_regression\datanoncld_test.csv")


# class Element:
def read_csv(filename, key):
    '''This creates a keyword named "Read CSV File"

    This keyword takes one argument, which is a path to a .csv file. It
    returns a list of rows, with each row being a list of the data in
    each column.
    '''
    data = []
    with open(filename, 'r') as csvfile:
        (reader) = csv.reader(csvfile)
        for row in reader:
            # data.append(row)
            if (row[0] == key):
                print(str(row[1]))
                return str(row[1])


# a=Element()
# new_data = a.read_csv("data.csv", "password")
# print("is",new_data)


def write_csv(time):
    print(time)

    with open(file, 'a', newline="") as csvFile:
        writer = csv.writer(csvFile)
        # reader = csv.reader(csvreader)

        # all = []
        # row = []
        # row.append(name)
        # row.append(time)

        writer.writerow(time)
