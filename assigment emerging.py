# Importing necessary modules
import requests  # For making HTTP requests
import json      # For handling JSON data

#define all the function include in the system

# Function to print the menu options
def print_menu():
    """
    Prints the menu options for the user to choose from.
    """
    print("\nOptions:")
    print("0. Test the connection with Webex server")
    print("1. Display your information")
    print("2. Display a list of rooms")
    print("3. Create a room")
    print("4. Send a message to a room")

#Option 0: 
# Function to test the connection with Webex server
def test_connection(accessToken):
    """
    Tests the connection with the Webex server using the provided access token.

    Parameters:
        accessToken (str): The access token for authentication.
    """
    headers = {
        "Authorization": accessToken
    }
    response = requests.get(f"https://webexapis.com/v1/people/me", headers=headers)

    if response.status_code == 200:
        data = response.json()
        print("Connection successful!")
    else:
        print("Connection failed. Status code:", response.status_code)



#Option 1: 
# Function to display user information
def display_user_info(accessToken):
    """
    Displays the user's information.

    Parameters:
        accessToken (str): The access token for authentication.
    """
    url = 'https://webexapis.com/v1/people/me'

    headers = {
        "Authorization": accessToken
    }
    res = requests.get(url, headers=headers)
    data = res.json()
    print("\nName: ", data.get("displayName"))
    print("Nickname: ", data.get("nickName"))
    print("Email: ", data.get("emails")[0])



#Option 2: 
# Function to display a list of rooms
def display_rooms(accessToken):
    """
    Displays a list of rooms the user is a member of.

    Parameters:
        accessToken (str): The access token for authentication.
    """
    url = 'https://webexapis.com/v1/rooms'

    headers = {
        "Authorization": accessToken,
        'Content-Type' : 'application/json'
    }
    params={'max':'100'}
    res = requests.get(url, headers=headers, params=params)
    if res.status_code == 200:
        data = res.json()
        rooms = data.get('items', [])
        i = 1 

        for room in rooms:
            room_id = room.get('id')
            room_title = room.get('title')
            date_created = room.get('created')
            last_activity = room.get('lastActivity')
            
            print("\nRoom ID ", (i),":", room_id)
            print("Room Title:", room_title)
            print("Date Created:", date_created)
            print("Last Activity:", last_activity)
            i += 1
    else:
        print("Failed to retrieve room data. Status code:", res.status_code)

#Option 3:
# Function to create a room
def create_room(accessToken):
    """
    Creates a new room with the specified title.

    Parameters:
        accessToken (str): The access token for authentication.
    """
    roomTitle = input("Enter the room title you want to create: ")
    url = 'https://webexapis.com/v1/rooms'

    headers = {
        "Authorization": accessToken,
        'Content-Type' : 'application/json'
    }
    params={'title': roomTitle}
    res = requests.post(url, headers=headers, json=params)
    if res.status_code == 200:
        data = res.json()
        room_id = data.get('id', None)
        roomTitle = data.get('title', None)

        if room_id and roomTitle:
            print(f"Room '{roomTitle}' has been successfully created.")
        else:
            print("Room creation response does not contain expected data.")
    else:
        print("Failed to create the room, Status code:", res.status_code)

#Option 4:
# Function to send a message to a room
# Option 4: Send a message to a room
def send_message(accessToken):
    """
    Sends a message to a specified room.

    Parameters:
        accessToken (str): The access token for authentication.
    """
    url = 'https://webexapis.com/v1/rooms'
    headers = {
        "Authorization": accessToken,
        'Content-Type' : 'application/json'
    }

    res = requests.get(url, headers=headers)

    if res.status_code == 200:
        data = res.json()
        rooms = data.get('items', [])

        # Display 5 rooms for the user to choose from
        for i, room in enumerate(rooms[:5]):
            print(f"{i+1}. {room.get('title')}")

        # User chooses which room to send the message to
        room_num = int(input("\nEnter the number of the room you want to send the message to: "))
        room_num -= 1

        if 0 <= room_num < len(rooms):
            room_id = rooms[room_num].get('id')
            message = input("Enter the message: ")

            params = {'roomId': room_id, 'markdown': message}
            res = requests.post('https://webexapis.com/v1/messages', headers=headers, json=params)

            if res.status_code == 200:
                print("Message has been sent successfully.")
            else:
                print("Failed to send the message. Status code:", res.status_code)
        else:
            print("Invalid room number.")
    else:
        print("Failed to fetch room data. Status code:", res.status_code)

# Main part of the program:

# Hard-coded access token
accessToken = 'MWIyNWRmYTktNzMzNy00YjE2LWJlZWEtMmRiNWQ1NjIxZDdjNDA4YjRhMjItMTZl_P0A1_a61a0b2b-feba-43a3-8a20-e8cc10a43c9a'

# Prompt user for access token if desired
choice = input("Do you wish to use the hard-coded token? (y/n)")

if choice.lower() == "n":
    accessToken = input("Enter your access token: ")
    accessToken = "Bearer " + accessToken
else:
    accessToken = "Bearer MWIyNWRmYTktNzMzNy00YjE2LWJlZWEtMmRiNWQ1NjIxZDdjNDA4YjRhMjItMTZl_P0A1_a61a0b2b-feba-43a3-8a20-e8cc10a43c9a"

# Main menu loop
while True:
    print_menu()
    option = input("\nSelect the option number you would like to proceed: ")

    if option == "0":
        test_connection(accessToken)
        input("Press Enter to return to the menu...")
    elif option == "1":
        display_user_info(accessToken)
        input("\nPress Enter to return to the menu...")
    elif option == "2":
        display_rooms(accessToken)
        input("\nPress Enter to return to the menu...")
    elif option == "3":
        create_room(accessToken)
        input("Press Enter to return to the menu...")
    elif option == "4":
        send_message(accessToken)
        input("Press Enter to return to the menu...")
    else:
        print("Invalid option. Please select a valid option.")