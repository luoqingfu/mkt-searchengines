import requests
from bs4 import BeautifulSoup

from function import Excel

search_key = ['英荔', '英荔教育', '英荔商学院']
class BingClimb:
    def get_excel_data(self, dataname, row=2):
        data = Excel(dataname)
        return data.read_excel(row)

    """给EXCEL表插入数据"""

    def set_excel_data(self, dataname,col, row, datas):
        excel_data = Excel(dataname)
        excel_data.write_excel_rol(col,row, datas)
    def climb_bing(self,key):
        # 发送HTTP请求时的HEAD信息，用于伪装为浏览器,不然可能被察觉到是爬虫脚本
        headersParameters = {
                'Connection': 'Keep-Alive',
                'Accept': 'text/html, application/xhtml+xml, */*',
                'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
                'Accept-Encoding': 'gzip, deflate',
                'User-Agent': 'Mozilla/6.1 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
        }

        httpRsp = requests.get("https://cn.bing.com/search?q={}".format(key), headers=headersParameters)
        if httpRsp.status_code != 200:
            print("数据获取失败")
        else:
            soup = BeautifulSoup(httpRsp.text, "lxml")
            results = soup.select(".b_algo")
            print(results)
            # 用于保存提取的数据
            resultArr = []
            for index in range(len(results)-5):
                # 获取标题所在的a标签
                #print(results[index])
                aTag = results[index].select("h2 a")[0]
                # 获取标题的文本
                title = aTag.get_text()
                print(title)
                # 获取网页的真实URL
                href = aTag.attrs["href"]
                print(href)
                sessions =requests.session()
                sessions.headers['User-Agent'] = 'Mozilla/6.1 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
                r = sessions.get(href)
                href = r.url
                resultArr.append({
                    "title": title,
                    "href": href,
                    })
            #print(resultArr)
            return resultArr


    def write(self):
        n = 0
        for i in range(len(search_key)):
            result = self.climb_bing(search_key[i])
            for c in range(len(result)):
                title = result[c].get('title')
                url = result[c].get('href')
                self.set_excel_data('search_result', c + 11, n, title)
                self.set_excel_data('search_result', c + 11, n + 1, url)
                if url == 'https://www.elitemba.cn' or url == 'https://www.elitemba.cn/':
                    self.set_excel_data('search_result', c + 11, n + 2, '是')
                else:
                    self.set_excel_data('search_result', c + 11, n + 2, '否')
            n += 4






if __name__ == '__main__':
    BingClimb().climb_bing('英荔商学院')
    #BingClimb().write()