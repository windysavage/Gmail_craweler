# Gmail_craweler
Utilize Gmail API to fetch information from your Gmail account

### Requirements
python 3.8+


### Setting
```
conda create --name Gmail python=3.8
activate Gmail
pip install -r requirements.txt
```

### Running
```
python Gmail.py
```

- You can modify exclude_words.txt to make sure that subjects containing these word will not be included
- 搜尋關鍵字可為"銀行", "優惠" ... 搜尋所有郵件請輸入"None"

### Warning
- Please don't open the "subject_list_*.csv" file when running the script
- Please close the access to your Gmail account after running the script
- Please check the output file and make sure there is no sensitive information or something you don't want to be seen
  
### How to close the access right
- 前往 https://myaccount.google.com/?utm_source=OGB&tab=wk&utm_medium=act
1. 安全性-->具有存取權的第三方應用程式-->選擇"Quickstart"-->移除存取權