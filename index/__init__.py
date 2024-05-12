from django.apps import AppConfig
import os

# 修改app在admin后台的名字
default_app_config = 'index.IndexConfig'
# 获取当前app名字
def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]

# 重写IndexConfig
class IndexConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = '网站首页'