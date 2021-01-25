在flask_0121之下，分別有templates、static兩個資料夾和app119.py，
flask預設會到templates中選用html，到static中選用css、js等靜態網頁要件。
啟動方法是在terminal中cd到flask_0121，然後輸入"python3 app119.py"執行程式。
如果有缺乏的套件就用"sudo pip3 install ..."安裝。
另外，要按照官網指示先安裝好MariaDB，再pip3 install mariadb才能順利使用mariadb的package，
我還沒弄懂為什麼，但這是我踩過的雷，總之不要跟他拚。