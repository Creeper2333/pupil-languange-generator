import json
from random import randint
import configparser
import time,os,sys
try:
    import bili_ky
except ImportError:
    input('依赖都安装完了吗？！')
    os._exit(0)

词库=None
配置=None

def read_config():
    conf=configparser.ConfigParser()
    path='config.ini'
    conf.read(path)

    基础=conf.items('basics')
    词库文件=基础[0][1]

    密度=conf.items('density')
    男魂密度=1/float(密度[0][1])
    空格密度=1/float(密度[1][1])
    句末加括号密度=1/float(密度[2][1])
    突发恶疾密度=1/float(密度[3][1])

    文本设置=conf.items('content')
    正文段落数=int(文本设置[0][1])
    开头部分最大长度=int(文本设置[1][1])
    正文段落最大长度=int(文本设置[2][1])
    是否使用结尾段=str(文本设置[3][1])

    迫真自动化=conf.items('automation')
    生成文章数=int(迫真自动化[0][1])
    自动保存文章=str(迫真自动化[1][1])
    睿站ky胜者为王=str(迫真自动化[2][1])
    ky视频列表=str(迫真自动化[3][1]).split()

    return (
        {
            "word_file":词库文件,
            "nanhun":男魂密度,
            "space":空格密度,
            "sentence_end":句末加括号密度,
            "bullshit":突发恶疾密度,
            "content_para":正文段落数,
            "head_maxlen":开头部分最大长度,
            "para_maxlen":正文段落最大长度,
            "use_ending":是否使用结尾段,
            "passages":生成文章数,
            "autosave":自动保存文章,
            "bili_ky":睿站ky胜者为王,
            'bili_ky_list':ky视频列表
        }
    )

def 加载json(filename='nonsence.json'):
    with open(filename,'r',encoding='utf-8') as file:
        return json.loads(file.read())

def 生成词汇组():
    词汇组列表=词库['meme_sets']
    词汇组=词汇组列表[randint(0,len(词汇组列表)-1)]
    return (
        词汇组['set'][0]*randint(
            int(词汇组['min_repeat']),
            int(词汇组['max_repeat'])
        )+
        词汇组['set'][1]*randint(
            int(词汇组['min_repeat_2']),
            int(词汇组['max_repeat_2'])
        )
    )

def 生成词汇():
    词汇列表=词库['meme_single']
    词汇=词汇列表[randint(0,len(词汇列表)-1)]
    return(
        词汇['value']*randint(
            词汇['min_repeat'],
            词汇['max_repeat']
        )
    )

def 生成可替换词汇_开头():
    可替换=词库['replaceable_head'][randint(0,len(词库['replaceable_head'])-1)]
    content=可替换['value']
    for i in 可替换['replace']:
        content=content.replace(i,
            可替换['replace'][i][randint(0,len(可替换['replace'][i])-1)]
        )
    return content
def 生成开头():
    tmp=生成可替换词汇_开头()
    end=词库['sentence_end_head']
    while len(tmp)<=配置['head_maxlen']:
        add=''
        use_which=randint(0,100)
        if use_which<10:
            add=生成词汇组()
        else:
            add=生成词汇()
        use_nanhun=randint(0,配置['nanhun'])
        if use_nanhun==0 and ('♂' not in add):
            nh=''
            for i in add:
                nh+=i.replace(i,i+'♂')
            add=nh
        else:
            use_space=randint(0,配置['space'])
            if use_space==0:
                sp=''
                for i in add:
                    sp+=i.replace(i,i+' ')
                add=sp.strip()
            else:
                use_end=randint(0,配置['sentence_end'])
                if use_end==0:
                    add+=end[randint(0,len(end)-1)]
        tmp+=add
        if randint(0,配置['bullshit'])==0:
            tmp+=词库['bullshit'][randint(0,len(词库['bullshit'])-1)]*randint(1,3)
        add=''
    #print(len(tmp))
    return tmp

def 生成正文():
    for i in range(0,配置['content_para']):
        tmp_all=''
        tmp=''
        end=词库['sentence_end_body']
        while len(tmp)<=配置['para_maxlen']:
            add=''
            use_which=randint(0,100)
            if use_which<10:
                add=生成词汇组()
            else:
                add=生成词汇()
            use_nanhun=randint(0,配置['nanhun'])
            if use_nanhun==0 and ('♂' not in add):
                nh=''
                for i in add:
                    nh+=i.replace(i,i+'♂')
                add=nh
            else:
                use_space=randint(0,配置['space'])
                if use_space==0:
                    sp=''
                    for i in add:
                        sp+=i.replace(i,i+' ')
                    add=sp.strip()
                else:
                    use_end=randint(0,配置['sentence_end'])
                    if use_end==0:
                        add+=end[randint(0,len(end)-1)]
            tmp+=add
            if randint(0,配置['bullshit'])==0:
                tmp+=词库['bullshit'][randint(0,len(词库['bullshit'])-1)]*randint(1,3)
            add=''
            #print(len(tmp))
        tmp_all+=tmp+'\n'
        tmp=''
    #print(len(tmp_all))
    return tmp_all.strip()

def 生成():
    tmp=''
    tmp+=生成开头()
    tmp+=生成正文()
    if 配置['use_ending'].lower()=='true':
        tmp+=词库['content_end'][randint(0,len(词库['content_end'])-1)]
    return tmp

if __name__=='__main__':
    debug_mode=True
    配置=read_config()
    词库=加载json(配置['word_file'])
    passages=[]
    for i in range(0,配置['passages']):
        p=生成()
        passages.append(p)
        print(p)
        if 配置['autosave']=='true':
            with open('passage_'+time.strftime('%Y-%m-%d-%H-%M-%S')+' No.'+str(i+1)+'.txt','w',encoding='utf-8') as f:
                f.write(p)
                f.close()
        if 配置['bili_ky']=='true':
            if debug_mode:
                sessdata=sys.argv[1]
                jct=sys.argv[2]
            else:
                sessdata,jct=bili_ky.run_login()
            count=0
            while count<len(passages) and count<len(配置['bili_ky_list']):
                bili_ky.send_comment(jct,sessdata,配置['bili_ky_list'][count],passages[count])
                count+=1