#MakeJSON

�եؼбN�s��tag����ƪ��ɮ��নJSON��X��
----

python MakeJSON.py "FileName"
�@���B�z�@�Ӹ�Ƨ��U�������ɮ� ls | python MakeJSON.py

(�l�O 12/30):
����b�ڥؿ��U(�H�U���d��)

-MakeJSON.py
-(dir)RawData
-(dir)JSONfile

�M��

ls RawData/ | ./MakeJSON.py

------

��ƨӷ����|
�ܼ� Froute�G�w�]�O ./RawData

JSON��X���|
�ܼ� Jroute�G�w�]�O ./JSONfile

�ɦW�w�]�O�z�L ls �ǤJ

�H�U�OJSON�����c
1)  PublicationNo_Name�G�ߤ@
2)  Title�G�Ƽƭ�
3)  Publication_Number�G�ߤ@
4)  Publication_Date�G�ߤ@�A�榡"data-month-year"
5)  Application_Number�G�ߤ@
6)  IPC�G�ƶq���w�A�@��(List)���|����ӭ�
7)  Applicants�G�ƶq���w
8)  Inventors�G�ߤ@
9)  Agents�G�ߤ@
10) Designated_States�G�Ѧr��(dict)�c��
                       �ӧO��a���M�Q����Jkey:['Global']��
                       �ϰ�M�Q�����h��Jkey:[�ӱM�Q���W��]����

-----------------------------------------------------------------------------
#abs

�Ϊk�P�W�����j�P�p��

����b�ڥؿ��U(�H�U���d��)

-MakeJSON.py
-(dir)RawData_abs
-(dir)ABSfile

�M��

ls RawData_abs/ | ./abs.py
