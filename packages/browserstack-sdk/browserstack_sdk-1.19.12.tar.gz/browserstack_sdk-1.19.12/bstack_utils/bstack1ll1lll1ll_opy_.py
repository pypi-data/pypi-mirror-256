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
import re
from bstack_utils.bstack1ll111ll1l_opy_ import bstack11111ll1l1_opy_
def bstack11111lll1l_opy_(fixture_name):
    if fixture_name.startswith(bstack11lll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᏸ")):
        return bstack11lll_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᏹ")
    elif fixture_name.startswith(bstack11lll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᏺ")):
        return bstack11lll_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱ࡲࡵࡤࡶ࡮ࡨࠫᏻ")
    elif fixture_name.startswith(bstack11lll_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᏼ")):
        return bstack11lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᏽ")
    elif fixture_name.startswith(bstack11lll_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭᏾")):
        return bstack11lll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱ࡲࡵࡤࡶ࡮ࡨࠫ᏿")
def bstack11111l111l_opy_(fixture_name):
    return bool(re.match(bstack11lll_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟ࠩࡨࡸࡲࡨࡺࡩࡰࡰࡿࡱࡴࡪࡵ࡭ࡧࠬࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨ᐀"), fixture_name))
def bstack11111l1lll_opy_(fixture_name):
    return bool(re.match(bstack11lll_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬᐁ"), fixture_name))
def bstack11111l1l11_opy_(fixture_name):
    return bool(re.match(bstack11lll_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬᐂ"), fixture_name))
def bstack11111l1ll1_opy_(fixture_name):
    if fixture_name.startswith(bstack11lll_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᐃ")):
        return bstack11lll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᐄ"), bstack11lll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ᐅ")
    elif fixture_name.startswith(bstack11lll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᐆ")):
        return bstack11lll_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡰࡳࡩࡻ࡬ࡦࠩᐇ"), bstack11lll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨᐈ")
    elif fixture_name.startswith(bstack11lll_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᐉ")):
        return bstack11lll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪᐊ"), bstack11lll_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫᐋ")
    elif fixture_name.startswith(bstack11lll_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᐌ")):
        return bstack11lll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱ࡲࡵࡤࡶ࡮ࡨࠫᐍ"), bstack11lll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭ᐎ")
    return None, None
def bstack11111l1l1l_opy_(hook_name):
    if hook_name in [bstack11lll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᐏ"), bstack11lll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧᐐ")]:
        return hook_name.capitalize()
    return hook_name
def bstack11111ll11l_opy_(hook_name):
    if hook_name in [bstack11lll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᐑ"), bstack11lll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ᐒ")]:
        return bstack11lll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ᐓ")
    elif hook_name in [bstack11lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨᐔ"), bstack11lll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨᐕ")]:
        return bstack11lll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨᐖ")
    elif hook_name in [bstack11lll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᐗ"), bstack11lll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨᐘ")]:
        return bstack11lll_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫᐙ")
    elif hook_name in [bstack11lll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪᐚ"), bstack11lll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪᐛ")]:
        return bstack11lll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭ᐜ")
    return hook_name
def bstack11111l11l1_opy_(node, scenario):
    if hasattr(node, bstack11lll_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭ᐝ")):
        parts = node.nodeid.rsplit(bstack11lll_opy_ (u"ࠧࡡࠢᐞ"))
        params = parts[-1]
        return bstack11lll_opy_ (u"ࠨࡻࡾࠢ࡞ࡿࢂࠨᐟ").format(scenario.name, params)
    return scenario.name
def bstack11111ll1ll_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack11lll_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᐠ")):
            examples = list(node.callspec.params[bstack11lll_opy_ (u"ࠨࡡࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡥࡹࡣࡰࡴࡱ࡫ࠧᐡ")].values())
        return examples
    except:
        return []
def bstack11111ll111_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack11111lll11_opy_(report):
    try:
        status = bstack11lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᐢ")
        if report.passed or (report.failed and hasattr(report, bstack11lll_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧᐣ"))):
            status = bstack11lll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᐤ")
        elif report.skipped:
            status = bstack11lll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᐥ")
        bstack11111ll1l1_opy_(status)
    except:
        pass
def bstack1llll111l_opy_(status):
    try:
        bstack11111l1111_opy_ = bstack11lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᐦ")
        if status == bstack11lll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᐧ"):
            bstack11111l1111_opy_ = bstack11lll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᐨ")
        elif status == bstack11lll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᐩ"):
            bstack11111l1111_opy_ = bstack11lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᐪ")
        bstack11111ll1l1_opy_(bstack11111l1111_opy_)
    except:
        pass
def bstack11111l11ll_opy_(item=None, report=None, summary=None, extra=None):
    return