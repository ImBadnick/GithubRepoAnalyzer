from RepoAnalyzer import *
from DisplayStats import displayStats

if __name__ == "__main__":
    #Load the config data
    with open('../ConfigFiles/config.json') as json_file:
        data = json.load(json_file)
        user = data['githubUser']
        access_token = data['githubAccessToken']

    menu = {}
    menu['1']="AddRepository to analyze" 
    menu['2']="Analyze data of the repositories"
    menu['3']="Show the chart of stats"
    menu['0']="EXIT"

    options=menu.keys()
    for entry in options: 
        print(entry, menu[entry])

    selection=input("Please Select: ") 
    if selection =='1': addRepo()
    elif selection == '2': analyzeData(user,access_token)
    elif selection == '3': 
        repoName = input("Insert repo to displayStats: ")
        displayStats(repoName)
        
    elif selection == '0': print("Program terminated")
    else: print ("Unknown Option Selected!") 
    
        
        
    