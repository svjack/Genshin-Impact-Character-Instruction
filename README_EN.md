<!-- PROJECT LOGO -->
<br />
<p align="center">
  <h3 align="center">Genshin-Impact-Character-Instruction</h3>

  <p align="center">
   		Genshin Impact Character Instruction Models tuned by Lora on LLM (build by ChatGLM3-6B-base Chinese-Llama-2-13B)
    <br />
  </p>
</p>

[中文介绍](README.md)

## Brief introduction

### BackGround
[Genshin Impact](https://genshin.hoyoverse.com/en/) is an action role-playing game developed by miHoYo, published by miHoYo in mainland China and worldwide by Cognosphere, 
HoYoverse. The game features an anime-style open-world environment and an action-based battle system using elemental magic and character-switching. 

In the Game, one can play many Characters to explore the amazing open-world environment. Some characters can be seen in below gallery.

<br/>

<div align="center">
<img src="imgs/characters_shot.png" alt="Girl in a jacket" width="550" height="6950"> 
</div>

<br/>

This project is an attempt to give Instruction Model demo for characters above.

## Installation and Running Results
### Install and Running Step
In the concept, the project can be divided into two parts, Basic_Part and LLM_Part. <br/>
* <b>Basic_Part</b> contains modules for text processing and display, you should install all of them By <br/>
```bash
pip install -r basic_requirements.txt
```
* <b>LLM_Part</b> are modules that you should choose one to install: [chatglm.cpp](https://github.com/li-plus/chatglm.cpp) [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) <br/> <br/>

Below are different LLM Repo types with their install and running command
|LLM Repo Name | LLM Model Name | Install Command in Linux | Run Gradio Demo Command |
|---------|--------|--------|--------|
| chatglm.cpp | THUDM/chatglm3-6b-base | pip install -r basic_requirements.txt && pip install chatglm-cpp==0.3.1 | python chatglm_character_instruction_gradio.py |
| llama-cpp-python | hfl/chinese-llama-2-13b | pip install -r basic_requirements.txt && pip install llama-cpp-python==0.2.55 | python llama2zh_character_instruction_gradio.py |


### Running Results

https://github.com/svjack/Genshin-Impact-Character-Instruction/assets/27874014/966364b2-bc35-4784-9125-dfdc7d950d7b

https://github.com/svjack/Genshin-Impact-Character-Instruction/assets/27874014/a248b68e-caff-4f4e-8a5b-12e09579a9f3

<br/>

As video example, you can click below example candidates and select character from the image gallery in gradio demo.
There are 7 different tasks include "介绍", "故事", "信", "聊天", "时候", "关于", "了解" this project can do for single character, and for two characters ChatGLM3-6B-base-lora-tuned 
can provide one character's perspective on another character's perspective. (chinese-llama-2-13b-lora-tuned not 
cover this part of the ability) <br/>

The gradio interface is the prompt editor for llm, Each editable input box (have "可编辑" fonts, ex: 角色姓名 身份 性格特征 角色介绍 任务追加信息) are free to change or edit,
each optional input box (have "可选择" fonts, ex: 性别 国籍 选择任务) are free to change or select. They describe the background of characters and the info of instruction tasks. <br/>

This relatively flexible prompt word setting gives more variability and controllability to characters and tasks, and makes it possible to create new characters. Belowing the new character "大慈树王" is the example for new character. And you can ask the model for open-ended content that is not included in the game itself. 

<br/>

Following are results of some tasks in different models. (take the favor one from 3 generations)

|    | Characters and Tasks                                                           | ChatGLM-6B-base-lora-tuned                                                                                                                                           | chinese-llama-2-13b-lora-tuned                                                                                                                                               |
|---:|:---------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|  1 | 行秋 介绍                                                            | 身为商人的他，却有着行侠仗义的侠客心肠。他时常与申鹤、重云一起，在璃月城内外奔走，保护璃月城的百姓。                                                                 | 他与兄长一同经营着家业，并且对家业中的事务了如指掌，对商业的敏锐度也十分高，在谈判中总是能占到优势，让对方无法招架。                                                         |
|    |                                                                      | 虽然他年纪尚轻，却有着远大的志向。他希望能够让飞云商会成为璃月最富有的商会，让璃月城的百姓们都能过上富足的生活。                                                     | 但作为「琉银」这柄名剑的继承者，他的内心里却一直渴望着，可以成为真正的大侠，斩草除根，维护正义，保护弱小，惩恶扬善。                                                         |
|    |                                                                      |                                                                                                                                                                      | 虽然他的家世显赫，但他却不愿享受优待，时常与兄长一同下乡，或到别处游玩，或与好友们切磋剑术，磨砺自己的身手。                                                                 |
|  2 | 行秋 故事 一天行秋在绝云间练剑。                                     | 行秋：「你今天练得怎么样？」                                                                                                                                         | 「唔，好痛…」他自言自语着，将剑放好，揉了揉酸痛的胳膊，又看了看手上的伤口，「果然是血洗剑…」                                                                                 |
|    |                                                                      | 重云：「还行。」                                                                                                                                                     |                                                                                                                                                                              |
|    |                                                                      | 行秋：「那今天我们就去飞云商会看看吧。」                                                                                                                             |                                                                                                                                                                              |
|    |                                                                      | 重云：「为什么？」                                                                                                                                                   |                                                                                                                                                                              |
|    |                                                                      | 行秋：「我今天看到一本书，上面说，读书能增加见识，提高智力。所以我想，你一定也看不懂那些书吧。」                                                                     |                                                                                                                                                                              |
|    |                                                                      | 重云：「那又怎样？」                                                                                                                                                 |                                                                                                                                                                              |
|    |                                                                      | 行秋：「所以，你今天陪我去飞云商会吧，我教你读书，你帮我做事。」                                                                                                     |                                                                                                                                                                              |
|    |                                                                      | 重云：「我为什么要帮你做事？」                                                                                                                                       |                                                                                                                                                                              |
|    |                                                                      | 行秋：「因为你是我的朋友啊。」                                                                                                                                       |                                                                                                                                                                              |
|    |                                                                      | 重云：「那好吧。」                                                                                                                                                   |                                                                                                                                                                              |
|  3 | 柯莱 信 鸟语花香                                                     | 春回大地，万物复苏，百花齐放，百鸟争鸣。                                                                                                                             | 今天天气不错，鸟儿们的叫声格外欢快，好像在庆祝什么一样，我也跟着哼起了歌，连我带树洞里的小猫都跟着哼起了歌，嘻嘻，真是热闹呀！                                               |
|    |                                                                      | 春天，是万物生长的季节，也是希望萌生的季节。                                                                                                                         |                                                                                                                                                                              |
|    |                                                                      | 在春天，你总能看到各种不同颜色的小花，听到各种不同音调的鸟鸣。                                                                                                       |                                                                                                                                                                              |
|    |                                                                      | 你，有没有发现它们都在向你传递着什么讯息呢？                                                                                                                         |                                                                                                                                                                              |
|    |                                                                      | 嗯，春天就是这样的，希望无处不在。                                                                                                                                   |                                                                                                                                                                              |
|    |                                                                      | 「春天在哪里？」                                                                                                                                                     |                                                                                                                                                                              |
|    |                                                                      | 「春天就在你的心里。」                                                                                                                                               |                                                                                                                                                                              |
|  4 | 魈 聊天 美味的杏仁豆腐                                               | 杏仁豆腐，细腻温润。                                                                                                                                                 | 杏仁豆腐？嗯…唔…这道菜的材料很讲究，只有天上人间才有的杏仁和甘露草才能做出来…嗯？你说你家也有做？那我也去尝尝看吧！                                                          |
|  5 | 凝光 时候 品尝璃月香茗                                               | 香茗虽好，但太淡了些。                                                                                                                                               | 香茗之中蕴含着茶农的智慧与心血，我与他们同为商人，因此也能够理解他们心意的精髓。                                                                                             |
|  6 | 可莉 关于 如何制造蹦蹦炸弹                                           | 嗯，要加一点炸药，再加一点火药，再加一点…哦，好像不够！                                                                                                              | 「蹦蹦炸弹」的制作方法很简单，只要把「蹦蹦」放在炸弹里就行了！                                                                                                               |
|  7 | 芙宁娜 了解                                                          | 就该先了解她的过去。                                                                                                                                                 | 哦？你问我？那可好，我可是个百分之百的坦率之人呢！只不过…嗯？我…我怎么会在你面前哭？那是…我的泪珠被风吹落在了你的脚边…呃…                                                    |
|    |                                                                      | 在芙宁娜成为枫丹水神之前，她的人生并不顺遂。                                                                                                                         |                                                                                                                                                                              |
|    |                                                                      | 在神明的世界中，芙宁娜是个「意外」。                                                                                                                                 |                                                                                                                                                                              |
|    |                                                                      | 她诞生的时间，并不在枫丹的「黄金时代」。                                                                                                                             |                                                                                                                                                                              |
|    |                                                                      | 她的母亲是位高贵的女祭司，在芙宁娜出生之前，她已经和神明订下了契约。                                                                                                 |                                                                                                                                                                              |
|    |                                                                      | 在芙宁娜出生的那一天，她的母亲就过世了。                                                                                                                             |                                                                                                                                                                              |
|    |                                                                      | 她的父亲，一位水神神官，因为无法承受丧妻之痛，将芙宁娜视作母亲的转世，甚至希望她也能像母亲一样成为水神祭司。                                                         |                                                                                                                                                                              |
|    |                                                                      | 芙宁娜在父亲的教导下，努力地学习着各种知识。                                                                                                                         |                                                                                                                                                                              |
|    |                                                                      | 然而，她并不认同父亲「水神祭司」的身份。                                                                                                                             |                                                                                                                                                                              |
|    |                                                                      | 她渴望着能像母亲那样，成为一名伟大的歌者。                                                                                                                           |                                                                                                                                                                              |
|    |                                                                      | 在芙宁娜十六岁那年，她终于获得了「歌者」的称号，并顺利成为枫丹的首席歌者。                                                                                           |                                                                                                                                                                              |
|    |                                                                      | 她曾以为自己终于找到了「母亲的转世」这个身份之外的「新的身份」。                                                                                                     |                                                                                                                                                                              |
|    |                                                                      | 然而，她很快发现，在枫丹的民众心中，这个身份似乎比「歌者」更加重要。                                                                                                 |                                                                                                                                                                              |
|    |                                                                      | 在芙宁娜看来，这是不公的。                                                                                                                                           |                                                                                                                                                                              |
|    |                                                                      | 她认为，无论以什么身份出现，她都应当被尊重。                                                                                                                         |                                                                                                                                                                              |
|    |                                                                      | 然而，民众却似乎并不在意她的「歌者」身份。                                                                                                                           |                                                                                                                                                                              |
|    |                                                                      | 「水神祭司」的身份才是他们最为看重。                                                                                                                                 |                                                                                                                                                                              |
|    |                                                                      | 他们甚至认为芙宁娜的母亲是水神祭司的转世。                                                                                                                           |                                                                                                                                                                              |
|    |                                                                      | 这令芙宁娜非常痛苦。                                                                                                                                                 |                                                                                                                                                                              |
|    |                                                                      | 她觉得自己被父亲背叛了。                                                                                                                                             |                                                                                                                                                                              |
|    |                                                                      | 她认为自己被民众背叛了。                                                                                                                                             |                                                                                                                                                                              |
|    |                                                                      | 她认为这个世界背叛了她。                                                                                                                                             |                                                                                                                                                                              |
|  8 | 大慈树王 故事 大慈树王到须弥沙漠上播种，并跟沙漠的统治者赤王交朋友。 | 大慈树王和赤王一起，创造出了须弥。大慈树王用智慧的力量，创造了雨林和须弥的生物，并且为它们创造了生命。赤王则是创造了沙漠。                                           | 在沙漠里，大慈树王遇到了赤王，赤王用自己特有的方式，表达了对大慈树王的敬意：「我的身体，是沙漠之神赐予我的，但你那颗强大的心，却是造物之神送给你的，所以，我敬你，我敬你！」 |
|    |                                                                      | 大慈树王和赤王是好朋友。赤王曾经想要毁灭世界，大慈树王为了拯救世界，用生命换取了世界树的永恒。                                                                       |                                                                                                                                                                              |
|  9 | 大慈树王 关于 教令院                                                 | 雨林的学者们，在过去的岁月里，为了理解我、理解世界，付出了难以想象的艰辛。他们一直守着雨林，守着知识，守着这个世界的智慧。但他们监禁小吉祥草王的行为我不能认同。                                           | 教令院是维持须弥秩序和知识传承的重要力量，我非常信任他们，相信他们会将我留在心中的位置，与我一同守护须弥，直到我再次醒来的那一天，把参与监禁犯罪的学者抓起来，听说带头监禁的那个博士是个医生。                                          |
| 10 | 芙宁娜 那维莱特  角色间看法                                                    | 「那维莱特先生，是一位非常出色的审判官。他有着丰富的经验，睿智的头脑，还有公正的眼光。他是我见过最出色的审判官。」                                                   | ''                                                                                                                                                                           |
| 11 | 提纳里 大慈树王  角色间看法                                                | 「大慈树王」？我听雨林里的居民说过她，他们都说，她很关心我们，很慈爱我们。但是，她已经很久没有露面了。雨林里现在还是有些不安定，我希望她能早日回来，让雨林恢复安宁。 | ''                                                                                                                                                                           |


### Note
From above conclusion, ChatGLM-6B-base-lora-tuned makes it easier to generate multi-line and dialogue conclusions, chinese-llama-2-13b-lora-tuned Easily generates single-line high-quality results. <br/>

I recommand you run the demo on GPU (10GB gpu memory is enough, all examples have been tested on GTX 1080Ti and GTX 3060) <br/><br/>

## Models
| Type | Base Model | HuggingFace Lora checkpoints link | Huggingface merged ggml or gguf link |
|---------|--------|--------|
| ChatGLM-6B-base-lora-tuned | THUDM/chatglm3-6b-base | https://huggingface.co/svjack/genshin_impact_character_glm6b_base_lora | https://huggingface.co/svjack/genshin_impact_character_glm6b_base_ggml |
| chinese-llama-2-13b-lora-tuned | hfl/chinese-llama-2-13b | https://huggingface.co/svjack/genshin_impact_character_llamazh13b_lora | https://huggingface.co/svjack/genshin_impact_character_llamazh13b_ggml |

