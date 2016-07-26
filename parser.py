#encoding=utf8
import os

import subprocess

DEBUG = False

root_parse_tree = {}

parse_list = [
{"sim":"伟大的Simon"},
{"haha":"Hǎhà"},
{"foric":"for(int i=0;i <= 100;i++){ }"},
]

def op(keys,content):
    parse_list.append({keys:content})
#=================================================================
import word_15w
import pinyin_table 

#op("zhongwen","中文")

#=================================================================
def add_to_parse_tree(keys,content):
    parse_tree = root_parse_tree
    for char in keys:
        if not char in parse_tree.keys():
            parse_tree[char] = {}

        parse_tree = parse_tree[char]
            
    parse_tree[Content(content)] = content        
    if DEBUG:
        print(root_parse_tree)        

class Content:
    convert_dict = {
        "\n":"\n"
    }

    @classmethod
    def content_to_seq(clz,content):
        content_list = list(content)

    def __init__(self,content):
        self.typeSequence = content
        self.content = content
    def send_content(self):
        os.system('xdotool getwindowfocus windowfocus --sync type --clearmodifiers \'%s\'' % self.typeSequence )
        #for c in self.typeSequence:
        #    os.system('xdotool type --delay 30 --clearmodifiers \'%s\'' % c )
        #subprocess.call('xdotool type --delay 30 --clearmodifiers \'%s\'' % self.typeSequence,shell=True )


class Parser:
    def __init__(self):
        pass
        for parse_pattern in parse_list:
            keys = parse_pattern.keys()[0]
            content = parse_pattern[keys]
            if DEBUG :
                print "keys:%s content:%s" % (keys,content)

            add_to_parse_tree(keys,content)
        self.search_sequence = []
        self.current_tree = root_parse_tree

        self.reset_search()
    def get_search_sequence_string(self):
        return "".join([x.keys()[0] for x in self.search_sequence])
    def _search_content_in_tree(self,tree,max_count=-1):
        search_queue = [tree]
        content_queue = []
        if DEBUG:
            print "searching %s" % tree
        while len(search_queue)>0:
            target_tree = search_queue.pop()
            for (key,value) in target_tree.iteritems():
                #print type(key)
                if type(key) is str:
                    #this is a sub tree
                    search_queue.insert(0,value)
                elif isinstance(key,Content):
                    #this is a content
                    content_queue.append(key)

                    if max_count != -1 and len(content_queue) >= max_count:
                        #now we have enough results
                        return content_queue
                else:
                    print "WARNING: in _search_content_in_tree. This must be a bug!"
                    return content_queue
        return content_queue            
    def add_search_char(self,char):
        if char not in self.current_tree:
            return False
        if DEBUG:
            print self.search_sequence
        temp_tree = self.current_tree[char]
        if DEBUG:
            print temp_tree 
        if type(temp_tree) is dict:
            self.current_tree = temp_tree
            self.search_sequence.append({char:self.current_tree})
        else:
            print "WARING: in add_search_char. bad type in tree. must be a bug."
            return False
        return True
    def dec_search_char(self):
        self.search_sequence.pop()
        if len(self.search_sequence) > 0:
            self.current_tree = self.search_sequence[-1].values()[0]
        pass

    def reset_search(self):
        self.search_sequence = []
        self.current_tree = root_parse_tree
        pass
    def get_result(self,max_count=150):
        if len(self.search_sequence) < 1:
            return []
        results =self._search_content_in_tree(self.current_tree, max_count)
        return results

if __name__ == "__main__":
    print "parser test."
    parser = Parser()
    parser.add_search_char("x")
    #parser.add_search_char("i")
    #parser.add_search_char("m")
    results = parser.get_result()
    print "results:"
    print results

    for content in results:
        content.send_content()

