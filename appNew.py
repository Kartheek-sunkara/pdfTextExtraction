import os
from tika import parser
from flask import Flask,abort,render_template,request,redirect,url_for,jsonify
import pandas as pd
import re
import string
import time



app = Flask(__name__)



@app.route('/',methods = ['POST', 'GET'])
def TextExtraction():  
    result=request.args['name']

    Path=[]
    label=[]
    
    #timestr = time.strftime("%Y_%m_%d-%H_%M_%S")
    timestr = time.strftime("%d-%H_%M")
    directory = "DocumentClassification"+"_"+timestr
    parent_dir = "D:/"
    path = os.path.join(parent_dir, directory)
    print(path)
    os.mkdir(path)
    for root, dirs, files in os.walk(result):
        for file in files:
            if file.endswith(".pdf"):
                filePath=os.path.join(root, file)
                filename=file
                fileLabel=filename.split("_")
                stringword=str(fileLabel[1])
                stringfilesplitLabel=stringword.split(".")
                label.append(stringfilesplitLabel[0])
                parsed = parser.from_file(filePath)
                pdfnewContent=parsed["content"]
                pdfnewContent = re.sub("@\S+", " ", pdfnewContent)
                pdfnewContent = re.sub("#\S+", " ", pdfnewContent)
                pdfnewContent= re.sub("\'\w+", '', pdfnewContent)
                xpdfnewContent= re.sub('[%s]' % re.escape(string.punctuation), ' ', pdfnewContent)
                pdfnewContent = re.sub(r'\w*\d+\w*', '', pdfnewContent)
                pdfnewContent = re.sub('\s{2,}', " ", pdfnewContent)
                Path.append(pdfnewContent)          
                
    df=pd.DataFrame()
    df['articleText']=Path
    df['DocType']= label
    df.to_csv(path+"/dataset.csv")
    result = df.to_json(orient="records")
    return result
    
if __name__ == "__main__":
     app.debug = True
     app.run()
