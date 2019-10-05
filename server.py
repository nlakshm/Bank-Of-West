from flask import Flask,render_template, request,json
from textblob import TextBlob
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"


@app.route('/signUpUser', methods=['GET','POST'])
def signUpUser():
    dct ={}
    dctc= {}
    if request.method == 'POST':
        test = [""]
        test[0] =  request.form['username'];
        test = clean(test)

        print(test)
        visited = []
        ans = (getInit(test))
        visited.append(ans)
        resultSet = []
        commentSet = []
        print(ans)
        dfs(ans, test, visited, resultSet, commentSet)
        
        for i in range(0,len(resultSet)):
            dct[i] = resultSet[i]
            print()

        for i in range(0,len(commentSet)):
            dctc[i] =commentSet[i]
            print()    
  
    return json.dumps({"rs":dct,"cs":dctc})

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
        predictions = classifier.predict(feature_vector_valid)

        return predictions

def predict(train, test, label):
    encoder = preprocessing.LabelEncoder()
    label = encoder.fit_transform(label)



    count_vect = CountVectorizer(analyzer='word', token_pattern=r'\w{1,}')
    count_vect.fit(train)


    xtrain_count =  count_vect.transform(train)
    xvalid_count =  count_vect.transform(test)


    

    prediction = train_model(naive_bayes.MultinomialNB(), xtrain_count, label, xvalid_count)
    return prediction[0]   

def alterTest(test, fileName):
    newTest =""
    for word in test[0].split(" "):
        if len(word) > 0:
            if word != fileName:
                newTest = newTest + " " +word 
    test[0] = newTest
    return test


def addTestInput(test, key):
    newTest = [" "]
    newTest[0] = test[0]
    if "-" in key:
        prev = key.split("-")
        key = prev[0]
        newTest[0] = newTest[0] +" "+ prev[1]
    return key,newTest
    
    
def addCommments(commentSet, fileName):
    file = open(fileName,"r")
    for line in file.readlines():
        blob =TextBlob(line)
        print(line)
        print(blob.sentiment.polarity)
        if blob.sentiment.polarity >= 0:
            commentSet.append(line)


def dfs(fileName, test,  visited, resultSet, commentSet):
    file = open(fileName,"r")
    inc = 0

    data = []

    train = []
    label = []

    for line in file.readlines():    
        train.append(line)
        label.append(inc)
        data.append(line)
        inc = inc + 1
   

    train = clean(train)
    answer = data[predict(train, test, label)]
    resultSet.append(answer)
    test = alterTest(test, fileName)
   
    if "keys" in answer:
        start_index = answer.find("keys") + len("keys")
        end_index = len(answer)
        
        keys = (answer[start_index:end_index].split(","))
        
        for key in keys:
            if len(key) > 0:
                key, newTest = addTestInput(test, key)
                key = key.rstrip().replace(" ","")
                if key not in visited:
                    visited.append(key)
                    if "comments" in key:
                        addCommments(commentSet, key)
                    else:    
                        dfs(key, newTest, visited, resultSet, commentSet)    

def getInit(test):
    files= ["finance","loan","property","rv_faq","home_faq","women"]
    train = []
    label = []
    for file in range(0, len(files)):
        f = open(files[file],"r")

        for line in f.readlines():
            if "keys" in line:
                start_index = line.find("keys") + len("keys")
                line = line[0:start_index]
            train.append(line)
            label.append(file)
        f.close()
    train = clean(train)
    answer = files[predict(train, test, label)]
    return answer




if __name__=="__main__":
    app.run()