from django.db import models
# from home.


class BaseModel(models.Model):
    """基础表"""
    is_show = models.BooleanField(default=False, verbose_name="是否显示")
    orders = models.IntegerField(default=1, verbose_name="图片排序")
    is_delete = models.BooleanField(default=False, verbose_name="是否删除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")


# class Nav(BaseModel):
#     """导航栏"""
#     POSITION_OPTION = (
#         (1, "顶部导航"),
#         (2, "底部导航"),
#     )
#     title = models.CharField(max_length=200, verbose_name="导航标题")
#     link = models.CharField(max_length=300, verbose_name="导航链接")
#     position = models.IntegerField(choices=POSITION_OPTION, default=1, verbose_name="导航位置")
#     is_site = models.BooleanField(default=False, verbose_name="是否是外部链接")
#
#     class Meta:
#         db_table = "bz_nav"
#         verbose_name = "导航栏"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.title
