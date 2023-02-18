import streamlit as st
import base64,PyPDF2
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords



st.title('MNC Resume ATS Cracker 📃')

file = st.file_uploader('Upload your resume here (.pdf only)',['.pdf'],accept_multiple_files=False)

def pdf_viewer(file_path):
    with open(save_pdf,'rb') as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.sidebar.markdown(pdf_display, unsafe_allow_html=True)
    

stop_words = set(stopwords.words("english")+['``',"''"])

def cleanText(resumeText):
    resumeText = re.sub("http/S+/s*", '', resumeText)
    resumeText = re.sub('RT|cc', ' ', resumeText)  # remove RT and cc
    resumeText = re.sub('#\S+', '', resumeText)  # remove hashtags
    resumeText = re.sub('@\S+', '  ', resumeText)  # remove mentions
    resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', resumeText)  # remove punctuations
    resumeText = re.sub(r'[^\x00-\x7f]',r' ', resumeText) 
    resumeText = re.sub('\s+', ' ', resumeText)
    resumeText = re.sub(r'[0-9]', "", resumeText)
    return resumeText

def data_extracttor(fp):
    global score

    pdf = PyPDF2.PdfReader(fp)

    st.write('_____________________________________________________________________________')
    # taking out the title or name from pdf
    data = pdf.metadata
    st.header(f'Hi, {data.title}')
    
    # counting the number of pages and scoring based on that 
    numofpg = len(pdf.pages)
    if numofpg == 1:
        score += 1
        st.subheader("Looks like, you're Fresher. But your length of resume is good ")
    elif numofpg <= 3:
        score += 1
        st.subheader("Looks like, you got some Experience ")
    else:
        st.subheader("Your Resume is Quite Lengthy ")
        score -= 1

    text = ''
    for i in range(numofpg):
         
        text += pdf.pages[i].extract_text()
    
    return text 



if file:
    
    save_pdf = './uploaded resumes/'+ file.name 

    with open(save_pdf,'wb') as sa:
        sa.write(file.getbuffer())

    pdf_viewer(save_pdf)
    
    score = 0
    text = data_extracttor(save_pdf)
    
    # Data Cleaning Part start from here ! 
    data = []
    clean_data = ""
    for i in text:
        temp_data = cleanText(i)
        clean_data += temp_data
        words = word_tokenize(clean_data)
        print(words)
        
    for j in words:
        if j not in stop_words:
            data.append(j)

    full_data = " ".join(data)
    st.write(full_data)
        
        # if words not in stop_words:
        #     data.append(words)
            
    # full_data = " ".join(words)
    # st.write(full_data)
            
            
    
    
    

   
    
    
    
    
    
    
    
    
