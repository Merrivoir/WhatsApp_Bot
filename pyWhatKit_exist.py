import pywhatkit
numbers = ["+77757468937", "+77474728450"]

group_id = ''

message = f"""*Хочешь путешествовать, создавать авторские туры и при этом зарабатывать? 🌍✈️*
🎯Мечтаешь о жизни, где каждое путешествие приносит доход?
💰 Мы запускаем закрытый чат для тех, кто хочет не просто путешествовать, но и строить прибыльный бизнес на этом!

*Присоединяйся к нам, узнавай секреты заработка на путешествиях и открывай для себя новые горизонты. 🚀✨*
https://chat.whatsapp.com/BXfnpMNOHoW5vF8xg614eO
Перейди в чат прямо сейчас и начни свое путешествие к успеху! 🌟
Если ссылка неактивна напиши слово *ОК* в ответ на это смс"""

waiting_time_to_send = 15
close_tab = True
waiting_time_to_close = 4
mode = "contact"

for number in numbers:
    if pywhatkit.open_web():
        print("WhatsApp open")
        pywhatkit.sendwhatmsg_instantly(number, message, waiting_time_to_send, close_tab, waiting_time_to_close)
    else:
        print("Error code: 97654")
        print("Error Message: Please select a mode to send your message.")