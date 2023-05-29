import requests
import json
import matplotlib.pyplot as plt
import numpy as np
import csv
import boto3
import botocore
from datetime import datetime
import pandas as pd

def write_to_file(json_data):
    text_from_bank= [json_data]  
    with open('bank_data_2021.json', 'w') as f:
        for line in text_from_bank:
            f.write(line)
            f.write('\n')  

def print_file_content():
    file = open('bank_data_2021.json','r')
    file_contents = file.read()
    print(file_contents)

def draw_diagram(x ,y):
    plt.plot(x, y)
    plt.xlabel('x - exchange date')
    plt.ylabel('y - rate')
    plt.title('rate 2021')
    plt.show()

url_usd = 'https://bank.gov.ua/NBU_Exchange/exchange_site?start=20210101&end=20211231&valcode=usd&sort=exchangedate&order=desc&json'
usd_json = requests.get(url_usd, allow_redirects=True)

url_eur = 'https://bank.gov.ua/NBU_Exchange/exchange_site?start=20210101&end=20211231&valcode=eur&sort=exchangedate&order=desc&json'
eur_json = requests.get(url_eur, allow_redirects=True)

choose_number =a = int(input("1-Dollar or 2-Euro :"))
if choose_number==1 : 
    write_to_file(usd_json.content.decode('utf-8'))    
elif choose_number==2 :
    write_to_file(eur_json.content.decode('utf-8'))
       
file  = open('bank_data_2021.json','r')
json_data= file.read()

with open('bank_data_2021.json', 'r') as f:
    array_by_date = json.load(f)

exchangedate_array = [] 
rate_array = []

for rate_by_date in array_by_date:
   
    #print(rate_by_date['exchangedate'] ,',' , rate_by_date['rate'])  
    exchangedate_array.append(rate_by_date['exchangedate'])
    rate_array.append(rate_by_date['rate'])

with open('eur_rate_2021.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(exchangedate_array)
    writer.writerow(rate_array)

draw_diagram(exchangedate_array, rate_array )

s3 = boto3.resource('s3')
data = open('eur_rate_2021.csv', 'rb')
s3.Bucket('bobernatalia-bucket').put_object(Key='eur_rate_2021.csv', Body=data)

#bucket_name = 'bobernatalia-bucket'
#object_key = 'eur_rate_2021.csv'
#s3.Bucket(bucket_name).upload_file('eur_rate_2021.csv', object_key)
