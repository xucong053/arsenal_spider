# 中华武器库爬虫 #

## 1. 地址 ##

***https://military.china.com/weapon/list.html***

## 2. 内容 ##

- **爬取武器的图片地址、简介和参数**

- **包括："飞行器", "舰船舰艇", "枪械与单兵", "坦克装甲车辆", "火炮", "导弹武器", "太空装备", "爆炸物"**

## 3. 已知BUG ##

- **selenium在翻页到最后几页时，点击下一页会出现`Message: no such element: Unable to locate element: {"method":"xpath","selector":"/html/body/div[5]/div[2]/div[2]/a[11]"}`**

- **xml中出现不支持的字符范围`not well-formed (invalid token)`"**