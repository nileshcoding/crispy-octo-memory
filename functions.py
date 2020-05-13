import csv

def read(path):
    file_hand = open(path,'r')
    csv_reader = csv.DictReader(file_hand)
    li = []
    for row in csv_reader:
        li.append(row)
    file_hand.close()
    return li

def append_row(path,header,value):
    file_hand = open(path,'a',newline='\n')
    csv_writer = csv.DictWriter(file_hand,fieldnames = header)
    csv_writer.writerow(value)
    file_hand.close()

def overwrite_file(path,li):
    file_hand = open(path,'w',newline = '\n')
    header = li[0].keys()
    csv_writer = csv.DictWriter(file_hand,fieldnames = header)
    csv_writer.writeheader()
    csv_writer.writerows(li)
    file_hand.close()     