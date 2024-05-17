# Imusic接口文档

[TOC]

## Vue3项目创建流程


1. 需要安装node.js
1. 打开一个终端，执行npm init vue@latest，会下载官方的脚手架
1. 按照步骤创建项目，前端项目需要用到router和pinia
1. 进入项目文件夹，执行npm i安装所需依赖
1. 依赖安装好后执行npm run dev即可启动项目
### 关于UI框架的安装

这儿以tailwind css为例，参考下面的文档，略去第一步

[Install Tailwind CSS with Vite - TailwindCSS中文文档 | TailwindCSS中文网](https://www.tailwindcss.cn/docs/guides/vite#vue)
## Django项目创建流程


1. 先安装python虚拟环境，推荐用conda创建
1. 执行`python -m pip install Django`
1. 安装成功后执行`python -m django --version`查看是否安装成功
1. 创建应用`django-admin startproject <mysite>`
1. 启动项目`python manage.py runserver`
1. 创建应用`python manage.py startapp <myapp>`

------

|大部分接口已加上token校验，前端同学注意修改请求代码！绿色字体的接口没有token校验|
| :- |
## 用户表接口
### 用户注册
- **请求类型：** POST
- **URL：** `/users/register`
- **请求参数：**
  - 用户名 (username) 必填
  - 密码 (password) 必填
  - 电子邮箱 (email) 必填
  - 验证码(verification\_code) 必填
  - 简介 (bio)：用户的简介或描述 可选
  - 头像 (avatar)：用户头像[文件] 可选
- **返回结果：**
  - 是否成功 (success)：表示注册是否成功
  - 消息 (message)：注册过程的结果消息
- 返回示例：

  ```json
  {
  	"success": true,
  	"message": "注册成功"
  }
  ```

### 发送验证码
为了更贴近真实情况，我们引入了邮箱验证码的功能

- **请求类型：** POST
- **URL：**`/users/send-code`
- **请求参数：**

  - 电子邮箱 (email) 必填且有效
- **返回结果：**
  - 是否成功 (success)：表示注册是否成功
  - 消息 (message)：注册过程的结果消息
- 返回示例：

  ```json
  {
  	"success": true, 
  	"message": "验证码发送成功" 
  }
  ```
### 用户登录
- **请求类型：** POST
- **URL：** `/users/login`
- **请求参数：**
  - 用户名 (username) 必填
  - 密码 (password) 必填
- **返回结果：**
  - 是否成功 (success)：表示登录是否成功
  - 消息 (message)：登录过程的结果消息
  - 用户信息 (user)：包括用户ID (user\_id)、用户名 (username)、角色 (role) 等
- 返回示例：

### 获取用户信息
- **请求类型：** GET
- **URL：** `/users/info/{username}`
- **请求参数：**
  - 用户名 (username) 必填
- **返回结果：**
  - 用户ID (user\_id)
  - 用户名 (username)
  - 电子邮箱 (email)
  - 注册时间 (registration\_date)
  - 简介 (bio)：用户的简介或描述
  - 头像 (avatar)：用户头像的URL
- 返回示例：
- 目前只有管理员和用户自己能查看详细信息

### 更新用户信息
- **请求类型：** POST
- **URL：** `/users/update/{username}`
- **请求参数：**
  - 用户名 (username) 必填
  - 更新后的用户信息 (Updateduser)：包括电子邮箱 (email)、简介 (bio)、头像 (avatar) 选填
  - 用户名、密码、注册时间暂不支持修改
- **返回结果：**
  - 是否成功 (success)：表示更新是否成功
  - 消息 (message)：更新过程的结果消息
- 返回示例：
- 目前只有管理员和用户自己能更改用户信息

  ```json
  {
  	"success": true,
  	"message": "用户信息修改成功"
  }
  ```

### 更改用户权限
- **请求类型：** POST
- **URL：** `users/change-role`
- **请求参数：**
  - 要修改权限的用户(dir\_user) 必填
  - 要修改成的角色(role) 必填
  - 授权密钥(key) 可选
- 注意有两种修改方式，一种是由管理员修改，要求当前身份需是管理员，这时不用传密钥；另一种时通过授权密钥修改，这时需要传密钥，不强制要求用户身份，密钥每天会更新，目前的密钥是f40bae40764f76b1e4d7a7c5006962dc

|2024/4/22|4d93be54deb544971ba3dfe37f083005|
| :- | :- |
|2024/4/23|64a148d91b4710ffe55e2a4756ed18d5|

- **返回结果：**
  - 是否成功 (success)：表示更新是否成功
  - 消息 (message)：更新过程的结果消息
- 返回示例：

  ```json
  {
  	"success": true,
  	"message": "用户权限修改成功"
  }
  ```

### 修改密码
- **请求类型：** POST
- **URL：** `/users/change-pwd`
- **请求参数：**
  - 修改后的密码(new\_password) 必填
  - 用户名(username) 必填
  - 验证码(verification\_code) 必填
- **返回结果：**
  - 是否成功 (success)：表示修改是否成功
  - 消息 (message)：修改过程的结果消息
- 返回示例：
- 用户只能修改自己的密码

  ```json
  {
  	"success": true,
  	"message": "密码修改成功"
  }
  ```

### 获取用户创建的所有歌单
- **请求类型：** GET
- **URL：** `/users/songlists`
- **请求参数：**

  - 用户姓名 (username) 必填
- 返回结果：
  - 是否成功 (success)：表示获取是否成功
  - 返回用户创建的所有歌单
- 返回示例

  ```json
  {
      "success": true,
      "message": "获取用户歌单成功",
      "data": [
          {
              "id": 4,
              "title": "xht的歌单",
              "cover": "http://182.92.100.66:5000/media/covers/47482bcb3a294e868546d6c73f1e7ca8.jpg",
              "introduction": null,
              "songs": [
                  {
                      "id": 6,
                      "title": "大眠",
                      "singer": "王心凌",
                      "cover": "http://182.92.100.66:5000/media/covers/%E5%A4%A7%E7%9C%A0.webp",
                      "gradient": "background: rgb(38, 27, 31);background: linear-gradient(135deg, rgb(237, 183, 187), rgb(38, 27, 31));",
                      "introduction": null,
                      "audio": "http://182.92.100.66:5000/media/audios/%E5%A4%A7%E7%9C%A0.mp3",
                      "duration": "239.595102",
                      "lyric": "http://182.92.100.66:5000/media/lyrics/%E5%A4%A7%E7%9C%A0.lrc",
                      "tag_theme": null,
                      "tag_scene": null,
                      "tag_mood": null,
                      "tag_style": null,
                      "tag_language": null,
                      "uploader": "xht",
                      "like": 0,
                      "upload_date": "2024-04-22 18:19:49"
                  }
              ],
              "tag_theme": null,
              "tag_scene": null,
              "tag_mood": null,
              "tag_style": null,
              "tag_language": null,
              "owner": "xht",
              "create_date": "2024-04-22 19:58:03",
              "like": 0
          },
          {
              "id": 9,
              "title": "drr",
              "cover": "http://182.92.100.66:5000/media/covers/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_2024-04-15_200250.png",
              "introduction": null,
              "songs": [],
              "tag_theme": null,
              "tag_scene": null,
              "tag_mood": null,
              "tag_style": null,
              "tag_language": null,
              "owner": "xht",
              "create_date": "2024-04-23 11:16:11",
              "like": 0
          },
          {
              "id": 14,
              "title": "歌单",
              "cover": "http://182.92.100.66:5000/media/covers/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_2024-02-19_170811.png",
              "introduction": "测试用的歌单",
              "songs": [],
              "tag_theme": "默认",
              "tag_scene": "咖啡馆",
              "tag_mood": "安静",
              "tag_style": "轻音乐",
              "tag_language": "国语",
              "owner": "xht",
              "create_date": "2024-04-26 21:47:47",
              "like": 0
          }
      ]
  }
  ```

### 获取用户上传的所有歌曲
- **请求类型：** GET
- **URL：** `/users/songs`
- **请求参数：**

  - 用户姓名 (username) 必填
- 返回结果：
  - 是否成功 (success)：表示获取是否成功
  - data:返回用户上传的所有歌曲
- 返回示例

  ```json
  {
      "success": true,
      "message": "获取用户歌曲成功",
      "data": [
          {
              "id": 8,
              "title": "betty",
              "singer": "Taylor Swift",
              "cover": "http://127.0.0.1:8000/media/covers/betty_cover.jpg",
              "gradient": "background: rgb(160, 160, 160);background: linear-gradient(135deg, rgb(174, 174, 174), rgb(68, 68, 68));",
              "introduction": "《贝蒂》（英语：\"Betty\"，风格化为全小写）是美国创作歌手泰勒·斯威夫特的一首歌曲，于2020年8月17日由联众唱片发行，作为她第八张录音室专辑《民间故事》的第三支单曲。这首歌由斯威夫特及乔·阿尔文（笔名威廉·鲍里）共同创作，由斯威夫特、杰克·安东诺夫及亚伦·戴斯纳共同制作[1]。《贝蒂》是一首乡村及民谣摇滚的歌曲，并有着由吉他及口琴交织而成的乐器。歌词方面，它叙述了詹姆斯的道歉，詹姆斯是《民间故事》中的三角恋核心人物之一。这首歌于发行首周在公告牌的《公告牌》百强单曲榜及热门乡村歌曲榜分别获得第42名及第6名，也成为斯威夫特在热门乡村歌曲榜的第22首前10名歌曲。",
              "audio": "http://127.0.0.1:8000/media/audios/betty_audio.mp3",
              "duration": "294.556734",
              "lyric": "http://127.0.0.1:8000/media/lyrics/betty_lyric.lrc",
              "tag_theme": null,
              "tag_scene": "旅行",
              "tag_mood": "宣泄",
              "tag_style": "流行",
              "tag_language": "英语",
              "uploader": "sivenlu",
              "like": 1,
              "upload_date": "2024-04-22 19:19:08",
              "user_like": false,
              "user_favor": false
          },
          ...
      ]
  }
  ```

### 获取用户关注列表(我关注了谁)
- **请求类型：** GET
- **URL：** `/users/followings`
- **请求参数：**

  - 被查看关注列表的用户名（username）必填
- 返回结果：
  - 是否成功(success)
  - 返回信息(message)
  - 数据(data)
- 返回示例：

  ```json
  示例url为：users/followings?username=sivenlu
  {
    "success": true,
    "message": "获取成功",
    "data": [
      {
        "user_id": 9,
        "username": "yy",
        "email": "21241072@buaa.edu.cn",
        "bio": "你好，我是yy123456",
        "avatar": "http://127.0.0.1:8000/media/avatars/avatar.jpg",
        "role": "admin",
        "registration_date": "2024-04-21 15:20:36"
      },
      {
        "user_id": 2,
        "username": "xht",
        "email": "13069167198@163.com",
        "bio": "你好",
        "avatar": "http://127.0.0.1:8000/media/avatars/c53c811f880411ebb6edd017c2d2eca2.jpg",
        "role": "admin",
        "registration_date": "2024-04-20 14:30:30"
      }
    ]
  }
  ```

### 获取用户关注者列表(谁关注了我)
- **请求类型：** GET
- **URL：** `/users/followers`
- **请求参数：**

  - 被查看关注者列表的用户名（username）必填
- 返回结果：
  - 是否成功(success)
  - 返回信息(message)
  - 数据(data)
- 返回示例：

  ```json
  示例url为：users/followers?username=yy
  {
      "success": true,
      "message": "获取成功",
      "data": [
          {
              "user_id": 16,
              "username": "sivenlu",
              "email": "",
              "bio": "test",
              "avatar": "http://127.0.0.1:8000/media/avatars/IMG_20240114_1825591-01.jpeg",
              "role": "user",
              "registration_date": "2024-04-22 19:04:47"
          }
      ]
  }
  ```

### 两个测试接口
#### 查看所有用户信息
```json
http://182.92.100.66:5000/users/alldata
```

```json
{
    "success": true,
    "message": "获取所有用户信息成功",
    "data": [
        {
            "user_id": 2,
            "username": "xht",
            "email": "13069167198@163.com",
            "bio": null,
            "avatar": null,
            "role": "user",
            "registration_date": "2024-04-20 14:30:30"
        },
        {
            "user_id": 8,
            "username": "yy9",
            "email": "1311095683@qq.com",
            "bio": "我是一个特立独行的人",
            "avatar": "http://182.92.100.66:5000/media/avatars/%E5%96%9C%E5%B8%96%E8%A1%97.webp",
            "role": "admin",
            "registration_date": "2024-04-20 16:04:48"
        },
        {
            "user_id": 9,
            "username": "yy",
            "email": "1311095683@qq.com",
            "bio": "你好，我是yy",
            "avatar": "http://182.92.100.66:5000/media/avatars/avatar.jpg",
            "role": "admin",
            "registration_date": "2024-04-21 15:20:36"
        },
        {
            "user_id": 10,
            "username": "xiaorenwu",
            "email": "13069167198@163.com",
            "bio": null,
            "avatar": null,
            "role": "user",
            "registration_date": "2024-04-22 12:03:38"
        },
        {
            "user_id": 11,
            "username": "Nzh",
            "email": "2810988992@qq.com",
            "bio": null,
            "avatar": null,
            "role": "user",
            "registration_date": "2024-04-22 14:15:25"
        },
        {
            "user_id": 12,
            "username": "xiaorenwu234",
            "email": "13069167198@163.com",
            "bio": null,
            "avatar": null,
            "role": "user",
            "registration_date": "2024-04-22 15:24:03"
        },
        {
            "user_id": 13,
            "username": "xht1",
            "email": "13069167198@163.com",
            "bio": null,
            "avatar": null,
            "role": "user",
            "registration_date": "2024-04-22 15:25:14"
        },
        {
            "user_id": 14,
            "username": "yees1012",
            "email": "yeestiew@qq.com",
            "bio": null,
            "avatar": null,
            "role": "user",
            "registration_date": "2024-04-22 17:36:41"
        },
        {
            "user_id": 15,
            "username": "Nzh2",
            "email": "2810988992@qq.com",
            "bio": null,
            "avatar": null,
            "role": "user",
            "registration_date": "2024-04-22 17:41:06"
        }
    ]
}
```

#### 删除用户
***注意是delete请求，只有用户自己能注销***

```json
182.92.100.66:5000/users/delete/<username>
```

## 歌曲表接口
### 上传歌曲
- **请求类型：** POST
- **URL：** `/songs/upload`
- **请求参数：**
  - 标题 (title) 必填
  - 演唱者(singer) 必填
  - 封面图(cover) 必填
  - 介绍(introduction)
  - 音频文件(audio) 必填
  - 歌词文件(lyric, 可选)
  - 标签（可为空）
    - 主题标签(tag\_theme)
    - 场景标签(tag\_scene)
    - 心情标签(tag\_mood)
    - 风格标签(tag\_style)
    - 语言标签(tag\_language)
  - 上传者(uploader, 是username) 必填
  - 喜欢人数(like) 默认为0
- **返回结果：**
  - 歌曲上传成功
  - 错误信息 (message)
    - 缺少字段：一些不可为空的字段没有传值
    - 缺少文件：一些必须上传的文件没有上传
    - 上传重复歌曲：当且仅当数据库中已经存在歌名相同&&歌手相同&&上传者相同
    - 上传了非MP3格式文件。音频格式必须是MP3
    - 文件大小超过限制：上传的音频文件大于25MB**或者**歌词文件大于10MB
  - 其他异常信息
    - 上传者不存在
    - try-catch 捕获到的 Exception

- 返回示例

  ```json
  {
      "success": true,
      "message": "歌曲上传成功"
  }
  ```
### 获取歌曲信息
- **请求类型：** GET
- **URL：** `/songs/info/{songID}`
- **请求参数：**
  - 歌曲ID (SongID) 必填
  - 用户名(username) 选填 如果有则会查询对应用户是否喜欢该歌曲
- **返回结果：**

  - 数据库中的一项（即一个song object）, 数据类型是字典,可以通过key-value的方法进一步获取信息
- 返回示例：

  ```json
  http://182.92.100.66:5000/songs/info/6?username=yy
  ```
  
  ```json
  {
      "success": true,
      "message": "获取歌曲信息成功",
      "data": {
          "id": 6,
          "title": "大眠",
          "singer": "王心凌",
          "cover": "http://182.92.100.66:5000/media/covers/%E5%A4%A7%E7%9C%A0.webp",
          "gradient": "background: rgb(38, 27, 31);background: linear-gradient(135deg, rgb(237, 183, 187), rgb(38, 27, 31));",
          "introduction": "null",
          "audio": "http://182.92.100.66:5000/media/audios/%E5%A4%A7%E7%9C%A0.mp3",
          "duration": "239.595102",
          "lyric": "http://182.92.100.66:5000/media/lyrics/%E5%A4%A7%E7%9C%A0.lrc",
          "tag_theme": null,
          "tag_scene": null,
          "tag_mood": null,
          "tag_style": null,
          "tag_language": null,
          "uploader": "xht",
          "like": 1,
          "upload_date": "2024-04-22 18:19:49",
          "user_like": true
      }
  }
  ```
  
  找不到歌曲的情况
  
  ```json
  {
      "success": false,
      "message": "Song matching query does not exist."
  }
  ```

### 获取歌曲信息（条件查询）
- **请求类型：** GET
- **URL：** `/songs/query?key1=value1&key2=value2`
- **返回结果：**
  - 字典组成的列表，可以理解为歌曲的集合
  - 注意是模糊查询
- 返回信息：
  - 搜索成功
  - 缺少搜索关键字：没有提供任何搜索信息
  - try-catch捕获到的Exception
- 请求示例：

  ```json
  http://182.92.100.66:5000/songs/query?singer=朴树
  ```

  ```json
  {
      "success": true,
      "message": "搜索成功",
      "data": [
          {
              "id": 19,
              "title": "平凡之路(live)",
              "singer": "朴树",
              "cover": "http://182.92.100.66:5000/media/covers/%E5%B9%B3%E5%87%A1%E4%B9%8B%E8%B7%AF.webp",
              "gradient": null,
              "introduction": "《平凡之路》是中国歌手朴树演唱的一首歌曲，最初是电影《后会无期》的主题曲。这首歌以简洁而深刻的歌词，表达了人们在追求梦想的道路上所经历的坎坷和挣扎，以及对于生活的思考和感悟。它深受听众喜爱，成为了中国流行音乐的经典之作。",
              "audio": "http://182.92.100.66:5000/media/audios/%E5%B9%B3%E5%87%A1%E4%B9%8B%E8%B7%AF_Live-%E6%9C%B4%E6%A0%91.128.mp3",
              "duration": "304.718367",
              "lyric": "http://182.92.100.66:5000/media/lyrics/%E5%B9%B3%E5%87%A1%E4%B9%8B%E8%B7%AF_Live_-_%E6%9C%B4%E6%A0%91.lrc",
              "tag_theme": null,
              "tag_scene": null,
              "tag_mood": null,
              "tag_style": null,
              "tag_language": null,
              "uploader": "yy",
              "like": 0,
              "upload_date": "2024-04-22 19:49:41"
          }
      ]
  }
  ```

  ```json
  http://182.92.100.66:5000/songs/query?title=你好
  ```

  ```json
  {
      "success": true,
      "message": "搜索成功",
      "data": [
          {
              "id": 20,
              "title": "明天，你好",
              "singer": "牛奶咖啡",
              "cover": "http://182.92.100.66:5000/media/covers/%E6%98%8E%E5%A4%A9%E4%BD%A0%E5%A5%BD.webp",
              "gradient": null,
              "introduction": "《明天，你好》是中国乐团牛奶咖啡演唱的一首歌曲，也是他们的代表作之一。这首歌以轻快、欢快的旋律和朗朗上口的歌词，传递了乐观、积极的生活态度。歌曲鼓励人们在面对困难时保持乐观，相信未来会更美好。牛奶咖啡通过这首歌曲，向听众传递了正能量和希望，受到了广泛的喜爱和欢迎。",
              "audio": "http://182.92.100.66:5000/media/audios/%E6%98%8E%E5%A4%A9%E4%BD%A0%E5%A5%BD%E7%94%B5%E8%A7%86%E5%89%A7%E5%8A%A0%E6%B2%B9%E5%90%A7%E5%AE%9E%E4%B9%A0%E7%94%9F%E6%8F%92%E6%9B%B2-%E7%89%9B%E5%92%96%E5%95%A1.128.mp3",
              "duration": "271.831269",
              "lyric": "http://182.92.100.66:5000/media/lyrics/%E6%98%8E%E5%A4%A9%E4%BD%A0%E5%A5%BD%E7%94%B5%E8%A7%86%E5%89%A7%E5%8A%A0%E6%B2%B9%E5%90%A7%E5%AE%9E%E4%B9%A0%E7%94%9F%E6%8F%92%E6%9B%B2_-_%E7%89%9B%E5%A5%B6%E5%92%96%E5%95%A1.lrc",
              "tag_theme": null,
              "tag_scene": null,
              "tag_mood": null,
              "tag_style": null,
              "tag_language": null,
              "uploader": "yy",
              "like": 0,
              "upload_date": "2024-04-22 19:53:53"
          }
      ]
  }
  ```

### 更新歌曲信息
- **请求类型：** POST
- **URL：** `/songs/update/{songID}`
- **请求参数：**
  - 歌曲ID (SongID) 必填 **(以下都是可选，放在请求体里)**
  - 标题 (title)
  - 演唱者(singer)
  - 封面图(cover)
  - 介绍(introduction)
  - 音频文件(audio)
  - 歌词文件(lyric)
  - 主题标签(tag\_theme)
  - 场景标签(tag\_scene)
  - 心情标签(tag\_mood)
  - 风格标签(tag\_style)
  - 语言标签(tag\_language)
- **返回结果：**
  - 是否成功 (success)：表示更新是否成功
  - 消息 (message)：更新过程的结果消息

### 删除歌曲
==现在最好不要删除歌曲，因为看题目好像是允许撤回删除操作，后面会改成逻辑删除==

- **请求类型：** DELETE
- **URL：** `/songs/delete/{songID}`
- **请求参数：**

  - 歌曲ID (SongID)
- **返回结果：**
  - 是否成功 (success)：表示删除是否成功
  - 消息 (message)：删除过程的结果消息
- 返回示例：

  ```json
  {
      "success": true,
      "message": "删除成功"
  }
  ```
### 查看歌曲评论
- **请求类型：** GET
- **URL：** `/songs/comments`
- **请求参数：**

  - 歌曲ID (songID)
- **返回结果：**
  - 是否成功(success)
  - 返回信息(message)
  - 返回数据(data)
- 返回示例

  ```json
  url示例为：songs/comments?songID=8
  {
      "success": true,
      "message": "获取评论成功",
      "data": [
          {
              "id": 6,
              "user": "sivenlu",
              "song": 8,
              "content": "太好听了",
              "comment_date": "2024-05-07T10:02:48.058713",
              "like": 0
          }
      ]
  }
  ```

### 歌曲可选标签
标签从下面列表里选择，不然存不进数据库

```python
THEME_CHOICES = [
    ('背景音乐', '背景音乐'),
    ('经典老歌', '经典老歌'),
    ('KTV金曲', 'KTV金曲'),
    ('游戏配乐', '游戏配乐'),
    ('电影配乐', '电影配乐'),
    ('情歌', '情歌'),
    ('乐器', '乐器'),
    ('ACG', 'ACG'),
    ('厂牌专区', '厂牌专区'),
    ('综艺', '综艺'),

]

SCENE_CHOICES = [
    ('咖啡馆', '咖啡馆'),
    ('运动', '运动'),
    ('睡前', '睡前'),
    ('旅行', '旅行'),
    ('派对', '派对'),
    ('夜店', '夜店'),
    ('学习工作', '学习工作'),
    ('跳舞', '跳舞'),
    ('婚礼', '婚礼'),
    ('约会', '约会'),
    ('校园', '校园'),
    ('驾驶', '驾驶'),
]

MOOD_CHOICES = [
    ('伤感', '伤感'),
    ('安静', '安静'),
    ('思念', '思念'),
    ('宣泄', '宣泄'),
    ('开心', '开心'),
    ('励志', '励志'),
    ('治愈', '治愈'),
    ('甜蜜', '甜蜜'),
    ('寂寞', '寂寞'),
]

STYLE_CHOICES = [
    ('摇滚', '摇滚'),
    ('民谣', '民谣'),
    ('轻音乐', '轻音乐'),
    ('电音', '电音'),
    ('流行', '流行'),
    ('金属', '金属'),
    ('说唱', '说唱'),
    ('中国风', '中国风'),
    ('布鲁斯', '布鲁斯'),
    ('乡村', '乡村'),
    ('古典', '古典'),
    ('爵士', '爵士'),
    ('中国传统', '中国传统'),

]

LANGUAGE_CHOICES = [
    ('英语', '英语'),
    ('日语', '日语'),
    ('粤语', '粤语'),
    ('国语', '国语'),
    ('韩语', '韩语'),
    ('法语', '法语'),
    ('拉丁语', '拉丁语'),
    ('闽南语', '闽南语'),
    ('小语种', '小语种'),
]
```

### 测试接口
#### 获取所有歌曲信息
```json
http://182.92.100.66:5000/songs/alldata
```

```json
{
    "success": true,
    "message": "获取所有歌曲信息成功",
    "data": [
        {
            "id": 1,
            "title": "喜帖街",
            "singer": "谢安琪",
            "cover": "http://182.92.100.66:5000/media/covers/%E5%96%9C%E5%B8%96%E8%A1%97.webp",
            "gradient": null,
            "introduction": "这是谢安琪写的一首歌",
            "audio": "http://182.92.100.66:5000/media/audios/%E5%96%9C%E5%B8%96%E8%A1%97.mp3",
            "duration": null,
            "lyric": null,
            "tag_theme": null,
            "tag_scene": null,
            "tag_mood": null,
            "tag_style": null,
            "tag_language": null,
            "uploader": "yy9",
            "like": 0,
            "upload_date": "2024-04-21 23:13:27"
        },
        {
            "id": 2,
            "title": "喜帖街",
            "singer": "谢安琪",
            "cover": "http://182.92.100.66:5000/media/covers/%E5%96%9C%E5%B8%96%E8%A1%97_AT5qMkj.webp",
            "gradient": null,
            "introduction": "这是谢安琪写的一首歌",
            "audio": "http://182.92.100.66:5000/media/audios/%E5%96%9C%E5%B8%96%E8%A1%97_c7fuYjm.mp3",
            "duration": null,
            "lyric": null,
            "tag_theme": null,
            "tag_scene": null,
            "tag_mood": null,
            "tag_style": null,
            "tag_language": null,
            "uploader": "xht",
            "like": 0,
            "upload_date": "2024-04-21 23:14:56"
        }
    ]
}
```

## 歌单表接口
### 创建歌单
- **请求类型：** POST
- **URL：** `/songlists/create`
- **请求参数：**
  - 标题 (title) 必填
  - 封面图(cover) 必填
  - 介绍(introduction)
  - 标签（可为空）
    - 主题标签(tag\_theme)
    - 场景标签(tag\_scene)
    - 心情标签(tag\_mood)
    - 风格标签(tag\_style)
    - 语言标签(tag\_language)
  - 所有者/创建者(owner) 必填
- **返回结果：**
  - 是否成功 (success)：表示创建是否成功
  - 消息 (message)：创建过程的结果消息

### 获取歌单信息
- **请求类型：** GET
- **URL：** `/songlists/info/{songlistID}`
- **请求参数：**
  - 歌单ID (SonglistID) 必填
  - 用户名(username) 选填 如果有则会查询对应用户是否喜欢该歌单
- **返回结果：**
  - 标题 (title)
  - 封面图(文件地址，cover\_url)
  - 介绍(introduction)
  - 包含的歌曲(歌曲列表，每个元素是字典，即[ {"id": , "title":, "singer": , "cover": }, { } ])
  - 标签（获取的结果可能为空）
    - 主题标签(tag\_theme)
    - 场景标签(tag\_scene)
    - 心情标签(tag\_mood)
    - 风格标签(tag\_style)
    - 语言标签(tag\_language)
  - 所有者/创建者(owner, 是username)
  - 创建时间(create\_date)
  - 喜欢人数(like)
- 返回示例：

  ```json
  http://182.92.100.66:5000/songlists/info/6?username=yy
  ```

  ```json
  {
      "success": true,
      "message": "获取歌单成功",
      "data": {
          "id": 6,
          "title": "yy的英文歌单",
          "cover": "http://182.92.100.66:5000/media/covers/yy_c.jpg",
          "introduction": "null",
          "songs": [
              {
                  "id": 10,
                  "title": "illicit affairs",
                  "singer": "Taylor Swift",
                  "cover": "http://182.92.100.66:5000/media/covers/IllicitAffairs_cover.jpg",
                  "gradient": "background: rgb(31, 31, 31);background: linear-gradient(135deg, rgb(44, 44, 44), rgb(152, 152, 152));",
                  "introduction": "《illicit affairs》是美国创作歌手泰勒·斯威夫特的一首歌曲。这首歌取自她于 2020 年 7 月 24 日发行的第八张录音室专辑《Folklore》 。这首歌由斯威夫特和杰克·安东诺夫创作和制作，乔·阿尔文被认为是联合制作人。《非法事务》是一首原声吉他主导的民谣情歌 ，描述了叙述者想要维持欺骗关系的 不忠行为。",
                  "audio": "http://182.92.100.66:5000/media/audios/IllicitAffairs_audio.mp3",
                  "duration": "190.928979",
                  "lyric": "http://182.92.100.66:5000/media/lyrics/IllicitAffairs_lyric.lrc",
                  "tag_theme": null,
                  "tag_scene": "旅行",
                  "tag_mood": "宣泄",
                  "tag_style": "流行",
                  "tag_language": "英语",
                  "uploader": "sivenlu",
                  "like": 2,
                  "upload_date": "2024-04-22 19:22:46",
                  "user_like": false
              },
              {
                  "id": 18,
                  "title": "Yellow",
                  "singer": "Coldplay",
                  "cover": "http://182.92.100.66:5000/media/covers/Yellow.webp",
                  "gradient": "background: rgb(231, 142, 49);background: linear-gradient(135deg, rgb(231, 142, 49), rgb(239, 201, 170));",
                  "introduction": "《Yellow》是英国摇滚乐队酷玩乐队演唱的歌曲，由乐队四位成员克里斯·马汀、盖·贝瑞曼、强尼·邦蓝、威尔·查平共同填词，肯·尼尔森和乐队四位成员共同制作。这首歌被收录于乐队的首张专辑《Parachutes》里，并于2000年6月26日作为专辑的第二支单曲发布。2001年，《Yellow》先后获得了全英音乐奖的英国最佳单曲、英国最佳录像带和MTV音乐录影带大奖的最佳新人的提名。2002年，《Yellow》获得了格莱美的最佳摇滚歌曲的提名，并因单曲获得最佳摇滚组合的提名。2000年的一个晚上，酷玩乐队录制完专辑《Parachutes》中的歌曲《Shiver》后，一起出门休息。当时天上的星星在漆黑夜空中显得特别耀眼。坐在一旁胡乱弹着吉他的主唱克里斯·马汀抬起头凝望着夜空，即兴哼出了《Yellow》的旋律，灵感迅速地冲进了马汀的大脑里。马汀在构思歌名的时候遇到了瓶颈，他想用一个特定的词来贴合这首歌。他无意间看见当时录音室里的斯蒂芬妮（马汀碰巧在录音室的朋友）的黄色皮肤，斯蒂芬妮皮肤洋溢的黄色光芒让马汀立即将这首歌被命名为《Yellow》。",
                  "audio": "http://182.92.100.66:5000/media/audios/Yellow.mp3",
                  "duration": "266.773333",
                  "lyric": "http://182.92.100.66:5000/media/lyrics/Yellow_-_Coldplay.lrc",
                  "tag_theme": null,
                  "tag_scene": null,
                  "tag_mood": null,
                  "tag_style": null,
                  "tag_language": null,
                  "uploader": "yy",
                  "like": 1,
                  "upload_date": "2024-04-22 19:44:50",
                  "user_like": false
              },
              {
                  "id": 26,
                  "title": "钟无艳",
                  "singer": "谢安琪",
                  "cover": "http://182.92.100.66:5000/media/covers/%E9%92%9F%E6%97%A0%E8%89%B3.webp",
                  "gradient": "background: rgb(111, 91, 113);background: linear-gradient(135deg, rgb(96, 79, 98), rgb(217, 208, 214));",
                  "introduction": null,
                  "audio": "http://182.92.100.66:5000/media/audios/%E9%92%9F%E6%97%A0%E8%89%B3.mp3",
                  "duration": "276.741224",
                  "lyric": null,
                  "tag_theme": null,
                  "tag_scene": null,
                  "tag_mood": null,
                  "tag_style": null,
                  "tag_language": null,
                  "uploader": "xht",
                  "like": 1,
                  "upload_date": "2024-04-25 22:18:06",
                  "user_like": false
              }
          ],
          "tag_theme": "null",
          "tag_scene": "null",
          "tag_mood": "null",
          "tag_style": "null",
          "tag_language": "null",
          "owner": "yy",
          "create_date": "2024-04-22 19:59:00",
          "like": 1,
          "user_favor": true
      }
  }
  ```

### 更新歌单信息
- **请求类型：** POST
- **URL：** `/songlists/update/{songlistID}`
- **请求参数：**
  - 歌单ID (SonglistID) 必填 (以下都可为空，放在请求体里)
  - 标题 (title) 
  - 封面图(cover)
  - 介绍(introduction)
  - 包含的歌曲(Songs)
  - 标签（可以更新为空）
    - 主题标签(tag\_theme)
    - 场景标签(tag\_scene)
    - 心情标签(tag\_mood)
    - 风格标签(tag\_style)
    - 语言标签(tag\_language)
- **返回结果：**
  - 是否成功 (success)：表示更新是否成功
  - 消息 (message)：更新过程的结果消息
- 返回示例：

  ```json
  {
      "success": true,
      "message": "更新歌单成功"
  }
  ```

### 删除歌单
- **请求类型：** DELETE
- **URL：** `/songlists/delete/{songlistID}`
- **请求参数：**
  - 歌单ID (SonglistID) 必填
- **返回结果：**
  - 是否成功 (success)：表示删除是否成功
  - 消息 (message)：删除过程的结果消息

### 向歌单添加歌曲
- **请求类型：** POST
- **URL：** `/songlists/addsong`
- **请求参数：**
  - 歌单ID (songlist\_id) 必填
  - 歌曲ID (song\_id) 必填
- **返回结果：**
  - 是否成功 (success)：表示添加是否成功
  - 消息 (message)：添加过程的结果消息

### 从歌单删除歌曲
- **请求类型：** POST
- **URL：** `/songlists/delsong`
- **请求参数：**
  - 歌单ID (songlist\_id) 必填
  - 歌曲ID (song\_id) 必填
- **返回结果：**
  - 是否成功 (success)：表示删除是否成功
  - 消息 (message)：删除过程的结果消息

### 测试接口
#### 获取所有歌单信息
```json
http://182.92.100.66:5000/songlists/alldata
```

```json
{
    "success": true,
    "message": "获取成功",
    "data": [
        {
            "id": 1,
            "title": "yy的歌单",
            "cover": "http://182.92.100.66:5000/media/covers/avatar.jpg",
            "introduction": null,
            "songs": [
                {
                    "id": 1,
                    "title": "喜帖街",
                    "singer": "谢安琪",
                    "cover": "http://182.92.100.66:5000/media/covers/%E5%96%9C%E5%B8%96%E8%A1%97.webp",
                    "gradient": null,
                    "introduction": "这是谢安琪写的一首歌",
                    "audio": "http://182.92.100.66:5000/media/audios/%E5%96%9C%E5%B8%96%E8%A1%97.mp3",
                    "duration": null,
                    "lyric": null,
                    "tag_theme": null,
                    "tag_scene": null,
                    "tag_mood": null,
                    "tag_style": null,
                    "tag_language": null,
                    "uploader": "yy9",
                    "like": 0,
                    "upload_date": "2024-04-21 23:13:27"
                }
            ],
            "tag_theme": null,
            "tag_scene": null,
            "tag_mood": null,
            "tag_style": null,
            "tag_language": null,
            "owner": "yy",
            "create_date": "2024-04-22 17:32:26",
            "like": 0
        }
    ]
}
```

## 搜索接口
### 搜索歌曲
- **请求类型：** GET
- **URL：** `/search/songs?keyword=value`
- **返回结果：**
  - 字典组成的列表，可以理解为歌曲的集合
  - 如果不加任何查询参数，默认返回所有歌曲，可以添加查询参数如keyword、tag\_theme等，也可以用num参数指定返回的数量
  - 注意是模糊查询
- 返回信息：
  - 搜索成功
  - try-catch捕获到的Exception
- 请求示例：

  ```json
  http://182.92.100.66:5000/search/songs?tag_scene=咖啡馆&num=2&keyword=taylor
  ```

  ```json
  {
      "success": true,
      "message": "搜索成功",
      "data": [
          {
              "id": 12,
              "title": "All Too Well",
              "singer": "Taylor Swift",
              "cover": "http://182.92.100.66:5000/media/covers/AllTooWell_cover.jpg",
              "duration": "613.041632",
              "uploader": "sivenlu",
              "like": 2
          }
      ]
  }
  ```

### 搜索歌单
- **请求类型：** GET
- **URL：** `/search/songlists?keyword=value`
- **返回结果：**
  - 字典组成的列表，可以理解为歌单的集合
  - 如果不加任何查询参数，默认返回所有歌单，可以添加查询参数如keyword、tag\_theme等，也可以用num参数指定返回的数量
  - 注意是模糊查询
- 返回信息：
  - 搜索成功
  - try-catch捕获到的Exception
- 请求示例：

  ```json
  http://182.92.100.66:5000/search/songlists?num=3&keyword=yy
  ```

  ```json
  {
      "success": true,
      "message": "搜索成功",
      "data": [
          {
              "id": 5,
              "title": "yy的中文歌单",
              "cover": "http://182.92.100.66:5000/media/covers/yy_e.jpg",
              "owner": "yy",
              "create_date": "2024-04-22 19:58:42",
              "like": 3
          },
          {
              "id": 6,
              "title": "yy的英文歌单",
              "cover": "http://182.92.100.66:5000/media/covers/yy_c.jpg",
              "owner": "yy",
              "create_date": "2024-04-22 19:59:00",
              "like": 1
          },
          {
              "id": 36,
              "title": "yy的纯音乐歌单",
              "cover": "http://182.92.100.66:5000/media/covers/avatar.jpg",
              "owner": "yy",
              "create_date": "2024-05-06 20:51:48",
              "like": 0
          }
      ]
  }
  ```

### 搜索用户
- **请求类型：** GET
- **URL：** `/search/users?keyword=value`
- **返回结果：**
  - 如果不加任何查询参数，默认返回所有用户，可以添加查询参数如keyword，也可以用num参数指定返回的数量
  - 注意是模糊查询
- 返回信息：
  - 搜索成功
  - try-catch捕获到的Exception
- 请求示例：

  ```json
  http://182.92.100.66:5000/search/users?keyword=yy
  ```

  ```json
  {
      "success": true,
      "message": "搜索成功",
      "data": [
          {
              "username": "yy9",
              "bio": "我是一个特立独行的人",
              "avatar": "http://182.92.100.66:5000/media/avatars/%E5%96%9C%E5%B8%96%E8%A1%97.webp",
              "follower_count": 0,
              "following_count": 0,
              "registration_date": "2024-04-20 16:04:48"
          },
          {
              "username": "yy",
              "bio": "你好，我是yy123456",
              "avatar": "http://182.92.100.66:5000/media/avatars/avatar.jpg",
              "follower_count": 0,
              "following_count": 1,
              "registration_date": "2024-04-21 15:20:36"
          }
      ]
  }
  ```

## 推荐(Recommend)表接口
### 获取最近上传的歌曲
- **请求类型：** GET
- **URL：** `recommend/latest`
- **请求参数：**
  - 需要获得最近歌曲的数量(num) 可选，默认为15
- **返回结果：**
  - 是否成功 (success)：表示删除是否成功
  - 消息 (message)：删除过程的结果消息
  - 返回用户播放列表，按照最近播放时间先后排序，目前有10首
  - 返回参数中的last\_play是最近播放时间，play\_count是播放次数
- 返回示例：（因篇幅限制只作参考）

需要歌曲的数量(num) 默认为15

```json
http://182.92.100.66:5000/recommend/latest
```

返回示例（大于15首只返回15首）

这里只展示3首

```json
{
    "success": true,
    "message": "获取最近歌曲成功",
    "data": [
        {
            "id": 22,
            "title": "明天过后",
            "singer": "张杰",
            "cover": "http://182.92.100.66:5000/media/covers/%E6%98%8E%E5%A4%A9%E8%BF%87%E5%90%8E-%E5%BC%A0%E6%9D%B0.png",
            "gradient": null,
            "introduction": "匿名的好友",
            "audio": "http://182.92.100.66:5000/media/audios/%E6%98%8E%E5%A4%A9%E8%BF%87%E5%90%8E-%E5%BC%A0%E6%9D%B0.mp3",
            "duration": "237.297392",
            "lyric": "http://182.92.100.66:5000/media/lyrics/%E6%98%8E%E5%A4%A9%E8%BF%87%E5%90%8E_-_%E5%BC%A0%E6%9D%B0.lrc",
            "tag_theme": null,
            "tag_scene": null,
            "tag_mood": null,
            "tag_style": null,
            "tag_language": null,
            "uploader": "yees",
            "like": 0,
            "upload_date": "2024-04-22 22:15:55"
        },
        {
            "id": 21,
            "title": "匿名的好友",
            "singer": "杨丞琳",
            "cover": "http://182.92.100.66:5000/media/covers/%E5%8C%BF%E5%90%8D%E7%9A%84%E5%A5%BD%E5%8F%8B-%E6%9D%A8%E4%B8%9E%E7%90%B3.png",
            "gradient": null,
            "introduction": "匿名的好友",
            "audio": "http://182.92.100.66:5000/media/audios/%E5%8C%BF%E5%90%8D%E7%9A%84%E5%A5%BD%E5%8F%8B-%E6%9D%A8%E4%B8%9E%E7%90%B3.128.mp3",
            "duration": "262.870204",
            "lyric": "http://182.92.100.66:5000/media/lyrics/%E5%8C%BF%E5%90%8D%E7%9A%84%E5%A5%BD%E5%8F%8B_-_%E6%9D%A8%E4%B8%9E%E7%90%B3.lrc",
            "tag_theme": null,
            "tag_scene": null,
            "tag_mood": null,
            "tag_style": null,
            "tag_language": null,
            "uploader": "yees",
            "like": 0,
            "upload_date": "2024-04-22 22:11:43"
        },
        {
            "id": 20,
            "title": "明天，你好",
            "singer": "牛奶咖啡",
            "cover": "http://182.92.100.66:5000/media/covers/%E6%98%8E%E5%A4%A9%E4%BD%A0%E5%A5%BD.webp",
            "gradient": null,
            "introduction": "《明天，你好》是中国乐团牛奶咖啡演唱的一首歌曲，也是他们的代表作之一。这首歌以轻快、欢快的旋律和朗朗上口的歌词，传递了乐观、积极的生活态度。歌曲鼓励人们在面对困难时保持乐观，相信未来会更美好。牛奶咖啡通过这首歌曲，向听众传递了正能量和希望，受到了广泛的喜爱和欢迎。",
            "audio": "http://182.92.100.66:5000/media/audios/%E6%98%8E%E5%A4%A9%E4%BD%A0%E5%A5%BD%E7%94%B5%E8%A7%86%E5%89%A7%E5%8A%A0%E6%B2%B9%E5%90%A7%E5%AE%9E%E4%B9%A0%E7%94%9F%E6%8F%92%E6%9B%B2-%E7%89%9B%E5%92%96%E5%95%A1.128.mp3",
            "duration": "271.831269",
            "lyric": "http://182.92.100.66:5000/media/lyrics/%E6%98%8E%E5%A4%A9%E4%BD%A0%E5%A5%BD%E7%94%B5%E8%A7%86%E5%89%A7%E5%8A%A0%E6%B2%B9%E5%90%A7%E5%AE%9E%E4%B9%A0%E7%94%9F%E6%8F%92%E6%9B%B2_-_%E7%89%9B%E5%A5%B6%E5%92%96%E5%95%A1.lrc",
            "tag_theme": null,
            "tag_scene": null,
            "tag_mood": null,
            "tag_style": null,
            "tag_language": null,
            "uploader": "yy",
            "like": 0,
            "upload_date": "2024-04-22 19:53:53"
        },
    ]
}
```

### 根据用户喜好获取推荐歌曲
- **请求类型：** GET
- **URL：** `recommend`
- **请求参数：**

  - 无（只要是已登录即可）
- **返回结果：**
  - 是否成功 (success)：表示获取是否成功
  - 消息 (message)：获取过程的消息
  - data: 推荐歌曲列表，目前是20首
- 返回示例：（因篇幅限制只作参考）

  ```json
  {
      "success": true,
      "message": "获取推荐歌曲成功",
      "data": [
          {
              "id": 29,
              "title": "有形的翅膀",
              "singer": "张韶涵",
              "cover": "http://127.0.0.1:8000/media/covers/%E6%9C%89%E5%BD%A2%E7%9A%84%E7%BF%85%E8%86%80_6qNIdNs.webp",
              "gradient": "background: rgb(21, 46, 45);background: linear-gradient(135deg, rgb(28, 63, 63), rgb(200, 226, 228));",
              "introduction": "有形的翅膀",
              "audio": "http://127.0.0.1:8000/media/audios/%E6%9C%89%E5%BD%A2%E7%9A%84%E7%BF%85%E8%86%80_D89Y7UL.mp3",
              "duration": "216.106666",
              "lyric": "http://127.0.0.1:8000/media/lyrics/%E6%9C%89%E5%BD%A2%E7%9A%84%E7%BF%85%E8%86%80.lrc",
              "tag_theme": "默认",
              "tag_scene": "咖啡馆",
              "tag_mood": "安静",
              "tag_style": "轻音乐",
              "tag_language": "国语",
              "uploader": "yy",
              "like": 0,
              "upload_date": "2024-04-25 23:55:22",
              "user_like": false,
              "user_favor": false
          },
          {
              "id": 32,
              "title": "岩石里的花",
              "singer": "邓紫棋",
              "cover": "http://127.0.0.1:8000/media/covers/0a8cdf6778b17e04f92d9a6788033ee6c8709f51.jpg1000w_1000h_1c.webp",
              "gradient": "background: rgb(196, 169, 194);background: linear-gradient(135deg, rgb(196, 169, 194), rgb(20, 9, 7));",
              "introduction": null,
              "audio": "http://127.0.0.1:8000/media/audios/%E5%B2%A9%E7%9F%B3%E9%87%8C%E7%9A%84%E8%8A%B1-G.E.M.%E9%82%93%E7%B4%AB%E6%A3%8B.mp3",
              "duration": "294.12",
              "lyric": "http://127.0.0.1:8000/media/lyrics/%E5%B2%A9%E7%9F%B3%E9%87%8C%E7%9A%84%E8%8A%B1.lrc",
              "tag_theme": "默认",
              "tag_scene": "咖啡馆",
              "tag_mood": "安静",
              "tag_style": "风格",
              "tag_language": "语言",
              "uploader": "xht",
              "like": 0,
              "upload_date": "2024-04-26 12:09:45",
              "user_like": false,
              "user_favor": false
          },
          {
              "id": 44,
              "title": "Someone Like You",
              "singer": "Adele",
              "cover": "http://127.0.0.1:8000/media/covers/Someone_Like_You-Adele_WZwjw7O.png",
              "gradient": "background: rgb(30, 30, 32);background: linear-gradient(135deg, rgb(43, 44, 46), rgb(169, 171, 173));",
              "introduction": null,
              "audio": "http://127.0.0.1:8000/media/audios/Someone_Like_You-Adele.128_wJaVcky.mp3",
              "duration": "285.24",
              "lyric": "http://127.0.0.1:8000/media/lyrics/Someone_Like_You.lrc",
              "tag_theme": "经典老歌",
              "tag_scene": "场景",
              "tag_mood": "伤感",
              "tag_style": "风格",
              "tag_language": "英语",
              "uploader": "yees",
              "like": 0,
              "upload_date": "2024-05-03 23:32:31",
              "user_like": false,
              "user_favor": false
          },
          {
              "id": 34,
              "title": "暗涌",
              "singer": "王菲",
              "cover": "http://127.0.0.1:8000/media/covers/3ad41f742513d2b12a54cada9d52436298b2d9dc.jpg1000w_1000h_1c.webp",
              "gradient": "background: rgb(214, 213, 218);background: linear-gradient(135deg, rgb(202, 200, 207), rgb(42, 36, 34));",
              "introduction": null,
              "audio": "http://127.0.0.1:8000/media/audios/d6f1_2c34_25cc_60734831031159aa4df413ebd0840698.mp3",
              "duration": "259.709387",
              "lyric": "http://127.0.0.1:8000/media/lyrics/%E6%9A%97%E6%B6%8C.lrc",
              "tag_theme": "经典老歌",
              "tag_scene": "睡前",
              "tag_mood": "安静",
              "tag_style": "默认",
              "tag_language": "国语",
              "uploader": "xht",
              "like": 0,
              "upload_date": "2024-04-27 22:46:15",
              "user_like": false,
              "user_favor": false
          },
      ]
  }
  ```

## 喜欢(Like)表接口
### 获取用户喜爱歌曲
- **请求类型：** GET
- **URL：** `/like/songs`
- **请求参数：**

  - 用户名 (username) 必填
- 返回参数：
  - success
  - message
  - data
  - token
- 返回示例：

  ```json
  示例url: /like/songs?username=sivenlu
  {
      "success": true,
      "message": "获取用户喜欢歌曲成功",
      "data": [
          {
              "id": 9,
              "title": "exile",
              "singer": "Taylor Swift",
              "cover": "http://127.0.0.1:8000/media/covers/exile_cover.jpg",
              "gradient": "background: rgb(160, 160, 160);background: linear-gradient(135deg, rgb(174, 174, 174), rgb(68, 68, 68));",
              "introduction": "《Exile》描绘了两个疏远恋人进行无声对话的想象故事，是一首极简但具有电影感的独立民谣，带有福音、管弦乐和室内流行元素，将斯威夫特甜蜜的歌声和弗农低沉的男中音结合成一首忧郁的二重唱，沉重的钢琴、旋转的弦乐和高亢的和声。 《Exile》一经发行就获得了广泛的好评，重点是二人组合的声乐化学反应、令人痛苦的抒情、丰富的器乐和阴郁的气氛。音乐评论家将其视为《Folklore》中的佼佼者，并将其称为斯威夫特迄今为止最好的合作作品之一，并将其​​与她 2011 年的歌曲“ Safe & Sound ”进行比较。多家出版物将《Exile》列为 2020 年最佳歌曲之一。",
              "audio": "http://127.0.0.1:8000/media/audios/exile_audio.mp3",
              "duration": "285.634172",
              "lyric": "http://127.0.0.1:8000/media/lyrics/exile_lyric.lrc",
              "tag_theme": null,
              "tag_scene": null,
              "tag_mood": null,
              "tag_style": null,
              "tag_language": null,
              "uploader": "sivenlu",
              "like": 1,
              "upload_date": "2024-04-22 19:21:37",
              "user_like": false,
              "user_favor": false
          }
      ],
      "token": null
  }
  ```

### 用户添加喜爱歌曲
- **请求类型：** POST
- **URL：** `/like/songs/add`
- **请求参数：**

  - 歌曲id（song\_id）必填
- **返回结果：**
  - success
  - message
    - 未获取到歌曲id
    - 未获取到用户名
    - 用户不存在
    - 歌曲不存在
    - 歌曲已添加到喜爱列表
    - 歌曲已在喜爱列表中
  - data
  - token
- 返回示例：

  ```json
  {
      "success": true,
      "message": "歌曲已添加到喜爱列表",
      "data": null,
      "token": null
  }
  ```

### 用户删除喜爱歌曲
- **请求类型：** POST
- **URL：** `/like/songs/delete`
- **请求参数：**

  - 歌曲id（song\_id）必填
- **返回结果：**
  - 是否成功 (success)
  - 信息 (message)
    - 未获取到歌曲id
    - 未获取到用户名
    - 用户不存在
    - 歌曲不存在
    - 删除成功
    - 歌曲不在喜爱列表中，删除失败
- 返回示例：

  ```json
  {
      "success": true,
      "message": "删除成功"
  }
  ```

### 获取用户喜爱歌单
- **请求类型：** GET
- **URL：** `/like/songlists`
- **请求参数：**

  - 用户名 (username) 必填
- **返回结果：**
  - success
  - 歌单组成的列表 (data)
- 返回示例：

  ```json
  示例url: /like/songlist?username=sivenlu
  {
      "success": true,
      "data": [
          {
              "id": 1,
              "title": "yy的歌单",
              "cover": "http://127.0.0.1:8000/media/covers/avatar.jpg",
              "introduction": null,
              "songs": [
                  {
                      "id": 1,
                      "title": "喜帖街",
                      "singer": "谢安琪",
                      "cover": "http://127.0.0.1:8000/media/covers/%E5%96%9C%E5%B8%96%E8%A1%97.webp",
                      "gradient": "background: rgb(73, 69, 68);background: linear-gradient(135deg, rgb(81, 76, 76), rgb(201, 191, 189));",
                      "introduction": "这是谢安琪写的一首歌",
                      "audio": "http://127.0.0.1:8000/media/audios/%E5%96%9C%E5%B8%96%E8%A1%97.mp3",
                      "duration": null,
                      "lyric": "http://127.0.0.1:8000/media/lyrics/%E5%96%9C%E5%B8%96%E8%A1%97_-_%E8%B0%A2%E5%AE%89%E7%90%AA.lrc",
                      "tag_theme": null,
                      "tag_scene": null,
                      "tag_mood": null,
                      "tag_style": null,
                      "tag_language": null,
                      "uploader": "yy9",
                      "like": 0,
                      "upload_date": "2024-04-21 23:13:27"
                  },
                  ...
   
              ],
              "tag_theme": null,
              "tag_scene": null,
              "tag_mood": null,
              "tag_style": null,
              "tag_language": null,
              "owner": "yy",
              "create_date": "2024-04-22 17:32:26",
              "like": 1
          }
      ]
  }
  ```

### 用户添加喜爱歌单
- **请求类型：** POST
- **URL：** `/like/songlists/add`
- **请求参数：**

  - 歌单id（songlist\_id）必填
- **返回结果：**
  - 是否成功 (success)
  - 信息 (message)
    - 未获取到歌单id
    - 未获取到用户名
    - 用户不存在
    - 歌单不存在
    - 添加成功
    - 歌单已在喜爱列表中，添加失败
- 返回示例：

  ```json
  {
      "success": true,
      "message": "添加成功"
  }
  ```

### 用户删除喜爱歌单
- **请求类型：** POST
- **URL：** `/like/songlists/delete`
- **请求参数：**

  - 歌单id（songlist\_id）必填
- **返回结果：**
  - 是否成功 (success)
  - 信息 (message)
    - 未获取到歌单id
    - 未获取到用户名
    - 用户不存在
    - 歌单不存在
    - 删除成功
    - 歌单不在喜爱列表中，删除失败
- 返回示例：

  ```json
  {
      "success": true,
      "message": "删除成功"
  }
  ```

## 关注(follow)表接口
### 加关注/取消关注
- **请求类型：** POST
- **URL：** `/users/follow`
- **请求参数：**

  - 被关注/取消关注用户姓名(username)
- 返回结果：
  - 是否成功(success): 加关注/取消关注是否成功
  - 消息(message): 加关注成功/取消关注成功
- 补充：
  - 加关注/取消关注 会对应的处理Message表
    - 加关注：创建一条信息，其中content为“x关注了你”，其中x会被替换为发起请求的用户；type为4
    - 取消关注：删除加关注的时候创建的那条信息
  - 加关注/取消关注 会对应的处理User的following\_count（正在关注的人数）字段和follower\_count（正在关注ta的人数）字段
    - 加关注：发起请求的用户的following\_count  += 1， 被关注的用户的follower\_count += 1
    - 取消关注：发起请求的用户的following\_count  -= 1， 被关注的用户的follower\_count -= 1
- 返回示例

  ```json
  {
    "success": true,
    "message": "取消关注成功"
  }
  ```

## 评论(Comment)表接口
### 发表评论
- **请求类型：** POST
- **URL：** `/comments/add`
- **请求参数：**
  - 歌曲ID (songID)
  - 评论内容(content)
- **返回结果：**
  - 是否成功 (success)：表示删除是否成功
  - 消息 (message)：删除过程的结果消息
- 返回示例

  ```json
  {
      "success": true,
      "message": "评论成功"
  }
  ```

### 删除评论
- **请求类型：** DELETE
- **URL：** `/comments/delete`
- **请求参数：**

  - 评论id(contentID)
- **返回结果：**
  - 是否成功 (success)：表示删除是否成功
  - 消息 (message)：删除过程的结果消息
- 返回示例

  ```json
  {
      "success": true,
      "message": "评论删除成功"
  }
  ```

## 消息(Message)表接口
**消息类型，对应type字段**

```python
# 消息通知类型
NOTICE_TYPE_CHOICES = [
    (1, '系统通知'),
    (2, '评论通知'),
    (3, '喜欢通知'),
    (4, '关注通知'),
    (5, '私信通知'),
    (6, '投诉通知'),
    (7, '申诉通知'),
]
```

消息分为已读和未读消息，用is\_read字段表示
### 获取用户消息
- **请求类型：** GET
- **URL：** `/messages`
- **请求参数：**

  - 无
- **返回结果：**
  - 是否成功 (success)：表示获取消息是否成功
  - 消息 (message)：获取过程的结果消息
- **注意这个接口返回的是除了私信以外的通知**
- 返回示例

  ```json
  {
      "success": true,
      "message": "获取用户消息成功",
      "data": [
          {
              "id": 9,
              "sender": "sivenlu",
              "receiver": "yy",
              "title": "新的关注",
              "content": "sivenlu关注了你",
              "type": 4,
              "send_date": "2024-05-06 19:30:02",
              "is_read": false
          },
          {
              "id": 42,
              "sender": "Nzh",
              "receiver": "yy",
              "title": "新的评论",
              "content": "Nzh评论了你上传的歌曲《当离别开出花》：369",
              "type": 2,
              "send_date": "2024-05-09 20:19:30",
              "is_read": false
          },
          {
              "id": 43,
              "sender": "Nzh",
              "receiver": "yy",
              "title": "新的评论",
              "content": "Nzh评论了你上传的歌曲《平凡之路(live)》：好听",
              "type": 2,
              "send_date": "2024-05-09 20:42:39",
              "is_read": false
          },
          {
              "id": 44,
              "sender": "yy",
              "receiver": "yy",
              "title": "新的评论",
              "content": "yy评论了你上传的歌曲《当离别开出花》：这首歌很好听！",
              "type": 2,
              "send_date": "2024-05-09 23:08:06",
              "is_read": false
          },
          {
              "id": 45,
              "sender": "xht",
              "receiver": "yy",
              "title": "新的评论",
              "content": "xht评论了你上传的歌曲《当离别开出花》：测试",
              "type": 2,
              "send_date": "2024-05-09 23:46:39",
              "is_read": false
          },
          {
              "id": 46,
              "sender": "system",
              "receiver": "yy",
              "title": "听歌周报",
              "content": "您在2024-05-03至2024-05-11这段时间内，共听歌0首，累计听歌时长0小时0分钟0秒。您最常听的歌曲是当离别开出花，共播放0次。您最常听的歌手是陈奕迅，共听过他/她的2首歌曲，分别是红玫瑰, 单车。您喜欢听的歌曲风格为国语, 流行, 安静。祝您生活愉快！",
              "type": 1,
              "send_date": "2024-05-10 11:15:41",
              "is_read": false
          }
      ]
  }
  ```

### 已读消息

- **请求类型：** POST
- **URL：** `/messages/read`
- **请求参数：**

  - 消息ID (message\_id) 必填
- **返回结果：**
  
  - 是否成功 (success)：表示读消息是否成功
  - 消息 (message)：过程的结果消息
- 返回示例

  ```json
  {
      "success": true, 
      "message": "消息已读"
  }
  ```

### 发送消息
- **请求类型：** POST

- **URL：** `/messages/send`

- **请求参数：**
  - 接收方 (receiver) 必填 为用户名
  - 消息内容 (content) 必填 不为空
  
- **返回结果：**
  - 是否成功 (success)：表示发送消息是否成功
  - 消息 (message)：发送过程的结果消息
  
- 返回示例

  **axios请求代码**

  ```javascript
  var axios = require('axios');
  var FormData = require('form-data');
  var data = new FormData();
  data.append('receiver', 'yees');
  data.append('content', '很高兴认识你！');
  
  var config = {
     method: 'post',
     url: 'http://182.92.100.66:5000/messages/send',
     headers: { 
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo5LCJ1c2VybmFtZSI6Inl5Iiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNzE1MzQ0OTcxfQ.cabVhfvA29twrFYyh54ck4QaxGnbRGOKxREwFDXfkYc', 
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)', 
        'Accept': '*/*', 
        'Host': '182.92.100.66:5000', 
        'Connection': 'keep-alive', 
        'Content-Type': 'multipart/form-data; boundary=--------------------------150963212448886818496073', 
        ...data.getHeaders()
     },
     data : data
  };
  
  axios(config)
  .then(function (response) {
     console.log(JSON.stringify(response.data));
  })
  .catch(function (error) {
     console.log(error);
  });
  ```

  ```json
  {
      "success": true,
      "message": "消息发送成功"
  }
  ```

### 删除消息
- **请求类型：** DELETE
- **URL：** `/messages/delete`
- **请求参数：**

  - 消息ID (message\_id) 必填
- **返回结果：**
  - 是否成功 (success)：表示删除消息是否成功
  - 消息 (message)：删除过程的结果消息
- 返回示例

  ```json
  {
      "success": true,
      "message": "消息已删除"
  }
  ```

### 查询聊天

- **请求类型：** GET

- **URL：** `/messages/chats`

- **请求参数：**

  - 无

- **返回结果：**

  - 是否成功 (success)：表示获取聊天是否成功
  - 消息 (message)：获取过程的结果消息

- **返回的是聊天列表，像微信聊天框的数据格式，有用户名，用户头像URL和最近的一条私信消息**

- **目前聊天的逻辑是，你关注了用户，那么你能收到他的更新消息，上传消息，但是此时你们不能互相发消息，互相关注后可以聊天**

- 返回示例

  ```json
  http://182.92.100.66:5000/messages/chats
  ```

  ```json
  {
      "success": true,
      "message": "获取聊天信息成功",
      "data": [
          {
              "friend": "xht",
              "friend_avatar": "http://182.92.100.66:5000/media/avatars/c53c811f880411ebb6edd017c2d2eca2.jpg",
              "last_message": {
                  "id": 233,
                  "sender": "yy",
                  "receiver": "xht",
                  "title": "私信",
                  "content": "测试",
                  "type": 5,
                  "send_date": "2024-05-17 10:23:10",
                  "is_read": false
              }
          },
          {
              "friend": "sivenlu",
              "friend_avatar": "http://182.92.100.66:5000/media/avatars/IMG_20240114_1825591-01.jpeg",
              "last_message": null
          }
      ]
  }
  ```

### 查询聊天信息

- **请求类型：** GET

- **URL：** `/messages/privates`

- **请求参数：**

  - 朋友(friend) 必填，为用户名

- **返回结果：**

  - 是否成功 (success)：表示获取详细信息是否成功
  - 消息 (message)：获取过程的结果消息

- **返回的是聊天列表，像微信聊天界面的数据格式，按照时间排序的消息**

- **目前聊天的逻辑是，你关注了用户，那么你能收到他的更新消息，上传消息，但是此时你们不能互相发消息，互相关注后可以聊天**

- 返回示例

  ```json
  http://182.92.100.66:5000/messages/private?friend=xht
  ```

  ```json
  {
      "success": true,
      "message": "获取私信消息成功",
      "data": [
          {
              "id": 17,
              "sender": "yy",
              "receiver": "xht",
              "title": "yy",
              "content": "你好呀",
              "type": 5,
              "send_date": "2024-05-06 22:34:14",
              "is_read": false
          },
          {
              "id": 202,
              "sender": "xht",
              "receiver": "yy",
              "title": "私信",
              "content": "你好",
              "type": 5,
              "send_date": "2024-05-17 10:07:41",
              "is_read": false
          },
          ...
          {
              "id": 233,
              "sender": "yy",
              "receiver": "xht",
              "title": "私信",
              "content": "测试",
              "type": 5,
              "send_date": "2024-05-17 10:23:10",
              "is_read": false
          }
      ]
  }
  ```

## 投诉(Complaint)接口

### （用户）投诉（歌曲或歌单）

- **请求类型：** POST
- **URL：** `/songs/complaint`或`/songlists/complaint`
- **请求参数：**

  - 投诉对象id (song_id或者songlist_id)
  - 投诉具体内容(str: content)

- **返回结果：**

  - 是否成功 (success)
  - 消息 (message)
- 返回示例：
```Json
{
    "success": true,
    "message": "投诉成功"
}
```

### （管理员）获取投诉内容

- **请求类型：** GET
- **URL：** `/complaints/review`
- **请求参数：**

  - 投诉ID (complaint_id)

- **返回结果：**

  - 是否成功 (success)
  - 消息 (message)
  - 数据 (data)
- 返回示例：
```Json
{
      "success": true,
      "message": "获取投诉信息成功",
      "data": {
            "id": 6,
            "complainer": "sivenlu",
            "complained": "xht",
            "content": "歌词不符合核心价值观",
            "object_type": "song",
            "object_id": 5,
            "complaint_date": "2024-05-15T12:06:31.788"
      }
}
```

### （管理员）处理投诉

- **请求类型：** POST
- **URL：** `/complaints/handle`
- **请求参数：**
  - 投诉id (complaint_id)
  - 是否下架 (boolean: is_remove)
  - 处理理由 (str: reason)

- **返回结果：**

  - 是否成功 (success)
  - 消息 (message)
  - 数据 (data)
- 返回示例：
```Json
{
  "success": true,
  "message": " 处理投诉成功"
}
```
### （被投诉导致下架的内容的所有者）申诉

- **请求类型：** POST
- **URL：** `/complaints/appeal`
- **请求参数：**
  - 自己的内容被投诉的那个投诉id (complaint_id)
  - 申诉理由 (str: reason)

- **返回结果：**

  - 是否成功 (success)
  - 消息 (message)
  - 数据 (data)
- 返回示例：
```Json
{
    "success": true,
    "message": " 申诉发送成功"
}
```
### （管理员）查看申诉

- **请求类型：** GET
- **URL：** `/complaints/appeals/review`
- **请求参数：**
  - 被投诉者发送给管理员的申诉的消息id (message_id)

- **返回结果：**

  - 是否成功 (success)
  - 消息 (message)
  - 数据 (data)：包括之前处理的投诉（方便管理员回顾事件）和被投诉者申诉的理由
- 返回示例：
```Json
{

      "success": true,
      "message": "获取申诉信息成功",
      "data": {
            "complaint": {
                  "id": 6,
                  "complainer": "sivenlu",
                  "complained": "xht",
                  "content": "歌词不符合核心价值观",
                  "object_type": "song",
                  "object_id": 5,
                  "complaint_date": "2024-05-15T12:06:31.788"
            },
            "reason": "#$@!%……哪里不符合核心价值观了！",
            "date": "2024-05-15T12:30:42.166"
      }
}
```

### （管理员）处理申诉

- **请求类型：** POST
- **URL：** `/complaints/appeals/handle`
- **请求参数：**
  - 被投诉者发送给管理员的申诉的消息id (message_id)
  - 是否恢复(is_recover)
  - 理由(reason)

- **返回结果：**

  - 是否成功 (success)
  - 消息 (message)
- 返回示例：
```Json
{
      "success": true,
      "message": "处理申诉成功"
}
```



## 特性接口

### 用户播放列表
#### 获取用户最近播放
- **请求类型：** GET

- **URL：** `feature/recent`

- **请求参数：**

  - 返回的歌曲数量(num) 可选 默认为10首，如果是-1则返回所有播放记录

- **返回结果：**
  - 是否成功 (success)：表示获取是否成功
  - 消息 (message)：结果消息
  - 返回用户播放列表，按照最近播放时间先后排序
  - 返回参数中的last\_play是最近播放时间，play\_count是播放次数
  
- 返回示例：（因篇幅限制只作参考）

  ```json
  http://127.0.0.1:8000/feature/recent?username=yy5
  ```

  ```json
  {
      "success": true,
      "message": "查询最近播放歌曲成功",
      "data": [
          {
              "song": {
                  "id": 6,
                  "title": "海阔天空",
                  "singer": "beyond",
                  "cover": "http://127.0.0.1:8000/media/covers/%E6%B5%B7%E9%98%94%E5%A4%A9%E7%A9%BA.jpg",
                  "gradient": "background: rgb(201, 126, 80);background: linear-gradient(135deg, rgb(177, 109, 76), rgb(137, 103, 177));",
                  "introduction": null,
                  "audio": "http://127.0.0.1:8000/media/audios/%E6%B5%B7%E9%98%94%E5%A4%A9%E7%A9%BA.mp3",
                  "duration": "324.825124",
                  "lyric": null,
                  "tag_theme": null,
                  "tag_scene": null,
                  "tag_mood": null,
                  "tag_style": null,
                  "tag_language": null,
                  "uploader": "yy5",
                  "like": 0,
                  "upload_date": "2024-04-23 18:38:14"
              },
              "last_play": "2024-04-26 10:16:45",
              "play_count": 3
          }
      ]
  }
  ```

#### 添加最近播放歌曲
- **请求类型：** POST

- **URL：** `feature/addrecent`

- **请求参数：**

  - 歌曲id(song\_id）必填

- **返回结果：**
  - 是否成功 (success)：表示添加是否成功
  - 消息 (message)：添加过程的结果消息
  
- 返回示例：（因篇幅限制只作参考）

  ```json
  {
      "success": true,
      "message": "添加最近播放成功"
  }
  ```

#### 删除最近播放歌曲
- **请求类型：** DELETE
- **URL：** `feature/delrecent`
- **请求参数：**
  - 歌曲id(song\_id) 必填
- **返回结果：**
  - 是否成功 (success)：表示删除是否成功
  - 消息 (message)：删除过程的结果消息
### 热门歌单
- **请求类型：** GET
- **URL：** `feature/hotsonglists`
- **请求参数：**

  - 需要的数量(num) 可选，默认为10首
- **返回结果：**
  - 是否成功 (success)：表示获取是否成功
  - 消息 (message)：获取过程的结果消息
  - 返回喜欢数量排名前十的歌单
- 返回示例：（因篇幅限制只作参考）

  ```json
  {
      "success": true,
      "message": "获取成功",
      "data": [
          {
              "id": 5,
              "title": "yy的中文歌单",
              "cover": "http://182.92.100.66:5000/media/covers/yy_e.jpg",
              "owner": "yy",
              "create_date": "2024-04-22 19:58:42",
              "like": 2
          },
          {
              "id": 7,
              "title": "测试",
              "cover": "http://182.92.100.66:5000/media/covers/abc.jpg",
              "owner": "yees",
              "create_date": "2024-04-22 22:13:40",
              "like": 1
          },
          {
              "id": 27,
              "title": "zys的韩文歌单",
              "cover": "http://182.92.100.66:5000/media/covers/Doom-at-your-service-tvn-2021-8.jpg",
              "owner": "yees",
              "create_date": "2024-05-02 09:37:08",
              "like": 1
          },
          {
              "id": 2,
              "title": "sivenlu的流行音乐歌单",
              "cover": "http://182.92.100.66:5000/media/covers/songlist_cover.jpg",
              "owner": "sivenlu",
              "create_date": "2024-04-22 19:13:09",
              "like": 0
          },
          {
              "id": 3,
              "title": "sivenlu的纯音乐歌单",
              "cover": "http://182.92.100.66:5000/media/covers/songlist_cover_D0bIRai.jpg",
              "owner": "sivenlu",
              "create_date": "2024-04-22 19:14:03",
              "like": 0
          },
          {
              "id": 6,
              "title": "yy的英文歌单",
              "cover": "http://182.92.100.66:5000/media/covers/yy_c.jpg",
              "owner": "yy",
              "create_date": "2024-04-22 19:59:00",
              "like": 0
          },
          {
              "id": 8,
              "title": "Nzh的民谣",
              "cover": "http://182.92.100.66:5000/media/covers/%E5%B0%81%E9%9D%A2.jpg",
              "owner": "Nzh",
              "create_date": "2024-04-22 23:18:56",
              "like": 0
          },
          {
              "id": 19,
              "title": "zys",
              "cover": "http://182.92.100.66:5000/media/covers/imgPlaylist_LsiJdmP.jpeg",
              "owner": "yees",
              "create_date": "2024-04-27 13:23:45",
              "like": 0
          },
          {
              "id": 20,
              "title": "测试123",
              "cover": "http://182.92.100.66:5000/media/covers/Someone_Like_You-Adele.png",
              "owner": "yees",
              "create_date": "2024-04-27 16:09:45",
              "like": 0
          },
          {
              "id": 23,
              "title": "zys的英文歌单",
              "cover": "http://182.92.100.66:5000/media/covers/moon.jpg",
              "owner": "yees",
              "create_date": "2024-04-29 17:03:45",
              "like": 0
          }
      ]
  }
  ```
### 热门歌曲
- **请求类型：** GET
- **URL：** `feature/hotsongs`
- **请求参数：**

  - 需要的数量(num) 可选，默认为10首
- **返回结果：**
  - 是否成功 (success)：表示获取是否成功
  - 消息 (message)：获取过程的结果消息
  - 返回喜欢数量排名前十的歌曲
- 返回示例：（因篇幅限制只作参考）

  ```json
  http://127.0.0.1:8000/feature/hotsongs?num=2
  ```

  ```json
  {
      "success": true,
      "message": "获取成功",
      "data": [
          {
              "id": 8,
              "title": "betty",
              "singer": "Taylor Swift",
              "cover": "http://127.0.0.1:8000/media/covers/betty_cover.jpg",
              "duration": "294.556734",
              "uploader": "sivenlu",
              "like": 2
          },
          {
              "id": 9,
              "title": "exile",
              "singer": "Taylor Swift",
              "cover": "http://127.0.0.1:8000/media/covers/exile_cover.jpg",
              "duration": "285.634172",
              "uploader": "sivenlu",
              "like": 2
          }
      ]
  }
  ```
