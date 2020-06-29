from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework import status

def exception_handeler(exc,context):
    # 定义详细的错误信息
    error = "%s %s %s" %(context["view"],context["request"].method,exc)

    # 先让DRF处理异常 根据异常的返回值可以判断异常是否被处理
    response = drf_exception_handler(exc,context)
    # 如果返回值为None ,代表无法处理此时发生的异常 需要自定义处理
    if response is None:
        return Response(
            {
                "error_msg":"程序内部错误，请稍等一会儿~"
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,exception=None
        )
    # 如果Response不为空 说明异常心已经被DRF处理了直接返回即可
    return response