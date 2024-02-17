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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.bstack1ll11ll111_opy_ as bstack1l11lll1_opy_
from browserstack_sdk.bstack1111llll_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack111lll1ll_opy_
class bstack11l1lll1_opy_:
    def __init__(self, args, logger, bstack11llll1111_opy_, bstack11lllll11l_opy_):
        self.args = args
        self.logger = logger
        self.bstack11llll1111_opy_ = bstack11llll1111_opy_
        self.bstack11lllll11l_opy_ = bstack11lllll11l_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1ll11l11ll_opy_ = []
        self.bstack11llll1lll_opy_ = None
        self.bstack1ll11lllll_opy_ = []
        self.bstack11lll1ll1l_opy_ = self.bstack1l11l1l1l_opy_()
        self.bstack11l11lll_opy_ = -1
    def bstack1ll1111l11_opy_(self, bstack11llll11l1_opy_):
        self.parse_args()
        self.bstack11lll1lll1_opy_()
        self.bstack11lll1llll_opy_(bstack11llll11l1_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    def bstack11llll1l1l_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack11l11lll_opy_ = -1
        if bstack11lll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ෯") in self.bstack11llll1111_opy_:
            self.bstack11l11lll_opy_ = int(self.bstack11llll1111_opy_[bstack11lll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ෰")])
        try:
            bstack11llll111l_opy_ = [bstack11lll_opy_ (u"࠭࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠨ෱"), bstack11lll_opy_ (u"ࠧ࠮࠯ࡳࡰࡺ࡭ࡩ࡯ࡵࠪෲ"), bstack11lll_opy_ (u"ࠨ࠯ࡳࠫෳ")]
            if self.bstack11l11lll_opy_ >= 0:
                bstack11llll111l_opy_.extend([bstack11lll_opy_ (u"ࠩ࠰࠱ࡳࡻ࡭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ෴"), bstack11lll_opy_ (u"ࠪ࠱ࡳ࠭෵")])
            for arg in bstack11llll111l_opy_:
                self.bstack11llll1l1l_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack11lll1lll1_opy_(self):
        bstack11llll1lll_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack11llll1lll_opy_ = bstack11llll1lll_opy_
        return bstack11llll1lll_opy_
    def bstack11lll1lll_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            import importlib
            bstack11llll11ll_opy_ = importlib.find_loader(bstack11lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭෶"))
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack111lll1ll_opy_)
    def bstack11lll1llll_opy_(self, bstack11llll11l1_opy_):
        bstack1ll11l1ll_opy_ = Config.bstack111llll1l_opy_()
        if bstack11llll11l1_opy_:
            self.bstack11llll1lll_opy_.append(bstack11lll_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ෷"))
            self.bstack11llll1lll_opy_.append(bstack11lll_opy_ (u"࠭ࡔࡳࡷࡨࠫ෸"))
        if bstack1ll11l1ll_opy_.bstack11lll1l1ll_opy_():
            self.bstack11llll1lll_opy_.append(bstack11lll_opy_ (u"ࠧ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭෹"))
            self.bstack11llll1lll_opy_.append(bstack11lll_opy_ (u"ࠨࡖࡵࡹࡪ࠭෺"))
        self.bstack11llll1lll_opy_.append(bstack11lll_opy_ (u"ࠩ࠰ࡴࠬ෻"))
        self.bstack11llll1lll_opy_.append(bstack11lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡲ࡯ࡹ࡬࡯࡮ࠨ෼"))
        self.bstack11llll1lll_opy_.append(bstack11lll_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭෽"))
        self.bstack11llll1lll_opy_.append(bstack11lll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬ෾"))
        if self.bstack11l11lll_opy_ > 1:
            self.bstack11llll1lll_opy_.append(bstack11lll_opy_ (u"࠭࠭࡯ࠩ෿"))
            self.bstack11llll1lll_opy_.append(str(self.bstack11l11lll_opy_))
    def bstack11lll1ll11_opy_(self):
        bstack1ll11lllll_opy_ = []
        for spec in self.bstack1ll11l11ll_opy_:
            bstack1lll111ll1_opy_ = [spec]
            bstack1lll111ll1_opy_ += self.bstack11llll1lll_opy_
            bstack1ll11lllll_opy_.append(bstack1lll111ll1_opy_)
        self.bstack1ll11lllll_opy_ = bstack1ll11lllll_opy_
        return bstack1ll11lllll_opy_
    def bstack1l11l1l1l_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11lll1ll1l_opy_ = True
            return True
        except Exception as e:
            self.bstack11lll1ll1l_opy_ = False
        return self.bstack11lll1ll1l_opy_
    def bstack1l11l111l_opy_(self, bstack11lllll111_opy_, bstack1ll1111l11_opy_):
        bstack1ll1111l11_opy_[bstack11lll_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧ฀")] = self.bstack11llll1111_opy_
        multiprocessing.set_start_method(bstack11lll_opy_ (u"ࠨࡵࡳࡥࡼࡴࠧก"))
        if bstack11lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬข") in self.bstack11llll1111_opy_:
            bstack1l1ll11l11_opy_ = []
            manager = multiprocessing.Manager()
            bstack11ll111l_opy_ = manager.list()
            for index, platform in enumerate(self.bstack11llll1111_opy_[bstack11lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ฃ")]):
                bstack1l1ll11l11_opy_.append(multiprocessing.Process(name=str(index),
                                                           target=bstack11lllll111_opy_,
                                                           args=(self.bstack11llll1lll_opy_, bstack1ll1111l11_opy_, bstack11ll111l_opy_)))
            i = 0
            bstack11llll1ll1_opy_ = len(self.bstack11llll1111_opy_[bstack11lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧค")])
            for t in bstack1l1ll11l11_opy_:
                os.environ[bstack11lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬฅ")] = str(i)
                os.environ[bstack11lll_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧฆ")] = json.dumps(self.bstack11llll1111_opy_[bstack11lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪง")][i % bstack11llll1ll1_opy_])
                i += 1
                t.start()
            for t in bstack1l1ll11l11_opy_:
                t.join()
            return list(bstack11ll111l_opy_)
    @staticmethod
    def bstack1111ll11l_opy_(driver, bstack1l1l111l_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack11lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬจ"), None)
        if item and getattr(item, bstack11lll_opy_ (u"ࠩࡢࡥ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡣࡢࡵࡨࠫฉ"), None) and not getattr(item, bstack11lll_opy_ (u"ࠪࡣࡦ࠷࠱ࡺࡡࡶࡸࡴࡶ࡟ࡥࡱࡱࡩࠬช"), False):
            logger.info(
                bstack11lll_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠢࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡮ࡹࠠࡶࡰࡧࡩࡷࡽࡡࡺ࠰ࠥซ"))
            bstack11llll1l11_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1l11lll1_opy_.bstack11l1l111l_opy_(driver, bstack11llll1l11_opy_, item.name, item.module.__name__, item.path, bstack1l1l111l_opy_)
            item._a11y_stop_done = True
            if wait:
                sleep(2)