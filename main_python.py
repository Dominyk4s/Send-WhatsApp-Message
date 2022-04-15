import whatsapp_chrome_handler as wa
import parameters as param
import pandas as pd
import time


def generate_messages(row, text_message_form):
    text_messages = []
    try:
        for message in text_message_form:
            text_messages.append(message.format(**row))
    except:
        print('LT: Patikrink, ar duomenų faile yra visi tekste nurodyti stulpeliai, kuriuos nori naudoti žinutėje')
        print('EN: Check if there are no missing columns from text input string in data file')
        # sys.exit(1)
    return text_messages


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Reading Data
    df = pd.read_csv(param.FILE_PATH)
    df.drop_duplicates(subset=[param.PHONE_COLUMN], inplace=True)  # Removing duplicates if phone number repeats
    if param.SELECT_RANDOM:
        df = df.sample(n=param.RANDOM_COUNT)
    df = df.fillna(value='')  # Filling na not to show "None" in text messages (shows '' instead)

    # Overwrite phone number if you want to test in on your phone number or any other single phone number:
    df[param.PHONE_COLUMN]=37060034020

    # Generating message text as pandas column
    messages = []
    df['message_to_send'] = ''
    for index, row in df.iterrows():
        message = generate_messages(row=row, text_message_form=param.text_message_form)
        df.at[index, 'message_to_send'] = message

    # Getting driver (opening browser)
    driver = wa.get_driver()

    # Logging in to WhatsApp
    wa.login(driver)
    print('LT: Nuskenuokite QR kodą, prisijungus spauskinte "Enter"')
    print('EN: Login by scanning QR Code, and press Enter')
    input()
    print('Prisijungta prie WhatsApp/Logged in to WhatsApp')
    time.sleep(3)

    # Sending messages to all people from the file
    for index, row in df.iterrows():
        wa.get_contact_compose_and_send(phone=df.at[index, param.PHONE_COLUMN], driver=driver,
                                        text_messages=df.at[index, 'message_to_send'])
        print('Išsiųstos visos žinutės kontaktui/Finished with contact')

    # Exiting Chrome:
    driver.quit()
