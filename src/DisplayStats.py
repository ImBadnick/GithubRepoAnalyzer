import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np

def update_annot(line, idx,annot):
    posx, posy = [line.get_xdata()[idx], line.get_ydata()[idx]] #Gets posx and posy of the point
    annot.xy = (posx, posy) #Sets x,y of the annotation
    text = f'{line.get_label()}: {float(posy)}' 
    annot.set_text(text) #Sets the text of the annotation
    # annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
    annot.get_bbox_patch().set_alpha(0.4)


def over(event,annot,lines,fig,ax):
    for i in range(len(annot)):
        if event.inaxes == ax[i]: #If the event is in one of the 2 charts
            vis = annot[i].get_visible()
            for line in lines[i]:
                cont, ind = line.contains(event) #If the lines of the chart contains the event
                if cont: #If the point is on the line -> Display annotation
                    update_annot(line, ind['ind'][0],annot[i]) #Update annotation
                    annot[i].set_visible(True) #Make annotation visible
                    fig.canvas.draw_idle()
                else:
                    if vis:
                        annot[i].set_visible(False)
                        fig.canvas.draw_idle()

def displayStats(repoName):
    foundViews = True
    foundClones = True
    #Loading data from json files
    with open('../RepoData.json') as f:
        data = json.load(f)
    found = False
    #Searching repoData of repoName
    for d in data['Repo']:
        if d['Name']==repoName:
            stats = d['Stats']
            stats['views'] = stats['views'][-14:]
            stats['clones'] = stats['clones'][-14:]
            found = True
    if found: #If repoData were found
        #format timestamps
        if(not stats['views']):
            foundViews = False
        else:
            for x in stats['views']: 
                x['timestamp'] = (x['timestamp'].split(" ")[0])[2:]
        if(not stats['clones']):
            foundClones = False
        else:
            for y in stats['clones']: 
                y['timestamp'] = (y['timestamp'].split(" ")[0])[2:]
        
        if ((not foundViews) and (not foundClones)):
            print("No views and clones found for this repo.")
            exit()
        
        charthValues = [pd.DataFrame(stats['views']),pd.DataFrame(stats['clones'])] #Transform data into a pandas DataFrame
        annot = []
        lines = [[],[]]
        if foundClones: fig, ax = plt.subplots(2,figsize=(15,7)) #Prepare plot with 2 subplots
        else: 
            ax = []
            fig, tmp = plt.subplots(1,figsize=(15,7))
            ax.append(tmp)
        for i in range(len(ax)): #Looping on the 2 charts
            #Plot lines
            sc1, = ax[i].plot(charthValues[i]['timestamp'], charthValues[i]['count'],"o-", label = "Views")
            if (i==0):
                name = "Unique Visitors"
            else:
                name = "Unique Cloners"
            sc2, = ax[i].plot(charthValues[i]['timestamp'], charthValues[i]['uniques'],"o-", label = name)
            #Save lines 
            lines[i].append(sc1)
            lines[i].append(sc2)
            # Set rotation of the timestamps
            ax[i].tick_params(labelrotation=30)
            # Set title of subplot
            if (i==0): ax[i].set_title('VIEWS') 
            else:  ax[i].set_title('CLONES')
            # Set the x axis label of the current axis.
            ax[i].set_xlabel('Dates')
            # Set the y axis label of the current axis.
            ax[i].set_ylabel('Values')
            # Set a title of the current axes.
            fig.canvas.set_window_title('REPOSITORY STATS')
            #Create annotation 
            annot.append(ax[i].annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->")))
            annot[i].set_visible(False)
            # show a legend on the plot
            ax[i].legend()

        fig.suptitle('REPOSITORY STATS', fontsize=16) #Big title of the figure
        fig.canvas.mpl_connect("motion_notify_event", lambda event: over(event,annot,lines,fig,ax)) #If mouse passes over
        plt.subplots_adjust(top=0.8, bottom=0.16,right=0.88,hspace = 0.8)  # Adjust the top of the graph (default = 0.90)
        plt.show() #Show chart
    
    else:
        print("REPO DATA NOT FOUND")

if __name__ == "__main__":
    repoName = input("Insert repo to displayStats: ")
    displayStats(repoName)
