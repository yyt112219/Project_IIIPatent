#!/usr/bin/python3

#1.1板改成 存成csv
#在檔案開頭放入PCT CODE

import re
import argparse
import sys
import csv

def FName_Input():
        parser = argparse.ArgumentParser()
        parser.add_argument('stdin', nargs='?',type=str ,default=sys.stdin)

        if not sys.stdin.isatty():
                FileName_List = parser.parse_args().stdin.read().splitlines()
        else:
                FileName_List = []
        return FileName_List

def OnlyWords(FileName):
        Froute="./RawData_abs"
        Sroute="./ABSfile"
        
        with open(f'{Froute}/{FileName}','r') as ff:
                #  read一次寫入，放入word進行處理
                word=ff.read()
        
        #  若有開頭EN，則去除開頭的EN
        if(word.split(";",1)[0]=="(EN)"):
                words=word.split(";",1)[1]
        else:
                words=word

        #  迴圈刪除文章內有的刮號
        n=0
        while(words.find("(") != (-1)):
                n=n+1
                rex="\(.{" + str(n) + "}\)"
                words=re.sub(rex,"",words)
                #因為有資料忘了加括弧的一邊了，所以設上限避免無限迴圈
                if(n>100):
                        break
        
        #刪標點符號
        words=words.replace(",","").replace(";","").replace(".","").replace("-","").replace("/"," ").replace('"','')

        #在檔案開頭加上PCT CODE欄位
        #PCT CODE目標格式 PCT/地區年份/流水號
        FN=FileName.replace(".txt","")
        PCT='"'+FN[0:3]+"/"+FN[3:9]+"/"+FN[9:15]+'"'
        words='"' + words + '"'
        
        #存檔
        SaveName="END_" + FN + ".csv"
        with open(f'{Sroute}/{SaveName}','w+') as ff2:
                ff2.write(PCT + ',' + words)

        #方便wc -l 用的
        print(FileName + " succsess")

if __name__ == '__main__':
    NameList = FName_Input()
    for File_Name in NameList:
            OnlyWords(File_Name)
