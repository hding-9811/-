from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import exception_handler as drf_exception_handler


def exception_handler(exc, context):
    # 详细错误信息的定义
    error = "%s %s %s" %(context["view"],context["request"].method,exc)
    print(error)
    # 先让DRF处理异常 根据异常的返回值可以判断异常是否被处理
    response = drf_exception_handler(exc,context)
    # 若果返回为 None,代表DRF无法处理此时发生的异常 需要自定义处理
    if response is None:
        return Response(
            {"error_msg":"程序内部错误，请稍等一会儿"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,exception=None
        )
    return response
