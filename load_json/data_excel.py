import pandas as pd
medical=pd.read_json("data.json",lines=True)
medical.fillna("",inplace=True)
df = pd.DataFrame()
for col in medical.columns:
    if col == 'index':
        i=0
        col_name = list((list(medical[col])[0]).keys())
        n = len(col_name)
        a = [[] for num in range(n)]
        for items in list(medical[col]):
            if i%2==0:
                for j in range(n):
                    a[j].append(list(items.values())[j])
            else:
                for j in range(n):
                    a[j].append('')
            i += 1
    else:
        for i in range(len(medical)):
            if i>0:
                medical[col][i-1] = medical[col][i]
col_name = ['index'+x for x in col_name]
for i in range(n):
    medical[col_name[i]]=a[i]
del medical['index']
medical = medical[medical[col_name[0]]!=''].reset_index()
print(medical)
