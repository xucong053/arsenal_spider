import re
import csv
import tqdm
import xmltodict

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


# from selenium.webdriver.common.keys import Keys


class Spider:
    """
    中华军事-武器库爬虫
    """

    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        # 使用headless无界面浏览器模式
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(chrome_options=self.chrome_options)
        self.mainUrl = "https://military.china.com/weapon/aircraft/zdj/130002600/20190724/10427.html"
        self.url_list = []
        self.fout = open("arsenal.csv", "w", newline='', encoding="utf_8_sig")

    def get_html(self, html):
        """启动浏览器，获取网页源代码"""
        self.browser.get(html)

    def find_element(self, xpath):
        """点击xpath目标，更新内容"""
        st = self.browser.find_element_by_xpath(xpath)
        ActionChains(self.browser).click(st).perform()

    def get_content(self):
        """返回源码内容"""
        return self.browser.page_source

    def __del__(self):
        self.fout.close()
        self.browser.close()


if __name__ == '__main__':
    sp = Spider()
    types = ["飞行器", "舰船舰艇", "枪械与单兵", "坦克装甲车辆", "火炮", "导弹武器", "太空装备", "爆炸物"]
    feature = ["战斗机", "攻击机", "轰炸机", "教练机", "预警机", "侦察机", "反潜机", "电子战机", "无人机", "运输机",
               "飞艇", "试验机", "加油机", "通用飞机", "干线", "支线", "运输直升机", "武装直升机", "多用途直升机", "分线器测试分类"]
    res_web_img = []
    bar = tqdm.tqdm(types)
    for type in bar:
        bar.set_description("Processing %s" % type)
        html = "https://military.china.com/weapon/list.html?feature=不限&weapon_type=" + type
        sp.get_html(html)
        # feature选择无限，当前类型，点击筛选，更新页面武器库列表
        sp.find_element("/html/body/div[4]/div[5]/a[1]")
        content = sp.get_content()
        # 当前类型总页数
        num = re.search(r'<span class="totalPage">(\d*)</span>', content).group(1)
        # 循环匹配所有武器的内容页地址和图片，并存于列表
        for _ in tqdm.trange(int(num) - 1):
            re_web_img_list = re.findall(
                r'<div class="search-item"><a href="(.*?)" target="_blank"><img src="(.*?)" alt="', content)
            res_web_img += re_web_img_list
            try:
                # 点击下一页
                sp.find_element("/html/body/div[5]/div[2]/div[2]/a[11]")
                content = sp.get_content()
            except Exception as e:
                print(e)
    # csv头标签
    headers = ["类型", "名称", "图片", "介绍", "参数"]
    f = csv.DictWriter(sp.fout, headers)
    f.writeheader()
    # 循环遍历所有武器内容页，读取介绍与参数，并写入csv
    bar = tqdm.tqdm(res_web_img)
    for web_img in bar:
        bar.set_description("Processing %s" % str(web_img[0]))
        try:
            web, img = web_img
            sp.get_html(web)
            # element = sp.browser.find_element_by_tag_name('body')
            # element.send_keys(Keys.CONTROL, Keys.SHIFT, 'f')
            content = sp.get_content()
            # 武器类型
            type = re.search(r'class="cur">(\S*)</a>', content).group(1)
            # 解析xml为dict格式
            content = xmltodict.parse(content)
            # 武器介绍
            introduce = content["html"]["body"]["div"][4]["div"][1]["div"][0]["div"][2]["p"]
            #武器名称
            name = content["html"]["body"]["div"][4]["div"][1]["div"][0]["h1"]["#text"]
            #武器参数
            parameters = re.findall(r", '(.*?)'\)",
                                    str(content["html"]["body"]["div"][4]["div"][1]["div"][0]["table"]["tbody"]["tr"]))
            row = {"类型": type, "名称": name, "图片": img, "介绍": introduce, "参数": parameters}
            f.writerow(row)
        except Exception as e:
            print(e)
