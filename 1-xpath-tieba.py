import urllib
import urllib.request
import requests
import urllib3
from lxml import etree

# 解决在verify=False下，控制台InsecureRequestWarning问题，添加下面一行代码可以不显示
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# http://tieba.baidu.com/f?kw=创造101&pn=50    每页50条数据
url_title = 'http://tieba.baidu.com'
url_tieba = 'http://tieba.baidu.com/f?ie=utf-8&kw=%s&pn=%d'


def load_tieba(key, start, end):
    for p in range(start, end + 1):
        url = url_tieba % (key, (p-1) * 50)
        # 百度贴吧 反人类，无需请求头
        # response = requests.get(url=url, headers=headers, verify=False)
        response = requests.get(url=url, verify=False)
        html = response.text
        tieba_tree = etree.HTML(html)

        # 贴吧页面获取各个楼主的链接

        # 置顶楼主
        # /html/body[@class='skin_normal']/div[@class='wrap1']/div[@class='wrap2']/div[@id='content']/div[@id='pagelet_frs-base/pagelet/content']/div[@class='forum_content clearfix']/div[@id='content_wrap']/div[@id='pagelet_frs-list/pagelet/content']/div[@id='pagelet_frs-list/pagelet/thread']/div[@id='content_leftList']/div[@id='pagelet_frs-list/pagelet/thread_list']/ul[@id='thread_list']/li[@class='thread_top_list_folder']/ul[@id='thread_top_list']/li[@class=' j_thread_list thread_top j_thread_list clearfix'][1]/div[@class='t_con cleafix']/div[@class='col2_right j_threadlist_li_right ']/div[@class='threadlist_lz clearfix']/div[@class='threadlist_title pull_left j_th_tit']/a[@class='j_th_tit']
        # 普通楼主
        # /html/body[@class='skin_normal']/div[@class='wrap1']/div[@class='wrap2']/div[@id='content']/div[@id='pagelet_frs-base/pagelet/content']/div[@class='forum_content clearfix']/div[@id='content_wrap']/div[@id='pagelet_frs-list/pagelet/content']/div[@id='pagelet_frs-list/pagelet/thread']/div[@id='content_leftList']/div[@id='pagelet_frs-list/pagelet/thread_list']/ul[@id='thread_list']/li[@class='j_thread_list clearfix'][2]/div[@class='t_con cleafix']/div[@class='col2_right j_threadlist_li_right ']/div[@class='threadlist_lz clearfix']/div[@class='threadlist_title pull_left j_th_tit']/a[@class='j_th_tit']
        # html中a标签的相关代码，找到href
        # <a rel="noreferrer" href="/p/5764534035" title="心疼豆子！心疼李子璇！" target="_blank" class="j_th_tit ">心疼豆子！心疼李子璇！</a>

        hoster = tieba_tree.xpath('//div[@class="threadlist_lz clearfix"]/div/a/@href')
        for host in hoster:
            # print(host)
            host_url =url_title + host
            response = requests.get(url=host_url, verify=False)
            response.encoding = 'utf-8'
            text = response.text
            tree = etree.HTML(text)


            # 楼主图片的html标签
            # <img class="BDE_Image" src="http://imgsrc.baidu.com/forum/w%3D580/sign=458bbcd5f1faaf5184e381b7bc5594ed/f8aff512b07eca80eea82d149d2397dda34483d7.jpg" size="70855" changedsize="true" width="560" height="373" style="cursor: url(&quot;http://tb2.bdstatic.com/tb/static-pb/img/cur_zin.cur&quot;), pointer;">

            srcs = tree.xpath('//img[@class="BDE_Image"]/@src')
            count = 0
            for img_url in srcs:
                # print(img_url)
                count += 1
                file_name = img_url.rsplit('/')[-1]
                urllib.request.urlretrieve(url=img_url, filename='./images/%s' %(file_name))
                print('保存%d张图片成功' %(count))



if __name__ == '__main__':
    key = input('请输入贴吧的名称：')
    start = int(input('请输入贴吧的起始页码：'))
    end = int(input('请输入贴吧的终止页码：'))

    # 请求贴吧的页面
    load_tieba(key, start, end)

