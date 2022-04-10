

def cleanScores(unformatted_score):
    '''
    remove unwanted formatting from scores
    '''
    import re

    scsplit = re.split('/',unformatted_score)
    score = float(scsplit[0] /  scsplit[1]) ### Split and format
    
    return score


