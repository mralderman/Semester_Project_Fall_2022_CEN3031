import PySimpleGUI as sg
import auth


def login_window(window):
    while True:
        window['-LOGIN-'].update(visible=True)
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event in 'Login':
            if auth.login(values['-USER-'], values['-PASS-']):
                values['-USER-'] = ''
                values['-PASS-'] = ''
                window['-LOGIN-'].update(visible=False)
                home_window(window)
            else:
                sg.popup_ok('Error: Incorrect username or password', background_color='#B7CECE', title='Error')
                continue
        elif event in 'Create New User':
            window['-LOGIN-'].update(visible=False)
            new_user_window(window)

    window.close()


def new_user_window(window):
    window['-CREATE-'].update(visible=True)
    while True:
        event, values = window.read()
        window['-CREATE-'].update(visible=False)
        if event == '__TITLEBAR CLOSE__3':
            break
        if event in 'Create':
            if values['-NEW PASS-'] == values['-PASS_CONF-']:
                auth.new_user(values['-NEW USER-'], values['-NEW PASS-'])
            #else:
                #show error and ask again
            # show a success message, return to login_window
            login_window(window)
        if event in 'Cancel':
            login_window(window)
    window.close()


def home_window(window):
    window['-HOME-'].update(visible=True)
    while True:
        event, values = window.read()
        window['-HOME-'].update(visible=False)
        if event == '__TITLEBAR CLOSE__9':
            break
        if event in 'Logout':
            login_window(window)
    window.close()


def window_layouts():
    login_layout = [[sg.Titlebar('Green Foot Forward')],
                    [sg.Text('Welcome to Green Foot Forward!')],
                    [sg.Text('Username:', size=(12, 1)), sg.InputText(key='-USER-', size=(15, 1))],
                    [sg.Text('Password:', size=(12, 1)), sg.InputText(key='-PASS-', size=(15, 1))],
                    [sg.Button('Login'), sg.Button('Create New User')]]

    create_user_layout = [[sg.Titlebar('Create New User')],
                          [sg.Text('Username:', size=(19, 1)), sg.InputText(key='-NEW USER-', size=(15, 1))],
                          [sg.Text('Password:', size=(19, 1)), sg.InputText(key='-NEW PASS-', size=(15, 1))],
                          [sg.Text('Confirm Password:', size=(19, 1)), sg.InputText(key='-PASS_CONF-', size=(15, 1))],
                          [sg.Button('Create'), sg.Button('Cancel')]]

    home_layout = [[sg.Titlebar('Green Foot Forward')],
                   [sg.Text('Main menu goes here. Also, authentication needs to be plugged in.')],
                   [sg.Button('Logout')]]

    layouts = [[sg.Column(login_layout, key='-LOGIN-', visible=False),
                sg.Column(create_user_layout, key='-CREATE-', visible=False),
                sg.Column(home_layout, key='-HOME-', visible=False)]]

    return layouts


def init():
    sg.theme('LightGreen')
    sg.Titlebar(title='Green Foot Forward')

    main_window = sg.Window('Green Foot Forward', window_layouts(), finalize=True)
    login_window(main_window)


init()

