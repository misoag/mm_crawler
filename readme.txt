##一、使用说明(本程序只能运行在Linux下)

    #查看帮助
    ./mm_crawler.py -h

    #抓取所有美女图片
    ./mm_crawler.py 

    #线程数:5 保存目录:images 抓取图片数量:10
    ./mm_crawler.py -n 5 -o ./images -l 10



##二、开发笔记

1、分析网站，网站的结构如下：

    22mm.cc
        - 清凉美女
            - page1
                - 套图首页
                    - 图片数量不固定
                - 套图首页
                - 套图首页
                - 套图首页
                - 每page共35个套图
            - page2
            - page3
        - 惊艳美女
        - 美女八卦
        - 素人美女
说明：
网站有4大分类（清凉美女，惊艳美女，美女八卦，素人美女）其他分类都是引用此分类中的图片，因此只需要按此4大分类抓取即可。
每个分类有多页
每页中有35个美女套图
每个套图有N张美女图片

    categories = [
        "http://www.22mm.cc/mm/qingliang/index.html",
        "http://www.22mm.cc/mm/jingyan/index.html",
        "http://www.22mm.cc/mm/bagua/index.html",
        "http://www.22mm.cc/mm/suren/index.html"
    ]


伪代码：

	for category in categories:
	    category_pages = fetch_category_pages(category)
	    for category_page in category_pages:
	        image_suite_list = fetch_image_suites(category_page)
	        for image_suite in image_suite_list:
	            fetch_image(image_suite)#抓图套图

2、如果考虑使用多线程，我的方案是建立一个线程池，将抓取任务丢入线程池中即可。

3、关于图片保存的问题

关于图片保存的两种方案（我使用了第二种）:

**第一种：**

如果把全部图片全部都放在一个目录下，有相同名称的图片会覆盖的问题。如果要解决问题，需要给每个图片唯一的名称，使用uuid可以解决这个问题。

**第二种：**

图片按原始目录保存，我想要的结果。这样我寂寞的时候还可以欣赏一下。。。套图哦。。。。

1. Python内置函数创建目录,这个要解决线程同步问题。
2. 使用shell创建目录，并使用wget或者curl直接下载图片即可，参考save_image函数

4、关于重复利用

本程序的ThreadPool可重复利用，如果想不修改代码抓取别的美女站（这个臣妾做不到...）。
大部分的美女站都跟这个网站的结构差别不大（分类-分页-套图首页-套图图片），只需要修改下面4个方法中的正则规则即可：

    get_next_category_page      #返回下一页分类
    fetch_suites(category_url)  #返回套图首页列表
    fetch_suite_images          #返回所有套图的图片


5、备注：

- html中的图片地址是错误的，js会替换为正确的地址，这个应该是站长为了防爬虫设定的。




