import os
from tika import parser
from flask import Flask,abort,render_template,request,redirect,url_for,jsonify
import pandas as pd
import re
import string


app = Flask(__name__)

@app.route('/',methods = ['POST', 'GET'])
def TextExtraction():  
    result=request.args['name']

    Path=[]
    label=[]
    for root, dirs, files in os.walk(result):
        for file in files:
            if file.endswith(".pdf"):
                filePath=os.path.join(root, file)
                filename=file
                fileLabel=filename.split(".")
                label.append(fileLabel[0])
                parsed = parser.from_file(filePath)
                pdfnewContent=parsed["content"]
                pdfnewContent = re.sub("@\S+", " ", pdfnewContent)
                pdfnewContent = re.sub("#\S+", " ", pdfnewContent)
                pdfnewContent= re.sub("\'\w+", '', pdfnewContent)
                xpdfnewContent= re.sub('[%s]' % re.escape(string.punctuation), ' ', pdfnewContent)
                pdfnewContent = re.sub(r'\w*\d+\w*', '', pdfnewContent)
                pdfnewContent = re.sub('\s{2,}', " ", pdfnewContent)
                Path.append(pdfnewContent)          
                
    df_prediction=pd.DataFrame(columns=['PdfText'])
    df_prediction['articleText']=Path
    df_prediction['DocType']= label
    print(df_prediction)
    result = df_prediction.to_json(orient="records")
    return result
    
if __name__ == "__main__":
     app.debug = True
     app.run()
