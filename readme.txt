運行程式指令：
python news_by_date.py YYYY/MM/DD YYYY/MM/DD

說明：
將檔案解壓縮後即可執行，
解壓縮後之資料夾應有此文件外一程式檔及一資料夾，
程式需配合此資料夾以啟動運行。

執行時需餵入兩個參數，
前者為起始日期，
後者為結束日期，
EX：若要下載2014年八月之所有新聞，
則指令為：python news_by_date.py 2014/08/01 2014/08/31
程式限制可下載的時間區間為：2013/01/01至2015/09/06。