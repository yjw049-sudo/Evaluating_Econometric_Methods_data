# Notes for coding
## 2026/04/21【如何输出所有personid对应的信息】

### 难点：
- 页面加载因为各种原因可能无法马上加载，Beutifulsoup可能捕捉到空页面。
    - 用WebDriverWait确保等待页面出body后再进行下一步，等待10秒，十秒后超时；循环3次，三次后都失败则返回空dictionary和储存错误信息。
- 每一个页面的label都不完全相同，如果直接用list组装df会错列，无法与列名对齐。
    - 将每一个页面中的label和span中的信息储存为key和value，确保信息和列名一一对应；对于重复的key，则用for查找并重命名。
- 网页可能有反爬虫程序或者偶发错误。eg, A timeout occurred Error code 524. 因此将personid分组，100个为一组，完成后立刻导出，最后将所有文件组装。

### Steps:
- 取出Link_ID中的每一个personid，并储存在list content中。
- 构造函数add_new_info，这个函数的输入一个personid，返回一个dictionary data。
- 构造一个空df和一个空list，循环取出content中的personid，并用add_new_info得到data存入list中。
- 循环list，将每一个data存入df中。
