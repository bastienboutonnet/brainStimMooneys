import pandas as pd
import numpy as np

def melt_df_feed_info_from_loop_merge(df):
    #MELT
    col_names=pd.Series(df.columns)
    valid_cols_mask=col_names.str.contains(colsToPull,regex=True)
    valid_cols = df.columns[valid_cols_mask]
    df=df[valid_cols]
    df=pd.melt(df,id_vars='subj_id',var_name='qual_col',value_name=measureName)

    #Extract useful information from qual_cols
    qualtrics_parsed=df.qual_col.str.extract('^(?P<measure>\w+)\((?P<row>\d+)\)$')
    qualtrics_parsed = qualtrics_parsed.convert_objects(convert_numeric=True)
    df = pd.concat([df, qualtrics_parsed], axis = 1)
    df = df.merge(loopmergeInfo, how='left')

    return df

def prepareForRAs(df):
    df['AiMatched']=(df.TextResp==df.Name).astype(int)
    return df

def spotRAdisagreement(df):
    df['RAdisag']=(df.correctPermissive1==df.correctPermissive2).astype(int)
    return df

def isCorrectFromRAChecked(df):
    df['isCorrect']=(df.TextResp==df.Name).astype(int)
    return df

def mergeAllVars(df,acc,rt,conf):
    df=df[['subj_id','subjcode','electrode']]
    rt=rt.drop(['qual_col','row'],1)
    conf=conf.drop(['qual_col','row'],1)
    AccRT=pd.merge(acc,rt,how='left',on=['subj_id','Name'])
    AccRTConf=pd.merge(AccRT,conf,how='left',on=['subj_id','Name'])
    AllVarsAndCondInfo=pd.merge(df,AccRTConf,how='left',on='subj_id')
    return AllVarsAndCondInfo


def reconstruct_order_and_melt_with_df(df):
    variables=loopmergeInfo.Name.as_matrix()
    order_split=ord.preorder.str.split("|")

    for v in variables:
        ord[v] = order_split.apply(lambda x: x.index(v) + 1)

    order=ord.drop(['preorder'],axis=1)
    #MELT ORDER
    order=pd.melt(order,id_vars='subj_id',var_name='Name',value_name='position')

    #MERGE WITH DF
    datNorder=pd.merge(df,order,how='left',on=['Name','subj_id'])

    return datNorder

if __name__=='__main__':
    operation=input("1:Pull Naming\n2:Prep For RA\n3:RA disagreement\n4:Correct from Permissive\n5:Pull other variables\n6:Merge Everything\n:")
    if operation==1:
        df=pd.read_csv("MooneysFreeNamingWAS.csv",skiprows=[1,])
        df=df.rename(columns={df.columns[0]:'subj_id'})
        loopmergeInfo=pd.read_csv("WASMooneyLoopMerge.csv")
        ord=df[['subj_id','preorder']]
        colsToPull='^subj_id|NameResp_TEXT' #whatever regEx works
        measureName="TextResp"
        recDF=melt_df_feed_info_from_loop_merge(df)
        recDF.to_csv("WASMooneyForRAs.csv",index=0)

    elif operation==2:
        df=pd.read_csv("WASMooneyForRAs.csv")
        prepRAs=prepareForRAs(df)
        prepRAs.to_csv("WASMooneysForRA.csv",index=0)

    elif operation==3:
        df=pd.read_csv("WASMooneysToCheck.csv")
        checked=spotRAdisagreement(df)
        checked.to_csv("WASMooneysChecked.csv",index=0)

    elif operation==4:
        df=pd.read_csv("WASMooneysChecked.csv")
        correct=isCorrectFromRAChecked(df)
        correct.to_csv("brainStimMOOAccuracy.csv",index=0)

    elif operation==5:
        df=pd.read_csv("MooneysFreeNamingWAS.csv",skiprows=[1,])
        df=df.rename(columns={df.columns[0]:'subj_id'})
        loopmergeInfo=pd.read_csv("WASMooneyLoopMerge.csv")
        ord=df[['subj_id','preorder']]
        varsToPull=['Timing_1','Confidence']
        for curVar in varsToPull:
            colsToPull='^subj_id|'+curVar
            measureName=curVar
            recDF=melt_df_feed_info_from_loop_merge(df)
            recDF=recDF.drop('measure',1)
            recDF.to_csv("brainStimMOO"+curVar+".csv",index=0)

    elif operation==6:
        df=pd.read_csv("MooneysFreeNamingWAS.csv",skiprows=[1,])
        df=df.rename(columns={df.columns[0]:'subj_id'})
        acc=pd.read_csv("brainStimMOOAccuracy.csv")
        rt=pd.read_csv("brainStimMOOTiming_1.csv")
        conf=pd.read_csv("brainStimMOOConfidence.csv")
        mergedAll=mergeAllVars(df,acc,rt,conf)
        mergedAll.to_csv("brainStimMOOAllVars.csv",index=0)

    else:
        print "Wrong operation code."
