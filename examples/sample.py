from whatsapphero import WhatsappHero
hero = WhatsappHero(headless= True)
hero.login()
while True:
    time.sleep(10)
    unread_contacts = hero.get_unread_message_contact_list()
    for contact in unread_contacts:
        contact.click()
        unread_messages = hero.get_unread_messages_of_contact()
        hero.reply_to_contact('Hey There')
        
    # temp fix click on last chat contact to not automatically remove the notification batch
    all_chat_contacts = hero.get_all_chat_contact_list()
    if len(all_chat_contacts):
        all_chat_contacts[1].click()
