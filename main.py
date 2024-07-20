import pyttsx3 
import time
from plyer import notification
from datetime import datetime
import mysql.connector
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

# Twilio credentials
account_sid = 'ACb659f28880fd6b16192f45fa3ae2a112'
auth_token = '03fc33c7c6769edcdfdb8902514ff75e'
twilio_phone_number = '+17083772457'  # Twilio phone number in E.164 format

# Initialize Twilio client
client = Client(account_sid, auth_token)

# Establish connection to the database
con = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="admin",
    database="tcs"
)
print(con)
mycursor = con.cursor()

# Get the current date and month
today = datetime.today()
formatted_date = today.strftime("%d")
current_month = today.month

# Function to convert text to speech
def speak(audio):
    """Converts text to speech"""
    engine = pyttsx3.init()
    engine.say(audio)
    engine.runAndWait()

# Function to send SMS using Twilio
def send_sms(to_number, message_body):
    try:
        message = client.messages.create(
            body=message_body,
            from_=twilio_phone_number,
            to=to_number
        )
        print(f"Message sent with SID: {message.sid}")
    except TwilioRestException as e:
        print(f"An error occurred: {e}")

# Execute SQL query to fetch employee details with matching birthday
query = "SELECT name, phone_number FROM employee_detail WHERE emp_dob_date = %s AND emp_dob_month = %s"
mycursor.execute(query, (formatted_date, current_month))
data = mycursor.fetchall()

# Check if any birthdays match
if mycursor.rowcount > 0:
    for row in data:
        name = row[0]
        phone_number = row[1]  # Assuming phone_number is stored in the database

        print(f"Today is {name}'s birthday.")
        notification.notify(
            title="Birthday",
            message=f"Today is {name}'s birthday",
            timeout=10
        )
        speak(f"Today is {name}'s birthday")

        # Send birthday SMS
        message_body = f"Happy Birthday, {name}!"
        send_sms(phone_number, message_body)
else:
    print("Today is no one's birthday")
    speak("Today is no one's birthday")

# Close the cursor and connection
mycursor.close()
con.close()
