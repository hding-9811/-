from my_task.main import app


@app.task(name='upload_file')
def upload_file():
    print("发送短信")
    return "短信"
