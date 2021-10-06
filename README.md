# 睿站小学生<sup>[1](#1--这里的小学生不是传统意义上的小学生剩下的应该不用我解释了)</sup>发病模拟

## 简介

本项目旨在~~（比较）~~真实地还原睿站小学生无脑 ky，突发恶疾时的状态。本项目仅供娱乐，请不要上纲上线。

## 使用方法

### 配置词库

本程序使用的词库结构如下：

```json
{
    "bullshit":[wtf??],
    "sentence_end_head":[text with brakes for the head of the content],
    "sentence_end_body":[text with brakes for the body of the content],
    "meme_sets":[
        {
            "set":[word1,word2],
            "min_repeat": minimum repitition times for word 1,
            "max_repeat": maximum repitition times for word 1,
            "min_repeat_2": .......................... word 2,
            "max_repeat_2": .......................... word 2
        },
        {
            ...
        }
    			],
   "meme_single":[
            {
            "value":word,
            "min_repeat": minimum repitition times,
            "max_repeat": maximum repitition times
        },
        {
            ...
        }
            	],
   "replaceable_head":[
            {
            "value": original, eg. 这个骷髅好像a,
            replace:{
            "(mark)": [option1, option2, ...] eg. "a":['sans','papyrus'], result: "这个骷髅好像sans", etc.
        }
        }
            		]
"replaceable_body":[same as "replaceable_head"]
"content_end": end of the passage.
}
```

理论上，通过自己修改词库，可以达到扩容或个性化的目的。（欢迎 pr 提交词库扩容！！(/≧▽≦)/  ）

### 修改配置文件

这里是一个程序使用的配置文件的示例：

```ini
[basics]
word_list=nonsense.json

[density]
nanhun_density=0.1
space_density=0.2
sentence_end_density=0.1
bullshit_density=0.05

[content]
body_paragraph=10
head_control_length=500
body_paragraph_control_length=5000
use_ending=true

[automation]
generate_passage_numbers=2
passage_auto_save=true
bilibili_auto_ky=false
```

其中，word list 字段为使用的词库。

nanhun density 字段则是“♂”符号出现的概率（越小概率越低，下同）。space density 是在句中打空格的概率，sentence end density指的是句末加括号文本的概率，bullshit density 是突发恶疾的概率。

body paragraph 指正文段落数，head control length 为开头最大字符数（最好设的比较大），body paragraph control length 为正文最大字符数（同样设大点），use ending 则是选择是否要抽取一个结尾。

generate passage numbers 指要生成几个文章，passage auto save 指是否自动保存生成的文章，bilibili auto ky 指是否要将生成的东西自动发到睿站（未做）。

ps：这个文件已经在 repo 里了。

### 运行

配置好相关文件后，直接

```
> python main.py
```

即可。

## 其它

- 本程序遵守 MIT 开源协议。
- 想法来源于 [menzi11/BullshitGenerator](https://github.com/menzi11/BullshitGenerator)

## 注释

##### <sup>[1]</sup>  这里的“小学生”不是传统意义上的小学生，剩下的应该不用我解释了。
