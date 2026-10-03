# page/__init__.py

from . import registry                          # 叶子，必须第一
from . import LoginPage                         # 触发 @register('login')
from . import InventoryPage                     # 触发 @register('inventory')
from . import DynamicCatalogLazyLoadPage
from . import DynamicCatalogSpinner
from . import DynamicCatalogSliderPage
from . import AboutPage
# 注意：不要 import SideBar

__all__ = ["registry"]