from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination


# 基础分页
class MyPageNumberPaginarion(PageNumberPagination):
    # 指定每页分页数量
    page_size = 2
    # 可以通过此参数指定分页最大数量
    max_page_size = 5
    # 自定前端修改每页分页数量的 Key
    page_size_query_param = "page_size"
    # 获取第几页的对象
    page_query_param = "page"


# 偏移分页

class MyLimitPagination(LimitOffsetPagination):
    # 默认每页数量
    default_limit = 3
    # 指定前端修改每页数量的key
    limit_query_param = "limit"
    # 前端指定偏移数量的key
    offset_query_param = "offset"
    # 每页获取的最大数量
    max_limit = 5

