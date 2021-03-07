from smtplib import SMTP_SSL, SMTPException
import random

def make_data_dict(file):
    f = open(file, "r")
    data = f.read().split('\n')
    f.close()
    data_list = []
    for d in data:
        data_list.append(d.split(','))

    number = len(data_list)

    student_address = []
    for i in range(number):
        student_address.append(data_list[i].pop(0))
    
    del student_address[-1]

    data_keys =  ["last_name", "first_name", "score1", "comment1", "score2", "comment2", "score3", "comment3"]
    list_of_dict = []
    for i in range(number):
        list_of_dict.append(dict(zip(data_keys, data_list[i])))
    
    return dict(zip(student_address, list_of_dict))

def send_mail(file):
    data_dictionary = make_data_dict(file)
    server = SMTP_SSL("smtp.mail.yahoo.co.jp", 465)
    choice = random.randint(0, len(data_dictionary) - 1)
    count = 0
    try:
        server.login("mailtestfor_man", "Umauma#7532")
        
    except SMTPException as err:
        print(err)
        exit(1)

    fromaddr = "mailtestfor_man@yahoo.co.jp"

    for key, item in data_dictionary.items():
        toaddr = key
        msg = "Dear {0[first_name]}, Your score for the book assignment is broken down below by question number\n\n".format(item)

        scores = "1. {0[score1]} %: {0[comment1]}\n2. {0[score2]} %: {0[comment2]}\n3. {0[score3]} %: {0[comment3]}\n\n".format(item)
        messages = "From: {0}\r\n To: {1}\r\n\r\n".format(fromaddr, toaddr) + msg + scores
        
        chosen_msg = "You've been randomly chosen to present a summary of the book in the next class. Looking forward to it!"

        if count == choice:
            messages = messages + chosen_msg
            print("{0[first_name]} was chosen\n".format(item))
        try:
            server.sendmail(fromaddr, toaddr, messages)
        except SMTPException as err:
            print(err)

        count += 1
