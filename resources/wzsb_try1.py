from PIL import Image
import time
import pytesseract
class Image_rec(object):
    def feedbackWord(self,address):
        text = pytesseract.image_to_string(Image.open(address), lang='chi_sim').replace(" ", "")
        return text


#start = time.time()
#text = pytesseract.image_to_string(Image.open('a8.png'),lang='chi_sim').replace(" ", "")
#end = time.time()
#print(text)
#print(end-start)

#1.1556389331817627s
#1.1014220714569092s 白底
#1.118582010269165 透明底
#1.63374924659729  增强对比度

#华文细黑牛皮
#化 `
#繁 华 事 散 逐 香 生

#素 华
#华 事 散 逐 香 尘       （对比度3）

#繁 华 事 散 选 香 尘 ,  （对比度4）

#化 事 散 ;
#繁 华 事 散 逐 香 生     （黑白分边）

#化 事 散 ;
#繁 华 事 散 逐 香 生

#做 软 雅 黑
#娉 娉 袅 袅 十 二 余 , 豆 蔻 悄 头 二 月 分 。
#春 风 十 里 扬 州 路 , 卷 上 珠 宗 尼 不 如 。
#
#多 情 却 似 总 无 情 , 唯 觉 橇 前 笑 不 成
#然 烛 有 心 还 惜 别 , 替 人 垂 泪 到 天 明  wrong:8

#做 软 雅 黑
#娉 娉 袅 袅 十 三 余 , 豆 蔻 梢 头 二 月 分 。
#春 风 十 里 扬 州 路 , 奕 上 珠 官 尽 不 如 。
#
#多 情 却 似 总 无 情 , 唯 觉 橇 前 笑 不 成
#焱 烛 有 心 还 惜 别 , 替 人 垂 泪 到 天 明  wrong:7

#做 软 雅 黑
#烘 婧 吴 宏 十 二 余 , 豆 著 悄 头 一 月 们 .
#春 风 十 里 扬 州 路 , 卷 上 珠 宗 忌 不 如 。
#
#多 惑 卯 似 总 无 情 , 唯 觉 樵 前 笑 不 成
#焰 炒 有 心 还 惜 别 , 替 人 垂 沁 到 天 明
