import PySimpleGUI as sg
import config


def get_new_data():
    """
    Get unlabelled data from mongoDB instance
    """
    return config.collection.find({"label": {"$nin": ['none', 'astroturf']}})


def update_layout(tweet, window):
    for field_name in config.tweet_schema:
        window.Element(field_name).update(tweet[field_name])


def gui_loop(tweet_data):
    """
    Display the GUI, update/save on advance and quit
    """
    layout = []
    for field_name in config.tweet_schema:
        layout.append([sg.Text(field_name), sg.Text('', key=field_name, size=(50, 3), justification='center')])
    layout.append([sg.Frame(layout=[
            [sg.Radio('None', group_id='label', key='none_label', default=True),
             sg.Radio('Astroturf', group_id='label', key='ast_label')]
        ], title='Choose label', relief=sg.RELIEF_GROOVE)])
    layout.append([sg.Button('Next'), sg.Exit()])

    window = sg.Window('Simple Label Maker', layout, grab_anywhere=False).Finalize()

    current = 0
    while True:
        if current >= tweet_data.count():
            break
        update_layout(tweet_data[current], window)
        event, values = window.Read()
        if event is None or event == 'Exit':
            break
        elif event == 'Next':
            new_label = 'none' if values['none_label'] else 'astroturf'
            config.collection.update_one({"_id": tweet_data[current]['_id']}, {'$set': {'label': new_label}})
            current += 1

    window.Close()


def setup():
    """
    Start the loop
    """
    gui_loop(get_new_data())


setup()
