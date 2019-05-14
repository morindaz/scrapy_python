import pandas
medical=pandas.read_json("medical.json",lines=True)[:]
medical.fillna("",inplace=True)

for col in medical.columns:
    if col=="_id":
        medical[col]=medical[col].map(lambda x:list(x.values())[0])
    elif col in ["cause","cost_money","cure_lasttime","cured_prob","desc","easy_get","get_prob","get_way","name","prevent","yibao_status"]:
        continue
    else:
            try:
                
                # medical[col]=medical[col].map(lambda x: ','.join(list(ix for ix in x)))
                medical[col]=medical[col].map(lambda x: ','.join(x))
            except:
                print(col)
medical.to_excel("medical.xlsx")
