from tasks import send_email_task

task = send_email_task.delay(
    "noddyhenry4@gmail.com",
    "Test Email",
    "hi is everything alright"
)

print("Task ID:", task.id)