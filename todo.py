import random
todo = ['JAVA', '数据结构', '数字电路', '线性代数', '英语']
where = ['图书馆1层','图书馆2层','图书馆3层','图书馆4层','图书馆5层']
using = ['Surface','教材','图书馆的书','网课']
num = random.randint(0,len(todo) - 1)
doko = random.randint(0,len(where) - 1)
use = random.randint(0,len(using) - 1)
print('在' + where[doko] + '用' +  using[use] + '学' + todo[num])
