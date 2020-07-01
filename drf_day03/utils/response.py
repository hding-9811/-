from rest_framework.response import Response


class APIResponse(Response):

    def __init__(self, data_status=200, data_message=0, results=None,
                 http_status=None, headers=None,
                 exception=False, **kwargs):
        # 定义数据返回的状态

        data = {
            "status": data_status,
            "message": data_message
        }

        # 判断results 是否有结果
        if results is not None:
            data["results"] = results

        # 如果还需要传递 自定义参数 使用K哇如果是接收
        # 如果kwargs 有值则添加到 data中 如果没值 不做任何操作
        data.update(kwargs)
        # 获取一个response对象 需要将自定义response 响应回去

        super().__init__(data=data,status=http_status,headers=headers,
                         exception=exception)