#### pip install gradio==3.50.2
import gradio as gr
import pandas as pd
import numpy as np
import os
import json
import re
from functools import partial

from rapidfuzz import fuzz
import imagehash
from datasets import load_dataset
from PIL import Image

character_img_ds = load_dataset("svjack/genshin-impact-character-image-add-some")
character_img_dict = dict(pd.Series(character_img_ds["train"]).map(lambda x: (x["name"], x["img"])).values.tolist())

partial_order_list = ['迭卡拉庇安',
 '安德留斯',
 '温妮莎',
 '特瓦林',
 '法尔伽',
 '艾伦德林',
 '鲁斯坦',
 '奥兹',
 '炎之魔女',
 '杜林',
 '克利普斯',
 '归终',
 '赫乌莉亚',
 '奥赛尔',
 '马科修斯',
 '若陀龙王',
 '浮舍',
 '铜雀',
 '削月筑阳真君',
 '理水叠山真君',
 '留云借风真君',
 '歌尘浪市真君',
 '移霄导天真君',
 '天叔',
 '跋掣',
 '奥罗巴斯',
 '狐斋宫',
 '御舆千代',
 '五百藏',
 '百代',
 '九条孝行',
 '九条镰治',
 '柊慎介',
 '柊千里',
 '哲平',
 '散兵倾奇者',
 '阿瑠',
 '雪奈茨芙娜',
 '阿赫玛尔',
 '阿扎尔',
 '迪娜泽黛',
 '泽维尔']

partial_order_list += [
 '那维莱特',
 "芙宁娜",
 '魈',

 "可莉",
 "提纳里",
 #"行秋", "柯莱", "凝光", "北斗", "五郎",

 '钟离',
 '纳西妲',
 '刻晴',
 '优菈',
 '八重神子',
 #'可莉',
 '夜兰',
 '妮露',
 '娜维娅',
 '宵宫',
 #'提纳里',
 '林尼',
 '枫原万叶',
 '流浪者',
 '温迪',
 '珊瑚宫心海',
 '琴',
 '甘雨',
 '申鹤',
 '白术',
 '神里绫人',
 '神里绫华',
 '胡桃',
 '艾尔海森',
 #'芙宁娜',
 '荒泷一斗',
 '莫娜',
 '莱欧斯利',
 '赛诺',
 '达达利亚',
 '迪卢克',
 '迪希雅',
 '阿贝多',
 '雷电将军',
 '七七'
 ]

im_list_a = []
im_list_b = []
for character_name, character_img in character_img_dict.items():
    if character_name in partial_order_list:
        im_list_a.append(character_img)
    else:
        im_list_b.append(character_img)
assert len(im_list_a) == len(partial_order_list)
im_list = pd.Series(partial_order_list).map(lambda x: character_img_dict[x]).values.tolist() + im_list_b


import jieba
def repeat_to_one_f(x):
    req = None
    for token in jieba.lcut(x):
        #print("req :", req)

        if len(set(token)) == 1:
            token = token[0]
        if req is None:
            req = token
        else:

            if token in req:
                continue
            else:
                while req.endswith(token[0]):
                    token = token[1:]
                req = req + token
    return req.strip()

def repeat_to_one_fb(x):
    return sorted(map(repeat_to_one_f, [x, "".join(jieba.lcut(x)[::-1])]),
                 key = len
                 )[0]

repeat_to_one = repeat_to_one_fb

def process_info(x, maintain_chars = ",.。，;:：；?？\n——"):
    req = re.findall(u"[0-9\u4e00-\u9fa5{}]+".format(maintain_chars) ,x)
    return "".join(req)

from huggingface_hub import snapshot_download

if not os.path.exists("genshin-impact-character-add-some"):
    path = snapshot_download(
        repo_id="svjack/genshin-impact-character-add-some",
        repo_type="dataset",
        local_dir="genshin-impact-character-add-some",
        local_dir_use_symlinks = False
    )

if not os.path.exists("genshin_impact_character_llamazh13b_ggml"):
    path = snapshot_download(
        repo_id="svjack/genshin_impact_character_llamazh13b_ggml",
        repo_type="model",
        local_dir="genshin_impact_character_llamazh13b_ggml",
        local_dir_use_symlinks = False
    )

info_df = pd.read_csv("genshin-impact-character-add-some/genshin_impact_background_settings_constrained.csv")
info_df["info"] = info_df["info"].map(eval)

with open("genshin-impact-character-add-some/genshin_impact_character_setting.json", "r") as f:
    character_setting_total_dict = json.load(f)

req_dict = {}
for k, v_dict in character_setting_total_dict.items():
    req_dict[k] = {}
    for kk, vv in v_dict.items():
        if kk != "元素力":
            req_dict[k][kk] = vv
character_setting_total_dict = req_dict

def get_character_background_list(info_dict):
    text = []
    if "角色详细" in info_dict["描述"]:
        text.append(info_dict["描述"]["角色详细"])
    if "更多描述" in info_dict["描述"]:
        text.append(info_dict["描述"]["更多描述"])
    return list(map(lambda x: x.replace(" ", "").replace("\n\n", "\n"), text))
def get_character_background(info_dict):
    return "\n".join(get_character_background_list(info_dict))

pd.DataFrame(
pd.Series(character_setting_total_dict.values()).map(
    lambda x: {
        "性别": x['性别'],
        "国籍": x["国籍"]
    }
).values.tolist()).apply(lambda x: set(x), axis = 0).to_dict()


character_setting_total_dist_dict = {
 '姓名': "",
 '性别': {'少女女性', '少年男性', '成年女性', '成年男性'},
 '国籍': {'枫丹', '璃月', '稻妻', '至冬', '蒙德', '须弥'},
 '身份': "",
 '性格特征': "",
 '角色介绍': "",
 }

'''
 #### text background_text
 text = get_character_background(info_dict)
'''

def get_character_setting_total_dict(name):
    from copy import deepcopy
    req = deepcopy(character_setting_total_dist_dict)
    if name in character_setting_total_dict:
        for k, v in character_setting_total_dict[name].items():
            req[k] = v
        info_dict = dict(info_df[["title", "info"]].values.tolist())[name]
        req["角色介绍"] = get_character_background(info_dict)
    req["姓名"] = name
    return req

get_character_setting_total_dict("迪卢克")

get_character_setting_total_dict("阿扎尔")

prompt_format_dict = {
    "Basic_Info": ["性别", "国籍", "身份", "性格特征"],

    "两人同属{}": ["国籍"],
    "{}来自{},{}来自{}。": ["姓名", "国籍", "姓名", "国籍"],

    "下面是{}的一些基本信息\n{}": ["姓名", "Basic_Info"],
    "下面是{}的一些基本信息\n{}\n这些是一段角色介绍\n{}": ["姓名", "Basic_Info", "角色介绍"],

    "续写下面的角色介绍，下面是角色介绍的开头。{}是{}。{}": ["姓名", "身份", "Text"],
    "续写下面的角色故事，下面是角色故事的开头。{}是{}。{}": ["姓名", "身份", "Text"],
    "续写下面获得神之眼的过程，下面是开头。{}是{}。{}": ["姓名", "身份", "Text"],
    "{}给你写了一封信，信主题是{}，信的内容是这样的。": ["姓名", "Text"],

    "{}在进行有关{}的聊天时会说什么？": ["姓名", "Text"],
    "{}在{}的时候会说什么？": ["姓名", "Text"],
    "{}在{}时会说什么？": ["姓名", "Text"],
    "关于{}，{}会说什么?": ["Text", "姓名"],
    "当你想要了解{}时": ["姓名"],

    "关于{}，{}会说什么?": ["姓名", "姓名"],
    "从{}那里，可以获得哪些关于{}的信息？": ["姓名", "姓名"]
}

def single_character_prompt_func(name,
    used_prompt_format_dict,
    character_setting_rewrite_dict = {},
    Text = "",
    ):
    assert type(used_prompt_format_dict) == type({})
    assert type(character_setting_rewrite_dict) == type({})
    character_setting_total_dict = get_character_setting_total_dict(name)
    for k, v in character_setting_rewrite_dict.items():
        if k in character_setting_total_dict:
            character_setting_total_dict[k] = v
    key = list(used_prompt_format_dict.keys())[0]
    assert key in prompt_format_dict
    if key == "Basic_Info":
        return "\n".join(
        map(lambda k: "{}:{}".format(k, character_setting_total_dict[k]), prompt_format_dict[key])
        )
    elif key == "两人同属{}":
        return "两人同属{}".format(character_setting_total_dict["国籍"])
    elif key == "下面是{}的一些基本信息\n{}":
        return "下面是{}的一些基本信息\n{}".format(name,
            single_character_prompt_func(name,
                {
                    "Basic_Info": ["性别", "国籍", "身份", "性格特征"]
                },
                character_setting_rewrite_dict
            )
        )
    elif key == "下面是{}的一些基本信息\n{}\n这些是一段角色介绍\n{}":
        return "下面是{}的一些基本信息\n{}\n这些是一段角色介绍\n{}".format(
            name,
            single_character_prompt_func(name,
                {
                    "Basic_Info": ["性别", "国籍", "身份", "性格特征"]
                },
                character_setting_rewrite_dict
            ),
            character_setting_total_dict["角色介绍"]
        )
    elif key == "续写下面的角色介绍，下面是角色介绍的开头。{}是{}。{}":
        return "续写下面的角色介绍，下面是角色介绍的开头。{}是{}。{}".format(
            name,
            character_setting_total_dict["身份"],
            Text
        )
    elif key == "续写下面的角色故事，下面是角色故事的开头。{}是{}。{}":
        return "续写下面的角色故事，下面是角色介绍的开头。{}是{}。{}".format(
            name,
            character_setting_total_dict["身份"],
            Text
        )
    elif key == "续写下面获得神之眼的过程，下面是开头。{}是{}。{}":
        return "续写下面获得神之眼的过程，下面是开头。{}是{}。{}".format(
            name,
            character_setting_total_dict["身份"],
            Text
        )
    elif key == "{}给你写了一封信，信主题是{}，信的内容是这样的。":
        return "{}给你写了一封信，信主题是{}，信的内容是这样的。".format(
            name,
            Text
        )
    elif key == "{}在进行有关{}的聊天时会说什么？":
        return "{}在进行有关{}的聊天时会说什么？".format(
            name,
            Text
        )
    elif key == "{}在{}的时候会说什么？":
        return "{}在{}的时候会说什么？".format(
            name,
            Text
        )
    elif key == "{}在{}时会说什么？":
        return "{}在{}时会说什么？".format(
            name,
            Text
        )
    elif key == "关于{}，{}会说什么?":
        return "关于{}，{}会说什么?".format(
            Text,
            name,
        )
    elif key == "当你想要了解{}时":
        return "当你想要了解{}时".format(
            name,
        )
    return 1 / 0

def two_character_prompt_func(
    name_1,
    name_2,
    used_prompt_format_dict,
    character_setting_rewrite_dict_1 = {},
    character_setting_rewrite_dict_2 = {},
    ):
    assert type(character_setting_rewrite_dict_1) == type({})
    character_setting_total_dict_1 = get_character_setting_total_dict(name_1)
    for k, v in character_setting_rewrite_dict_1.items():
        if k in character_setting_total_dict_1:
            character_setting_total_dict_1[k] = v
    character_setting_total_dict_2 = get_character_setting_total_dict(name_2)
    for k, v in character_setting_rewrite_dict_2.items():
        if k in character_setting_total_dict_2:
            character_setting_total_dict_2[k] = v
    key = list(used_prompt_format_dict.keys())[0]
    assert key in prompt_format_dict
    if key == "关于{}，{}会说什么?":
        return "关于{}，{}会说什么?".format(name_1, name_2)
    elif key == "从{}那里，可以获得哪些关于{}的信息？":
        return "从{}那里，可以获得哪些关于{}的信息？".format(name_1, name_2)
    elif key == "{}来自{},{}来自{}。":
        return "{}来自{},{}来自{}。".format(name_1, character_setting_total_dict_1["国籍"],
        name_2, character_setting_total_dict_2["国籍"],
        )
    return 1 / 0

def main_single_character_prompt_func(name,
    used_prompt_format_dict,
    character_setting_rewrite_dict = {},
    Text = "",
    ):
    key = list(used_prompt_format_dict.keys())[0]
    assert key in prompt_format_dict
    if key == "续写下面的角色介绍，下面是角色介绍的开头。{}是{}。{}":
        task_prompt = single_character_prompt_func(
            name,
            used_prompt_format_dict,
            character_setting_rewrite_dict,
            Text
        )
        info_prompt = single_character_prompt_func(
            name,
            {
                "下面是{}的一些基本信息\n{}": ["姓名", "Basic_Info"]
            },
            character_setting_rewrite_dict,
            Text
        )
    elif key == "续写下面的角色故事，下面是角色故事的开头。{}是{}。{}":
        task_prompt = single_character_prompt_func(
            name,
            used_prompt_format_dict,
            character_setting_rewrite_dict,
            Text
        )
        info_prompt = single_character_prompt_func(
            name,
            {
            "下面是{}的一些基本信息\n{}\n这些是一段角色介绍\n{}": ["姓名", "Basic_Info", "角色介绍"]
            },
            character_setting_rewrite_dict,
            Text
            )

    elif key == "续写下面获得神之眼的过程，下面是开头。{}是{}。{}":
        task_prompt = single_character_prompt_func(
            name,
            used_prompt_format_dict,
            character_setting_rewrite_dict,
            Text
        )
        info_prompt = single_character_prompt_func(
            name,
            {
            "下面是{}的一些基本信息\n{}\n这些是一段角色介绍\n{}": ["姓名", "Basic_Info", "角色介绍"]
            },
            character_setting_rewrite_dict,
            Text
            )

    elif key == "{}给你写了一封信，信主题是{}，信的内容是这样的。":
        task_prompt = single_character_prompt_func(
            name,
            used_prompt_format_dict,
            character_setting_rewrite_dict,
            Text
        )
        info_prompt = single_character_prompt_func(
            name,
            {
            "下面是{}的一些基本信息\n{}\n这些是一段角色介绍\n{}": ["姓名", "Basic_Info", "角色介绍"]
            },
            character_setting_rewrite_dict,
            Text
            )
    elif key == "{}在进行有关{}的聊天时会说什么？":
        task_prompt = single_character_prompt_func(
            name,
            used_prompt_format_dict,
            character_setting_rewrite_dict,
            Text
        )
        info_prompt = single_character_prompt_func(
            name,
            {
            "下面是{}的一些基本信息\n{}\n这些是一段角色介绍\n{}": ["姓名", "Basic_Info", "角色介绍"]
            },
            character_setting_rewrite_dict,
            Text
            )
    elif key == "{}在{}的时候会说什么？":
        task_prompt = single_character_prompt_func(
            name,
            used_prompt_format_dict,
            character_setting_rewrite_dict,
            Text
        )
        info_prompt = single_character_prompt_func(
            name,
            {
            "下面是{}的一些基本信息\n{}\n这些是一段角色介绍\n{}": ["姓名", "Basic_Info", "角色介绍"]
            },
            character_setting_rewrite_dict,
            Text
            )
    elif key == "{}在{}时会说什么？":
        task_prompt = single_character_prompt_func(
            name,
            used_prompt_format_dict,
            character_setting_rewrite_dict,
            Text
        )
        info_prompt = single_character_prompt_func(
            name,
            {
            "下面是{}的一些基本信息\n{}\n这些是一段角色介绍\n{}": ["姓名", "Basic_Info", "角色介绍"]
            },
            character_setting_rewrite_dict,
            Text
            )
    elif key == "关于{}，{}会说什么?":
        task_prompt = single_character_prompt_func(
            name,
            used_prompt_format_dict,
            character_setting_rewrite_dict,
            Text
        )
        info_prompt = single_character_prompt_func(
            name,
            {
            "下面是{}的一些基本信息\n{}\n这些是一段角色介绍\n{}": ["姓名", "Basic_Info", "角色介绍"]
            },
            character_setting_rewrite_dict,
            Text
            )
    elif key == "当你想要了解{}时":
        task_prompt = single_character_prompt_func(
            name,
            used_prompt_format_dict,
            character_setting_rewrite_dict,
            Text
        )
        info_prompt = single_character_prompt_func(
            name,
            {
            "下面是{}的一些基本信息\n{}\n这些是一段角色介绍\n{}": ["姓名", "Basic_Info", "角色介绍"]
            },
            character_setting_rewrite_dict,
            Text
            )
    return task_prompt, info_prompt

def main_two_character_prompt_func(
    name_1,
    name_2,
    used_prompt_format_dict,
    character_setting_rewrite_dict_1 = {},
    character_setting_rewrite_dict_2 = {},
    ):
    task_prompt = two_character_prompt_func(
        name_1,
        name_2,
        used_prompt_format_dict,
        character_setting_rewrite_dict_1,
        character_setting_rewrite_dict_2)
    info_prompt_1 = single_character_prompt_func(
        name_1,
        {
            "下面是{}的一些基本信息\n{}\n这些是一段角色介绍\n{}": ["姓名", "Basic_Info", "角色介绍"]
        },
        character_setting_rewrite_dict_1,
        )
    info_prompt_2 = single_character_prompt_func(
        name_2,
        {
            "下面是{}的一些基本信息\n{}\n这些是一段角色介绍\n{}": ["姓名", "Basic_Info", "角色介绍"]
        },
        character_setting_rewrite_dict_2,
        )
    character_setting_total_dict_1 = get_character_setting_total_dict(name_1)
    for k, v in character_setting_rewrite_dict_1.items():
        if k in character_setting_total_dict_1:
            character_setting_total_dict_1[k] = v
    character_setting_total_dict_2 = get_character_setting_total_dict(name_2)
    for k, v in character_setting_rewrite_dict_2.items():
        if k in character_setting_total_dict_2:
            character_setting_total_dict_2[k] = v

    country_prompt = ""
    same_country = character_setting_total_dict_1["国籍"] == character_setting_total_dict_2["国籍"]
    if same_country:
        country_prompt = single_character_prompt_func(
            name_1,
            {
                "两人同属{}": ["国籍"]
            },
            character_setting_rewrite_dict_1,
            )
    else:
        country_prompt = two_character_prompt_func(
                name_1,
                name_2,
                {
                "{}来自{},{}来自{}。": ["姓名", "国籍", "姓名", "国籍"]
                },
                character_setting_rewrite_dict_1,
                character_setting_rewrite_dict_2,
            )
    info_prompt = "\n".join(
        [info_prompt_1, info_prompt_2, country_prompt]
    )
    return task_prompt, info_prompt

def main_single_character_prompt_func_cls(
    name,
    task,
    character_setting_rewrite_dict = {},
    Text = "",
):
    #assert task in ["介绍", "故事", "神之眼", "信", "聊天", "时候", "关于", "了解"]
    assert task in ["介绍", "故事", "信", "聊天", "时候", "关于", "了解"]
    if task == "介绍":
        return main_single_character_prompt_func(
            name,
            {
            "续写下面的角色介绍，下面是角色介绍的开头。{}是{}。{}": ["姓名", "身份", "Text"],
            },
            character_setting_rewrite_dict = character_setting_rewrite_dict,
            Text = Text,
        )
    elif task == "故事":
        return main_single_character_prompt_func(
            name,
            {
            "续写下面的角色故事，下面是角色故事的开头。{}是{}。{}": ["姓名", "身份", "Text"],
            },
            character_setting_rewrite_dict = character_setting_rewrite_dict,
            Text = Text,
        )
    elif task == "神之眼":
        return main_single_character_prompt_func(
            name,
            {
            "续写下面获得神之眼的过程，下面是开头。{}是{}。{}": ["姓名", "身份", "Text"],
            },
            character_setting_rewrite_dict = character_setting_rewrite_dict,
            Text = Text,
        )
    elif task == "信":
        return main_single_character_prompt_func(
            name,
            {
            "{}给你写了一封信，信主题是{}，信的内容是这样的。": ["姓名", "Text"],
            },
            character_setting_rewrite_dict = character_setting_rewrite_dict,
            Text = Text,
        )
    elif task == "聊天":
        return main_single_character_prompt_func(
            name,
            {
            "{}在进行有关{}的聊天时会说什么？": ["姓名", "Text"],
            },
            character_setting_rewrite_dict = character_setting_rewrite_dict,
            Text = Text,
        )
    elif task == "时候":
        return main_single_character_prompt_func(
            name,
            {
            "{}在{}的时候会说什么？": ["姓名", "Text"],
            },
            character_setting_rewrite_dict = character_setting_rewrite_dict,
            Text = Text,
        )
    elif task == "关于":
        return main_single_character_prompt_func(
            name,
            {
            "关于{}，{}会说什么?": ["Text", "姓名"],
            },
            character_setting_rewrite_dict = character_setting_rewrite_dict,
            Text = Text,
        )
    elif task == "了解":
        return main_single_character_prompt_func(
            name,
            {
            "当你想要了解{}时": ["姓名"],
            },
            character_setting_rewrite_dict = character_setting_rewrite_dict,
            Text = Text,
        )
    return 1 / 0

def main_two_character_prompt_func_cls(
    name_1,
    name_2,
    task,
    character_setting_rewrite_dict_1 = {},
    character_setting_rewrite_dict_2 = {},
    ):
    assert task in ["会说什么", "哪些信息"]
    if task == "会说什么":
        return main_two_character_prompt_func(
            name_1,
            name_2,
            {
            "关于{}，{}会说什么?": ["姓名", "姓名"],
            },
            character_setting_rewrite_dict_1,
            character_setting_rewrite_dict_2
        )
    elif task == "哪些信息":
        return main_two_character_prompt_func(
            name_1,
            name_2,
            {
            "从{}那里，可以获得哪些关于{}的信息？": ["姓名", "姓名"]
            },
            character_setting_rewrite_dict_1,
            character_setting_rewrite_dict_2
        )
    return 1 / 0

character_setting_total_dist_dict = {
 '姓名': "",
 '性别': {'少女女性', '少年男性', '成年女性', '成年男性'},
 '国籍': {'枫丹', '璃月', '稻妻', '至冬', '蒙德', '须弥'},
 '身份': "",
 '性格特征': "",
 '角色介绍': "",
 }

all_single_task = ["介绍", "故事", "信", "聊天", "时候", "关于", "了解"]
all_two_task = ["会说什么", "哪些信息"]

all_genders = ['少女女性', '少年男性', '成年女性', '成年男性']
all_countries = ['蒙德','璃月', '稻妻', '须弥','枫丹', '至冬']

def get_single_name(images, evt: gr.SelectData, repo_card_im_dict = character_img_dict):
    img_selected = images[evt.index]
    #print(img_selected)
    im_data = img_selected["name"]
    im = Image.open(im_data)
    im_hash = imagehash.average_hash(
        im, hash_size = 1024
    )
    min_diff = int(1e10)
    min_repo_name = ""
    for repo_name, repo_card_image in repo_card_im_dict.items():
        repo_img = repo_card_image
        repo_img_hash = imagehash.average_hash(
            repo_img, hash_size = 1024
        )
        diff = im_hash - repo_img_hash
        if diff < min_diff:
            min_diff = diff
            min_repo_name = repo_name
    print(im_data ,min_repo_name, min_diff)
    assert len(min_repo_name) > 0
    single_name = min_repo_name
    return single_name

#def change_single_name(single_name):
def change_single_name(images, evt: gr.SelectData,):
    single_name = get_single_name(images, evt)

    if hasattr(single_name, "value"):
        single_name_ = single_name.value
    else:
        single_name_ = single_name
    character_setting_total_dict = get_character_setting_total_dict(single_name)
    character_setting_total_dict = dict(map(lambda t2: (t2[0] ,t2[1] if type(t2[1]) == type("") else ""),
        character_setting_total_dict.items()))
    return character_setting_total_dict["姓名"], \
    gr.Dropdown.update(value = character_setting_total_dict["性别"], choices = all_genders), \
    gr.Dropdown.update(value = character_setting_total_dict["国籍"], choices = all_countries), \
        character_setting_total_dict["身份"], \
        character_setting_total_dict["性格特征"], character_setting_total_dict["角色介绍"]

def get_single_prompt(
    single_name, select_gender, select_country, single_identity, single_disposition,
    select_task, Text, single_introduction
):
    if hasattr(single_name, "value"):
        single_name_ = single_name.value
    else:
        single_name_ = single_name
    if hasattr(select_gender, "value"):
        select_gender_ = select_gender.value
    else:
        select_gender_ = select_gender
    if hasattr(select_country, "value"):
        select_country_ = select_country.value
    else:
        select_country_ = select_country
    if hasattr(single_identity, "value"):
        single_identity_ = single_identity.value
    else:
        single_identity_ = single_identity
    if hasattr(single_disposition, "value"):
        single_disposition_ = single_disposition.value
    else:
        single_disposition_ = single_disposition
    if hasattr(select_task, "value"):
        select_task_ = select_task.value
    else:
        select_task_ = select_task
    if hasattr(Text, "value"):
        Text_ = Text.value
    else:
        Text_ = Text
    if hasattr(single_introduction, "value"):
        single_introduction_ = single_introduction.value
    else:
        single_introduction_ = single_introduction
    character_setting_rewrite_dict = {
     '姓名': single_name_,
     '性别': select_gender_,
     '国籍': select_country_,
     '身份': single_identity_,
     '性格特征': single_disposition_,
     '角色介绍': single_introduction_,
     }
    a, b = main_single_character_prompt_func_cls(
        single_name_,
        select_task_,
        character_setting_rewrite_dict = character_setting_rewrite_dict,
        Text = Text,
        )
    #a = a.replace("？", "?")
    req = "\n".join([b, a])
    req = process_info(req)
    return req
    #return "\n".join([b, a])

def get_two_prompt(
    single_name_1, select_gender_1, select_country_1, single_identity_1, single_disposition_1,
    single_introduction_1,
    single_name_2, select_gender_2, select_country_2, single_identity_2, single_disposition_2,
    single_introduction_2, two_task,
):
    assert two_task in ["会说什么", "哪些信息"]
    if hasattr(single_name_1, "value"):
        single_name_1_ = single_name_1.value
    else:
        single_name_1_ = single_name_1
    if hasattr(select_gender_1, "value"):
        select_gender_1_ = select_gender_1.value
    else:
        select_gender_1_ = select_gender_1
    if hasattr(select_country_1, "value"):
        select_country_1_ = select_country_1.value
    else:
        select_country_1_ = select_country_1
    if hasattr(single_identity_1, "value"):
        single_identity_1_ = single_identity_1.value
    else:
        single_identity_1_ = single_identity_1
    if hasattr(single_disposition_1, "value"):
        single_disposition_1_ = single_disposition_1.value
    else:
        single_disposition_1_ = single_disposition_1
    if hasattr(single_introduction_1, "value"):
        single_introduction_1_ = single_introduction_1.value
    else:
        single_introduction_1_ = single_introduction_1

    if hasattr(single_name_2, "value"):
        single_name_2_ = single_name_2.value
    else:
        single_name_2_ = single_name_2
    if hasattr(select_gender_2, "value"):
        select_gender_2_ = select_gender_2.value
    else:
        select_gender_2_ = select_gender_2
    if hasattr(select_country_2, "value"):
        select_country_2_ = select_country_2.value
    else:
        select_country_2_ = select_country_2
    if hasattr(single_identity_2, "value"):
        single_identity_2_ = single_identity_2.value
    else:
        single_identity_2_ = single_identity_2
    if hasattr(single_disposition_2, "value"):
        single_disposition_2_ = single_disposition_2.value
    else:
        single_disposition_2_ = single_disposition_2
    if hasattr(single_introduction_2, "value"):
        single_introduction_2_ = single_introduction_2.value
    else:
        single_introduction_2_ = single_introduction_2
    character_setting_rewrite_dict_1 = {
     '姓名': single_name_1_,
     '性别': select_gender_1_,
     '国籍': select_country_1_,
     '身份': single_identity_1_,
     '性格特征': single_disposition_1_,
     '角色介绍': single_introduction_1_,
     }
    character_setting_rewrite_dict_2 = {
     '姓名': single_name_2_,
     '性别': select_gender_2_,
     '国籍': select_country_2_,
     '身份': single_identity_2_,
     '性格特征': single_disposition_2_,
     '角色介绍': single_introduction_2_,
     }

    a, b = main_two_character_prompt_func_cls(
        single_name_1_,
        single_name_2_,
        two_task,
        character_setting_rewrite_dict_1 = character_setting_rewrite_dict_1,
        character_setting_rewrite_dict_2 = character_setting_rewrite_dict_2,
        )
    #a = a.replace("？", "?")
    req = "\n".join([b, a])
    req = process_info(req)
    return req
    #return "\n".join([b, a])

import re
import pandas as pd
def retrieve_sent_split(sent,
                       stops_split_pattern = "|".join(map(lambda x: r"\{}".format(x),
                                                                 ",." + "，。" + ":" + "n"))
                       ):
    if not sent.strip():
        return []

    split_list = re.split(stops_split_pattern, sent)
    split_list = list(filter(lambda x: x.strip() ,split_list))
    return split_list

def stop_criteria(sent, min_sub_len = 4):
    #### chunk rec stop
    split_list = retrieve_sent_split(sent)
    split_list = list(filter(lambda x: len(x) >= min_sub_len,split_list))
    if split_list:
        if pd.Series(split_list).value_counts().max() >= 2:
            print("stop in : {}".format(sent))
            return "stop"
    #### row rec stop
    if list(filter(lambda x: x ,map(lambda x: x.strip(),sent.split("\n")))) and pd.Series(list(filter(lambda x: x ,map(lambda x: x.strip(),sent.split("\n"))))).value_counts().max() >= 2:
        return "stop"
    return "continue"

#model_file_path = "genshin_impact_character_llamazh13b_ggml/llama2zh-13b-3900-q2_k.gguf"
#model_file_path = "genshin_impact_character_llamazh13b_ggml/llama2zh-13b-7500-q2_k.gguf"
#model_file_path = "genshin_impact_character_llamazh13b_ggml/llama2zh-13b-7500-q4_0.gguf"
model_file_path = "genshin_impact_character_llamazh13b_ggml/llama2zh-13b-3900-q4_0.gguf"

from llama_cpp import Llama
llama = Llama(model_file_path,
                  n_ctx = 4090,
                  n_threads=8,            # The number of CPU threads to use, tailor to your system and the resulting performance
                  n_gpu_layers=-1
                  )
print("load {}".format(model_file_path))

def repeat_cmp_process(x, ratio_threshold = 0.3):
    l = x.split("\n")
    l = list(filter(lambda y: y.strip(), l))
    req = []
    for ele in l:
        one_ele = repeat_to_one(ele)
        if ele.strip() and (len(one_ele) / len(ele)) <= ratio_threshold:
            req.append(one_ele)
        else:
            req.append(ele)
    return "\n".join(req)

def text_process_before_yield(x, add_repeat_process = True):
    import re
    x = x.strip()
    if len(x.split("\n")) <= 1:
        #return repeat_to_one_fb(x)
        if add_repeat_process:
            return repeat_cmp_process(x)
        return x
    zh_list = re.findall(u"[\u4e00-\u9fa5]+" ,x)
    if zh_list:
        last_zh = zh_list[-1]
        l = list(map(lambda y: y.strip() ,x.split("\n")))
        l_rev = l[::-1]
        l_rev_collect = []
        find_it = False
        for ele in l_rev:
            if not ele.endswith(last_zh):
                find_it = True
            else:
                pass
            if find_it:
                l_rev_collect.append(ele)
        l_collect = l_rev_collect[::-1]
        #print(l_collect)
        req = "\n".join(l_collect)
        '''
        zh_list = re.findall(u"[\u4e00-\u9fa5]+" ,x)
        if zh_list:
            req = req[req.find(zh_list[0]):]
        '''
        #return repeat_to_one_fb(req)
        if add_repeat_process:
            return repeat_cmp_process(req)
        return req
    return ""

def llama2_zh_predict(message, llama = llama,
    max_output_length = 512, max_message_length = 1024, top_p = 0.8,
    use_system = True, temperature = 0.8
):
    message = message[:max_message_length]
    DEFAULT_SYSTEM_PROMPT = """You are a helpful assistant. 你是一个乐于助人的助手。"""

    TEMPLATE_WITH_SYSTEM_PROMPT = (
        "[INST] <<SYS>>\n"
        "{system_prompt}\n"
        "<</SYS>>\n\n"
        "{instruction} [/INST]"
    )

    TEMPLATE_WITHOUT_SYSTEM_PROMPT = "[INST] {instruction} [/INST]"
    if use_system:
        input_prompt = TEMPLATE_WITH_SYSTEM_PROMPT.format(
            **{
                "system_prompt": DEFAULT_SYSTEM_PROMPT,
                "instruction": message
            }
        )
    else:
        input_prompt = TEMPLATE_WITHOUT_SYSTEM_PROMPT.format(**{"instruction": message})
    #print(input_prompt)
    streamer = llama(input_prompt,max_tokens=max_output_length,
    stream = True, temperature = temperature, top_p = top_p)
    #print(output["choices"][0]["text"])
    partial_message = ""
    for msg in streamer:
        #print(msg)
        message = msg['choices'][0]['text']
        #if 'content' in message:
        partial_message += message
        #print(partial_message)
        if stop_criteria(partial_message) == "stop":
            partial_message = "\n".join(partial_message.split("\n")[:-1])
            break
        yield text_process_before_yield(partial_message)
        if len(partial_message) >= max_output_length:
            break

def process_text(x):
    rp_list = ["[/INST]","/INST]","[/INST","/INST","[/INST>","INST","[/CHARACTER]"]
    for ele in rp_list:
        x = x.replace(ele, " ")
    return x

def run_single(
    single_name, select_gender, select_country, single_identity, single_disposition,
    select_task, Text, single_introduction,
    gen_times, max_length, top_p, temperature):
    prompt = get_single_prompt(
        single_name, select_gender, select_country, single_identity, single_disposition,
        select_task, Text, single_introduction
    )
    req = []
    for i in range(gen_times):
        for ele in llama2_zh_predict(prompt,
            max_output_length = max_length,
            top_p = top_p,
            temperature = temperature
        ):
            pass
        #yield ele
        req.append(ele)
    #req = sorted(set(filter(lambda x: x.strip(), req)), key = lambda y: -1 * len(y))
    if hasattr(Text, "value"):
        Text_ = Text.value
    else:
        Text_ = Text
    if Text_.strip():
        req = sorted(set(filter(lambda x: x.strip(), req)), key = lambda y: -1 * fuzz.ratio(y, Text_))
    else:
        req = sorted(set(filter(lambda x: x.strip(), req)), key = lambda y: -1 * len(y))

    req = "\n\n".join(map(lambda t2: "结果{}:\n{}".format(t2[0], t2[1]), enumerate(req)))
    req = process_text(req)
    #req = process_info(req)
    return req

def run_two(
    single_name_1, select_gender_1, select_country_1, single_identity_1, single_disposition_1,
    single_introduction_1,
    single_name_2, select_gender_2, select_country_2, single_identity_2, single_disposition_2,
    single_introduction_2,
    gen_times, max_length, top_p, temperature):
    two_prompt = partial(get_two_prompt, two_task = "哪些信息")(
        single_name_1, select_gender_1, select_country_1, single_identity_1, single_disposition_1,
        single_introduction_1,
        single_name_2, select_gender_2, select_country_2, single_identity_2, single_disposition_2,
        single_introduction_2
    )
    req = []
    for i in range(gen_times):
        for ele in llama2_zh_predict(two_prompt,
            max_output_length = max_length,
            top_p = top_p,
            temperature = temperature
        ):
            pass
        #yield ele
        req.append(ele)
    req = sorted(set(filter(lambda x: x.strip(), req)), key = lambda y: -1 * len(y))
    req_ = []
    for ele in req:
        zh_list = re.findall(u"[\u4e00-\u9fa5]+" ,ele)
        if len(zh_list) >= 2:
            ele = ele[ele.find(zh_list[1]):]
        req_.append(ele)
    req = req_
    req = "\n\n".join(map(lambda t2: "结果{}:\n{}".format(t2[0], t2[1]), enumerate(req)))
    req = process_text(req)
    #req = process_info(req)
    return req

all_single_task = ["介绍", "故事", "信", "聊天", "时候", "关于", "了解"]
all_two_task = ["会说什么", "哪些信息"]

with gr.Blocks() as demo:
    title = gr.HTML(
            """<h1 align="center"> <font size="+3"> Genshin Impact Character llama2zh Instruction 📊 </font> </h1>""",
            elem_id="title",
    )

    with gr.Tab("单个角色任务指令"):
        with gr.Row():
            with gr.Column(0.5):
                select_name = gr.Gallery(im_list, elem_id="gallery",
                        #scale = 0.1,
                        columns=[3], object_fit="contain",
                        height=512+128,
                        allow_preview = False,
                        label="选择角色",
                        info = "可选择。原神沉玉谷前的内建角色"
                        )
                select_task = gr.Dropdown(label="选择任务",
                        choices=all_single_task,
                        info = "可选择",
                        value=all_single_task[0], interactive = True)
                Text = gr.Text(label = "任务追加信息", interactive = True, lines = 4,
                    info = "可编辑。这些信息除了‘了解’任务外不应该为空。对于不同任务填入的值不同。"
                    "（介绍->前缀 故事->前缀 信->主题 聊天->主题 时候->事件 关于->看法 了解->了解角色自身）"
                )

            with gr.Column(0.5):
                single_name = gr.Text(label = "角色姓名",
                                            info = "可编辑。角色姓名会重写选择角色，用这个选项可以新建角色",
                                            interactive = True)
                #with gr.Row():
                select_gender = gr.Dropdown(label="性别",
                                            choices=all_genders,
                                            info = "可选择",
                                            value=all_genders[0], interactive = True)
                select_country = gr.Dropdown(label="国籍",
                                            choices=all_countries,
                                            info = "可选择",
                                            value=all_countries[0], interactive = True)
                                    #with gr.Column():
                single_identity = gr.Text(label = "身份", info = "可编辑", interactive = True)
                single_disposition = gr.Text(label = "性格特征", info = "可编辑", interactive = True)

                single_introduction = gr.Text(label = "角色介绍", info = "可编辑",
                interactive = True, lines = 15)

        with gr.Row():
            single_prompt_run_button = gr.Button("得到任务结果")
            output = gr.Text(label = "任务生成结果", info = "可编辑", lines = 2, scale = 5.0)

    with gr.Row():
        gen_times = gr.Slider(1, 10, value=10, step=1.0, label="Generate Num", interactive=True)
        max_length = gr.Slider(0, 32768, value=512, step=1.0, label="Maximum length", interactive=True)
        top_p = gr.Slider(0, 1, value=0.8, step=0.01, label="Top P", interactive=True)
        temperature = gr.Slider(0.01, 1, value=0.6, step=0.01, label="Temperature", interactive=True)

    with gr.Row():
        gr.HTML(
            """<h2 align="center"> <font size="+0"> 例子（这里面涉及推荐选择的需要从左面或上面的角色图片集里面点按选取） </font> </h2>""",
            elem_id="title",
    )

    with gr.Row():
        gr.Examples(
            [
            ["这里推荐从左面选择：迭卡拉庇安" ,"信", "阿莫斯"],
            ["这里推荐从左面选择：安德留斯" ,"关于", "狼群"],
            ["这里推荐从左面选择：温妮莎" ,"故事", "一天温妮莎前往骑士团办公。"],
            ["这里推荐从左面选择：特瓦林" ,"信", "龙脊雪山"],
            ["这里推荐从左面选择：法尔伽" ,"关于", "远征的目的"],
            ["这里推荐从左面选择：艾伦德林" ,"故事", "一天艾伦德林和女士开始了一场甜蜜的约会。"],
            ["这里推荐从左面选择：鲁斯坦" ,"聊天", "生个孩子，传承血脉。"],
            ["这里推荐从左面选择：奥兹" ,"关于", "菲谢尔"],
            ["这里推荐从左面选择：炎之魔女" ,"关于", "自己的过去"],
            ["这里推荐从左面选择：克利普斯" ,"信", "凯亚"],
            ["这里推荐从左面选择：归终" ,"故事", "一天魔神归终考察了归离原中前代尘神的古代遗迹。"],
            ["这里推荐从左面选择：赫乌莉亚" ,"了解", ""],
            ["这里推荐从左面选择：奥赛尔" ,"信", "跟岩神钟离的决斗书"],
            ["这里推荐从左面选择：马科修斯" ,"故事", "马科修斯参与了一场新的斗虫比赛。"],
            ["这里推荐从左面选择：若陀龙王" ,"关于", "如何减肥"],
            ["这里推荐从左面选择：浮舍" ,"关于", "岩王帝君"],
            ["这里推荐从左面选择：铜雀" ,"了解", ""],
            ["这里推荐从左面选择：削月筑阳真君" ,"关于", "夜叉弥怒对抗魔神的过程"],
            ["这里推荐从左面选择：理水叠山真君" ,"时候", "睡觉"],
            ["这里推荐从左面选择：留云借风真君" ,"关于", "望舒客栈"],
            ["这里推荐从左面选择：歌尘浪市真君" ,"聊天", "高山流水"],
            ["这里推荐从左面选择：移霄导天真君" ,"时候", "爬璃月高山"],
            ["这里推荐从左面选择：天叔" ,"关于", "退休"],
            ["这里推荐从左面选择：跋掣" ,"信", "亲爱的奥塞尔我怀了你的孩子"],
            ["这里推荐从左面选择：奥罗巴斯" ,"了解", ""],
            ["这里推荐从左面选择：狐斋宫" ,"信", "晨起雪纷纷"],
            ["这里推荐从左面选择：御舆千代" ,"关于", "自己的武艺"],
            ["这里推荐从左面选择：五百藏" ,"时候", "捉迷藏"],
            ],
            inputs = [single_name ,select_task, Text],
            label = "单个角色任务指令例子"
        )

    select_name.select(change_single_name,
        inputs = select_name,
        outputs = [
                    single_name, select_gender, select_country,
                    single_identity, single_disposition, single_introduction
                ],
        )

    single_prompt_run_button.click(run_single, [
        single_name, select_gender, select_country, single_identity, single_disposition,
        select_task, Text, single_introduction,
    gen_times, max_length, top_p, temperature
    ], output)


#demo.launch("0.0.0.0", show_api=False, share = True)
demo.queue(max_size=4, concurrency_count=1).launch(debug=True, show_api=False, share = True)
