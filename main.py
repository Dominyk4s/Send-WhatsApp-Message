from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

import parameters as params
import whatsapp_chrome_handler as wa

import pandas as pd

FILE_PATH = params.FILE_PATH
SELECT_RANDOM = params.SELECT_RANDOM
RANDOM_COUNT = params.RANDOM_COUNT
text_message_form = params.text_message_form
PHONE_COLUMN = params.PHONE_COLUMN
df = pd.DataFrame()
driver = ''


## THE BUILDER HAS THE CODE THAT DEFINES THE APPEARANCE OF THE APP. IT IS THE KIVY CODE
# Builder.load_file('padekimukrainai.kv')

## THIS PART IS THE PYTHON CODE


def generate_messages(row, form):
    text_messages = []
    try:
        for message in form:
            text_messages.append(message.format(**row))
    except:
        print('LT: Patikrink, ar duomenų faile yra visi tekste nurodyti stulpeliai, kuriuos nori naudoti žinutėje')
        print('EN: Check if there are no missing columns from text input string in data file')
        # sys.exit(1)
    return text_messages


def read_file():
    global FILE_PATH
    return pd.read_csv(FILE_PATH)


def data_pipeline(df):
    global PHONE_COLUMN
    global SELECT_RANDOM
    global RANDOM_COUNT

    df.drop_duplicates(subset=[PHONE_COLUMN], inplace=True)  # Removing duplicates if phone number repeats
    #try:
    if int(RANDOM_COUNT) > 0:
        if SELECT_RANDOM:
            df = df.sample(n=int(RANDOM_COUNT))
            print('Selected random')
        else:
            df = df.head(int(RANDOM_COUNT))
            print('Selected sample')
    #except:
    #    print('Did not select data subset')
    df = df.fillna(value='')  # Filling na not to show "None" in text messages (shows '' instead)
    return df


class Parameters(Screen):
    # Controls the visibility of fields based on send random checkmark
    random_label = ObjectProperty(None)
    random_input = ObjectProperty(None)


class Parameters2(Screen):
    def on_enter(self, *args):
        global FILE_PATH
        global SELECT_RANDOM
        global RANDOM_COUNT
        FILE_PATH = self.manager.ids.parameters.ids.FILE_PATH_ID.text
        SELECT_RANDOM = self.manager.ids.parameters.ids.SELECT_RANDOM_ID.active
        RANDOM_COUNT = self.manager.ids.parameters.ids.RANDOM_COUNT_ID.text
        try:
            df_temp = pd.read_csv(FILE_PATH)
            self.df_columns.text = str(df_temp.columns)
        except:
            self.df_columns.text = 'KLAIDA: Nepavyko nuskaityti duomenų failo'

class ReadyToSend(Screen):
    def on_enter(self, *args):
        global FILE_PATH
        global SELECT_RANDOM
        global RANDOM_COUNT
        global text_message_form
        global PHONE_COLUMN

        # Assigning global parameters from Parameters2 window
        PHONE_COLUMN = self.manager.ids.parameters2.ids.PHONE_COLUMN.text
        text_message_form = [self.manager.ids.parameters2.ids.text_message_form_1.text, self.manager.ids.parameters2.ids.text_message_form_2.text, self.manager.ids.parameters2.ids.text_message_form_3.text]
        print(text_message_form)


class ScreenManagement(ScreenManager):
    pass


class SlavaUkrainaApp(App):
    global df

    def login(self):
        global driver
        global FILE_PATH

        global driver
        global PHONE_COLUMN
        global text_message_form
        global df

        print('Inside login: ' + FILE_PATH)


        df = read_file()
        df = data_pipeline(df)

        # In case of testing, overwrites all the numbers
        #df[PHONE_COLUMN] = 37060000000

        driver = wa.get_driver()
        # Logging in to WhatsApp
        wa.login(driver)

        # Generating message text as pandas column
        # messages = []
        df['message_to_send'] = ''
        for index, row in df.iterrows():
            message = generate_messages(row=row, form=text_message_form)
            df.at[index, 'message_to_send'] = message

    def get_contact_compose_and_send(self):
        # Sending messages to all people from the file
        for index, self.row in df.iterrows():
            try:
                # message = generate_messages(row=row, text_message_form=text_message_form)
                wa.get_contact_compose_and_send(phone=df.at[index, PHONE_COLUMN], driver=driver,
                                                # text_messages=message
                                                text_messages=df.at[index, 'message_to_send']
                                                )
            except:
                print('Nepavyko išsiųsti žinutės numieriui: ' + str(df.at[index, PHONE_COLUMN]))
                continue
            print('Issiustos visos zinutes kontaktui/Finished with contact')

    def build(self):
        return ScreenManagement()


if __name__ == '__main__':
    SlavaUkrainaApp().run()
