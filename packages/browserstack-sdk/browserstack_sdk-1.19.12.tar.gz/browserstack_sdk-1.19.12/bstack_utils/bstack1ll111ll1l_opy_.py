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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack11l11ll1ll_opy_, bstack11l1ll1l1_opy_, bstack11ll1l1ll_opy_, bstack11l1l1l11_opy_, \
    bstack11l1l1l11l_opy_
def bstack111llllll_opy_(bstack1llllllllll_opy_):
    for driver in bstack1llllllllll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack111l1l11_opy_(driver, status, reason=bstack11lll_opy_ (u"࠭ࠧᐭ")):
    bstack1ll11l1ll_opy_ = Config.bstack111llll1l_opy_()
    if bstack1ll11l1ll_opy_.bstack11lll1l1ll_opy_():
        return
    bstack1l1l11lll_opy_ = bstack1ll111llll_opy_(bstack11lll_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪᐮ"), bstack11lll_opy_ (u"ࠨࠩᐯ"), status, reason, bstack11lll_opy_ (u"ࠩࠪᐰ"), bstack11lll_opy_ (u"ࠪࠫᐱ"))
    driver.execute_script(bstack1l1l11lll_opy_)
def bstack11lll111l_opy_(page, status, reason=bstack11lll_opy_ (u"ࠫࠬᐲ")):
    try:
        if page is None:
            return
        bstack1ll11l1ll_opy_ = Config.bstack111llll1l_opy_()
        if bstack1ll11l1ll_opy_.bstack11lll1l1ll_opy_():
            return
        bstack1l1l11lll_opy_ = bstack1ll111llll_opy_(bstack11lll_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨᐳ"), bstack11lll_opy_ (u"࠭ࠧᐴ"), status, reason, bstack11lll_opy_ (u"ࠧࠨᐵ"), bstack11lll_opy_ (u"ࠨࠩᐶ"))
        page.evaluate(bstack11lll_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥᐷ"), bstack1l1l11lll_opy_)
    except Exception as e:
        print(bstack11lll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࢁࡽࠣᐸ"), e)
def bstack1ll111llll_opy_(type, name, status, reason, bstack1lll11l1l1_opy_, bstack1111l1ll1_opy_):
    bstack1l1111l11_opy_ = {
        bstack11lll_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫᐹ"): type,
        bstack11lll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᐺ"): {}
    }
    if type == bstack11lll_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨᐻ"):
        bstack1l1111l11_opy_[bstack11lll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᐼ")][bstack11lll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᐽ")] = bstack1lll11l1l1_opy_
        bstack1l1111l11_opy_[bstack11lll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᐾ")][bstack11lll_opy_ (u"ࠪࡨࡦࡺࡡࠨᐿ")] = json.dumps(str(bstack1111l1ll1_opy_))
    if type == bstack11lll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᑀ"):
        bstack1l1111l11_opy_[bstack11lll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᑁ")][bstack11lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᑂ")] = name
    if type == bstack11lll_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪᑃ"):
        bstack1l1111l11_opy_[bstack11lll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᑄ")][bstack11lll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᑅ")] = status
        if status == bstack11lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᑆ") and str(reason) != bstack11lll_opy_ (u"ࠦࠧᑇ"):
            bstack1l1111l11_opy_[bstack11lll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᑈ")][bstack11lll_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ᑉ")] = json.dumps(str(reason))
    bstack1ll11111l1_opy_ = bstack11lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬᑊ").format(json.dumps(bstack1l1111l11_opy_))
    return bstack1ll11111l1_opy_
def bstack11ll1l11_opy_(url, config, logger, bstack1l11llll1_opy_=False):
    hostname = bstack11l1ll1l1_opy_(url)
    is_private = bstack11l1l1l11_opy_(hostname)
    try:
        if is_private or bstack1l11llll1_opy_:
            file_path = bstack11l11ll1ll_opy_(bstack11lll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᑋ"), bstack11lll_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨᑌ"), logger)
            if os.environ.get(bstack11lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨᑍ")) and eval(
                    os.environ.get(bstack11lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩᑎ"))):
                return
            if (bstack11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᑏ") in config and not config[bstack11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᑐ")]):
                os.environ[bstack11lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬᑑ")] = str(True)
                bstack1lllllllll1_opy_ = {bstack11lll_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪᑒ"): hostname}
                bstack11l1l1l11l_opy_(bstack11lll_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨᑓ"), bstack11lll_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨᑔ"), bstack1lllllllll1_opy_, logger)
    except Exception as e:
        pass
def bstack11l1ll111_opy_(caps, bstack1llllllll1l_opy_):
    if bstack11lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᑕ") in caps:
        caps[bstack11lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᑖ")][bstack11lll_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬᑗ")] = True
        if bstack1llllllll1l_opy_:
            caps[bstack11lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᑘ")][bstack11lll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᑙ")] = bstack1llllllll1l_opy_
    else:
        caps[bstack11lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧᑚ")] = True
        if bstack1llllllll1l_opy_:
            caps[bstack11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᑛ")] = bstack1llllllll1l_opy_
def bstack11111ll1l1_opy_(bstack1l11l1ll1l_opy_):
    bstack1llllllll11_opy_ = bstack11ll1l1ll_opy_(threading.current_thread(), bstack11lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡕࡷࡥࡹࡻࡳࠨᑜ"), bstack11lll_opy_ (u"ࠬ࠭ᑝ"))
    if bstack1llllllll11_opy_ == bstack11lll_opy_ (u"࠭ࠧᑞ") or bstack1llllllll11_opy_ == bstack11lll_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᑟ"):
        threading.current_thread().testStatus = bstack1l11l1ll1l_opy_
    else:
        if bstack1l11l1ll1l_opy_ == bstack11lll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᑠ"):
            threading.current_thread().testStatus = bstack1l11l1ll1l_opy_