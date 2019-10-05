from flask import Flask,render_template, request,json
app = Flask(__name__)
stopWords = ["as","if","need","required","and","take","to","there","here","youll","dont","cant","tomorrow","for","w","your","their","them","have","about","on","in","after","his","her","the","is","you","will","would","could","can","also","another","other","we","our","yours","ourselves","theirs","how","why","when","who","todays","tomorrowss","than","more","less","by","it's","get","we've" ,"types" ,"all","here","at","only","now","next","with","while","where","whom","so","ever","&","of","a","like","via","going","got","do","new","an","us","or","this","shes", 'its', "couldnt", 'we', 'through', 'should', 'on', 'now', 'she', 'until', 'here', 'or', 'shouldnt', 'than', 're', 'under', 'by', 'will', 'to', "isnt", 'nor', 'out', 'can', 'yours', 'both', 'what', 'few', 'that', 'myself', 'an', 'o', 'if', 'ma', 'over', 'does', 'down', 'too', 'at', 'same', 'i', 'her', 'been', 'aren', 'about', 'there', 'didn', 'am', "didnt", 'some', 'between', 'the', 'had', 'he', 'couldn', 'our', 'up', 'not', 'himself', 'mightn', 'very', 'a', "shouldnt", 'having', 'doesn', 'ain', "shant", 'did', 'do', 'isn', "thatll", 'are', 'ourselves', "wont", "mustnt", 'during', 'his', 'wouldn', 'other', 'has', 'him', 'don', 'then', 'is', "hasnt", 'their', 'this', 'll', "doesnt", 'just', "neednt", 'it', "wasnt", "shouldve", "off", "once", "y", "hasnt", "because", "ve", "m", "yourself", "them", "most", "youll", "weren", "theirs", 'as', 'against', 'which', "youre", 'ours', 'you', 'so', 'in', 'with', 'below', 'needn', 'where', 'haven', 'such', 'wasn', "hadnt", "youd", "its", 'how', 'when', 'was', "wouldnt", 'again', 'these', 'after', 'why', "hadnt", 'be', 'who', 'yourselves', 'and', "arent", 't', 'd', 'were', 'whom', 'your', 'my', 'won', 'of', 'for', "werent", 'themselves', 'me', 'more', "dont", 'shan', 'those', 'being', 'own', 'all', 'hers', 'further', 'mustn', 'into', "youve", 'above', 'no', 'each', 'from', 'herself', "havent", 'before', 'doing', 'they', 'have', "any", "but", "only", "while", "s", 'itself', "mightnt","able","go","may","use"]
def clean(lst):
    for i in range(0, len(lst)):
        doc = lst[i]
        doc = doc.replace(".","").replace(":","").replace("?","").replace(",","").replace("(","").replace(")","").replace("'","").replace("!","").replace("#","").replace("@","").replace("-"," ").replace("$"," ").replace("-"," ")

        sb = ""

        for word in doc.split(" "):
            word = word.lower()
            if word not in stopWords and len(word) > 0 and not word.isdigit():
                sb += word + " "      
        lst[i] = sb
    return lst  
from sklearn import model_selection, preprocessing, linear_model, naive_bayes, metrics, svm
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import decomposition, ensemble

def train_model(classifier, feature_vector_train, label, feature_vector_valid):

        classifier.fit(feature_vector_train, label)
        predictions = classifier.predict_proba(feature_vector_valid)

        return predictions

def predict(train, test, label):
    encoder = preprocessing.LabelEncoder()
    label = encoder.fit_transform(label)

    count_vect = CountVectorizer(analyzer='word', token_pattern=r'\w{1,}')
    count_vect.fit(train)

    xtrain_count =  count_vect.transform(train)
    xvalid_count =  count_vect.transform(test)

    predictions = train_model(naive_bayes.MultinomialNB(), xtrain_count, label, xvalid_count)
    return predictions    

@app.route('/pair', methods=['GET','POST'])
def signUpUser():
    if request.method == 'POST':
        test = [""]
        test[0] =  request.form['username'];
        test = clean(test)

        train = []
        dct ={"0":"Nachiappan","1":"Madhu","2":"Chandan","3":"Harsh","4":"Chandu"}
        label = []

        file  = open("search","r")
        inc = 0
        x = 1 
        for line in file.readlines():
            train.append(line)    
            label.append(inc)
            x = x + 1
            if x%10 == 0:
                inc = inc +1

        train = clean(train)


        ans = 0
        rs = {}
        for i in (predict(train,test,label))[0]:
            if i > 0.5:
                print(dct[str(ans)])
                rs[ans] = dct[str(ans)]
                
            ans = ans + 1
        print(rs)    
        return json.dumps(rs)

if __name__=="__main__":
    app.run()        
