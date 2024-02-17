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
import sys
class bstack1l11l11ll1_opy_:
    def __init__(self, handler):
        self._11ll11lll1_opy_ = sys.stdout.write
        self._11ll11ll1l_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack11ll11ll11_opy_
        sys.stdout.error = self.bstack11ll11l1ll_opy_
    def bstack11ll11ll11_opy_(self, _str):
        self._11ll11lll1_opy_(_str)
        if self.handler:
            self.handler({bstack11lll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ຨ"): bstack11lll_opy_ (u"ࠨࡋࡑࡊࡔ࠭ຩ"), bstack11lll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪສ"): _str})
    def bstack11ll11l1ll_opy_(self, _str):
        self._11ll11ll1l_opy_(_str)
        if self.handler:
            self.handler({bstack11lll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩຫ"): bstack11lll_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪຬ"), bstack11lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ອ"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._11ll11lll1_opy_
        sys.stderr.write = self._11ll11ll1l_opy_