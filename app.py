import os
from tika import parser
from flask import Flask,abort,render_template,request,redirect,url_for,jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/',methods = ['POST', 'GET'])
def TextExtraction():  
    result=request.args['name']

    Path=[]
    for root, dirs, files in os.walk(result):
        for file in files:
            if file.endswith(".pdf"):
                filePath=os.path.join(root, file)
                parsed = parser.from_file(filePath)
                pdfnewContent=parsed["content"]
                Path.append(pdfnewContent)          
                
    df_prediction=pd.DataFrame(columns=['PdfText'])
    df_prediction['PdfText']=Path
    #df_prediction['pred']= preds
    print(df_prediction)
    result = df_prediction.to_json(orient="records")
    return result
    
if __name__ == "__main__":
     app.debug = True
     app.run()
