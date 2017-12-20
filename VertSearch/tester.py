from queryProcessing_and_Ranking import QueryProcessing

def getdata(query):
    Processing = QueryProcessing()
    ranked_list = Processing.getDataFromQuery(query)
    return ranked_list


data = getdata('"dry brew"')
print( data )
