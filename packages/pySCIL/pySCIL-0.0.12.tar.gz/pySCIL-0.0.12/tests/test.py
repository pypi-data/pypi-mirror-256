# File for testing the scil class

import json
from os import listdir
from os.path import isfile, join

# scil.SCIL
from scil import scil



# obj = scil.SCIL()
with open("datasets/Feb28GrA_1_DAtag.json") as f:
    obj = scil.SCIL(f)
obj.preprocessStanford()


tpc = obj.TopicControlFunctions()
tsc = obj.TaskControlFunctions()
inv = obj.InvolvementFunctions()
dis = obj.DisagreementFunctions()
led = obj.Leadership(tpc,tsc,inv,dis)

speakers = [speaker for speaker in tpc['speakers']]

tpcScores = []
for speaker in speakers:
    tpcScores.append((tpc['speakers'][speaker]['averageTopicControl'],speaker))
tpcScores.sort(reverse=True)
print(', '.join([score[1].upper() for score in tpcScores]))
print(', '.join([score[0] for score in tpcScores]))

tscScores = []
for speaker in speakers:
    tscScores.append((tsc['speakers'][speaker]['averageTaskControl'],speaker))
tscScores.sort(reverse=True)
print(', '.join([score[1].upper() for score in tscScores]))
print(', '.join([score[0] for score in tscScores]))

invScores = []
for speaker in speakers:
    invScores.append((inv['speakers'][speaker]['averageInvolvement'],speaker))
invScores.sort(reverse=True)
print(', '.join([score[1].upper() for score in invScores]))
print(', '.join([score[0] for score in invScores]))

disScores = []
for speaker in speakers:
    disScores.append((dis['speakers'][speaker]['averageDisagreement'],speaker))
disScores.sort(reverse=True)
print(', '.join([score[1].upper() for score in disScores]))
print(', '.join([score[0] for score in disScores]))

ledScores = []
for speaker in speakers:
    ledScores.append((led['speakers'][speaker]['Leadership'],speaker))
ledScores.sort(reverse=True)
print(', '.join([score[1].upper() for score in ledScores]))
print(', '.join([score[0] for score in ledScores]))
print(led)


'''
saved for later
'''

# results = {}
# tagcount = {}
# for turn in obj.jsonData['turns']:
#     meta = turn['metaTag']
#     tag = turn['tag']
    
#     if tag not in tagcount:
#         tagcount[tag] = 0
#     tagcount[tag] += 1
#     # if meta == '': continue

#     if meta not in results:
#         results[meta] = {}
#     if tag not in results[meta]:
#         results[meta][tag] = 0
#     results[meta][tag] += 1

# print(',' + ','.join([meta for meta in results]) + ',frequency,count')
# for tag in tagcount:
#     print(tag,end='')
#     for meta in results:
#         if tag in results[meta]:
#             print(','+str(round(100*results[meta][tag] / tagcount[tag], 3)),end='')
#         else:
#             print(',0',end='')
#     print(',' + str(round(100*tagcount[tag]/len(obj.jsonData['turns']),3)) + ',' + str(tagcount[tag]))
# files = [f for f in listdir('/home/max/Desktop/scil-package/pySCIL/tests/chat_sessions_annotated') if isfile(join('/home/max/Desktop/scil-package/pySCIL/tests/chat_sessions_annotated', f))]

# results = {}
# tagcount = {}
# totalturns = 0
# for f in files:
#     with open('chat_sessions_annotated/'+f) as handle:
#         obj = scil.SCIL(handle)
#         for turn in obj.jsonData['turns']:
#             meta = turn['metaTag']
#             tag = turn['tag']
#             if tag == '':
#                 tag = "<untagged>"
#                 print(f)
#             if meta == '':
#                 meta = "<untagged>"

#             if tag not in tagcount:
#                 tagcount[tag] = 0
#             tagcount[tag] += 1
#             totalturns += 1

#             if meta not in results:
#                 results[meta] = {}
#             if tag not in results[meta]:
#                 results[meta][tag] = 0
#             results[meta][tag] += 1

# print(',' + ','.join([meta for meta in results if meta != "<untagged>"]) + ',<untagged>,frequency,count')
# for tag in tagcount:
#     print(tag,end='')
#     for meta in results:
#         if meta == "<untagged>": continue
#         if tag in results[meta]:
#             print(','+str(round(100*results[meta][tag] / tagcount[tag], 3)),end='')
#         else:
#             print(',0',end='')
#     if tag in results["<untagged>"]:
#         print(','+str(round(100*results["<untagged>"][tag] / tagcount[tag], 3)),end='')
#     else:
#         print(',0',end='')

#     print(',' + str(round(100*tagcount[tag]/totalturns,3)) + ',' + str(tagcount[tag]))
#TODO: Calculate frequency of each