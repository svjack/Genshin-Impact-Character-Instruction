<!-- PROJECT LOGO -->
<br />
<p align="center">
  <h3 align="center">Genshin-Impact-Character-Instruction</h3>

  <p align="center">
   		使用Lora在LLM上微调的原神角色指令模型 (由 ChatGLM3-6B-base Chinese-Llama-2-13B 构建)
    <br />
  </p>
</p>

[In English](README_EN.md)


## 简要介绍

### 背景
[Genshin Impact](https://genshin.hoyoverse.com/en/)是miHoYo开发的动作角色扮演游戏，由HoYoverse在大陆中国和全球发布 。该游戏具有动画风格的开放世界环境和基于元素魔法和角色换位的战斗系统。

在游戏中，玩家可以操纵很多个角色来探索壮美的开放世界环境。本工程包含的一些角色如下图所示。

<br/>

<div align="center">
<img src="imgs/characters_shot.png" alt="女孩穿羽衣" width="550" height="6950"> 
</div>

<br/>

本项目是对上述游戏角色做一个在指令数据集上模型微调与展示尝试。

## 安装和运行结果
### 安装和运行步骤
从概念角度，该项目可分为两部分，Basic\_Part和LLM\_Part。 <br/>
* <b>Basic\_Part</b>包含用于文本处理和显示的基本模块，您应该使用如下命令安装这些模块： <br/>
```bash
pip install -r basic_requirements.txt
```
* <b>LLM\_Part</b>是你需要选择安装的模块：[chatglm.cpp](https://github.com/li-plus/chatglm.cpp) [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) <br/> <br/>

下表列出了不同类型的LLM Repo名称、LLM模型名称 及其 Linux安装命令 和 Gradio 示例运行命令
|LLM Repo Name   | LLM Model Name       | Linux安装命令          | Gradio Demo运行命令        |
|---------------|----------------------|-----------------------|---------------------------|
| chatglm.cpp    | THUDM/chatglm3-6b-base | pip install -r basic_requirements.txt && pip install chatglm-cpp==0.3.1 | python chatglm_character_instruction_gradio.py |
| llama-cpp-python | hfl/chinese-llama-2-13b | pip install -r basic_requirements.txt && pip install llama-cpp-python==0.2.55 | python llama2zh_character_instruction_gradio.py |

### 运行结果

https://github.com/svjack/Genshin-Impact-Character-Instruction/assets/27874014/966364b2-bc35-4784-9125-dfdc7d950d7b

https://github.com/svjack/Genshin-Impact-Character-Instruction/assets/27874014/a248b68e-caff-4f4e-8a5b-12e09579a9f3

<br/>

通过视频示例，您可以发现，您可以通过点击下方示例候选项并在Gradio示例中的图片选择框指定角色。
此项目对单个角色可执行七种任务，包括“介绍”、“故事”、“信”、“聊天”、“时间”、“关于”和“了解”。 ChatGLM3-6B-base-lora-tuned可从一个角色的角度提供对另一个角色的观点(chinese-llama-2-13b-lora-tuned则未具有此能力)。 <br/>

Gradio示例接口可以看作与LLM交互的提示编辑器。每个可编辑输入框(具有“可编辑”字样，例如：角色名称、职业、性格特征、角色介绍、任务附加信息)都是可自由更改或编辑的，每个可选择输入框(具有“可选择”字样，例如：性别、国家、选择任务)是可以自由更改或选择的。它们描述了人物的背景和指令任务信息。 <br/>

这种相较而言灵活的提示词设置给予了对于角色和任务更多变化性和操作性，使创造新角色成为可能。下方新角色“大慈树王”是一个示例，您还可向模型请求没有在游戏内容中包含的开放式内容。 <br/>

<br/>

下面是不同模型完成各种任务的结果例子(每个例子生成三个结果，取最好的一个)。角色和任务的第二列指定任务类型，第三列指定任务附加信息，作为任务提示的附加信息。

|    | 角色和任务                                                         | ChatGLM-6B-base-lora-tuned                                                                                                                                           | chinese-llama-2-13b-lora-tuned                                                                                                                                               |
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
|  9 | 大慈树王 关于 教令院                                                 | 雨林的学者们，在过去的岁月里，为了理解我、理解世界，付出了难以想象的艰辛。他们一直守着雨林，守着知识，守着这个世界的智慧，但他们监禁小吉祥草王的行为我不能认同。听说阿扎尔想体会一下监狱的滋味。                                           | 教令院是维持须弥秩序和知识传承的重要力量，我非常信任他们，相信他们会将我留在心中的位置，与我一同守护须弥，直到我再次醒来的那一天，把参与监禁犯罪的学者抓起来，听说带头监禁的那个博士是个医生。                                          |
| 10 | 芙宁娜 那维莱特  角色间看法                                                    | 「那维莱特先生，是一位非常出色的审判官。他有着丰富的经验，睿智的头脑，还有公正的眼光。他是我见过最出色的审判官。」                                                   | ''                                                                                                                                                                           |
| 11 | 提纳里 大慈树王  角色间看法                                                | 「大慈树王」？我听雨林里的居民说过她，他们都说，她很关心我们，很慈爱我们。但是，她已经很久没有露面了。雨林里现在还是有些不安定，我希望她能早日回来，让雨林恢复安宁。 | ''                                                                                                                                                                           |

### 注意
从上方结论中看出，ChatGLM-6B-base-lora-tuned更易于生成多行对话结论，chinese-llama-2-13b-lora-tuned则更易于生成单行高质量结果。 <br/>
当您自己尝试时，如果输出不太好，您可以尝试修改Gradio UI中可编辑的任何部分，值得注意的是缩短角色介绍通常会有利但会损害输出的多样性。 <br/>
我推荐您在GPU上运行demo（10GB GPU内存足够，所有示例已经在GTX 1080Ti和GTX 3060上测试过） <br/><br/>

## 模型
| 类型 | 基础模型             | HuggingFace Lora checkpoint 链接              | HuggingFace合并ggml或gguf链接            |
|-------|---------------------|------------------------------------------|------------------------------------------|
| ChatGLM-6B-base-lora-tuned | THUDM/chatglm3-6b-base | https://huggingface.co/svjack/genshin_impact_character_glm6b_base_lora | https://huggingface.co/svjack/genshin_impact_character_glm6b_base_ggml |
| chinese-llama-2-13b-lora-tuned | hfl/chinese-llama-2-13b | https://huggingface.co/svjack/genshin_impact_character_llamazh13b_lora | https://huggingface.co/svjack/genshin_impact_character_llamazh13b_ggml |

### 注意
每个上方HuggingFace合并ggml或gguf仓库中都包含两个合并的4bit量化模型，它们是本项目所使用的模型，由我在7000条标注数据集上训练。 <br/>
如果您想尝试在其他lora checkpoint中的结果，您可以使用HuggingFace Lora checkpoint链接中的文件，并自行合并， <br/>您可以参考[chatglm.cpp](https://github.com/li-plus/chatglm.cpp)和[llama-cpp-python](https://github.com/abetlen/llama-cpp-python)了解如何合并它们。

<br/>

## 进一步阅读
我还发布了一项关于基于量化大模型的原神书目问答工程 (由 LangChain Haystack ChatGLM Mistral OLlama 构造)。 <br/>
如果您对它感兴趣，请查看[svjack/Genshin-Impact-BookQA-LLM](https://github.com/svjack/Genshin-Impact-BookQA-LLM) 😊


<br/>

<!-- CONTACT -->
## Contact

<!--
Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com
-->
svjack - https://huggingface.co/svjack - svjackbt@gmail.com - ehangzhou@outlook.com

<!--
Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)
-->
Project Link:[https://github.com/svjack/Genshin-Impact-Character-Instruction](https://github.com/svjack/Genshin-Impact-Character-Instruction)


<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [Genshin Impact](https://genshin.hoyoverse.com/en/)
* [Huggingface](https://huggingface.co)
* [chatglm.cpp](https://github.com/li-plus/chatglm.cpp)
* [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
* [svjack/Genshin-Impact-BookQA-LLM](https://github.com/svjack/Genshin-Impact-BookQA-LLM)
* [svjack](https://huggingface.co/svjack)

