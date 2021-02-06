import csv, smtplib, ssl
from datetime import date
import pandas as pd
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


today = date.today()
print("Today's date is", today)
print("Date components", today.year, today.month, today.day)


df = pd.read_csv("~/csvs/example.csv")


example_filter_cols = df[
    [
        "example",
        "example"
    ]
]

example_filter_cols

filter1 = df["month"] == today.month
filter2 = df["day"] == today.day

example_filter = filter1 & filter2

example_final_df = example_filter_cols[example_filter]
example_final_df


example_final_df_cols = example_final_df[
    ["full_name", "name", "birthday", "email", "phone", "gift_ideas", "address"]
]


example_final_df_cols.to_csv("example_final_df.csv", index=False)



# Email:

subject = "Example"
body = "Example"



sender_email = "email@gmail.com"
receiver_email = "email@gmail.com"


# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message["Bcc"] = receiver_email  # Recommended for mass emails

# Add body to email
message.attach(MIMEText(body, "plain"))

filename = "example_final_df.csv"  # In same directory as script

# Open PDF file in binary mode
with open(filename, "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Encode file in ASCII characters to send by email
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)

# Add attachment to message and convert message to string
message.attach(part)
text = message.as_string()

# Log in to server using secure context and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)
