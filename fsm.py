from transitions.extensions import GraphMachine
import telegram
import pymysql

current_shop = ''
verify_flag = 0

def update_data_of_db(query_name,new_num,isNext):
    # Open database connection
    db = pymysql.connect("localhost","chatbot","chatbot","BOTDB" )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to UPDATE required records
    if isNext:
        sql = "UPDATE shops SET counter = counter + 1 \
                            WHERE name = '%s'" % (query_name)
       
    else:
        sql = "UPDATE shops SET counter = '%d' \
                            WHERE name = '%s'" % (new_num,query_name)
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

    # disconnect from server
    db.close()

def read_data_from_db(update,query_name):
    db = pymysql.connect("localhost","chatbot","chatbot","BOTDB" )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

        # Prepare SQL query to INSERT a record into the database.
    sql = "SELECT * FROM shops \
        WHERE name = '%s'" %(query_name)
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        for row in results:
            theid = row[0]
            name = row[1]
            passwd = row[2]
            count = row[3]
            # Now print fetched result
            print ("theid = %d,name = %s,passwd = %d,count = %d" % \
                    (theid, name, passwd, count))
            
            update.message.reply_text('目前號碼： %d' %count)
    except:
        print ("Error: unable to fetch data")
    # disconnect from server
    db.close()

def read_data_on_verify(update,bot,chat_id,query_name):
    db = pymysql.connect("localhost","chatbot","chatbot","BOTDB" )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "SELECT * FROM shops \
        WHERE name = '%s'" %(query_name)
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        for row in results:
            theid = row[0]
            name = row[1]
            passwd = row[2]
            count = row[3]
            # Now print fetched result
            print ("theid = %d,name = %s,passwd = %d,count = %d" % \
                    (theid, name, passwd, count))
            custom_keyboard = [['下一位','重設號碼']]
            reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
            bot.send_message(chat_id=chat_id, text='目前號碼：%d' %count,reply_markup=reply_markup)
            # update.message.reply_text('目前號碼： %d' %count)
    except:
        print ("Error: unable to fetch data")

    # disconnect from server
    db.close()

def verify_from_db(update,query_passwd):
    global current_shop
    global verify_flag
    db = pymysql.connect("localhost","chatbot","chatbot","BOTDB" )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "SELECT * FROM shops \
       WHERE passwd = '%s'" %(query_passwd)
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        for row in results:
            theid = row[0]
            name = row[1]
            current_shop = row[1]
            passwd = row[2]
            count = row[3]
            # Now print fetched result
            print ("current_shop = %s" %current_shop)
            update.message.reply_text('歡迎回來： %s' %current_shop)
            verify_flag = 1
    except:
        verify_flag = 0
        print ("Error: unable to fetch data2")

    # disconnect from server
    db.close()


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    def go_back_to_user(self, update,bot,chat_id):
        text = update.message.text
        return text.lower() == 'exit'

    def reset_done(self,update,bot,chat_id):
        text = update.message.text
        if text.isdigit():
            update_data_of_db(current_shop,int(text),0)
            return True
        else:
            update.message.reply_text("請輸入純數字")
            print('non-digit-input')
            return False
            
    # --- boring
    def is_going_to_boring(self, update,bot,chat_id):
        text = update.message.text
        return text.lower() == '3'

    # --- customer side

    # def is_going_to_user(self, update,bot,chat_id):
    #     text = update.message.text
    #     return True

    def is_going_to_customer(self, update,bot,chat_id):
        text = update.message.text
        return text.lower() == '1'

    def is_going_to_Taipei(self, update,bot,chat_id):
        text = update.message.text
        return text == '臺北'
    
    def is_going_to_Taichung(self, update,bot,chat_id):
        text = update.message.text
        return text == '臺中'

    def is_going_to_Tainan(self, update,bot,chat_id):
        text = update.message.text
        return text == '臺南'
    
    # --- shops

    def is_going_to_subway(self, update,bot,chat_id):
        text = update.message.text
        return text == '1'

    def is_going_to_donut(self, update,bot,chat_id):
        text = update.message.text
        return text == '2'

    def is_going_to_tasty(self, update,bot,chat_id):
        text = update.message.text
        return text == '1'

    def is_going_to_mcdonald(self, update,bot,chat_id):
        text = update.message.text
        return text == '2'

    def is_going_to_doublecheese(self, update,bot,chat_id):
        text = update.message.text
        return text == '1'

    def is_going_to_burgerking(self, update,bot,chat_id):
        text = update.message.text
        return text == '2'

    def is_going_to_check(self, update,bot,chat_id):
        text = update.message.text
        return text == '再次查詢'


    # --- owner side

    def is_going_to_owner(self, update,bot,chat_id):
        text = update.message.text
        return text.lower() == '2'

    def is_going_to_login(self, update,bot,chat_id):
        text = update.message.text
        return text.lower() == '登入'

    def is_going_to_signup(self, update,bot,chat_id):
        text = update.message.text
        return text.lower() == '新註冊'

    def is_going_to_verify(self, update,bot,chat_id):
        
        # global whichshop
        global verify_flag
        text = update.message.text
        verify_from_db(update,text)
        if verify_flag == 1:
            return True
        else:
            return False 

    def is_going_to_next(self, update,bot,chat_id):
        text = update.message.text
        return text == '下一位'

    def is_going_to_reset(self, update,bot,chat_id):
        text = update.message.text
        return text == '重設號碼'

    # --- select the customer or owner

    def on_enter_user(self, update,bot,chat_id):
        reply_markup = telegram.ReplyKeyboardRemove()
        bot.send_message(chat_id=chat_id, text="歡迎使用排隊小幫手！\n如果您是消費者請輸入 <b>1</b>\n如果您是店家請輸入 <b>2</b>\n如果您很無聊請輸入 <b>3</b>\n接下來每個步驟都將有指引!\n(在任何時候輸入<b> exit </b>可回到起始畫面)", parse_mode=telegram.ParseMode.HTML , reply_markup=reply_markup)

    def on_enter_boring(self, update,bot,chat_id):
        reply_markup = telegram.ReplyKeyboardRemove()
        bot.send_photo(chat_id=chat_id, photo=open('img/taiwanstat.png', 'rb'))
        bot.send_message(chat_id=chat_id, text="如果有空，這裡提供個窗口讓您更認識台灣\nhttps://www.taiwanstat.com/", disable_web_page_preview = False,reply_markup=reply_markup)

    def on_exit_boring(self, update,bot,chat_id):
        print('Leaving boring')

    def on_enter_customer(self, update,bot,chat_id):
        update.message.reply_text("親愛的顧客您好")
        custom_keyboard = [['臺北','臺中','臺南']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="請選擇店家所在城市：", reply_markup=reply_markup)
    
    def on_exit_customer(self, update,bot,chat_id):
        reply_markup = telegram.ReplyKeyboardRemove()
        bot.send_message(chat_id=chat_id, text="選定成功！", reply_markup=reply_markup)
        print('Leaving customer')

    def on_enter_owner(self, update,bot,chat_id):
        update.message.reply_text("親愛的店家您好")
        custom_keyboard = [['登入','新註冊']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="請選擇功能：", reply_markup=reply_markup)

    def on_exit_owner(self, update,bot,chat_id):
        reply_markup = telegram.ReplyKeyboardRemove()
        bot.send_message(chat_id=chat_id, text="選定成功！", reply_markup=reply_markup)
        print('Leaving owner')


    # --- select the city

    def on_enter_Taipei(self, update,bot,chat_id):
        update.message.reply_text("以下是台北可選擇店家！\n1. subway\n2. donut \n請輸入數字以選擇店家")

    def on_exit_Taipei(self, update,bot,chat_id):
        print('Leaving Taipei')

    def on_enter_Taichung(self, update,bot,chat_id):
        update.message.reply_text("以下是台中可選擇店家！\n1. 西堤牛排\n2.麥當勞 \n請輸入數字以選擇店家")

    def on_exit_Taichung(self, update,bot,chat_id):
        print('Leaving Taichung')

    def on_enter_Tainan(self, update,bot,chat_id):
        update.message.reply_text("以下是台南可選擇店家！\n1. Double cheese\n2.漢堡王 \n請輸入數字以選擇店家")

    def on_exit_Tainan(self, update,bot,chat_id):
        print('Leaving Tainan')

    # --- select login or sign up

    def on_enter_login(self, update,bot,chat_id):
        update.message.reply_text("請輸入密碼：")

    def on_exit_login(self, update,bot,chat_id):
        update.message.reply_text("登入成功！")

    def on_enter_signup(self, update,bot,chat_id):
        update.message.reply_text("請到以下連結申請：")

    def on_exit_signup(self, update,bot,chat_id):
        update.message.reply_text("離開註冊")

    # --- next or reset number

    def on_enter_verify(self,update,bot,chat_id):
        read_data_on_verify(update,bot,chat_id,current_shop)

    def on_enter_next(self, update,bot,chat_id):
        update_data_of_db(current_shop,0,1)
        self.go_back(update,bot,chat_id)

    def on_exit_next(self, update,bot,chat_id):
        print("離開next")

    def on_enter_reset(self, update,bot,chat_id):
        reply_markup = telegram.ReplyKeyboardRemove()
        bot.send_message(chat_id=chat_id, text="請重設您的號碼：", reply_markup=reply_markup)

    def on_exit_reset(self, update,bot,chat_id):
        print("離開reset")

    def on_enter_resetnum(self, update,bot,chat_id):
        update.message.reply_text("重設成功！")
        self.go_back_from_reset(update,bot,chat_id)

    def on_exit_resetnum(self, update,bot,chat_id):
        print("離開resetnum")

    # --- shop

    def on_enter_subway(self, update,bot,chat_id):
        custom_keyboard = [['再次查詢']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="為您查看subway排隊進度！", reply_markup=reply_markup)
        # update.message.reply_text("為您查看subway排隊進度！")
        read_data_from_db(update,"subway")

    def on_exit_subway(self, update,bot,chat_id):
        print("離開subway")

    def on_enter_donut(self, update,bot,chat_id):
        custom_keyboard = [['再次查詢']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="為您查看donut排隊進度！", reply_markup=reply_markup)
        #update.message.reply_text("為您查看donut排隊進度！")
        read_data_from_db(update,"donut")

    def on_exit_donut(self, update,bot,chat_id):
        print("離開donut")

    def on_enter_tasty(self, update,bot,chat_id):
        custom_keyboard = [['再次查詢']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="為您查看西堤牛排排隊進度！", reply_markup=reply_markup)
        #update.message.reply_text("為您查看西堤牛排排隊進度！")
        read_data_from_db(update,"tasty")

    def on_exit_tasty(self, update,bot,chat_id):
        print("離開tasty")

    def on_enter_mcdonald(self, update,bot,chat_id):
        custom_keyboard = [['再次查詢']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="為您查看麥當勞排隊進度！", reply_markup=reply_markup)
        #update.message.reply_text("為您查看麥當勞排隊進度！")
        read_data_from_db(update,"mcdonald")

    def on_exit_mcdonald(self, update,bot,chat_id):
        print("離開mcdonald")

    def on_enter_doublecheese(self, update,bot,chat_id):
        custom_keyboard = [['再次查詢']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="為您查看Double cheese排隊進度！", reply_markup=reply_markup)
        #update.message.reply_text("為您查看Double Cheese排隊進度！")
        read_data_from_db(update,"doublecheese")

    def on_exit_doublecheese(self, update,bot,chat_id):
        print("離開doublecheese")

    def on_enter_burgerking(self, update,bot,chat_id):
        custom_keyboard = [['再次查詢']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="為您查看漢堡王排隊進度！", reply_markup=reply_markup)
        #update.message.reply_text("為您查看漢堡王排隊進度！")
        read_data_from_db(update,"burgerking")

    def on_exit_burgerking(self, update,bot,chat_id):
        print("離開burgerking")

    def on_enter_subwaycheck(self, update,bot,chat_id):
        self.go_back_to_subway(update,bot,chat_id)

    def on_enter_donutcheck(self, update,bot,chat_id):
        self.go_back_to_donut(update,bot,chat_id)
    
    def on_enter_tastycheck(self, update,bot,chat_id):
        self.go_back_to_tasty(update,bot,chat_id)

    def on_enter_mcdonaldcheck(self, update,bot,chat_id):
        self.go_back_to_mcdonald(update,bot,chat_id)

    def on_enter_doublecheesecheck(self, update,bot,chat_id):
        self.go_back_to_doublecheese(update,bot,chat_id)

    def on_enter_burgerkingcheck(self, update,bot,chat_id):
        self.go_back_to_burgerking(update,bot,chat_id)
