# from rest_framework.serializers import ModelSerializer
#
# from course.models import CourseCategory, Course, Teacher
#
#
# class CourseCategorySerializer(ModelSerializer):
#     """课程分类序列化器"""
#
#     class Meta:
#         model = CourseCategory
#         fields = ["id", "name"]
#
#
# class CourseTeacherSerializer(ModelSerializer):
#     """课程所属老师的序列化器"""
#
#     class Meta:
#         model = Teacher
#         fields = ["id", "name", "title", "signature"]
#
#
# class CourseModelSerializer(ModelSerializer):
#     """课程表列表"""
#
#     # 序列化器嵌套查询老师信息
#     teacher = CourseCategorySerializer()
#
#     class Meta:
#         model = Course
#         fields = ["id", "name", "course_img", "students", "lessons",
#                   "pub_lessons", "price", "teacher", "lesson_list"]


from rest_framework.serializers import ModelSerializer

from course.models import CourseCategory, Course, Teacher, CourseChapter, CourseLesson


class CourseCategorySerializer(ModelSerializer):
    """课程分类"""

    class Meta:
        model = CourseCategory
        fields = ["id", "name"]


class CourseTeacherSerializer(ModelSerializer):
    """课程所属老师的序列化器"""

    class Meta:
        model = Teacher
        fields = ("id", "name", "title", "signature")


class CourseTeacherModelSerializer(ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name', 'role', 'signature', 'image', "brief", 'title']


class CourseModelSerializer(ModelSerializer):
    """课程列表"""

    # 序列化器嵌套查询老师信息
    teacher = CourseTeacherSerializer()

    '''
    discount_name:返回前台活动所需要的名称
    '''

    class Meta:
        model = Course
        fields = ["id", "name", "course_img", "students", "lessons",
                  "pub_lessons", "price", "teacher", "lesson_list", "discount_name",
                  "real_price"]


class CourseOneSerializer(ModelSerializer):
    """ """
    teacher = CourseTeacherModelSerializer()

    class Meta:
        model = Course

        fields = [
            'id', 'name', 'course_img', 'students', 'lessons', 'pub_lessons', 'course_type',
            'price', 'teacher', 'level_name', 'course_video', 'brief_html', "discount_name",
            "real_price","active_time"
        ]


class CourseLessonSerializer(ModelSerializer):
    """课时表"""

    class Meta:
        model = CourseLesson
        fields = [
            'name', 'section_link', 'id', 'free_trail'
        ]


class CourseChapterSerializer(ModelSerializer):
    '''章节 课时表'''

    coursesections = CourseLessonSerializer(many=True)

    class Meta:
        model = CourseChapter

        fields = [
            'id', 'chapter', 'name', 'coursesections'
        ]
