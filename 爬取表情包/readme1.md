## 爬取表情包:(practical.py不使用多线程，thread-spider使用)

使用time模块计算时间看爬取十页多线程快了多少

代码结果截图如下：

![捕获](C:\Users\谢旭康\Desktop\捕获.PNG)

实现提取标题分类，获取图片信息，易于下一步使用以及图片命名用alt上的信息命名



不使用多线程时间为：practice.py:81: DeprecationWarning: time.clock has been deprecated in Python 3.3 and will be removed from Python 3.8: use time.perf_counter or time.process_time instead
  print((time.clock()-start_time))
6.7756891