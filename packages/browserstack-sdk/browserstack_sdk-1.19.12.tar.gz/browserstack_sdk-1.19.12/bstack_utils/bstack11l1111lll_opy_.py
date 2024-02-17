# coding: UTF-8
import sys
bstack111l11l_opy_ = sys.version_info [0] == 2
bstack1111lll_opy_ = 2048
bstack1111ll_opy_ = 7
def bstack11lll_opy_ (bstack1l1l_opy_):
    global bstack1ll_opy_
    bstack1111l1l_opy_ = ord (bstack1l1l_opy_ [-1])
    bstack1111l1_opy_ = bstack1l1l_opy_ [:-1]
    bstack1ll1_opy_ = bstack1111l1l_opy_ % len (bstack1111l1_opy_)
    bstack111l11_opy_ = bstack1111l1_opy_ [:bstack1ll1_opy_] + bstack1111l1_opy_ [bstack1ll1_opy_:]
    if bstack111l11l_opy_:
        bstack11lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1111lll_opy_ - (bstack1l1l1_opy_ + bstack1111l1l_opy_) % bstack1111ll_opy_) for bstack1l1l1_opy_, char in enumerate (bstack111l11_opy_)])
    else:
        bstack11lll1l_opy_ = str () .join ([chr (ord (char) - bstack1111lll_opy_ - (bstack1l1l1_opy_ + bstack1111l1l_opy_) % bstack1111ll_opy_) for bstack1l1l1_opy_, char in enumerate (bstack111l11_opy_)])
    return eval (bstack11lll1l_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result
def _11l1111ll1_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack11l111111l_opy_:
    def __init__(self, handler):
        self._111lllll11_opy_ = {}
        self._11l11111l1_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        self._111lllll11_opy_[bstack11lll_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩዖ")] = Module._inject_setup_function_fixture
        self._111lllll11_opy_[bstack11lll_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ዗")] = Module._inject_setup_module_fixture
        self._111lllll11_opy_[bstack11lll_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨዘ")] = Class._inject_setup_class_fixture
        self._111lllll11_opy_[bstack11lll_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪዙ")] = Class._inject_setup_method_fixture
        Module._inject_setup_function_fixture = self.bstack111lllll1l_opy_(bstack11lll_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ዚ"))
        Module._inject_setup_module_fixture = self.bstack111lllll1l_opy_(bstack11lll_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬዛ"))
        Class._inject_setup_class_fixture = self.bstack111lllll1l_opy_(bstack11lll_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬዜ"))
        Class._inject_setup_method_fixture = self.bstack111lllll1l_opy_(bstack11lll_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧዝ"))
    def bstack111llllll1_opy_(self, bstack11l1111l11_opy_, hook_type):
        meth = getattr(bstack11l1111l11_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._11l11111l1_opy_[hook_type] = meth
            setattr(bstack11l1111l11_opy_, hook_type, self.bstack11l111l1l1_opy_(hook_type))
    def bstack11l11111ll_opy_(self, instance, bstack11l1111l1l_opy_):
        if bstack11l1111l1l_opy_ == bstack11lll_opy_ (u"ࠢࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠥዞ"):
            self.bstack111llllll1_opy_(instance.obj, bstack11lll_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠤዟ"))
            self.bstack111llllll1_opy_(instance.obj, bstack11lll_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠨዠ"))
        if bstack11l1111l1l_opy_ == bstack11lll_opy_ (u"ࠥࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠦዡ"):
            self.bstack111llllll1_opy_(instance.obj, bstack11lll_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠥዢ"))
            self.bstack111llllll1_opy_(instance.obj, bstack11lll_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠢዣ"))
        if bstack11l1111l1l_opy_ == bstack11lll_opy_ (u"ࠨࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪࠨዤ"):
            self.bstack111llllll1_opy_(instance.obj, bstack11lll_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠧዥ"))
            self.bstack111llllll1_opy_(instance.obj, bstack11lll_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠤዦ"))
        if bstack11l1111l1l_opy_ == bstack11lll_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠥዧ"):
            self.bstack111llllll1_opy_(instance.obj, bstack11lll_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠤየ"))
            self.bstack111llllll1_opy_(instance.obj, bstack11lll_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩࠨዩ"))
    @staticmethod
    def bstack11l1111111_opy_(hook_type, func, args):
        if hook_type in [bstack11lll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫዪ"), bstack11lll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨያ")]:
            _11l1111ll1_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11l111l1l1_opy_(self, hook_type):
        def bstack11l111l111_opy_(arg=None):
            self.handler(hook_type, bstack11lll_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧዬ"))
            result = None
            exception = None
            try:
                self.bstack11l1111111_opy_(hook_type, self._11l11111l1_opy_[hook_type], (arg,))
                result = Result(result=bstack11lll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨይ"))
            except Exception as e:
                result = Result(result=bstack11lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩዮ"), exception=e)
                self.handler(hook_type, bstack11lll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩዯ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11lll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪደ"), result)
        def bstack111lllllll_opy_(this, arg=None):
            self.handler(hook_type, bstack11lll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬዱ"))
            result = None
            exception = None
            try:
                self.bstack11l1111111_opy_(hook_type, self._11l11111l1_opy_[hook_type], (this, arg))
                result = Result(result=bstack11lll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ዲ"))
            except Exception as e:
                result = Result(result=bstack11lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧዳ"), exception=e)
                self.handler(hook_type, bstack11lll_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧዴ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11lll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨድ"), result)
        if hook_type in [bstack11lll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩዶ"), bstack11lll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ዷ")]:
            return bstack111lllllll_opy_
        return bstack11l111l111_opy_
    def bstack111lllll1l_opy_(self, bstack11l1111l1l_opy_):
        def bstack11l111l11l_opy_(this, *args, **kwargs):
            self.bstack11l11111ll_opy_(this, bstack11l1111l1l_opy_)
            self._111lllll11_opy_[bstack11l1111l1l_opy_](this, *args, **kwargs)
        return bstack11l111l11l_opy_