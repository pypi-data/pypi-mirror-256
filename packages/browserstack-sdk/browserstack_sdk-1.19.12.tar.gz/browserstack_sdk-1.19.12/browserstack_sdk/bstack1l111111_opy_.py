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
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack111ll1l1l_opy_ = {}
        bstack1l11lll1l1_opy_ = os.environ.get(bstack11lll_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧ೼"), bstack11lll_opy_ (u"ࠧࠨ೽"))
        if not bstack1l11lll1l1_opy_:
            return bstack111ll1l1l_opy_
        try:
            bstack1l11lll1ll_opy_ = json.loads(bstack1l11lll1l1_opy_)
            if bstack11lll_opy_ (u"ࠣࡱࡶࠦ೾") in bstack1l11lll1ll_opy_:
                bstack111ll1l1l_opy_[bstack11lll_opy_ (u"ࠤࡲࡷࠧ೿")] = bstack1l11lll1ll_opy_[bstack11lll_opy_ (u"ࠥࡳࡸࠨഀ")]
            if bstack11lll_opy_ (u"ࠦࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣഁ") in bstack1l11lll1ll_opy_ or bstack11lll_opy_ (u"ࠧࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠣം") in bstack1l11lll1ll_opy_:
                bstack111ll1l1l_opy_[bstack11lll_opy_ (u"ࠨ࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠤഃ")] = bstack1l11lll1ll_opy_.get(bstack11lll_opy_ (u"ࠢࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠦഄ"), bstack1l11lll1ll_opy_.get(bstack11lll_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠦഅ")))
            if bstack11lll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࠥആ") in bstack1l11lll1ll_opy_ or bstack11lll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣഇ") in bstack1l11lll1ll_opy_:
                bstack111ll1l1l_opy_[bstack11lll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠤഈ")] = bstack1l11lll1ll_opy_.get(bstack11lll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࠨഉ"), bstack1l11lll1ll_opy_.get(bstack11lll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦഊ")))
            if bstack11lll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠤഋ") in bstack1l11lll1ll_opy_ or bstack11lll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤഌ") in bstack1l11lll1ll_opy_:
                bstack111ll1l1l_opy_[bstack11lll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠥ഍")] = bstack1l11lll1ll_opy_.get(bstack11lll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧഎ"), bstack1l11lll1ll_opy_.get(bstack11lll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧഏ")))
            if bstack11lll_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࠧഐ") in bstack1l11lll1ll_opy_ or bstack11lll_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠥ഑") in bstack1l11lll1ll_opy_:
                bstack111ll1l1l_opy_[bstack11lll_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠦഒ")] = bstack1l11lll1ll_opy_.get(bstack11lll_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࠣഓ"), bstack1l11lll1ll_opy_.get(bstack11lll_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨഔ")))
            if bstack11lll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧക") in bstack1l11lll1ll_opy_ or bstack11lll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥഖ") in bstack1l11lll1ll_opy_:
                bstack111ll1l1l_opy_[bstack11lll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦഗ")] = bstack1l11lll1ll_opy_.get(bstack11lll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣഘ"), bstack1l11lll1ll_opy_.get(bstack11lll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨങ")))
            if bstack11lll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠦച") in bstack1l11lll1ll_opy_ or bstack11lll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦഛ") in bstack1l11lll1ll_opy_:
                bstack111ll1l1l_opy_[bstack11lll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧജ")] = bstack1l11lll1ll_opy_.get(bstack11lll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠢഝ"), bstack1l11lll1ll_opy_.get(bstack11lll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢഞ")))
            if bstack11lll_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠣട") in bstack1l11lll1ll_opy_:
                bstack111ll1l1l_opy_[bstack11lll_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠤഠ")] = bstack1l11lll1ll_opy_[bstack11lll_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠥഡ")]
        except Exception as error:
            logger.error(bstack11lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡩࡵࡳࡴࡨࡲࡹࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡦࡤࡸࡦࡀࠠࠣഢ") +  str(error))
        return bstack111ll1l1l_opy_