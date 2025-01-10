"""
This Python script calculates and presents the overlap of concepts within the 17 datasets with Swadesh 1955. 
Note: For this script, one must first download and save the Swadesh_POStagged.tsv file (Under: Additional Data).
"""

from pyconcepticon import Concepticon
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path

concepticon = Concepticon("concepticon-data")

swadesh = concepticon.conceptlists["Swadesh-1952-200"].concepts
nouns = []
for concept in swadesh.values():
    if concepticon.conceptsets[concept.concepticon_id].ontological_category == "Person/Thing":
        nouns += [concept.concepticon_gloss]

#Specific comparison: which Swadesh concepts and how many are present in which dataset
with open(Path(__file__).parent / "conceptlists.tsv") as f:
    conceptlists = [row.strip() for row in f]

common_concepts = {}

for conceptlist in conceptlists:
    concepts = [concept.concepticon_gloss for concept in
                concepticon.conceptlists[conceptlist].concepts.values() if
                concept.concepticon_gloss in nouns]
    common_concepts[conceptlist] = sorted(concepts)

for cl, concepts in common_concepts.items():
    print('# Conceptlist {0} has {1} common concepts'.format(cl, len(concepts)))
    for concept in concepts:
        print('* ' + concept)
    print("")


common_counts = [len(common_concepts[clist]) for clist in conceptlists]

sorted_data = sorted(zip(common_counts, conceptlists), key=lambda x: x[0], reverse=True)
sorted_counts, sorted_names = zip(*sorted_data)
norm = plt.Normalize(min(sorted_counts), max(sorted_counts))
cmap = plt.cm.Oranges
plt.clf() # clear figures
plt.figure(figsize=(10, 6))
bars = plt.bar(sorted_names, sorted_counts, color=cmap(norm(sorted_counts)))

for bar, count in zip(bars, sorted_counts):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),                  #Height
        str(count),                        #Displaying the count
        ha='center',                       
        va='bottom',                       
        fontsize=10                        
    )

plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("swadesh-barcharts.pdf")

plt.clf()
plt.figure(figsize=(15, 9)) 
cmap = ListedColormap(['#fca663', '#de5b12'])

# create dataframe data for heatmap (with pandas)
heatmap_data = pd.DataFrame(0, index=conceptlists, columns=nouns)
for dataset, nouns in common_concepts.items():
    for noun in nouns:
        heatmap_data.at[dataset, noun] = 1


heatmap = sns.heatmap(heatmap_data, cmap=cmap, cbar=True, linewidths=0.5, vmin=0.0, vmax=1.0, square=True,  cbar_kws={"orientation": "vertical", "shrink": 0.25})

colorbar = heatmap.collections[0].colorbar
colorbar.set_ticks([0, 1])
colorbar.set_ticklabels(['Absent', 'Present']) 

plt.title('')
plt.xlabel('')
plt.ylabel('')

plt.tight_layout()
plt.savefig("swadesh-heatmap.pdf")
