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
import datetime
import json
import logging
import os
import threading
from bstack_utils.helper import bstack11ll1l11l1_opy_, bstack1ll11llll1_opy_, get_host_info, bstack11ll1l1111_opy_, bstack11ll1llll1_opy_, bstack11l1ll11l1_opy_, \
    bstack11l11l11ll_opy_, bstack11l11ll111_opy_, bstack1lll11l1ll_opy_, bstack11l1llll11_opy_, bstack1lll111l1l_opy_, bstack1l111l1ll1_opy_
from bstack_utils.bstack111111l11l_opy_ import bstack1111111l1l_opy_
from bstack_utils.bstack1l11111ll1_opy_ import bstack1l11ll1111_opy_
import bstack_utils.bstack1ll11ll111_opy_ as bstack1l11lll1_opy_
from bstack_utils.constants import bstack11ll1111ll_opy_
bstack1llll1ll1l1_opy_ = [
    bstack11lll_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬᒟ"), bstack11lll_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭ᒠ"), bstack11lll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᒡ"), bstack11lll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬᒢ"),
    bstack11lll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᒣ"), bstack11lll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᒤ"), bstack11lll_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᒥ")
]
bstack1lllll11l11_opy_ = bstack11lll_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡦࡳࡱࡲࡥࡤࡶࡲࡶ࠲ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨᒦ")
logger = logging.getLogger(__name__)
class bstack1l111l11_opy_:
    bstack111111l11l_opy_ = None
    bs_config = None
    @classmethod
    @bstack1l111l1ll1_opy_(class_method=True)
    def launch(cls, bs_config, bstack1llll1lllll_opy_):
        cls.bs_config = bs_config
        cls.bstack1llll1lll1l_opy_()
        bstack11ll1ll1l1_opy_ = bstack11ll1l1111_opy_(bs_config)
        bstack11ll1l1l1l_opy_ = bstack11ll1llll1_opy_(bs_config)
        bstack1lllll1lll_opy_ = False
        bstack11l11lll1_opy_ = False
        if bstack11lll_opy_ (u"ࠩࡤࡴࡵ࠭ᒧ") in bs_config:
            bstack1lllll1lll_opy_ = True
        else:
            bstack11l11lll1_opy_ = True
        bstack1111llll1_opy_ = {
            bstack11lll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᒨ"): cls.bstack111ll111l_opy_(),
            bstack11lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᒩ"): bstack1l11lll1_opy_.bstack1l1l1l111l_opy_(bs_config),
            bstack11lll_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫᒪ"): bs_config.get(bstack11lll_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬᒫ"), False),
            bstack11lll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩᒬ"): bstack11l11lll1_opy_,
            bstack11lll_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᒭ"): bstack1lllll1lll_opy_
        }
        data = {
            bstack11lll_opy_ (u"ࠩࡩࡳࡷࡳࡡࡵࠩᒮ"): bstack11lll_opy_ (u"ࠪ࡮ࡸࡵ࡮ࠨᒯ"),
            bstack11lll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡤࡴࡡ࡮ࡧࠪᒰ"): bs_config.get(bstack11lll_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᒱ"), bstack11lll_opy_ (u"࠭ࠧᒲ")),
            bstack11lll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᒳ"): bs_config.get(bstack11lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᒴ"), os.path.basename(os.path.abspath(os.getcwd()))),
            bstack11lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᒵ"): bs_config.get(bstack11lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᒶ")),
            bstack11lll_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᒷ"): bs_config.get(bstack11lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᒸ"), bstack11lll_opy_ (u"࠭ࠧᒹ")),
            bstack11lll_opy_ (u"ࠧࡴࡶࡤࡶࡹࡥࡴࡪ࡯ࡨࠫᒺ"): datetime.datetime.now().isoformat(),
            bstack11lll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᒻ"): bstack11l1ll11l1_opy_(bs_config),
            bstack11lll_opy_ (u"ࠩ࡫ࡳࡸࡺ࡟ࡪࡰࡩࡳࠬᒼ"): get_host_info(),
            bstack11lll_opy_ (u"ࠪࡧ࡮ࡥࡩ࡯ࡨࡲࠫᒽ"): bstack1ll11llll1_opy_(),
            bstack11lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡶࡺࡴ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᒾ"): os.environ.get(bstack11lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫᒿ")),
            bstack11lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࡤࡸࡥࡳࡷࡱࠫᓀ"): os.environ.get(bstack11lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠬᓁ"), False),
            bstack11lll_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࡡࡦࡳࡳࡺࡲࡰ࡮ࠪᓂ"): bstack11ll1l11l1_opy_(),
            bstack11lll_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧᓃ"): bstack1111llll1_opy_,
            bstack11lll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࡢࡺࡪࡸࡳࡪࡱࡱࠫᓄ"): {
                bstack11lll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫᓅ"): bstack1llll1lllll_opy_.get(bstack11lll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪ࠭ᓆ"), bstack11lll_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭ᓇ")),
                bstack11lll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᓈ"): bstack1llll1lllll_opy_.get(bstack11lll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᓉ")),
                bstack11lll_opy_ (u"ࠩࡶࡨࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᓊ"): bstack1llll1lllll_opy_.get(bstack11lll_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᓋ"))
            }
        }
        config = {
            bstack11lll_opy_ (u"ࠫࡦࡻࡴࡩࠩᓌ"): (bstack11ll1ll1l1_opy_, bstack11ll1l1l1l_opy_),
            bstack11lll_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᓍ"): cls.default_headers()
        }
        response = bstack1lll11l1ll_opy_(bstack11lll_opy_ (u"࠭ࡐࡐࡕࡗࠫᓎ"), cls.request_url(bstack11lll_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹࠧᓏ")), data, config)
        if response.status_code != 200:
            os.environ[bstack11lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᓐ")] = bstack11lll_opy_ (u"ࠩࡱࡹࡱࡲࠧᓑ")
            os.environ[bstack11lll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩᓒ")] = bstack11lll_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪᓓ")
            os.environ[bstack11lll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ᓔ")] = bstack11lll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᓕ")
            os.environ[bstack11lll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ᓖ")] = bstack11lll_opy_ (u"ࠣࡰࡸࡰࡱࠨᓗ")
            os.environ[bstack11lll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪᓘ")] = bstack11lll_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᓙ")
            bstack1lllll11111_opy_ = response.json()
            if bstack1lllll11111_opy_ and bstack1lllll11111_opy_[bstack11lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᓚ")]:
                error_message = bstack1lllll11111_opy_[bstack11lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᓛ")]
                if bstack1lllll11111_opy_[bstack11lll_opy_ (u"࠭ࡥࡳࡴࡲࡶ࡙ࡿࡰࡦࠩᓜ")] == bstack11lll_opy_ (u"ࠧࡆࡔࡕࡓࡗࡥࡉࡏࡘࡄࡐࡎࡊ࡟ࡄࡔࡈࡈࡊࡔࡔࡊࡃࡏࡗࠬᓝ"):
                    logger.error(error_message)
                elif bstack1lllll11111_opy_[bstack11lll_opy_ (u"ࠨࡧࡵࡶࡴࡸࡔࡺࡲࡨࠫᓞ")] == bstack11lll_opy_ (u"ࠩࡈࡖࡗࡕࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡆࡈࡒࡎࡋࡄࠨᓟ"):
                    logger.info(error_message)
                elif bstack1lllll11111_opy_[bstack11lll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡖࡼࡴࡪ࠭ᓠ")] == bstack11lll_opy_ (u"ࠫࡊࡘࡒࡐࡔࡢࡗࡉࡑ࡟ࡅࡇࡓࡖࡊࡉࡁࡕࡇࡇࠫᓡ"):
                    logger.error(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack11lll_opy_ (u"ࠧࡊࡡࡵࡣࠣࡹࡵࡲ࡯ࡢࡦࠣࡸࡴࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯࡚ࠥࡥࡴࡶࠣࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠣࡪࡦ࡯࡬ࡦࡦࠣࡨࡺ࡫ࠠࡵࡱࠣࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠢᓢ"))
            return [None, None, None]
        bstack1lllll11111_opy_ = response.json()
        os.environ[bstack11lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᓣ")] = bstack1lllll11111_opy_[bstack11lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᓤ")]
        if cls.bstack111ll111l_opy_() is True and bstack1llll1lllll_opy_.get(bstack11lll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡺࡹࡥࡥࠩᓥ")) in bstack11ll1111ll_opy_:
            logger.debug(bstack11lll_opy_ (u"ࠩࡗࡩࡸࡺࠠࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠦ࠭ᓦ"))
            os.environ[bstack11lll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩᓧ")] = bstack11lll_opy_ (u"ࠫࡹࡸࡵࡦࠩᓨ")
            if bstack1lllll11111_opy_.get(bstack11lll_opy_ (u"ࠬࡰࡷࡵࠩᓩ")):
                os.environ[bstack11lll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᓪ")] = bstack1lllll11111_opy_[bstack11lll_opy_ (u"ࠧ࡫ࡹࡷࠫᓫ")]
                os.environ[bstack11lll_opy_ (u"ࠨࡅࡕࡉࡉࡋࡎࡕࡋࡄࡐࡘࡥࡆࡐࡔࡢࡇࡗࡇࡓࡉࡡࡕࡉࡕࡕࡒࡕࡋࡑࡋࠬᓬ")] = json.dumps({
                    bstack11lll_opy_ (u"ࠩࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫᓭ"): bstack11ll1ll1l1_opy_,
                    bstack11lll_opy_ (u"ࠪࡴࡦࡹࡳࡸࡱࡵࡨࠬᓮ"): bstack11ll1l1l1l_opy_
                })
            if bstack1lllll11111_opy_.get(bstack11lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᓯ")):
                os.environ[bstack11lll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫᓰ")] = bstack1lllll11111_opy_[bstack11lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᓱ")]
            if bstack1lllll11111_opy_.get(bstack11lll_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫᓲ")):
                os.environ[bstack11lll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩᓳ")] = str(bstack1lllll11111_opy_[bstack11lll_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᓴ")])
        return [bstack1lllll11111_opy_[bstack11lll_opy_ (u"ࠪ࡮ࡼࡺࠧᓵ")], bstack1lllll11111_opy_[bstack11lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᓶ")], bstack1lllll11111_opy_[bstack11lll_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩᓷ")]]
    @classmethod
    @bstack1l111l1ll1_opy_(class_method=True)
    def stop(cls):
        if not cls.on():
            return
        if os.environ[bstack11lll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᓸ")] == bstack11lll_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᓹ") or os.environ[bstack11lll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧᓺ")] == bstack11lll_opy_ (u"ࠤࡱࡹࡱࡲࠢᓻ"):
            print(bstack11lll_opy_ (u"ࠪࡉ࡝ࡉࡅࡑࡖࡌࡓࡓࠦࡉࡏࠢࡶࡸࡴࡶࡂࡶ࡫࡯ࡨ࡚ࡶࡳࡵࡴࡨࡥࡲࠦࡒࡆࡓࡘࡉࡘ࡚ࠠࡕࡑࠣࡘࡊ࡙ࡔࠡࡑࡅࡗࡊࡘࡖࡂࡄࡌࡐࡎ࡚࡙ࠡ࠼ࠣࡑ࡮ࡹࡳࡪࡰࡪࠤࡦࡻࡴࡩࡧࡱࡸ࡮ࡩࡡࡵ࡫ࡲࡲࠥࡺ࡯࡬ࡧࡱࠫᓼ"))
            return {
                bstack11lll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᓽ"): bstack11lll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᓾ"),
                bstack11lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᓿ"): bstack11lll_opy_ (u"ࠧࡕࡱ࡮ࡩࡳ࠵ࡢࡶ࡫࡯ࡨࡎࡊࠠࡪࡵࠣࡹࡳࡪࡥࡧ࡫ࡱࡩࡩ࠲ࠠࡣࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡ࡯࡬࡫࡭ࡺࠠࡩࡣࡹࡩࠥ࡬ࡡࡪ࡮ࡨࡨࠬᔀ")
            }
        else:
            cls.bstack111111l11l_opy_.shutdown()
            data = {
                bstack11lll_opy_ (u"ࠨࡵࡷࡳࡵࡥࡴࡪ࡯ࡨࠫᔁ"): datetime.datetime.now().isoformat()
            }
            config = {
                bstack11lll_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪᔂ"): cls.default_headers()
            }
            bstack11l1l1ll1l_opy_ = bstack11lll_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂ࠵ࡳࡵࡱࡳࠫᔃ").format(os.environ[bstack11lll_opy_ (u"ࠦࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠥᔄ")])
            bstack1lllll111ll_opy_ = cls.request_url(bstack11l1l1ll1l_opy_)
            response = bstack1lll11l1ll_opy_(bstack11lll_opy_ (u"ࠬࡖࡕࡕࠩᔅ"), bstack1lllll111ll_opy_, data, config)
            if not response.ok:
                raise Exception(bstack11lll_opy_ (u"ࠨࡓࡵࡱࡳࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡴ࡯ࡵࠢࡲ࡯ࠧᔆ"))
    @classmethod
    def bstack1l11l111ll_opy_(cls):
        if cls.bstack111111l11l_opy_ is None:
            return
        cls.bstack111111l11l_opy_.shutdown()
    @classmethod
    def bstack11l111l1_opy_(cls):
        if cls.on():
            print(
                bstack11lll_opy_ (u"ࠧࡗ࡫ࡶ࡭ࡹࠦࡨࡵࡶࡳࡷ࠿࠵࠯ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂࠦࡴࡰࠢࡹ࡭ࡪࡽࠠࡣࡷ࡬ࡰࡩࠦࡲࡦࡲࡲࡶࡹ࠲ࠠࡪࡰࡶ࡭࡬࡮ࡴࡴ࠮ࠣࡥࡳࡪࠠ࡮ࡣࡱࡽࠥࡳ࡯ࡳࡧࠣࡨࡪࡨࡵࡨࡩ࡬ࡲ࡬ࠦࡩ࡯ࡨࡲࡶࡲࡧࡴࡪࡱࡱࠤࡦࡲ࡬ࠡࡣࡷࠤࡴࡴࡥࠡࡲ࡯ࡥࡨ࡫ࠡ࡝ࡰࠪᔇ").format(os.environ[bstack11lll_opy_ (u"ࠣࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠢᔈ")]))
    @classmethod
    def bstack1llll1lll1l_opy_(cls):
        if cls.bstack111111l11l_opy_ is not None:
            return
        cls.bstack111111l11l_opy_ = bstack1111111l1l_opy_(cls.bstack1lllll1l111_opy_)
        cls.bstack111111l11l_opy_.start()
    @classmethod
    def bstack1l111l1lll_opy_(cls, bstack11lllll1ll_opy_, bstack1llll1l1ll1_opy_=bstack11lll_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨᔉ")):
        if not cls.on():
            return
        bstack11111lll_opy_ = bstack11lllll1ll_opy_[bstack11lll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᔊ")]
        bstack1llll1llll1_opy_ = {
            bstack11lll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᔋ"): bstack11lll_opy_ (u"࡚ࠬࡥࡴࡶࡢࡗࡹࡧࡲࡵࡡࡘࡴࡱࡵࡡࡥࠩᔌ"),
            bstack11lll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᔍ"): bstack11lll_opy_ (u"ࠧࡕࡧࡶࡸࡤࡋ࡮ࡥࡡࡘࡴࡱࡵࡡࡥࠩᔎ"),
            bstack11lll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩᔏ"): bstack11lll_opy_ (u"ࠩࡗࡩࡸࡺ࡟ࡔ࡭࡬ࡴࡵ࡫ࡤࡠࡗࡳࡰࡴࡧࡤࠨᔐ"),
            bstack11lll_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧᔑ"): bstack11lll_opy_ (u"ࠫࡑࡵࡧࡠࡗࡳࡰࡴࡧࡤࠨᔒ"),
            bstack11lll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᔓ"): bstack11lll_opy_ (u"࠭ࡈࡰࡱ࡮ࡣࡘࡺࡡࡳࡶࡢ࡙ࡵࡲ࡯ࡢࡦࠪᔔ"),
            bstack11lll_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᔕ"): bstack11lll_opy_ (u"ࠨࡊࡲࡳࡰࡥࡅ࡯ࡦࡢ࡙ࡵࡲ࡯ࡢࡦࠪᔖ"),
            bstack11lll_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭ᔗ"): bstack11lll_opy_ (u"ࠪࡇࡇ࡚࡟ࡖࡲ࡯ࡳࡦࡪࠧᔘ")
        }.get(bstack11111lll_opy_)
        if bstack1llll1l1ll1_opy_ == bstack11lll_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪᔙ"):
            cls.bstack1llll1lll1l_opy_()
            cls.bstack111111l11l_opy_.add(bstack11lllll1ll_opy_)
        elif bstack1llll1l1ll1_opy_ == bstack11lll_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪᔚ"):
            cls.bstack1lllll1l111_opy_([bstack11lllll1ll_opy_], bstack1llll1l1ll1_opy_)
    @classmethod
    @bstack1l111l1ll1_opy_(class_method=True)
    def bstack1lllll1l111_opy_(cls, bstack11lllll1ll_opy_, bstack1llll1l1ll1_opy_=bstack11lll_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬᔛ")):
        config = {
            bstack11lll_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᔜ"): cls.default_headers()
        }
        response = bstack1lll11l1ll_opy_(bstack11lll_opy_ (u"ࠨࡒࡒࡗ࡙࠭ᔝ"), cls.request_url(bstack1llll1l1ll1_opy_), bstack11lllll1ll_opy_, config)
        bstack11ll1ll11l_opy_ = response.json()
    @classmethod
    @bstack1l111l1ll1_opy_(class_method=True)
    def bstack1ll1lllll1_opy_(cls, bstack1l111ll1l1_opy_):
        bstack1lllll1111l_opy_ = []
        for log in bstack1l111ll1l1_opy_:
            bstack1llll1ll111_opy_ = {
                bstack11lll_opy_ (u"ࠩ࡮࡭ࡳࡪࠧᔞ"): bstack11lll_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡎࡒࡋࠬᔟ"),
                bstack11lll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᔠ"): log[bstack11lll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᔡ")],
                bstack11lll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᔢ"): log[bstack11lll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᔣ")],
                bstack11lll_opy_ (u"ࠨࡪࡷࡸࡵࡥࡲࡦࡵࡳࡳࡳࡹࡥࠨᔤ"): {},
                bstack11lll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᔥ"): log[bstack11lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᔦ")],
            }
            if bstack11lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᔧ") in log:
                bstack1llll1ll111_opy_[bstack11lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᔨ")] = log[bstack11lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᔩ")]
            elif bstack11lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᔪ") in log:
                bstack1llll1ll111_opy_[bstack11lll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᔫ")] = log[bstack11lll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᔬ")]
            bstack1lllll1111l_opy_.append(bstack1llll1ll111_opy_)
        cls.bstack1l111l1lll_opy_({
            bstack11lll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᔭ"): bstack11lll_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨᔮ"),
            bstack11lll_opy_ (u"ࠬࡲ࡯ࡨࡵࠪᔯ"): bstack1lllll1111l_opy_
        })
    @classmethod
    @bstack1l111l1ll1_opy_(class_method=True)
    def bstack1llll1ll1ll_opy_(cls, steps):
        bstack1lllll11lll_opy_ = []
        for step in steps:
            bstack1llll1lll11_opy_ = {
                bstack11lll_opy_ (u"࠭࡫ࡪࡰࡧࠫᔰ"): bstack11lll_opy_ (u"ࠧࡕࡇࡖࡘࡤ࡙ࡔࡆࡒࠪᔱ"),
                bstack11lll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᔲ"): step[bstack11lll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᔳ")],
                bstack11lll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᔴ"): step[bstack11lll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᔵ")],
                bstack11lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᔶ"): step[bstack11lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᔷ")],
                bstack11lll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩᔸ"): step[bstack11lll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪᔹ")]
            }
            if bstack11lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᔺ") in step:
                bstack1llll1lll11_opy_[bstack11lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᔻ")] = step[bstack11lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᔼ")]
            elif bstack11lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᔽ") in step:
                bstack1llll1lll11_opy_[bstack11lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᔾ")] = step[bstack11lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᔿ")]
            bstack1lllll11lll_opy_.append(bstack1llll1lll11_opy_)
        cls.bstack1l111l1lll_opy_({
            bstack11lll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᕀ"): bstack11lll_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ᕁ"),
            bstack11lll_opy_ (u"ࠪࡰࡴ࡭ࡳࠨᕂ"): bstack1lllll11lll_opy_
        })
    @classmethod
    @bstack1l111l1ll1_opy_(class_method=True)
    def bstack1lll1111l1_opy_(cls, screenshot):
        cls.bstack1l111l1lll_opy_({
            bstack11lll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᕃ"): bstack11lll_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩᕄ"),
            bstack11lll_opy_ (u"࠭࡬ࡰࡩࡶࠫᕅ"): [{
                bstack11lll_opy_ (u"ࠧ࡬࡫ࡱࡨࠬᕆ"): bstack11lll_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࠪᕇ"),
                bstack11lll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᕈ"): datetime.datetime.utcnow().isoformat() + bstack11lll_opy_ (u"ࠪ࡞ࠬᕉ"),
                bstack11lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᕊ"): screenshot[bstack11lll_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫᕋ")],
                bstack11lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᕌ"): screenshot[bstack11lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᕍ")]
            }]
        }, bstack1llll1l1ll1_opy_=bstack11lll_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᕎ"))
    @classmethod
    @bstack1l111l1ll1_opy_(class_method=True)
    def bstack1lll111ll_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l111l1lll_opy_({
            bstack11lll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ᕏ"): bstack11lll_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧᕐ"),
            bstack11lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ᕑ"): {
                bstack11lll_opy_ (u"ࠧࡻࡵࡪࡦࠥᕒ"): cls.current_test_uuid(),
                bstack11lll_opy_ (u"ࠨࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠧᕓ"): cls.bstack1l111llll1_opy_(driver)
            }
        })
    @classmethod
    def on(cls):
        if os.environ.get(bstack11lll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠨᕔ"), None) is None or os.environ[bstack11lll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩᕕ")] == bstack11lll_opy_ (u"ࠤࡱࡹࡱࡲࠢᕖ"):
            return False
        return True
    @classmethod
    def bstack111ll111l_opy_(cls):
        return bstack1lll111l1l_opy_(cls.bs_config.get(bstack11lll_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᕗ"), False))
    @staticmethod
    def request_url(url):
        return bstack11lll_opy_ (u"ࠫࢀࢃ࠯ࡼࡿࠪᕘ").format(bstack1lllll11l11_opy_, url)
    @staticmethod
    def default_headers():
        headers = {
            bstack11lll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫᕙ"): bstack11lll_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩᕚ"),
            bstack11lll_opy_ (u"࡙ࠧ࠯ࡅࡗ࡙ࡇࡃࡌ࠯ࡗࡉࡘ࡚ࡏࡑࡕࠪᕛ"): bstack11lll_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᕜ")
        }
        if os.environ.get(bstack11lll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠪᕝ"), None):
            headers[bstack11lll_opy_ (u"ࠪࡅࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪᕞ")] = bstack11lll_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧᕟ").format(os.environ[bstack11lll_opy_ (u"ࠧࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙ࠨᕠ")])
        return headers
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack11lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᕡ"), None)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack11lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᕢ"), None)
    @staticmethod
    def bstack1l11l11lll_opy_():
        if getattr(threading.current_thread(), bstack11lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᕣ"), None):
            return {
                bstack11lll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᕤ"): bstack11lll_opy_ (u"ࠪࡸࡪࡹࡴࠨᕥ"),
                bstack11lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᕦ"): getattr(threading.current_thread(), bstack11lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᕧ"), None)
            }
        if getattr(threading.current_thread(), bstack11lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᕨ"), None):
            return {
                bstack11lll_opy_ (u"ࠧࡵࡻࡳࡩࠬᕩ"): bstack11lll_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᕪ"),
                bstack11lll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᕫ"): getattr(threading.current_thread(), bstack11lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᕬ"), None)
            }
        return None
    @staticmethod
    def bstack1l111llll1_opy_(driver):
        return {
            bstack11l11ll111_opy_(): bstack11l11l11ll_opy_(driver)
        }
    @staticmethod
    def bstack1lllll11l1l_opy_(exception_info, report):
        return [{bstack11lll_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᕭ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack11lll1l11l_opy_(typename):
        if bstack11lll_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣᕮ") in typename:
            return bstack11lll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢᕯ")
        return bstack11lll_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣᕰ")
    @staticmethod
    def bstack1lllll111l1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l111l11_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1l11l11111_opy_(test, hook_name=None):
        bstack1llll1ll11l_opy_ = test.parent
        if hook_name in [bstack11lll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭ᕱ"), bstack11lll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪᕲ"), bstack11lll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩᕳ"), bstack11lll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭ᕴ")]:
            bstack1llll1ll11l_opy_ = test
        scope = []
        while bstack1llll1ll11l_opy_ is not None:
            scope.append(bstack1llll1ll11l_opy_.name)
            bstack1llll1ll11l_opy_ = bstack1llll1ll11l_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1llll1l1lll_opy_(hook_type):
        if hook_type == bstack11lll_opy_ (u"ࠧࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠥᕵ"):
            return bstack11lll_opy_ (u"ࠨࡓࡦࡶࡸࡴࠥ࡮࡯ࡰ࡭ࠥᕶ")
        elif hook_type == bstack11lll_opy_ (u"ࠢࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠦᕷ"):
            return bstack11lll_opy_ (u"ࠣࡖࡨࡥࡷࡪ࡯ࡸࡰࠣ࡬ࡴࡵ࡫ࠣᕸ")
    @staticmethod
    def bstack1lllll11ll1_opy_(bstack1ll11l11ll_opy_):
        try:
            if not bstack1l111l11_opy_.on():
                return bstack1ll11l11ll_opy_
            if os.environ.get(bstack11lll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠢᕹ"), None) == bstack11lll_opy_ (u"ࠥࡸࡷࡻࡥࠣᕺ"):
                tests = os.environ.get(bstack11lll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠣᕻ"), None)
                if tests is None or tests == bstack11lll_opy_ (u"ࠧࡴࡵ࡭࡮ࠥᕼ"):
                    return bstack1ll11l11ll_opy_
                bstack1ll11l11ll_opy_ = tests.split(bstack11lll_opy_ (u"࠭ࠬࠨᕽ"))
                return bstack1ll11l11ll_opy_
        except Exception as exc:
            print(bstack11lll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡲࡦࡴࡸࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࡀࠠࠣᕾ"), str(exc))
        return bstack1ll11l11ll_opy_
    @classmethod
    def bstack1l11111l1l_opy_(cls, event: str, bstack11lllll1ll_opy_: bstack1l11ll1111_opy_):
        bstack11llllllll_opy_ = {
            bstack11lll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᕿ"): event,
            bstack11lllll1ll_opy_.bstack1l11111111_opy_(): bstack11lllll1ll_opy_.bstack1l111lll1l_opy_(event)
        }
        bstack1l111l11_opy_.bstack1l111l1lll_opy_(bstack11llllllll_opy_)