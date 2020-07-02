from rest_framework.throttling import SimpleRateThrottle


class SendMessageRate(SimpleRateThrottle):
    scope = "send"

    # 只对手机号的请求做验证
    def get_cache_key(self, request, view):
        phone = request.query_params.get("phone")

        if not phone:
            return None

        # 返回数据 根据手机号和动态展示返回的值
        return "throttle_#(scope)s_%(ident)s" % {"scope": self.scope, "ident": phone}
