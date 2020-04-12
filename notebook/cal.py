import pandas as pd
from datetime import datetime
import re
files = ['悲伤.xlsx','愤怒.xlsx','焦虑.xlsx','恐慌.xlsx','恐惧.xlsx','快乐.xlsx','乐观.xlsx','平静.xlsx','无助.xlsx','压力.xlsx','抑郁.xlsx']
a = {}
for file in files:
    a[file[:-5]] = pd.read_excel('~/ftp/心理词表/'+file)[0].iloc[:400].dropna(how='any').tolist()
for key, value in a.items():
    print(key)
    import pymongo
    from tqdm import tqdm
    client = pymongo.MongoClient('localhost',27017)
    co = client.Weibo_Local_Db.comment
    pat = '|'.join(value)

    for x in tqdm(co.find({"comment_context":{"$regex":pat},"update_time":{"$gte":datetime(2020,4,10,12)}},{'comment_context':1})):
        pat_answer = ','.join(sorted(list(set(re.findall(pat,x['comment_context'])))))
        co.update({'_id':x['_id']},{'$set':{key:pat_answer}})
