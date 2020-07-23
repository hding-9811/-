def get_select_course(self, request):
    """
    获取购物车中已勾选的商品  返回前端所需的数据
    """

    user_id = request.user.id
    redis_connection = get_redis_connection("cart")

    # 获取当前登录用户的购车中所有的商品
    cart_list = redis_connection.hgetall("cart_%s" % user_id)
    select_list = redis_connection.smembers("selected_%s" % user_id)

    total_price = 0  # 商品总价
    data = []

    for course_id_byte, expire_id_byte in cart_list.items():
        course_id = int(course_id_byte)
        expire_id = int(expire_id_byte)
        print(course_id, expire_id)

        # 判断商品id是否在已勾选的的列表中
        if course_id_byte in select_list:
            try:
                # 获取到的所有的课程信息
                course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
            except Course.DoesNotExist:
                continue
            # 如果有效期的id大于0  则需要计算商品的价格  id不大于0则代表永久有效 需要默认值
            original_price = course.price
            expire_text = "永久有效"

            try:
                if expire_id > 0:
                    course_expire = CourseExpire.objects.get(id=expire_id)
                    # 对应有效期的价格
                    original_price = course_expire.price
                    expire_text = course_expire.expire_text
            except CourseExpire.DoesNotExist:
                pass

            # 根据已勾选的商品的对应有效期的价格去计算勾选商品的最终价格
            real_expire_price = course.real_expire_price(expire_id)

            # 将购物车所需的信息返回
            data.append({
                "course_img": constants.IMAGE_SRC + course.course_img.url,
                "name": course.name,
                "id": course.id,
                "expire_text": expire_text,
                # 活动、有效期计算完成后的  真实价格
                "real_price": "%.2f" % float(real_expire_price),
                # 原价
                "price": original_price,
                "discount_name": course.discount_name,
            })

            # 商品叠加后的总价
            total_price += float(real_expire_price)

    return Response({"course_list": data, "total_price": total_price, "message": '获取成功'})