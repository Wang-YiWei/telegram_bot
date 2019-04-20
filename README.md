# telegram-bot

## 主題：排隊免等小幫手

## 欲解決問題：
常常我們去看診或是買東西的時候，前面在排隊的人也很多，這時候我們可能想暫時離開做其他事情，等到快輪到我的時候再回來。因此我們可能會詢問：「大概還要多久才會輪到我？」，通常得到的回覆大概都是：「不好意思今天客人很多，要等多久不一定哦！」。因此我想透過實做一個能讓顧客知道目前的排隊進度的聊天機器人。

## 開發工具：
* telegram bot
* ngrok
* transitions
* python3
* MySQL

## 概念：
#### 店家端
1. 店家可透過輸入密碼進行登入
2. 登入之後有兩種按鈕
    - 下一位:當店家完成一個客人的訂單，按一下。（counter++）
    - 重設號碼: 設定從幾號開始計數（reset counter）
#### 客戶端：
1. 選擇店家所在城市
2. 選擇店家
3. 顧客選完店家後，便可知道現在的排隊進度（show counter）
 
## 狀態圖：
![](https://i.imgur.com/2doLpAn.png)

### 備註：
目前的還沒想到比較公平，安全的註冊方式，因此註冊按鈕尚無功能！

## 作者
[Lee-W](https://github.com/Lee-W)、[yiwei01](https://github.com/yiwei01)