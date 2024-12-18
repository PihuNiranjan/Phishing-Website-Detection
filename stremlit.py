import streamlit as st
page_bg_img = '''
<style>
body {
background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
background-size: cover;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)
st.title("Phishing-Website-Detection-by-Machine-Learning-Techniques-master")
url = st.text_input('Enter Your Url...')



# ----------------------------feature extraction--------------------------------------
from urllib.parse import urlparse,urlencode
import ipaddress
import re

# 1.Domain of the URL (Domain) 
def getDomain(url):  
  domain = urlparse(url).netloc
  if re.match(r"^www.",domain):
    domain = domain.replace("www.","")
  return domain


# 2.Checks for IP address in URL (Have_IP)
def havingIP(url):
  print("check for ipaddress")
  try:
    print(ipaddress.ip_address(url))
    ipaddress.ip_address(url)
    ip = 1
  except:
    ip = 0
  return ip

# 3.Checks the presence of @ in URL (Have_At)
def haveAtSign(url):
  
  if "@" in url:
    at = 1    
  else:
    at = 0    
  return at

# 4.Finding the length of URL and categorizing (URL_Length)
def getLength(url):
  
  if len(url) < 54:
    length = 0            
  else:
    length = 1            
  return length

# 5.Gives number of '/' in URL (URL_Depth)
def getDepth(url):

  s = urlparse(url).path.split('/')
  depth = 0
  for j in range(len(s)):
    if len(s[j]) != 0:
      depth = depth+1
  return depth

# 6.Checking for redirection '//' in the url (Redirection)
def redirection(url):
  
  pos = url.rfind('//')
  if pos > 6:
    if pos > 7:
      return 1
    else:
      return 0
  else:
    return 0
  
  # 7.Existence of “HTTPS” Token in the Domain Part of the URL (https_Domain)
def httpDomain(url):
  domain = urlparse(url).scheme
  
  print(domain)
  if 'https' in domain:
    return 0
  else:
    return 1
  
#listing shortening services
shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                      r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                      r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                      r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                      r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                      r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                      r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                      r"tr\.im|link\.zip\.net"

# 8. Checking for Shortening Services in URL (Tiny_URL)
def tinyURL(url):
    match=re.search(shortening_services,url)
    
    if match:
        return 1
    else:
        return 0
    
# 9.Checking for Prefix or Suffix Separated by (-) in the Domain (Prefix/Suffix)
def prefixSuffix(url):
    
    if '-' in urlparse(url).netloc:
        return 1            # phishing
    else:
        return 0            # legitimate


# from bs4 import BeautifulSoup
import whois

import urllib.request
from datetime import datetime
    


# 13.Survival time of domain: The difference between termination time and creation time (Domain_Age)  
def domainAge(domain_name):
 
  creation_date = domain_name.creation_date
  expiration_date = domain_name.expiration_date
  if (isinstance(creation_date,str) or isinstance(expiration_date,str)):
    try:
      creation_date = datetime.strptime(creation_date,'%Y-%m-%d')
      expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
    except:
      return 1
  if ((expiration_date is None) or (creation_date is None)):
      return 1
  elif ((type(expiration_date) is list) or (type(creation_date) is list)):
      return 1
  else:
    ageofdomain = abs((expiration_date - creation_date).days)
    if ((ageofdomain/30) < 6):
      age = 1
    else:
      age = 0
  return age

# 14.End time of domain: The difference between termination time and current time (Domain_End) 
def domainEnd(domain_name):
 
  expiration_date = domain_name.expiration_date
  if isinstance(expiration_date,str):
    try:
      expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
    except:
      return 1
  if (expiration_date is None):
      return 1
  elif (type(expiration_date) is list):
      return 1
  else:
    today = datetime.now()
    end = abs((expiration_date - today).days)
    if ((end/30) < 6):
      end = 0
    else:
      end = 1
  return end

import requests

# 15. IFrame Redirection (iFrame)
def iframe(response):
 
  if response == "":
      return 1
  else:
      if re.findall(r"[<iframe>|<frameBorder>]", response.text):
          return 0
      else:
          return 1

# 16.Checks the effect of mouse over on status bar (Mouse_Over)
def mouseOver(response): 

  if response == "" :
    return 1
  else:
    if re.findall("<script>.+onmouseover.+</script>", response.text):
      return 1
    else:
      return 0

# 17.Checks the status of the right click attribute (Right_Click)
def rightClick(response):
  
  if response == "":
    return 1
  else:
    if re.findall(r"event.button ?== ?2", response.text):
      return 0
    else:
      return 1


# 18.Checks the number of forwardings (Web_Forwards)    
def forwarding(response):
  
  if response == "":
    return 1
  else:
    if len(response.history) <= 2:
      return 0
    else:
      return 1

#Function to extract features
def featureExtraction(url):

  features = []
  #Address bar based features (10)
#   features.append(getDomain(url))
  features.append(havingIP(url))  #1
  features.append(haveAtSign(url)) #2
  features.append(getLength(url))  #3
  features.append(getDepth(url))   #4
  features.append(redirection(url))   #5
  features.append(httpDomain(url))  #6
  features.append(tinyURL(url))   #7
  features.append(prefixSuffix(url))    #8
  
  #Domain based features (4)
  dns = 0
  try:
    domain_name = whois.whois(urlparse(url).netloc)
  except:
    dns = 1
  print(dns)
  features.append(dns)   #9
  # features.append(web_traffic(url))
  features.append(1 if dns == 1 else domainAge(domain_name))   #10
  features.append(1 if dns == 1 else domainEnd(domain_name))   #11
  
  # HTML & Javascript based features (4)
  try:
    response = requests.get(url)
  except:
    response = ""
  print(" this is response : ",response)
  features.append(iframe(response))     #12
  features.append(mouseOver(response))   #13
  features.append(rightClick(response))   #14  
  features.append(forwarding(response))   #15
#   features.append(label)
  import numpy as np


  array_2d = np.array(features).reshape(1, -1)
  print(array_2d)
  # array_2d = array.reshape(-1, 1)
  return array_2d
  # test = []
  # return test

# modle test and train
import pandas as pd
data = pd.read_csv('DataFiles/5.urldata.csv')
data = data.drop(['Domain'], axis = 1).copy()
data = data.drop(['Web_Traffic'], axis = 1).copy()
data = data.sample(frac=1).reset_index(drop=True)
y = data['Label']
X = data.drop('Label',axis=1)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y,                                               test_size = 0.4, random_state = 12)

# from sklearn.neighbors import KNeighborsClassifier

# k = 3  # Number of neighbors
# knn = KNeighborsClassifier(n_neighbors=k)

# # Fit the model on training data
# knn.fit(X_train, y_train)
# # Predict on test data
# y_pred_test = knn.predict(X_test)
# y_pred_train = knn.predict(X_train)
#XGBoost Classification model
from xgboost import XGBClassifier

# instantiate the model
xgb = XGBClassifier(learning_rate=0.4,max_depth=7)
#fit the model
xgb.fit(X_train, y_train)
y_pred_test = xgb.predict(X_test)
y_pred_train = xgb.predict(X_train)
from sklearn.metrics import accuracy_score
#computing the accuracy of the model performance
acc_train_knn = accuracy_score(y_train,y_pred_train)
acc_test_knn = accuracy_score(y_test,y_pred_test)

print("KNN: Accuracy on training Data: {:.3f}".format(acc_train_knn))
print("KNN : Accuracy on test Data: {:.3f}".format(acc_test_knn))




# save XGBoost model to file
import pickle
pickle.dump(xgb, open("XGBoostClassifier.pickle.dat", "wb"))
# load model from file
loaded_model = pickle.load(open("XGBoostClassifier.pickle.dat", "rb"))
userinput = featureExtraction(url)
feature_names = [
    "Have_IP", "Have_At", "URL_Length", "URL_Depth", "Redirection",
    "https_Domain", "TinyURL", "Prefix/Suffix", "DNS_Record", 
    "Domain_Age", "Domain_End", "iFrame", "Mouse_Over", "Right_Click", "Web_Forwards"
]

test = pd.DataFrame(userinput,  # Adjust values as per your test case
    columns=feature_names)
# test = pd.DataFrame([[0,0,	1,	1,	0,	0,	0,	0,	0,	1,	1,	0,	0,	1,	0	]],  # Adjust values as per your test case
#     columns=feature_names)
y_pred = loaded_model.predict(test)


# if y_pred[0]==0:
if userinput.sum()<=3:
  st.subheader("This is :green[Legit Website]")
else:
  st.subheader("This is :red[Phishing Website]")
