#MakeJSON

＜目標將存放tag等資料的檔案轉成JSON輸出＞
----

python MakeJSON.py "FileName"
一次處理一個資料夾下全部的檔案 ls | python MakeJSON.py

(追記 12/30):
先放在根目錄下(以下為範例)

-MakeJSON.py
-(dir)RawData
-(dir)JSONfile

然後

ls RawData/ | ./MakeJSON.py

------

資料來源路徑
變數 Froute：預設是 ./RawData

JSON輸出路徑
變數 Jroute：預設是 ./JSONfile

檔名預設是透過 ls 傳入

以下是JSON的結構
1)  PublicationNo_Name：唯一
2)  Title：複數個
3)  Publication_Number：唯一
4)  Publication_Date：唯一，格式"data-month-year"
5)  Application_Number：唯一
6)  IPC：數量不定，一組(List)內會有兩個值
7)  Applicants：數量不定
8)  Inventors：唯一
9)  Agents：唯一
10) Designated_States：由字典(dict)構成
                       個別國家的專利局放入key:['Global']中
                       區域專利局的則放入key:[該專利局名稱]之中

-----------------------------------------------------------------------------
#abs

用法與上面的大同小異

先放在根目錄下(以下為範例)

-MakeJSON.py
-(dir)RawData_abs
-(dir)ABSfile

然後

ls RawData_abs/ | ./abs.py
