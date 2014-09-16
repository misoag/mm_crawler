##说明

由于http://www.22mm.cc/的服务器不是很稳定，有时候会不能访问。我找到http://www.mnsfz.com/跟22mm的网站结构是相同的，程序不需要修改即可使用。

参考 mm_crawler.py:

    if __name__ == "__main__":
        options = helper.get_options()
        mm_crawler = MMCrawler(options.threads,options.output,options.limits)
        #22MM美女网
        # mm_crawler.recursion_category("http://www.22mm.cc/mm/qingliang/index.html")
        # mm_crawler.recursion_category("http://www.22mm.cc/mm/jingyan/index.html")
        # mm_crawler.recursion_category("http://www.22mm.cc/mm/bagua/index.html")
        # mm_crawler.recursion_category("http://www.22mm.cc/mm/suren/index.html")
        #美女私房照
        mm_crawler.recursion_category("http://www.mnsfz.com/h/qingchun/index.html")
        # mm_crawler.recursion_category("http://www.mnsfz.com/h/meihuo/index.html")
        # mm_crawler.recursion_category("http://www.mnsfz.com/h/yangguang/index.html")
        # mm_crawler.recursion_category("http://www.mnsfz.com/h/qiaopi/index.html")

如果22mm.cc不能访问，可切换到另外一个尝试。
