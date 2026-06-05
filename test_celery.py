from tasks import send_email_task


result = send_email_task.delay(
    "agentic8888@gmail.com",
    "Celery Test",
    "Testing background email task"
)


print("Task ID:")
print(result.id)