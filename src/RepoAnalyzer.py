from github import GithubException
from github import Github
import json
import datetime

#Converts a datatime object to string (Used for serialization!)
def myconverter(o):
    if isinstance(o, datetime.date):
        return "{}-{}-{} {}:{}:{}".format(o.strftime("%Y"), o.strftime("%m"), o.strftime("%d"),o.strftime("%H"),o.strftime("%M"),o.strftime("%S"))


def analyzeData(user,access_token):
    g = Github(access_token) #Creates github object
    
    #Load json repo file
    with open('../ConfigFiles/repo.json','r') as json_file:
        try:
            data = json.load(json_file)
        except json.decoder.JSONDecodeError:
            print('Repo list not found')
            exit(0)
            
    repoNotFound = [] #Saves the repo that are not found in the repo user list
    test = False #Used to check if a repo was not found
    
    for repository in data: #Foreach repo in the list, get traffic info and save them
        try:
            repo = g.get_repo(user + '/' + repository) #Repo
            traffic = repo.get_views_traffic() #Traffic info
            clones = repo.get_clones_traffic() #Clones info
            #File used to save traffic info of the repositories
            with open('../RepoData.json','r') as json_file:
                try:
                    repoDatas = json.load(json_file)
                except json.decoder.JSONDecodeError:
                    repoDatas = {
                        "Repo":[ ]
                    }
                    with open('../RepoData.json','w') as writeFile:
                         json.dump(repoDatas, writeFile,indent=4)
            
            toAdd = False #Used to check if a repo was not found in the list of repositories that had already traffic info saved
            addDatesView = [] #Dates that are not already saved to add
            addDatesClone = []
            #Check if the repo has already traffic info saved
            for repoData in repoDatas['Repo']: 
                name = repoData['Name']
                if(repo.name == name): #If it has then check which dates program needs to save
                    if not repoData['Stats']['views']:
                        for view in traffic['views']:
                            element = {}
                            element['uniques'] = view.uniques
                            element['timestamp'] = myconverter(view.timestamp)
                            element['count'] = view.count
                            addDatesView.append(element)
                    else:
                        lastUpdate = repoData['Stats']['views'][-1]['timestamp'] 
                        for view in traffic['views']:
                            if datetime.datetime.strptime(lastUpdate, '%Y-%m-%d %H:%M:%S')<view.timestamp:
                                element = {}
                                element['uniques'] = view.uniques
                                element['timestamp'] = myconverter(view.timestamp)
                                element['count'] = view.count
                                addDatesView.append(element)
                    
                    if not repoData['Stats']['clones']:
                        for clone in clones['clones']:
                            element = {}
                            element['uniques'] = clone.uniques
                            element['timestamp'] = myconverter(clone.timestamp)
                            element['count'] = clone.count
                            addDatesClone.append(element)
                    else:
                        lastUpdate = repoData['Stats']['clones'][-1]['timestamp'] 
                        for clone in clones['clones']:
                            if datetime.datetime.strptime(lastUpdate, '%Y-%m-%d %H:%M:%S')<clone.timestamp:
                                element = {}
                                element['uniques'] = clone.uniques
                                element['timestamp'] = myconverter(clone.timestamp)
                                element['count'] = clone.count
                                addDatesClone.append(element)
                    
                    toAdd = True
            
               
            #If the repo hasnt already traffic info saved -> addes the repo name and the all the traffic info
            if(not toAdd):
                viewsList = []
                clonesList = []
                for value in traffic['views']:
                    element = {}
                    element['uniques'] = value.uniques
                    element['timestamp'] = myconverter(value.timestamp)
                    element['count'] = value.count
                    viewsList.append(element)
                for value in clones['clones']:
                    element = {}
                    element['uniques'] = value.uniques
                    element['timestamp'] = myconverter(value.timestamp)
                    element['count'] = value.count
                    clonesList.append(element)
                newData = {
                            "Name" : repo.name,
                            "Stats": 
                                {
                                    "views"  : viewsList,
                                    "clones" : clonesList
                                }
                          }
                repoDatas['Repo'].append(newData)
                with open('../RepoData.json','w') as writeFile:
                    json.dump(repoDatas, writeFile,indent=4)
                    
            #If the repo has already traffic info saved 
            else:
                for repoData in repoDatas['Repo']:
                    name = repoData['Name']
                    if(repo.name == name):
                        repoData['Stats']['views'].extend(addDatesView) #Addes the new traffic info
                        repoData['Stats']['clones'].extend(addDatesClone)
                        with open('../RepoData.json','w') as writeFile:
                            json.dump(repoDatas, writeFile,indent=4)
        except GithubException: #If repo not found in the account
            test = True
            print("Repo not found, repo will be deleted from the list")
            repoNotFound.append(repository)
    #Clear the repo names not found
    if test:
        clearedList = [x for x in data if x not in repoNotFound]
        with open('../ConfigFiles/repo.json','w') as json_file:
            json.dump(clearedList, json_file,indent=4)
    
        
    

def addRepo():
    repo = input("Input the repo name: ")
    
    #Loads repo names
    with open('../ConfigFiles/repo.json') as json_file:
        try:
            data = json.load(json_file)
        except json.decoder.JSONDecodeError:
            data = []
    
    #Appends repo name      
    data.append(repo)
    
    #Write the updated array to the json file
    with open('../ConfigFiles/repo.json','w') as json_file:
        json.dump(data, json_file,indent=4)
        

if __name__ == "__main__":
    #Load the config data
    with open('../ConfigFiles/config.json') as json_file:
        data = json.load(json_file)
        user = data['githubUser']
        access_token = data['githubAccessToken']
    analyzeData(user,access_token)
