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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11llll1111_opy_, bstack11lllll11l_opy_):
        self.args = args
        self.logger = logger
        self.bstack11llll1111_opy_ = bstack11llll1111_opy_
        self.bstack11lllll11l_opy_ = bstack11lllll11l_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1l11l11111_opy_(bstack11lll1l111_opy_):
        bstack11lll11lll_opy_ = []
        if bstack11lll1l111_opy_:
            tokens = str(os.path.basename(bstack11lll1l111_opy_)).split(bstack11lll_opy_ (u"ࠧࡥࠢฌ"))
            camelcase_name = bstack11lll_opy_ (u"ࠨࠠࠣญ").join(t.title() for t in tokens)
            suite_name, bstack11lll1l1l1_opy_ = os.path.splitext(camelcase_name)
            bstack11lll11lll_opy_.append(suite_name)
        return bstack11lll11lll_opy_
    @staticmethod
    def bstack11lll1l11l_opy_(typename):
        if bstack11lll_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥฎ") in typename:
            return bstack11lll_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤฏ")
        return bstack11lll_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥฐ")