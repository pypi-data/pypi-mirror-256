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
from browserstack_sdk.bstack11llllll_opy_ import bstack11l1lll1_opy_
from browserstack_sdk.bstack1l1111l1ll_opy_ import RobotHandler
def bstack1l1lllll1_opy_(framework):
    if framework.lower() == bstack11lll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᄹ"):
        return bstack11l1lll1_opy_.version()
    elif framework.lower() == bstack11lll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ᄺ"):
        return RobotHandler.version()
    elif framework.lower() == bstack11lll_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨᄻ"):
        import behave
        return behave.__version__
    else:
        return bstack11lll_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࠪᄼ")