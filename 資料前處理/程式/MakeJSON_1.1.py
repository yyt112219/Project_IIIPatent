#!/usr/bin/python3

import re
import json
import argparse
import sys

def FName_Input():
        parser = argparse.ArgumentParser()
        parser.add_argument('stdin', nargs='?',type=str ,default=sys.stdin)

        if not sys.stdin.isatty():
                FileName_List = parser.parse_args().stdin.read().splitlines()
        else:
                FileName_List = []
        return FileName_List

def Make_JSON(FName):
        # 路徑
        Froute="RawData"
        # 檔名
        #FName="PCTAT1987000021.txt"
        
        FullRoute=Froute + FName

        # 處理非abstract之名的檔案
        with open(f'./{Froute}/{FName}','r',encoding="utf-8") as ff3:
                #  read文字進來
                word=ff3.read()

        # 空字典
        Jdict={}

        # 分開字串
        words=word.split(";")
        if (len(words)>1 and words[0]!='nan'):
                # (1)Publication Number + Name：只會有一個，固定數字排列+不定長度名稱
                Jdict['PublicationNo_Name']=words[0].strip('"')

                # (2)Title : 複數存在，看起來大多是兩個左右
                wd_1=words[1].strip('"').strip("[").strip("]").replace("'","").strip("(")\
                          .replace(",","").split('(')
                #這裡處理完之後的wd_1 格式如下
                # [0+2n]:地區) 名字
                # [1+2n]:'' 空字串
                List_wd_1=[]

                # 只把有裝資料的填入list
                for i in range(len(wd_1)):
                        if(i%2==1):
                                continue
                        List_wd_1.append(wd_1[i].replace(")","),"))
                Jdict['Title']=List_wd_1

                # (3)Publication Number : only one ,EZ
                Jdict['Publication_Number']=words[2].strip('"')

                # (4)Publication Date : only one ,EZ    我把日期改成用-來間隔
                Jdict['Publication_Date']=words[3].strip('"').replace(".","-")

                # (5)Application Number : only one, EZ
                Jdict['Application_Number']=words[4].strip('"')

                # (6)IPC code 不定多數
                wd_5=words[5].strip('"').strip("[").strip("]").split(")")
                #這裡處理結束後的格式如下
                #list的最後一項是空的
                #其它每一項都有值
                List_wd_5=[]
                for i in range(len(wd_5)-1):
                        List_wd_5.append(wd_5[i].strip(",").strip(' ').strip("("))
                Jdict['IPC']=List_wd_5

                # (7)Applicants 不定多數
                wd_6=words[6].strip('"').strip("{").strip('}').split("', ")
                List_wd_6=[]
                for i in range(len(wd_6)):
                        List_wd_6.append(wd_6[i])
                Jdict['Applicants']=List_wd_6

                # (8)Inventors Only one ,EZ
                Jdict['Inventors']=words[7].strip('"').strip("[").strip("]")

                # (9)Agents Only one ,EZ
                Jdict['Agents']=words[8].strip('"').strip("[").strip("]")

                # (10)Designated States 有一大堆：單獨出現的自己存一個，European Patent Office這種一次包很多的自己放入一個List
                wd_9=words[9].strip('"')

                List_wd_9=[]
                dict_wd_9={}
                
                # 單獨抓取
                if len(wd_9.split('\n')[0])>1:
                        Solo=wd_9.split('\n',1)[0].split(',')
                        for i in range(len(Solo)):
                                List_wd_9.append(Solo[i])
                        dict_wd_9['Global']=List_wd_9

                # 群體抓取
                try:
                        if len(wd_9.split('\n')[1])>1:
                                        Multi=wd_9.split('\n',1)[1].split('\n')
                                        
                                        List_wd_9=[]
                                        for i in range(len(Multi)):
                                                        List_wd_9=[]
                                                        for n in [3,4,5]:
                                                                        rex="\(.{" + str(n) + "}\)"
                                                                        Multi[i]=re.sub(rex,"",Multi[i])
                                                        NameSpace=Multi[i].split('(')[0]
                                                        ValueSpace=Multi[i].split('(')[1].split(')')[0].split(',')
                                                        for i in range(len(ValueSpace)):
                                                                        List_wd_9.append(ValueSpace[i])
                                                        # 動態命名：以f'{}'解讀變數後作為key使用
                                                        dict_wd_9[f'{NameSpace}']=List_wd_9
                except:
                        print("fine")
                
                Jdict['Designated_States']=dict_wd_9
                
                # 製成json檔
                JName=FName.replace(".txt",".json")
                Jroute="JSONfile"
                with open(f'./{Jroute}/{JName}','w') as f:
                        f.write(json.dumps(Jdict))
                # 如果想統計成功幾筆，方便wc -l用的
                print('success:' + JName)


if __name__ == '__main__':
    NameList = FName_Input()
    for File_Name in NameList:
            Make_JSON(File_Name)
