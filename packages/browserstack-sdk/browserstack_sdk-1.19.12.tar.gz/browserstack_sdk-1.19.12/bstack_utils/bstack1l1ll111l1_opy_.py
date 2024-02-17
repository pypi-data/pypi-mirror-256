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
class bstack1111l1l1l_opy_:
    def __init__(self, handler):
        self._111111111l_opy_ = None
        self.handler = handler
        self._11111111ll_opy_ = self.bstack1111111111_opy_()
        self.patch()
    def patch(self):
        self._111111111l_opy_ = self._11111111ll_opy_.execute
        self._11111111ll_opy_.execute = self.bstack11111111l1_opy_()
    def bstack11111111l1_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack11lll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࠦᐫ"), driver_command)
            response = self._111111111l_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack11lll_opy_ (u"ࠧࡧࡦࡵࡧࡵࠦᐬ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._11111111ll_opy_.execute = self._111111111l_opy_
    @staticmethod
    def bstack1111111111_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver