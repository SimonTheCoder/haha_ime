
#encoding=utf8

code_table_template = '''
#encoding=utf8
from parser import op
%s
'''

def word_15w():
    '''
    found at http://27.28.171.30/ws.cdn.baidupcs.com/file/d7028b37d9135d0d0325ae222f941367?bkt=p-a80639e70493d8259aba8a59fa539068&xcode=e31097a8d3aa04a4ad33d096a93a6e4fe1e78643b22f9534837047dfb5e85c39&fid=2584619759-250528-863540945&time=1469435807&sign=FDTAXGERBH-DCb740ccc5511e5e8fedcff06b081203-183XLVcHaAXvBU341XwOVAVUtz4%3D&to=cb&fm=Nan,B,T,t&sta_dx=4&sta_cs=17&sta_ft=rar&sta_ct=7&fm2=Nanjing,B,T,t&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=1400d7028b37d9135d0d0325ae222f941367f47967370000003ff311&expires=8h&rt=sh&r=123098255&mlogid=4793775978570420406&vuk=738459737&vbdid=3414377365&fin=cikukuozhan.rar&fn=cikukuozhan.rar&uta=0&rtype=0&iv=2&isw=0&dp-logid=4793775978570420406&dp-callid=0.1.1&wshc_tag=0&wsts_tag=5795cfa5&wsid_tag=3b2e732e&wsiphost=ipdbm
    '''
    filename = "./word_15w.txt"
    line_temp = 'op("%s","%s")\n'
    if_obj = open(filename,"r")
    of_obj = open("./word_15w.py","w")
    result_string = ""
     
    data_list = []
    for line in if_obj:
        #print line
        if line.startswith("#") or len(line) < 4:
            continue
        line = line.replace("\n","")
        print line
        (content,keys_raw,factor) = line.split(" ")
        result_string += (line_temp % (keys_raw.replace("|",""),content))

    if_obj.close()

    of_obj.write( code_table_template % result_string)

    of_obj.close()
def pinyin_table():
    '''
    found at /usr/share/ibus-table/data/pinyin_table.txt
    '''
    filename = "./pinyin_table.txt"
    line_temp = 'op("%s","%s")\n'
    if_obj = open(filename,"r")
    of_obj = open("./pinyin_table.py","w")
    result_string = ""
     
    data_list = []
    for line in if_obj:
        #print line
        if line.startswith("#") or len(line) < 4:
            continue
        line = line.replace("\n","")
        (content,keys_raw,factor) = line.split("\t") # it is a TAB
        if int(factor) < 3660001:
            continue
        data_list.append((content,keys_raw,int(factor)))
    
    sort_data_list = sorted(data_list,key=lambda factor:factor[2],reverse=True)
    #print sort_data_list
    for data in sort_data_list:
        (content,keys_raw,factor) = data
        for keys in keys_raw.split(" "):
            result_string += (line_temp % (keys,content)) + "#" +str(factor) +"\n"

    if_obj.close()

    of_obj.write( code_table_template % result_string)

    of_obj.close()
            


def sogou_2013_9_13():
    pass
    filename = "./sogou1.txt"

    if_obj = open(filename,"r")
    of_obj = open("./sogou1.py","w")
    result_string = ""
    for line in if_obj:
        line = line.replace("\n","")
        oldlen = len(line)
        line = line.replace("'","")
        is_word = False
        if oldlen - len(line) >1:
            is_word = True
        print line
        (keys,content) =  line.split(" ")
        content_list = list(content.decode("utf8"))
        if is_word:
            result_string += 'op("%s","%s")\n'% (keys, content)
        else:
            for word in content_list:
                result_string += 'op( "%s","%s")\n' % (keys, word.encode("utf8"))
    if_obj.close()

    of_obj.write( code_table_template % result_string)

    of_obj.close()

def main():
    #sogou_2013_9_13()
    word_15w()
    pinyin_table()

if __name__ == "__main__":
    main()
