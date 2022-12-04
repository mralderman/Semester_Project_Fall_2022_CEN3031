import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import auth
import data

def login_window(window) -> None:
    while True:
        window['-LOGIN-'].update(visible=True)
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break

        # User clicks Login
        elif event in 'Login':

            # Credentials are valid
            if auth.login(values['-USER-'], values['-PASS-']):
                curr_user_id: str = values['-USER-']
                window['-LOGIN-'].update(visible=False)
                home_window(window, curr_user_id)

            # Credentials are invalid
            else:
                sg.popup_ok('Incorrect username or password.', 'Please try again.',
                            background_color='#B7CECE', title='Error')
                continue

        # User clicks Create New User
        elif event in 'Create New User':
            window['-LOGIN-'].update(visible=False)
            new_user_window(window)
    window.close()
    exit(0)

def new_user_window(window) -> None:
    while True:
        window['-CREATE-'].update(visible=True)
        event, values = window.read()
        if event == '__TITLEBAR CLOSE__3':
            break

        # User clicks Create
        elif event in 'Create':
            user_created = auth.new_user(values['-NEW-USER-'], values['-NEW-PASS-'], values['-PASS-CONF-'])

            # Username is taken
            if user_created == auth.NewUserOptions.USER_EXISTS:
                sg.popup_ok('This username is already in use.', 'Please try again.',
                            background_color='#B7CECE', title='Error')
                continue

            # Passwords don't Match
            elif user_created == auth.NewUserOptions.PAS_MISMATCH:
                sg.popup_ok('The passwords you entered do not match.', 'Please try again.',
                            background_color='#B7CECE', title='Error')
                continue

            # Username is blank
            elif user_created == auth.NewUserOptions.BLANK_USER:
                sg.popup_ok('User name cannot be blank.', 'Please try again.',
                            background_color='#B7CECE', title='Error')
                continue

            # Successful User Creation
            elif user_created == auth.NewUserOptions.USER_CREATED:
                sg.popup('New user created successfully', background_color='#B7CECE', title='Success')
                window['-CREATE-'].update(visible=False)
                login_window(window)

        # User clicks Cancel
        elif event in 'Cancel':
            window['-CREATE-'].update(visible=False)
            login_window(window)
    window.close()
    exit(0)

# Define list of default activities
activities_list = [key for key in data.activities_templates.keys()]
activities_list.insert(0, 'Add new activity')

def home_window(window: sg.Window, curr_user_id: str) -> None:
    for key in data.users[curr_user_id].custom_activities.keys():
        activities_list.append(key)

    table_data: list[list[int, str, str]] = []
    ranked_users = dict(sorted(data.users.items(), key=lambda x: x[1].grand_total, reverse=True))
    i = 1
    for user in ranked_users.values():
        if user.private == False:
            temp = [i, user.user_id, user.grand_total]
            i += 1
            table_data.append(temp)
    window['-RANKING-'].update(table_data)

    while True:
        window['-HOME-'].update(visible=True)
        window['-OUTPUT-'].update(data.users[curr_user_id].grand_total)
        event, values = window.read()
        values['grandTotal'] = data.users[curr_user_id].grand_total

        if event == '__TITLEBAR CLOSE__7':
            break

        # User Clicks Logout
        elif event == 'Logout':
            window['-HOME-'].update(visible=False)
            login_window(window)

        # User Clicks Add Activity
        elif event == 'Add Activity':
            if values['dropDown'] in data.activities_templates.keys():
                try:
                    data.users[curr_user_id].add_activity(curr_user_id, values['dropDown'], data.activities_templates[values['dropDown']][0], int(values['-IN-']))
                    new_table_data: list[list[int, str, str]] = []
                    i = 1
                    for user in ranked_users.values():
                        if user.private == False:
                            temp = [i, user.user_id, user.grand_total]
                            i += 1
                            new_table_data.append(temp)
                    window['-RANKING-'].update(new_table_data)

                except:
                    sg.popup_ok('Inncorrect Value', 'Please try again.',
                            background_color='#B7CECE', title='Error')
                continue
            else:
                data.users[curr_user_id].add_activity(curr_user_id, values['dropDown'], data.users[curr_user_id].custom_activities[values['dropDown']][0], int(values['-IN-']))    
            window['-OUTPUT-'].update(data.users[curr_user_id].grand_total)

        # User Clicks Create Activity
        elif event == 'Create Activity':
            try:
                data.create_custom_activity_template(curr_user_id, (values['-NAME-']), float(values['-RATE-']))
                activities_list.append((values['-NAME-']))
                window['dropDown'].update(values=activities_list)
            except:
                sg.popup_ok('Inncorrect Value', 'Please try again.',
                        background_color='#B7CECE', title='Error')
            continue

        # User clicks Compare
        #   uses the current row selected from the table to output two bar charts displaying the ammounts
        #   of the top 3 user and comparison user activities.
        #   if a user is not selected, an error message it displayed
        elif event == 'Compare':
            try:
                currUser = data.get_user(curr_user_id) 
                compUser = data.get_user(table_data[values['-RANKING-'][0]][1])
                drawPlot(currUser, compUser)
            except:
                sg.popup_ok('Please select a user', 'Please try again.')
            continue

        # User Clicks Hide data
        elif event == 'Hide Data':
            data.users[curr_user_id].privacy_on()
            new_table_data: list[list[int, str, str]] = []
            i = 1
            for user in ranked_users.values():
                if user.private == False:
                    temp = [i, user.user_id, user.grand_total]
                    i += 1
                    new_table_data.append(temp)
            window['-RANKING-'].update(new_table_data)            
            continue

        # User Clicks Show data
        elif event == 'Show Data':
            data.users[curr_user_id].privacy_off()
            new_table_data: list[list[int, str, str]] = []
            i = 1
            for user in ranked_users.values():
                if user.private == False:
                    temp = [i, user.user_id, user.grand_total]
                    i += 1
                    new_table_data.append(temp)
            window['-RANKING-'].update(new_table_data)   
        continue
    exit(0)


def make_window():
    sg.theme('LightGreen')
    sg.Titlebar(title='Green Foot Forward')

    # Login window template
    login_layout = [[sg.Titlebar('Green Foot Forward')],
                    [sg.Text('Welcome to Green Foot Forward!')],
                    [sg.Text('Username:', size=(12, 1)), sg.InputText(key='-USER-', size=(15, 1), do_not_clear=False)],
                    [sg.Text('Password:', size=(12, 1)), sg.InputText(key='-PASS-', size=(15, 1), do_not_clear=False)],
                    [sg.Button('Login'), sg.Button('Create New User')]]

    # Create New User window template
    create_user_layout = [[sg.Titlebar('Create New User')],
                          [sg.Text('Username:', size=(19, 1)),
                           sg.InputText(key='-NEW-USER-', size=(15, 1), do_not_clear=False)],
                          [sg.Text('Password:', size=(19, 1)),
                           sg.InputText(key='-NEW-PASS-', size=(15, 1), do_not_clear=False)],
                          [sg.Text('Confirm Password:', size=(19, 1)),
                           sg.InputText(key='-PASS-CONF-', size=(15, 1), do_not_clear=False)],
                          [sg.Button('Create'), sg.Button('Cancel')]]

    #   This section generates a 2-D List of the data that goes in the table
    headings = ['Rank', 'User', 'Total (kg)']

    # Home window template
    home_layout = [[sg.Titlebar('Green Foot Forward')],
                   [sg.Text('Choose an activity'),  sg.Combo(values=activities_list, enable_events=True, key='dropDown'),
                    sg.Text('Amount: ', key='-AMOUNT-'),  sg.Input(key='-IN-', size=(15,1)), sg.Button('Add Activity')],
                   [sg.Text('Name: '), sg.Input(key='-NAME-', size=(20, 1)), sg.Text('Carbon Saved per Unit (kg): '), sg.Input(key='-RATE-', size=(10, 1)), sg.Button('Create Activity')],
                   [sg.Text('Your total carbon reduction:'), sg.Text(key='-OUTPUT-'), sg.Text('kg')],
                   [sg.Text('Public Ranking Table:')],
                   [sg.Button('Hide Data'), sg.Button('Show Data'), sg.Button('Compare')],
                   [sg.Table(values=[[]], headings=headings, 
                            enable_events=True, 
                            # enable_click_events= True,
                            selected_row_colors='red on yellow', 
                            key='-RANKING-'), 
                    sg.Graph(key = 'User Graph',canvas_size=(3,3),graph_bottom_left=any,graph_top_right=any)],
                   [sg.Button('Logout')]]

    layouts = [[sg.Column(login_layout, key='-LOGIN-', visible=False),
                sg.Column(create_user_layout, key='-CREATE-', visible=False),
                sg.Column(home_layout, key='-HOME-', visible=False)]]

    window = sg.Window('Green Foot Forward', layouts, grab_anywhere=True, resizable=True, finalize=True)
    return window

def drawPlot(currUser: data.User, compUser: data.User):

        tempDictUser: dict(str, int) = {}
        for activity in currUser.activities:
            if (activity.name in tempDictUser):
                tempDictUser[activity.name] = tempDictUser[activity.name] + activity.amount
            else:
                tempDictUser[activity.name] = activity.amount

        tempDictComp: dict(str, int) = {}
        for activity in compUser.activities:
            if (activity.name in tempDictComp):
                tempDictComp[activity.name] = tempDictComp[activity.name] + activity.amount
            else:
                tempDictComp[activity.name] = activity.amount

        tempDictUserTwo = sorted(tempDictUser.items(), key=lambda x:x[1],reverse=True)
        tempDictCompTwo = sorted(tempDictComp.items(), key=lambda x:x[1],reverse=True)

        tempDictUserFinal = dict(tempDictUserTwo[0:3])    
        tempDictCompFinal = dict(tempDictCompTwo[0:3])

        userYvalues = []
        compYvalues = []
        
        for values in tempDictUserFinal.values():
            userYvalues.append(values)

        for values in tempDictCompFinal.values():
            compYvalues.append(values)


        if (len(userYvalues) < 3):
            userYvaluesLen = 3 - len(userYvalues)
            i = 0
            for i in range(userYvaluesLen):
                userYvalues.append(0)
                userYvaluesLen += 1

        if (len(compYvalues) < 3):
            compYvaluesLen = 3 - len(compYvalues)
            i = 0
            for i in range(compYvaluesLen):
                compYvalues.append(0)
                i += 1
                
        maxUserVal = max(userYvalues)
        maxCompVal = max(compYvalues)

        tickSetter = max(maxUserVal,maxCompVal) + 5

        plt.figure(figsize=(4.25,2))
        plt.subplot(121)
        plt.title(currUser.user_id,fontsize = 10)
        plt.bar([0,0.2,0.4],userYvalues, hatch='//', color='Green',width = 0.1)
        plt.tick_params(axis='y',labelsize = 7)
        plt.yticks(np.arange(0, tickSetter+5,tickSetter))
        plt.xticks([])
        plt.xlabel('Top Three Activities',loc='center')


        plt.subplot(122)
        plt.title(compUser.user_id,fontsize = 10)
        plt.bar([0,0.2,0.4],compYvalues, hatch='//', color='Green',width = 0.1)
        plt.tick_params(axis='y',labelsize = 7)
        plt.yticks(np.arange(0, tickSetter+5,tickSetter))
        plt.xticks([])
        plt.xlabel('Top Three Activities',loc='center')

        plt.show()

def init():
    auth.data.get_users_from_file()
    auth.data.get_activities_from_file()
    login_window(make_window())


