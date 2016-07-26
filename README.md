# haha_ime
Hǎhà输入法,用于linux系统的多字节文字输入。
不需要输入法框架。
不需要配置x window。
即起即用。

# 环境 python 2.7.x
需要以下包：
sudo apt-get install python-xlib
sudo apt-get install xdotool

#使用方法
1 python haha.py
2 需要输入时： Ctrl + Alt + Space
3 目前默认词库是全拼，所以输入汉语拼音吧.F1 - F4分别代表调号的1到4声.F5代表轻声.
4 看到候选字词之后，可以使用Space键选择第一个选项或者使用数字键选中对应选项.
5 使用pageup pagedown来翻页.


#注意
Hǎhà输入法主要用于万般无奈的情况下输入文字,并不适合日常编辑文本使用.


#files

converter.py
	将文本码表转换为haha使用的码表。

haha.py
	输入法主程序。
	
parser.py
	输入法的一部分。主要是查询和数据操作。
	
pinyin_table.py  word_15w.py
    用converter.py对xxxxxxxx.txt处理后，得到的字库初始化程序。
