'''
File contains functions for cleaning the raw data from Beer Advocate

'''

def cleanDigits(unformatted_score):
    '''
    remove unwanted formatting from scores
    '''
    import re

    scsplit = re.split('/',unformatted_score)
    ## If there was character to split on, normalize it
    if len(scsplit) > 1:
        score = float(scsplit[0]) /  float(scsplit[1]) ### Split and format
    
    return score

def cleanText(unformatted_text):
    '''
    remove non-utc characters from text
    '''
    f_text = unformatted_text.strip()

    ## !!! How to fix style specialization to read right, not just 

    return text

def cleanString(unformatted_text):
    '''
    Function to be applied across all data loaded
        Cleans character data of non utf-8 characters
        Fixes Score data to read as percentage, rather than '9/10' str
    '''
    import re
    
    #test if string has character text
    if re.match('\w+',unformatted_text):
        #if so, edit for text
        form_text = cleanText(unformatted_text)
    else:
        form_text = cleanDigits(unformatted_text)

    return form_text





