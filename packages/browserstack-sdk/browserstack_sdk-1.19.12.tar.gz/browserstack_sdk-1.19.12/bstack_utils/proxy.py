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
from urllib.parse import urlparse
from bstack_utils.messages import bstack111ll1l11l_opy_
def bstack1111l1111l_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack11111llll1_opy_(bstack1111l11l11_opy_, bstack1111l111l1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1111l11l11_opy_):
        with open(bstack1111l11l11_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1111l1111l_opy_(bstack1111l11l11_opy_):
        pac = get_pac(url=bstack1111l11l11_opy_)
    else:
        raise Exception(bstack11lll_opy_ (u"ࠧࡑࡣࡦࠤ࡫࡯࡬ࡦࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶ࠽ࠤࢀࢃࠧᏓ").format(bstack1111l11l11_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack11lll_opy_ (u"ࠣ࠺࠱࠼࠳࠾࠮࠹ࠤᏔ"), 80))
        bstack1111l111ll_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1111l111ll_opy_ = bstack11lll_opy_ (u"ࠩ࠳࠲࠵࠴࠰࠯࠲ࠪᏕ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1111l111l1_opy_, bstack1111l111ll_opy_)
    return proxy_url
def bstack1l1ll11ll1_opy_(config):
    return bstack11lll_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭Ꮦ") in config or bstack11lll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᏗ") in config
def bstack1l11l1ll_opy_(config):
    if not bstack1l1ll11ll1_opy_(config):
        return
    if config.get(bstack11lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᏘ")):
        return config.get(bstack11lll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᏙ"))
    if config.get(bstack11lll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᏚ")):
        return config.get(bstack11lll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᏛ"))
def bstack1ll1ll11l1_opy_(config, bstack1111l111l1_opy_):
    proxy = bstack1l11l1ll_opy_(config)
    proxies = {}
    if config.get(bstack11lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᏜ")) or config.get(bstack11lll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᏝ")):
        if proxy.endswith(bstack11lll_opy_ (u"ࠫ࠳ࡶࡡࡤࠩᏞ")):
            proxies = bstack111111ll_opy_(proxy, bstack1111l111l1_opy_)
        else:
            proxies = {
                bstack11lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᏟ"): proxy
            }
    return proxies
def bstack111111ll_opy_(bstack1111l11l11_opy_, bstack1111l111l1_opy_):
    proxies = {}
    global bstack1111l11111_opy_
    if bstack11lll_opy_ (u"࠭ࡐࡂࡅࡢࡔࡗࡕࡘ࡚ࠩᏠ") in globals():
        return bstack1111l11111_opy_
    try:
        proxy = bstack11111llll1_opy_(bstack1111l11l11_opy_, bstack1111l111l1_opy_)
        if bstack11lll_opy_ (u"ࠢࡅࡋࡕࡉࡈ࡚ࠢᏡ") in proxy:
            proxies = {}
        elif bstack11lll_opy_ (u"ࠣࡊࡗࡘࡕࠨᏢ") in proxy or bstack11lll_opy_ (u"ࠤࡋࡘ࡙ࡖࡓࠣᏣ") in proxy or bstack11lll_opy_ (u"ࠥࡗࡔࡉࡋࡔࠤᏤ") in proxy:
            bstack11111lllll_opy_ = proxy.split(bstack11lll_opy_ (u"ࠦࠥࠨᏥ"))
            if bstack11lll_opy_ (u"ࠧࡀ࠯࠰ࠤᏦ") in bstack11lll_opy_ (u"ࠨࠢᏧ").join(bstack11111lllll_opy_[1:]):
                proxies = {
                    bstack11lll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭Ꮸ"): bstack11lll_opy_ (u"ࠣࠤᏩ").join(bstack11111lllll_opy_[1:])
                }
            else:
                proxies = {
                    bstack11lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᏪ"): str(bstack11111lllll_opy_[0]).lower() + bstack11lll_opy_ (u"ࠥ࠾࠴࠵ࠢᏫ") + bstack11lll_opy_ (u"ࠦࠧᏬ").join(bstack11111lllll_opy_[1:])
                }
        elif bstack11lll_opy_ (u"ࠧࡖࡒࡐ࡚࡜ࠦᏭ") in proxy:
            bstack11111lllll_opy_ = proxy.split(bstack11lll_opy_ (u"ࠨࠠࠣᏮ"))
            if bstack11lll_opy_ (u"ࠢ࠻࠱࠲ࠦᏯ") in bstack11lll_opy_ (u"ࠣࠤᏰ").join(bstack11111lllll_opy_[1:]):
                proxies = {
                    bstack11lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᏱ"): bstack11lll_opy_ (u"ࠥࠦᏲ").join(bstack11111lllll_opy_[1:])
                }
            else:
                proxies = {
                    bstack11lll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᏳ"): bstack11lll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨᏴ") + bstack11lll_opy_ (u"ࠨࠢᏵ").join(bstack11111lllll_opy_[1:])
                }
        else:
            proxies = {
                bstack11lll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭᏶"): proxy
            }
    except Exception as e:
        print(bstack11lll_opy_ (u"ࠣࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠧ᏷"), bstack111ll1l11l_opy_.format(bstack1111l11l11_opy_, str(e)))
    bstack1111l11111_opy_ = proxies
    return proxies