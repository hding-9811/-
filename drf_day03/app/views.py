from django.shortcuts import render
from utils.response import APIResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.models import Book
from .serializers import BookModelSerializerV2, BookDeModelSerializer, BookModelSerializer


# Create your views here.

class BookAPIView(APIView):

    def get(self, request, *args, **kwargs):

        book_id = kwargs.get("id")
        if book_id:
            book_obj = Book.objects.get(pk=book_id)
            book_ser = BookModelSerializer(book_obj).data
            print(book_ser)
            return Response({
                "status": status.HTTP_200_OK,
                "message": "查询单个图书成功",
                "results": book_ser
            })

            return APIResponse(200,"查询成功",results=book_ser)
        else:
            book_list = Book.objects.all()
            book_list_ser = BookModelSerializer(book_list, many=True)
            return Response({
                "status": status.HTTP_200_OK,
                "message": "查询所有图书成功",
                "results": book_list_ser
            })

    def post(self, request, *args, **kwargs):
        """
        完成增加单个对象
        """
        request_data = request.data

        # 将前端发送过来的数据交给反序列化器进行校验
        book_ser = BookDeModelSerializer(data=request_data)

        # 校验数据是否合法 raise_exception：一旦校验失败 立即抛出异常
        book_ser.is_valid(raise_exception=True)
        book_obj = book_ser.save()

        return Response({
            "status": status.HTTP_200_OK,
            "message": "添加图书成功",
            "result": BookModelSerializer(book_obj).data
        })


class BookAPIViewV2(APIView):

    def get(self, request, *args, **kwargs):
        book_id = kwargs.get("id")
        if book_id:
            book_obj = Book.objects.get(pk=book_id, is_delete=False)
            book_ser = BookModelSerializerV2(book_obj).data
            # return Response({
            #     "status": status.HTTP_200_OK,
            #     "me""message": "查询单个图书成功",
            #     "results": book_ser
            # })
            return APIResponse(200, "查询成功", results=book_ser)
        else:
            book_list = Book.objects.filter(is_delete=False)
            book_list_ser = BookModelSerializerV2(book_list, many=True).data
            return Response({
                "status": status.HTTP_200_OK,
                "message": "查询所有图书成功",
                "results": book_list_ser
            })

    def post(self, request, *args, **kwargs):
        """
        完成增加单个对象
        同时完成增加多个对象

        """
        request_data = request.data
        if isinstance(request_data, dict):  # 代表增加的是单个图书
            many = False
        elif isinstance(request_data, list):
            many = True
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "请求参数格式有误",
            })
        book_ser = BookModelSerializerV2(data=request_data, many=many, context={"request": request})
        # 校验数据是否合法 raise_exception 一旦校验失败 立即抛出异常

        book_ser.is_valid(raise_exception=True)
        book_obj = book_ser.save()

        return Response({
            "status": status.HTTP_200_OK,
            "message": "添加图书成功",
            # 当群增多个时，无法序列化多个对象到前台所以报错
            "result": BookModelSerializerV2(book_obj, many=many).data
        })

    def delete(self, request, *args, **kwargs):
        """
        删除单个以及删除多个
        单个删除：通过url传递id v2/books/1/
        删除多个：有多个id {ids:[1,2,3]}

        """
        book_id = kwargs.get("id")
        if book_id:
            # 删除单个 也作为删除多个
            ids = [book_id]
        else:
            # 删除多个
            ids = request.data.get("ids")
        # 判断传递过来的图书的id 是否在数据库 且还未删除
        response = Book.objects.filter(pk__in=ids,
                                       is_delete=False).update(is_delete=True)
        if response:
            return Response({
                "status": status.HTTP_200_OK,
                "message": "删除成功"
            })
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "删除失败或图书不存在"
        })

    def put(self, request, *args, **kwargs):
        """
              整体修改单个： 修改一个对象的全部字段
              :return: 修改后的对象
              """
        # 要修改的参数
        request_data = request.data
        # 要修改图书的id
        book_id = kwargs.get('id')
        try:
            book_obj = Book.objects.get(pk=book_id)
        except:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "图书不存在"
            })

        book_ser = BookModelSerializerV2(data=request_data, instance=book_obj, partial=True)
        book_ser.is_valid(raise_exception=True)
        book_ser.save()
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "更新成功",
            "results": BookModelSerializerV2(book_obj).data
        })

    def patch(self, request, *args, **kwargs):

        # 先获取要修改的数据
        request_data = request.data
        book_id = kwargs.get("id")

        # 判断id 和传递过来的参数是否是字典
        if book_id and isinstance(request_data, dict):
            book_ids = [book_id]
            request_data = [request_data]
        # 如果id 不存在且参数是列表 代表修改多个
        elif not book_id and isinstance(request_data, list):
            book_ids = []
            # 将要修改的图书id取出来放进book_ids中
            for dic in request_data:
                pk = dic.pop("pk", None)
                if pk:
                    book_ids.append(pk)
                else:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "PK不存在",
                    })
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "数据格式有误",
            })

        book_list = []  # 所有需要修改的图书对象
        new_data = []  # 所有要修改的参数
        # TODO 禁止在循环中对列表的长度做改变
        # 遍历获取到的参数
        for index, pk in enumerate(book_ids):
            try:
                book_obj = Book.objects.get(pk=pk)
                book_list.append(book_obj)
                new_data.append(request_data[index])
                print(request_data[index])
            except:
                # 如果图书对象不存在 则将id宇对应数据都移除
                continue

        # 反序列化获取到的数据
        book_ser = BookModelSerializerV2(data=new_data, instance=book_list, partial=True, many=True)
        # 如果序列化失败立即抛出异常
        book_ser.is_valid(raise_exception=True)
        book_ser.save()

        return Response({
            "status": status.HTTP_200_OK,
            "message": "修改成功",
        })
