#!usr/bin/env python
# -*- coding:utf-8 -*-
import re

str = '我的电话号码是13809120303'

# 匹配所有的手机号码
res = re.findall('[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}', str)
print(res)


tg_regexs = ['[tT][gG][:|：|-]?([@0-9a-zA-Z]+)','[tT]elegram[:|：|-|][ | ]([@0-9a-zA-Z ]+)','t\.me/([@0-9a-zA-Z]+)']
for tg_regex in tg_regexs:
    print(tg_regex)
    text = """
	<< 境外国际团队长期高价收购中国内幕文件及支持白纸运动>> 面对国家队永无止境地备战，对外强硬的外交争夺。 你是否也开始质疑这一切为了什么？打着中国伟大复兴的旗帜，对付反对这些立场的自己人，打击却从不手软！又是谁让中国成为全世界的头号对手！这些难道真是你内心的追求？ 区域和平才是国际共同的利益，我们期待你展开双臂，共同担当这道友谊的推手。 如果你认同我们的想法，也对目前的境遇有所不满。我们的合作不限任何形式，请和我们联系，提供你所知道的内幕，或背后暗算你的无耻之徒，我们会尽最大力量，满足你所提的财富或其他追求。相信你就是那位让和平，风生水起的那位关键人物！ 联系TG飞机：@PEACEFUL2023 联系TG飞机：@siyuchenchen 联系TG飞机：@asosasin88 Have you ever questioned yourself what it is all about when you see your country preparing for war and undergoing endless diplomatic fighting against others? Holding high the huge banner of great rejuvenation, China never gives up torturing and fighting against those who possess right standpoints, making itself the biggest enemy to the whole world. We can not help but wonder, is it all you want to see? Peace is the common interest of the universe. We sincerely open arms to welcome you to be part of us, to be a helping hand in pushing forward friendship and common value of democracy. If you agree with us, just step forward and join us. No matter who you are or where you are from, please contact us with every possible means. Let us know what you’ve seen or been through by unfair treatment or shameless people. We will do our best to help you with anything you search for and change those wrongdoings. You, will be the ONE who make world peace happen! Contact Telegram: @ PEACEFUL2023 Contact Telegram: @ siyuchenchen Contact Telegram: @ asosasin88
	    """
    result = re.findall(tg_regex,text)
    print(result)