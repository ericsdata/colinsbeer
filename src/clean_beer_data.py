'''
Module to hold functions designed to clean the source data
    Text and rating info


'''

## Fix the rating format
def adjustOverallScore(unformatted_score):
    '''
    Function removes '/20/ from text field and normalizes to 0 - 1 scale
    '''
    score = float(unformatted_score.split('/20')[0]) / 20 ### Split and format
    return score

def adjustOverallScore_rounddown(unformatted_score):
    score = float(unformatted_score.split('/20')[0]) / 20 ### Split and format
    return int(round(score*10,0))