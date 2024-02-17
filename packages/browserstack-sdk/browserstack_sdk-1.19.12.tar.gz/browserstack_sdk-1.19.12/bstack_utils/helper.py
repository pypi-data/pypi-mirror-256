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
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
from urllib.parse import urlparse
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import bstack11l1llllll_opy_, bstack1ll1l1l11l_opy_, bstack1lllll111_opy_, bstack1111l11l1_opy_
from bstack_utils.messages import bstack1111l1111_opy_, bstack1llll11l1l_opy_
from bstack_utils.proxy import bstack1ll1ll11l1_opy_, bstack1l11l1ll_opy_
bstack1ll11l1ll_opy_ = Config.bstack111llll1l_opy_()
def bstack11ll1l1111_opy_(config):
    return config[bstack11lll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᄽ")]
def bstack11ll1llll1_opy_(config):
    return config[bstack11lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᄾ")]
def bstack11l111l11_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11l1ll1l1l_opy_(obj):
    values = []
    bstack11l11llll1_opy_ = re.compile(bstack11lll_opy_ (u"ࡷࠨ࡞ࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣࡡࡪࠫࠥࠤᄿ"), re.I)
    for key in obj.keys():
        if bstack11l11llll1_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11l1ll11l1_opy_(config):
    tags = []
    tags.extend(bstack11l1ll1l1l_opy_(os.environ))
    tags.extend(bstack11l1ll1l1l_opy_(config))
    return tags
def bstack11l1ll1ll1_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11l1l1111l_opy_(bstack11l11l1111_opy_):
    if not bstack11l11l1111_opy_:
        return bstack11lll_opy_ (u"࠭ࠧᅀ")
    return bstack11lll_opy_ (u"ࠢࡼࡿࠣࠬࢀࢃࠩࠣᅁ").format(bstack11l11l1111_opy_.name, bstack11l11l1111_opy_.email)
def bstack11ll1l11l1_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11l1l1lll1_opy_ = repo.common_dir
        info = {
            bstack11lll_opy_ (u"ࠣࡵ࡫ࡥࠧᅂ"): repo.head.commit.hexsha,
            bstack11lll_opy_ (u"ࠤࡶ࡬ࡴࡸࡴࡠࡵ࡫ࡥࠧᅃ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack11lll_opy_ (u"ࠥࡦࡷࡧ࡮ࡤࡪࠥᅄ"): repo.active_branch.name,
            bstack11lll_opy_ (u"ࠦࡹࡧࡧࠣᅅ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack11lll_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡹ࡫ࡲࠣᅆ"): bstack11l1l1111l_opy_(repo.head.commit.committer),
            bstack11lll_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡺࡥࡳࡡࡧࡥࡹ࡫ࠢᅇ"): repo.head.commit.committed_datetime.isoformat(),
            bstack11lll_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࠢᅈ"): bstack11l1l1111l_opy_(repo.head.commit.author),
            bstack11lll_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࡠࡦࡤࡸࡪࠨᅉ"): repo.head.commit.authored_datetime.isoformat(),
            bstack11lll_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡡࡰࡩࡸࡹࡡࡨࡧࠥᅊ"): repo.head.commit.message,
            bstack11lll_opy_ (u"ࠥࡶࡴࡵࡴࠣᅋ"): repo.git.rev_parse(bstack11lll_opy_ (u"ࠦ࠲࠳ࡳࡩࡱࡺ࠱ࡹࡵࡰ࡭ࡧࡹࡩࡱࠨᅌ")),
            bstack11lll_opy_ (u"ࠧࡩ࡯࡮࡯ࡲࡲࡤ࡭ࡩࡵࡡࡧ࡭ࡷࠨᅍ"): bstack11l1l1lll1_opy_,
            bstack11lll_opy_ (u"ࠨࡷࡰࡴ࡮ࡸࡷ࡫ࡥࡠࡩ࡬ࡸࡤࡪࡩࡳࠤᅎ"): subprocess.check_output([bstack11lll_opy_ (u"ࠢࡨ࡫ࡷࠦᅏ"), bstack11lll_opy_ (u"ࠣࡴࡨࡺ࠲ࡶࡡࡳࡵࡨࠦᅐ"), bstack11lll_opy_ (u"ࠤ࠰࠱࡬࡯ࡴ࠮ࡥࡲࡱࡲࡵ࡮࠮ࡦ࡬ࡶࠧᅑ")]).strip().decode(
                bstack11lll_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᅒ")),
            bstack11lll_opy_ (u"ࠦࡱࡧࡳࡵࡡࡷࡥ࡬ࠨᅓ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack11lll_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡸࡥࡳࡪࡰࡦࡩࡤࡲࡡࡴࡶࡢࡸࡦ࡭ࠢᅔ"): repo.git.rev_list(
                bstack11lll_opy_ (u"ࠨࡻࡾ࠰࠱ࡿࢂࠨᅕ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11l1l1llll_opy_ = []
        for remote in remotes:
            bstack11l1l11111_opy_ = {
                bstack11lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᅖ"): remote.name,
                bstack11lll_opy_ (u"ࠣࡷࡵࡰࠧᅗ"): remote.url,
            }
            bstack11l1l1llll_opy_.append(bstack11l1l11111_opy_)
        return {
            bstack11lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᅘ"): bstack11lll_opy_ (u"ࠥ࡫࡮ࡺࠢᅙ"),
            **info,
            bstack11lll_opy_ (u"ࠦࡷ࡫࡭ࡰࡶࡨࡷࠧᅚ"): bstack11l1l1llll_opy_
        }
    except Exception as err:
        print(bstack11lll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡵࡰࡶ࡮ࡤࡸ࡮ࡴࡧࠡࡉ࡬ࡸࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣᅛ").format(err))
        return {}
def bstack1ll11llll1_opy_():
    env = os.environ
    if (bstack11lll_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠦᅜ") in env and len(env[bstack11lll_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧᅝ")]) > 0) or (
            bstack11lll_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠢᅞ") in env and len(env[bstack11lll_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣᅟ")]) > 0):
        return {
            bstack11lll_opy_ (u"ࠥࡲࡦࡳࡥࠣᅠ"): bstack11lll_opy_ (u"ࠦࡏ࡫࡮࡬࡫ࡱࡷࠧᅡ"),
            bstack11lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᅢ"): env.get(bstack11lll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᅣ")),
            bstack11lll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᅤ"): env.get(bstack11lll_opy_ (u"ࠣࡌࡒࡆࡤࡔࡁࡎࡇࠥᅥ")),
            bstack11lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᅦ"): env.get(bstack11lll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᅧ"))
        }
    if env.get(bstack11lll_opy_ (u"ࠦࡈࡏࠢᅨ")) == bstack11lll_opy_ (u"ࠧࡺࡲࡶࡧࠥᅩ") and bstack1lll111l1l_opy_(env.get(bstack11lll_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡉࡉࠣᅪ"))):
        return {
            bstack11lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᅫ"): bstack11lll_opy_ (u"ࠣࡅ࡬ࡶࡨࡲࡥࡄࡋࠥᅬ"),
            bstack11lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᅭ"): env.get(bstack11lll_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᅮ")),
            bstack11lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᅯ"): env.get(bstack11lll_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡐࡏࡃࠤᅰ")),
            bstack11lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᅱ"): env.get(bstack11lll_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࠥᅲ"))
        }
    if env.get(bstack11lll_opy_ (u"ࠣࡅࡌࠦᅳ")) == bstack11lll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᅴ") and bstack1lll111l1l_opy_(env.get(bstack11lll_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࠥᅵ"))):
        return {
            bstack11lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᅶ"): bstack11lll_opy_ (u"࡚ࠧࡲࡢࡸ࡬ࡷࠥࡉࡉࠣᅷ"),
            bstack11lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᅸ"): env.get(bstack11lll_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡃࡗࡌࡐࡉࡥࡗࡆࡄࡢ࡙ࡗࡒࠢᅹ")),
            bstack11lll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᅺ"): env.get(bstack11lll_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦᅻ")),
            bstack11lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᅼ"): env.get(bstack11lll_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᅽ"))
        }
    if env.get(bstack11lll_opy_ (u"ࠧࡉࡉࠣᅾ")) == bstack11lll_opy_ (u"ࠨࡴࡳࡷࡨࠦᅿ") and env.get(bstack11lll_opy_ (u"ࠢࡄࡋࡢࡒࡆࡓࡅࠣᆀ")) == bstack11lll_opy_ (u"ࠣࡥࡲࡨࡪࡹࡨࡪࡲࠥᆁ"):
        return {
            bstack11lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᆂ"): bstack11lll_opy_ (u"ࠥࡇࡴࡪࡥࡴࡪ࡬ࡴࠧᆃ"),
            bstack11lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᆄ"): None,
            bstack11lll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᆅ"): None,
            bstack11lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᆆ"): None
        }
    if env.get(bstack11lll_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡆࡗࡇࡎࡄࡊࠥᆇ")) and env.get(bstack11lll_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡈࡕࡍࡎࡋࡗࠦᆈ")):
        return {
            bstack11lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᆉ"): bstack11lll_opy_ (u"ࠥࡆ࡮ࡺࡢࡶࡥ࡮ࡩࡹࠨᆊ"),
            bstack11lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᆋ"): env.get(bstack11lll_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡉࡌࡘࡤࡎࡔࡕࡒࡢࡓࡗࡏࡇࡊࡐࠥᆌ")),
            bstack11lll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᆍ"): None,
            bstack11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᆎ"): env.get(bstack11lll_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᆏ"))
        }
    if env.get(bstack11lll_opy_ (u"ࠤࡆࡍࠧᆐ")) == bstack11lll_opy_ (u"ࠥࡸࡷࡻࡥࠣᆑ") and bstack1lll111l1l_opy_(env.get(bstack11lll_opy_ (u"ࠦࡉࡘࡏࡏࡇࠥᆒ"))):
        return {
            bstack11lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᆓ"): bstack11lll_opy_ (u"ࠨࡄࡳࡱࡱࡩࠧᆔ"),
            bstack11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᆕ"): env.get(bstack11lll_opy_ (u"ࠣࡆࡕࡓࡓࡋ࡟ࡃࡗࡌࡐࡉࡥࡌࡊࡐࡎࠦᆖ")),
            bstack11lll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᆗ"): None,
            bstack11lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᆘ"): env.get(bstack11lll_opy_ (u"ࠦࡉࡘࡏࡏࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᆙ"))
        }
    if env.get(bstack11lll_opy_ (u"ࠧࡉࡉࠣᆚ")) == bstack11lll_opy_ (u"ࠨࡴࡳࡷࡨࠦᆛ") and bstack1lll111l1l_opy_(env.get(bstack11lll_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࠥᆜ"))):
        return {
            bstack11lll_opy_ (u"ࠣࡰࡤࡱࡪࠨᆝ"): bstack11lll_opy_ (u"ࠤࡖࡩࡲࡧࡰࡩࡱࡵࡩࠧᆞ"),
            bstack11lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᆟ"): env.get(bstack11lll_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡐࡔࡊࡅࡓࡏ࡚ࡂࡖࡌࡓࡓࡥࡕࡓࡎࠥᆠ")),
            bstack11lll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᆡ"): env.get(bstack11lll_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦᆢ")),
            bstack11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᆣ"): env.get(bstack11lll_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡏࡕࡂࡠࡋࡇࠦᆤ"))
        }
    if env.get(bstack11lll_opy_ (u"ࠤࡆࡍࠧᆥ")) == bstack11lll_opy_ (u"ࠥࡸࡷࡻࡥࠣᆦ") and bstack1lll111l1l_opy_(env.get(bstack11lll_opy_ (u"ࠦࡌࡏࡔࡍࡃࡅࡣࡈࡏࠢᆧ"))):
        return {
            bstack11lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᆨ"): bstack11lll_opy_ (u"ࠨࡇࡪࡶࡏࡥࡧࠨᆩ"),
            bstack11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᆪ"): env.get(bstack11lll_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡗࡕࡐࠧᆫ")),
            bstack11lll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᆬ"): env.get(bstack11lll_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᆭ")),
            bstack11lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᆮ"): env.get(bstack11lll_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤࡏࡄࠣᆯ"))
        }
    if env.get(bstack11lll_opy_ (u"ࠨࡃࡊࠤᆰ")) == bstack11lll_opy_ (u"ࠢࡵࡴࡸࡩࠧᆱ") and bstack1lll111l1l_opy_(env.get(bstack11lll_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࠦᆲ"))):
        return {
            bstack11lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᆳ"): bstack11lll_opy_ (u"ࠥࡆࡺ࡯࡬ࡥ࡭࡬ࡸࡪࠨᆴ"),
            bstack11lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᆵ"): env.get(bstack11lll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᆶ")),
            bstack11lll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᆷ"): env.get(bstack11lll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡐࡆࡈࡅࡍࠤᆸ")) or env.get(bstack11lll_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡎࡂࡏࡈࠦᆹ")),
            bstack11lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᆺ"): env.get(bstack11lll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᆻ"))
        }
    if bstack1lll111l1l_opy_(env.get(bstack11lll_opy_ (u"࡙ࠦࡌ࡟ࡃࡗࡌࡐࡉࠨᆼ"))):
        return {
            bstack11lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᆽ"): bstack11lll_opy_ (u"ࠨࡖࡪࡵࡸࡥࡱࠦࡓࡵࡷࡧ࡭ࡴࠦࡔࡦࡣࡰࠤࡘ࡫ࡲࡷ࡫ࡦࡩࡸࠨᆾ"),
            bstack11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᆿ"): bstack11lll_opy_ (u"ࠣࡽࢀࡿࢂࠨᇀ").format(env.get(bstack11lll_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡆࡐࡗࡑࡈࡆ࡚ࡉࡐࡐࡖࡉࡗ࡜ࡅࡓࡗࡕࡍࠬᇁ")), env.get(bstack11lll_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡑࡔࡒࡎࡊࡉࡔࡊࡆࠪᇂ"))),
            bstack11lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᇃ"): env.get(bstack11lll_opy_ (u"࡙࡙ࠧࡔࡖࡈࡑࡤࡊࡅࡇࡋࡑࡍ࡙ࡏࡏࡏࡋࡇࠦᇄ")),
            bstack11lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᇅ"): env.get(bstack11lll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢᇆ"))
        }
    if bstack1lll111l1l_opy_(env.get(bstack11lll_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࠥᇇ"))):
        return {
            bstack11lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᇈ"): bstack11lll_opy_ (u"ࠥࡅࡵࡶࡶࡦࡻࡲࡶࠧᇉ"),
            bstack11lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᇊ"): bstack11lll_opy_ (u"ࠧࢁࡽ࠰ࡲࡵࡳ࡯࡫ࡣࡵ࠱ࡾࢁ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠦᇋ").format(env.get(bstack11lll_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡗࡕࡐࠬᇌ")), env.get(bstack11lll_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡄࡇࡈࡕࡕࡏࡖࡢࡒࡆࡓࡅࠨᇍ")), env.get(bstack11lll_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡔࡗࡕࡊࡆࡅࡗࡣࡘࡒࡕࡈࠩᇎ")), env.get(bstack11lll_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ᇏ"))),
            bstack11lll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᇐ"): env.get(bstack11lll_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᇑ")),
            bstack11lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᇒ"): env.get(bstack11lll_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᇓ"))
        }
    if env.get(bstack11lll_opy_ (u"ࠢࡂ࡜ࡘࡖࡊࡥࡈࡕࡖࡓࡣ࡚࡙ࡅࡓࡡࡄࡋࡊࡔࡔࠣᇔ")) and env.get(bstack11lll_opy_ (u"ࠣࡖࡉࡣࡇ࡛ࡉࡍࡆࠥᇕ")):
        return {
            bstack11lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᇖ"): bstack11lll_opy_ (u"ࠥࡅࡿࡻࡲࡦࠢࡆࡍࠧᇗ"),
            bstack11lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᇘ"): bstack11lll_opy_ (u"ࠧࢁࡽࡼࡿ࠲ࡣࡧࡻࡩ࡭ࡦ࠲ࡶࡪࡹࡵ࡭ࡶࡶࡃࡧࡻࡩ࡭ࡦࡌࡨࡂࢁࡽࠣᇙ").format(env.get(bstack11lll_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡊࡔ࡛ࡎࡅࡃࡗࡍࡔࡔࡓࡆࡔ࡙ࡉࡗ࡛ࡒࡊࠩᇚ")), env.get(bstack11lll_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡕࡘࡏࡋࡇࡆࡘࠬᇛ")), env.get(bstack11lll_opy_ (u"ࠨࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠨᇜ"))),
            bstack11lll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᇝ"): env.get(bstack11lll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥᇞ")),
            bstack11lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᇟ"): env.get(bstack11lll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧᇠ"))
        }
    if any([env.get(bstack11lll_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᇡ")), env.get(bstack11lll_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡖࡊ࡙ࡏࡍࡘࡈࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨᇢ")), env.get(bstack11lll_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡘࡕࡕࡓࡅࡈࡣ࡛ࡋࡒࡔࡋࡒࡒࠧᇣ"))]):
        return {
            bstack11lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᇤ"): bstack11lll_opy_ (u"ࠥࡅ࡜࡙ࠠࡄࡱࡧࡩࡇࡻࡩ࡭ࡦࠥᇥ"),
            bstack11lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᇦ"): env.get(bstack11lll_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡒࡘࡆࡑࡏࡃࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᇧ")),
            bstack11lll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᇨ"): env.get(bstack11lll_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᇩ")),
            bstack11lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᇪ"): env.get(bstack11lll_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢᇫ"))
        }
    if env.get(bstack11lll_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡐࡸࡱࡧ࡫ࡲࠣᇬ")):
        return {
            bstack11lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᇭ"): bstack11lll_opy_ (u"ࠧࡈࡡ࡮ࡤࡲࡳࠧᇮ"),
            bstack11lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᇯ"): env.get(bstack11lll_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡘࡥࡴࡷ࡯ࡸࡸ࡛ࡲ࡭ࠤᇰ")),
            bstack11lll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᇱ"): env.get(bstack11lll_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡶ࡬ࡴࡸࡴࡋࡱࡥࡒࡦࡳࡥࠣᇲ")),
            bstack11lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᇳ"): env.get(bstack11lll_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤᇴ"))
        }
    if env.get(bstack11lll_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࠨᇵ")) or env.get(bstack11lll_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡎࡃࡌࡒࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠣᇶ")):
        return {
            bstack11lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᇷ"): bstack11lll_opy_ (u"࡙ࠣࡨࡶࡨࡱࡥࡳࠤᇸ"),
            bstack11lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᇹ"): env.get(bstack11lll_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᇺ")),
            bstack11lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᇻ"): bstack11lll_opy_ (u"ࠧࡓࡡࡪࡰࠣࡔ࡮ࡶࡥ࡭࡫ࡱࡩࠧᇼ") if env.get(bstack11lll_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡎࡃࡌࡒࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠣᇽ")) else None,
            bstack11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᇾ"): env.get(bstack11lll_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡊࡍ࡙ࡥࡃࡐࡏࡐࡍ࡙ࠨᇿ"))
        }
    if any([env.get(bstack11lll_opy_ (u"ࠤࡊࡇࡕࡥࡐࡓࡑࡍࡉࡈ࡚ࠢሀ")), env.get(bstack11lll_opy_ (u"ࠥࡋࡈࡒࡏࡖࡆࡢࡔࡗࡕࡊࡆࡅࡗࠦሁ")), env.get(bstack11lll_opy_ (u"ࠦࡌࡕࡏࡈࡎࡈࡣࡈࡒࡏࡖࡆࡢࡔࡗࡕࡊࡆࡅࡗࠦሂ"))]):
        return {
            bstack11lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥሃ"): bstack11lll_opy_ (u"ࠨࡇࡰࡱࡪࡰࡪࠦࡃ࡭ࡱࡸࡨࠧሄ"),
            bstack11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥህ"): None,
            bstack11lll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥሆ"): env.get(bstack11lll_opy_ (u"ࠤࡓࡖࡔࡐࡅࡄࡖࡢࡍࡉࠨሇ")),
            bstack11lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤለ"): env.get(bstack11lll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨሉ"))
        }
    if env.get(bstack11lll_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࠣሊ")):
        return {
            bstack11lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦላ"): bstack11lll_opy_ (u"ࠢࡔࡪ࡬ࡴࡵࡧࡢ࡭ࡧࠥሌ"),
            bstack11lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦል"): env.get(bstack11lll_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣሎ")),
            bstack11lll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧሏ"): bstack11lll_opy_ (u"ࠦࡏࡵࡢࠡࠥࡾࢁࠧሐ").format(env.get(bstack11lll_opy_ (u"࡙ࠬࡈࡊࡒࡓࡅࡇࡒࡅࡠࡌࡒࡆࡤࡏࡄࠨሑ"))) if env.get(bstack11lll_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠤሒ")) else None,
            bstack11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨሓ"): env.get(bstack11lll_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥሔ"))
        }
    if bstack1lll111l1l_opy_(env.get(bstack11lll_opy_ (u"ࠤࡑࡉ࡙ࡒࡉࡇ࡛ࠥሕ"))):
        return {
            bstack11lll_opy_ (u"ࠥࡲࡦࡳࡥࠣሖ"): bstack11lll_opy_ (u"ࠦࡓ࡫ࡴ࡭࡫ࡩࡽࠧሗ"),
            bstack11lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣመ"): env.get(bstack11lll_opy_ (u"ࠨࡄࡆࡒࡏࡓ࡞ࡥࡕࡓࡎࠥሙ")),
            bstack11lll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤሚ"): env.get(bstack11lll_opy_ (u"ࠣࡕࡌࡘࡊࡥࡎࡂࡏࡈࠦማ")),
            bstack11lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣሜ"): env.get(bstack11lll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧም"))
        }
    if bstack1lll111l1l_opy_(env.get(bstack11lll_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣࡆࡉࡔࡊࡑࡑࡗࠧሞ"))):
        return {
            bstack11lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥሟ"): bstack11lll_opy_ (u"ࠨࡇࡪࡶࡋࡹࡧࠦࡁࡤࡶ࡬ࡳࡳࡹࠢሠ"),
            bstack11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥሡ"): bstack11lll_opy_ (u"ࠣࡽࢀ࠳ࢀࢃ࠯ࡢࡥࡷ࡭ࡴࡴࡳ࠰ࡴࡸࡲࡸ࠵ࡻࡾࠤሢ").format(env.get(bstack11lll_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡖࡉࡗ࡜ࡅࡓࡡࡘࡖࡑ࠭ሣ")), env.get(bstack11lll_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡖࡊࡖࡏࡔࡋࡗࡓࡗ࡟ࠧሤ")), env.get(bstack11lll_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗ࡛ࡎࡠࡋࡇࠫሥ"))),
            bstack11lll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢሦ"): env.get(bstack11lll_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡗࡐࡔࡎࡊࡑࡕࡗࠣሧ")),
            bstack11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨረ"): env.get(bstack11lll_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠࡔࡘࡒࡤࡏࡄࠣሩ"))
        }
    if env.get(bstack11lll_opy_ (u"ࠤࡆࡍࠧሪ")) == bstack11lll_opy_ (u"ࠥࡸࡷࡻࡥࠣራ") and env.get(bstack11lll_opy_ (u"࡛ࠦࡋࡒࡄࡇࡏࠦሬ")) == bstack11lll_opy_ (u"ࠧ࠷ࠢር"):
        return {
            bstack11lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦሮ"): bstack11lll_opy_ (u"ࠢࡗࡧࡵࡧࡪࡲࠢሯ"),
            bstack11lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦሰ"): bstack11lll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࡾࢁࠧሱ").format(env.get(bstack11lll_opy_ (u"࡚ࠪࡊࡘࡃࡆࡎࡢ࡙ࡗࡒࠧሲ"))),
            bstack11lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨሳ"): None,
            bstack11lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦሴ"): None,
        }
    if env.get(bstack11lll_opy_ (u"ࠨࡔࡆࡃࡐࡇࡎ࡚࡙ࡠࡘࡈࡖࡘࡏࡏࡏࠤስ")):
        return {
            bstack11lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧሶ"): bstack11lll_opy_ (u"ࠣࡖࡨࡥࡲࡩࡩࡵࡻࠥሷ"),
            bstack11lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧሸ"): None,
            bstack11lll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧሹ"): env.get(bstack11lll_opy_ (u"࡙ࠦࡋࡁࡎࡅࡌࡘ࡞ࡥࡐࡓࡑࡍࡉࡈ࡚࡟ࡏࡃࡐࡉࠧሺ")),
            bstack11lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦሻ"): env.get(bstack11lll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧሼ"))
        }
    if any([env.get(bstack11lll_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࠥሽ")), env.get(bstack11lll_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡚ࡘࡌࠣሾ")), env.get(bstack11lll_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠢሿ")), env.get(bstack11lll_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡔࡆࡃࡐࠦቀ"))]):
        return {
            bstack11lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤቁ"): bstack11lll_opy_ (u"ࠧࡉ࡯࡯ࡥࡲࡹࡷࡹࡥࠣቂ"),
            bstack11lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤቃ"): None,
            bstack11lll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤቄ"): env.get(bstack11lll_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤቅ")) or None,
            bstack11lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣቆ"): env.get(bstack11lll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧቇ"), 0)
        }
    if env.get(bstack11lll_opy_ (u"ࠦࡌࡕ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤቈ")):
        return {
            bstack11lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ቉"): bstack11lll_opy_ (u"ࠨࡇࡰࡅࡇࠦቊ"),
            bstack11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥቋ"): None,
            bstack11lll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥቌ"): env.get(bstack11lll_opy_ (u"ࠤࡊࡓࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢቍ")),
            bstack11lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ቎"): env.get(bstack11lll_opy_ (u"ࠦࡌࡕ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡆࡓ࡚ࡔࡔࡆࡔࠥ቏"))
        }
    if env.get(bstack11lll_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥቐ")):
        return {
            bstack11lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦቑ"): bstack11lll_opy_ (u"ࠢࡄࡱࡧࡩࡋࡸࡥࡴࡪࠥቒ"),
            bstack11lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦቓ"): env.get(bstack11lll_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣቔ")),
            bstack11lll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧቕ"): env.get(bstack11lll_opy_ (u"ࠦࡈࡌ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡑࡅࡒࡋࠢቖ")),
            bstack11lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ቗"): env.get(bstack11lll_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦቘ"))
        }
    return {bstack11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ቙"): None}
def get_host_info():
    return {
        bstack11lll_opy_ (u"ࠣࡪࡲࡷࡹࡴࡡ࡮ࡧࠥቚ"): platform.node(),
        bstack11lll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦቛ"): platform.system(),
        bstack11lll_opy_ (u"ࠥࡸࡾࡶࡥࠣቜ"): platform.machine(),
        bstack11lll_opy_ (u"ࠦࡻ࡫ࡲࡴ࡫ࡲࡲࠧቝ"): platform.version(),
        bstack11lll_opy_ (u"ࠧࡧࡲࡤࡪࠥ቞"): platform.architecture()[0]
    }
def bstack1ll1llll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11l11ll111_opy_():
    if bstack1ll11l1ll_opy_.get_property(bstack11lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ቟")):
        return bstack11lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭በ")
    return bstack11lll_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࡡࡪࡶ࡮ࡪࠧቡ")
def bstack11l11l11ll_opy_(driver):
    info = {
        bstack11lll_opy_ (u"ࠩࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨቢ"): driver.capabilities,
        bstack11lll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠧባ"): driver.session_id,
        bstack11lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬቤ"): driver.capabilities.get(bstack11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪብ"), None),
        bstack11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨቦ"): driver.capabilities.get(bstack11lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨቧ"), None),
        bstack11lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪቨ"): driver.capabilities.get(bstack11lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨቩ"), None),
    }
    if bstack11l11ll111_opy_() == bstack11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩቪ"):
        info[bstack11lll_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬቫ")] = bstack11lll_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫቬ") if bstack11llll111_opy_() else bstack11lll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨቭ")
    return info
def bstack11llll111_opy_():
    if bstack1ll11l1ll_opy_.get_property(bstack11lll_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ቮ")):
        return True
    if bstack1lll111l1l_opy_(os.environ.get(bstack11lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩቯ"), None)):
        return True
    return False
def bstack1lll11l1ll_opy_(bstack11l1llll1l_opy_, url, data, config):
    headers = config.get(bstack11lll_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪተ"), None)
    proxies = bstack1ll1ll11l1_opy_(config, url)
    auth = config.get(bstack11lll_opy_ (u"ࠪࡥࡺࡺࡨࠨቱ"), None)
    response = requests.request(
            bstack11l1llll1l_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1llll111ll_opy_(bstack11l111ll_opy_, size):
    bstack1l11llll1l_opy_ = []
    while len(bstack11l111ll_opy_) > size:
        bstack1ll1ll1ll_opy_ = bstack11l111ll_opy_[:size]
        bstack1l11llll1l_opy_.append(bstack1ll1ll1ll_opy_)
        bstack11l111ll_opy_ = bstack11l111ll_opy_[size:]
    bstack1l11llll1l_opy_.append(bstack11l111ll_opy_)
    return bstack1l11llll1l_opy_
def bstack11l1llll11_opy_(message, bstack11l1l111ll_opy_=False):
    os.write(1, bytes(message, bstack11lll_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪቲ")))
    os.write(1, bytes(bstack11lll_opy_ (u"ࠬࡢ࡮ࠨታ"), bstack11lll_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬቴ")))
    if bstack11l1l111ll_opy_:
        with open(bstack11lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠭ࡰ࠳࠴ࡽ࠲࠭ት") + os.environ[bstack11lll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧቶ")] + bstack11lll_opy_ (u"ࠩ࠱ࡰࡴ࡭ࠧቷ"), bstack11lll_opy_ (u"ࠪࡥࠬቸ")) as f:
            f.write(message + bstack11lll_opy_ (u"ࠫࡡࡴࠧቹ"))
def bstack11l11l111l_opy_():
    return os.environ[bstack11lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨቺ")].lower() == bstack11lll_opy_ (u"࠭ࡴࡳࡷࡨࠫቻ")
def bstack1l1l1l1l11_opy_(bstack11l1l1ll1l_opy_):
    return bstack11lll_opy_ (u"ࠧࡼࡿ࠲ࡿࢂ࠭ቼ").format(bstack11l1llllll_opy_, bstack11l1l1ll1l_opy_)
def bstack1ll1ll1lll_opy_():
    return datetime.datetime.utcnow().isoformat() + bstack11lll_opy_ (u"ࠨ࡜ࠪች")
def bstack11l1ll11ll_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack11lll_opy_ (u"ࠩ࡝ࠫቾ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack11lll_opy_ (u"ࠪ࡞ࠬቿ")))).total_seconds() * 1000
def bstack11l111lll1_opy_(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp).isoformat() + bstack11lll_opy_ (u"ࠫ࡟࠭ኀ")
def bstack11l111llll_opy_(bstack11l1l11l11_opy_):
    date_format = bstack11lll_opy_ (u"࡙ࠬࠫࠦ࡯ࠨࡨࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪ࠮ࠦࡨࠪኁ")
    bstack11l111l1ll_opy_ = datetime.datetime.strptime(bstack11l1l11l11_opy_, date_format)
    return bstack11l111l1ll_opy_.isoformat() + bstack11lll_opy_ (u"࡚࠭ࠨኂ")
def bstack11l11l1l11_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack11lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧኃ")
    else:
        return bstack11lll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨኄ")
def bstack1lll111l1l_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack11lll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧኅ")
def bstack11l11l11l1_opy_(val):
    return val.__str__().lower() == bstack11lll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩኆ")
def bstack1l111l1ll1_opy_(bstack11l1l11ll1_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l1l11ll1_opy_ as e:
                print(bstack11lll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦኇ").format(func.__name__, bstack11l1l11ll1_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11l111ll11_opy_(bstack11l1l1l1l1_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11l1l1l1l1_opy_(cls, *args, **kwargs)
            except bstack11l1l11ll1_opy_ as e:
                print(bstack11lll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡻࡾࠢ࠰ࡂࠥࢁࡽ࠻ࠢࡾࢁࠧኈ").format(bstack11l1l1l1l1_opy_.__name__, bstack11l1l11ll1_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11l111ll11_opy_
    else:
        return decorator
def bstack1l1llll11l_opy_(bstack11llll1111_opy_):
    if bstack11lll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ኉") in bstack11llll1111_opy_ and bstack11l11l11l1_opy_(bstack11llll1111_opy_[bstack11lll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫኊ")]):
        return False
    if bstack11lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪኋ") in bstack11llll1111_opy_ and bstack11l11l11l1_opy_(bstack11llll1111_opy_[bstack11lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫኌ")]):
        return False
    return True
def bstack1lll1lll1l_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1ll111ll11_opy_(hub_url):
    if bstack1l1111l1_opy_() <= version.parse(bstack11lll_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪኍ")):
        if hub_url != bstack11lll_opy_ (u"ࠫࠬ኎"):
            return bstack11lll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨ኏") + hub_url + bstack11lll_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥነ")
        return bstack1lllll111_opy_
    if hub_url != bstack11lll_opy_ (u"ࠧࠨኑ"):
        return bstack11lll_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥኒ") + hub_url + bstack11lll_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥና")
    return bstack1111l11l1_opy_
def bstack11l11l1l1l_opy_():
    return isinstance(os.getenv(bstack11lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡐ࡚ࡍࡉࡏࠩኔ")), str)
def bstack11l1ll1l1_opy_(url):
    return urlparse(url).hostname
def bstack11l1l1l11_opy_(hostname):
    for bstack111111111_opy_ in bstack1ll1l1l11l_opy_:
        regex = re.compile(bstack111111111_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l11ll1ll_opy_(bstack11l1l1ll11_opy_, file_name, logger):
    bstack1l1ll1111l_opy_ = os.path.join(os.path.expanduser(bstack11lll_opy_ (u"ࠫࢃ࠭ን")), bstack11l1l1ll11_opy_)
    try:
        if not os.path.exists(bstack1l1ll1111l_opy_):
            os.makedirs(bstack1l1ll1111l_opy_)
        file_path = os.path.join(os.path.expanduser(bstack11lll_opy_ (u"ࠬࢄࠧኖ")), bstack11l1l1ll11_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack11lll_opy_ (u"࠭ࡷࠨኗ")):
                pass
            with open(file_path, bstack11lll_opy_ (u"ࠢࡸ࠭ࠥኘ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1111l1111_opy_.format(str(e)))
def bstack11l1l1l11l_opy_(file_name, key, value, logger):
    file_path = bstack11l11ll1ll_opy_(bstack11lll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨኙ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1111l1ll_opy_ = json.load(open(file_path, bstack11lll_opy_ (u"ࠩࡵࡦࠬኚ")))
        else:
            bstack1111l1ll_opy_ = {}
        bstack1111l1ll_opy_[key] = value
        with open(file_path, bstack11lll_opy_ (u"ࠥࡻ࠰ࠨኛ")) as outfile:
            json.dump(bstack1111l1ll_opy_, outfile)
def bstack111l11111_opy_(file_name, logger):
    file_path = bstack11l11ll1ll_opy_(bstack11lll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫኜ"), file_name, logger)
    bstack1111l1ll_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack11lll_opy_ (u"ࠬࡸࠧኝ")) as bstack111l1l1l1_opy_:
            bstack1111l1ll_opy_ = json.load(bstack111l1l1l1_opy_)
    return bstack1111l1ll_opy_
def bstack11111l11_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack11lll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡪ࡮ࡲࡥ࠻ࠢࠪኞ") + file_path + bstack11lll_opy_ (u"ࠧࠡࠩኟ") + str(e))
def bstack1l1111l1_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack11lll_opy_ (u"ࠣ࠾ࡑࡓ࡙࡙ࡅࡕࡀࠥአ")
def bstack1lll111l1_opy_(config):
    if bstack11lll_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨኡ") in config:
        del (config[bstack11lll_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩኢ")])
        return False
    if bstack1l1111l1_opy_() < version.parse(bstack11lll_opy_ (u"ࠫ࠸࠴࠴࠯࠲ࠪኣ")):
        return False
    if bstack1l1111l1_opy_() >= version.parse(bstack11lll_opy_ (u"ࠬ࠺࠮࠲࠰࠸ࠫኤ")):
        return True
    if bstack11lll_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭እ") in config and config[bstack11lll_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧኦ")] is False:
        return False
    else:
        return True
def bstack11111llll_opy_(args_list, bstack11l1lll1ll_opy_):
    index = -1
    for value in bstack11l1lll1ll_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1l11ll1ll1_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1l11ll1ll1_opy_ = bstack1l11ll1ll1_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack11lll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨኧ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack11lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩከ"), exception=exception)
    def bstack11lll1l11l_opy_(self):
        if self.result != bstack11lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪኩ"):
            return None
        if bstack11lll_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢኪ") in self.exception_type:
            return bstack11lll_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨካ")
        return bstack11lll_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢኬ")
    def bstack11l1ll1111_opy_(self):
        if self.result != bstack11lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧክ"):
            return None
        if self.bstack1l11ll1ll1_opy_:
            return self.bstack1l11ll1ll1_opy_
        return bstack11l11l1lll_opy_(self.exception)
def bstack11l11l1lll_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11l1lll111_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack11ll1l1ll_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1l1lll11l_opy_(config, logger):
    try:
        import playwright
        bstack11l11lllll_opy_ = playwright.__file__
        bstack11l1lll11l_opy_ = os.path.split(bstack11l11lllll_opy_)
        bstack11l11ll11l_opy_ = bstack11l1lll11l_opy_[0] + bstack11lll_opy_ (u"ࠨ࠱ࡧࡶ࡮ࡼࡥࡳ࠱ࡳࡥࡨࡱࡡࡨࡧ࠲ࡰ࡮ࡨ࠯ࡤ࡮࡬࠳ࡨࡲࡩ࠯࡬ࡶࠫኮ")
        os.environ[bstack11lll_opy_ (u"ࠩࡊࡐࡔࡈࡁࡍࡡࡄࡋࡊࡔࡔࡠࡊࡗࡘࡕࡥࡐࡓࡑ࡛࡝ࠬኯ")] = bstack1l11l1ll_opy_(config)
        with open(bstack11l11ll11l_opy_, bstack11lll_opy_ (u"ࠪࡶࠬኰ")) as f:
            bstack1l1l1lll_opy_ = f.read()
            bstack11l111ll1l_opy_ = bstack11lll_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠪ኱")
            bstack11l1ll111l_opy_ = bstack1l1l1lll_opy_.find(bstack11l111ll1l_opy_)
            if bstack11l1ll111l_opy_ == -1:
              process = subprocess.Popen(bstack11lll_opy_ (u"ࠧࡴࡰ࡮ࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠤኲ"), shell=True, cwd=bstack11l1lll11l_opy_[0])
              process.wait()
              bstack11l1lll1l1_opy_ = bstack11lll_opy_ (u"࠭ࠢࡶࡵࡨࠤࡸࡺࡲࡪࡥࡷࠦࡀ࠭ኳ")
              bstack11l1ll1lll_opy_ = bstack11lll_opy_ (u"ࠢࠣࠤࠣࡠࠧࡻࡳࡦࠢࡶࡸࡷ࡯ࡣࡵ࡞ࠥ࠿ࠥࡩ࡯࡯ࡵࡷࠤࢀࠦࡢࡰࡱࡷࡷࡹࡸࡡࡱࠢࢀࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨࠨࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠧࠪ࠽ࠣ࡭࡫ࠦࠨࡱࡴࡲࡧࡪࡹࡳ࠯ࡧࡱࡺ࠳ࡍࡌࡐࡄࡄࡐࡤࡇࡇࡆࡐࡗࡣࡍ࡚ࡔࡑࡡࡓࡖࡔ࡞࡙ࠪࠢࡥࡳࡴࡺࡳࡵࡴࡤࡴ࠭࠯࠻ࠡࠤࠥࠦኴ")
              bstack11l1l1l111_opy_ = bstack1l1l1lll_opy_.replace(bstack11l1lll1l1_opy_, bstack11l1ll1lll_opy_)
              with open(bstack11l11ll11l_opy_, bstack11lll_opy_ (u"ࠨࡹࠪኵ")) as f:
                f.write(bstack11l1l1l111_opy_)
    except Exception as e:
        logger.error(bstack1llll11l1l_opy_.format(str(e)))
def bstack111llll1_opy_():
  try:
    bstack11l1l11l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack11lll_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯࠲࡯ࡹ࡯࡯ࠩ኶"))
    bstack11l1ll1l11_opy_ = []
    if os.path.exists(bstack11l1l11l1l_opy_):
      with open(bstack11l1l11l1l_opy_) as f:
        bstack11l1ll1l11_opy_ = json.load(f)
      os.remove(bstack11l1l11l1l_opy_)
    return bstack11l1ll1l11_opy_
  except:
    pass
  return []
def bstack1lllllll1l_opy_(bstack1llll1lll_opy_):
  try:
    bstack11l1ll1l11_opy_ = []
    bstack11l1l11l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack11lll_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰ࠳ࡰࡳࡰࡰࠪ኷"))
    if os.path.exists(bstack11l1l11l1l_opy_):
      with open(bstack11l1l11l1l_opy_) as f:
        bstack11l1ll1l11_opy_ = json.load(f)
    bstack11l1ll1l11_opy_.append(bstack1llll1lll_opy_)
    with open(bstack11l1l11l1l_opy_, bstack11lll_opy_ (u"ࠫࡼ࠭ኸ")) as f:
        json.dump(bstack11l1ll1l11_opy_, f)
  except:
    pass
def bstack1l1l1lllll_opy_(logger, bstack11l11lll11_opy_ = False):
  try:
    test_name = os.environ.get(bstack11lll_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨኹ"), bstack11lll_opy_ (u"࠭ࠧኺ"))
    if test_name == bstack11lll_opy_ (u"ࠧࠨኻ"):
        test_name = threading.current_thread().__dict__.get(bstack11lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡃࡦࡧࡣࡹ࡫ࡳࡵࡡࡱࡥࡲ࡫ࠧኼ"), bstack11lll_opy_ (u"ࠩࠪኽ"))
    bstack11l1l1l1ll_opy_ = bstack11lll_opy_ (u"ࠪ࠰ࠥ࠭ኾ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11l11lll11_opy_:
        bstack1l111l1l_opy_ = os.environ.get(bstack11lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ኿"), bstack11lll_opy_ (u"ࠬ࠶ࠧዀ"))
        bstack11ll11111_opy_ = {bstack11lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ዁"): test_name, bstack11lll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ዂ"): bstack11l1l1l1ll_opy_, bstack11lll_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧዃ"): bstack1l111l1l_opy_}
        bstack11l11lll1l_opy_ = []
        bstack11l11l1ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack11lll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡳࡴࡵࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨዄ"))
        if os.path.exists(bstack11l11l1ll1_opy_):
            with open(bstack11l11l1ll1_opy_) as f:
                bstack11l11lll1l_opy_ = json.load(f)
        bstack11l11lll1l_opy_.append(bstack11ll11111_opy_)
        with open(bstack11l11l1ll1_opy_, bstack11lll_opy_ (u"ࠪࡻࠬዅ")) as f:
            json.dump(bstack11l11lll1l_opy_, f)
    else:
        bstack11ll11111_opy_ = {bstack11lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ዆"): test_name, bstack11lll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ዇"): bstack11l1l1l1ll_opy_, bstack11lll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬወ"): str(multiprocessing.current_process().name)}
        if bstack11lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷࠫዉ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack11ll11111_opy_)
  except Exception as e:
      logger.warn(bstack11lll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡴࡾࡺࡥࡴࡶࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧዊ").format(e))
def bstack11111lll1_opy_(error_message, test_name, index, logger):
  try:
    bstack11l1l11lll_opy_ = []
    bstack11ll11111_opy_ = {bstack11lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧዋ"): test_name, bstack11lll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩዌ"): error_message, bstack11lll_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪው"): index}
    bstack11l1l111l1_opy_ = os.path.join(tempfile.gettempdir(), bstack11lll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ዎ"))
    if os.path.exists(bstack11l1l111l1_opy_):
        with open(bstack11l1l111l1_opy_) as f:
            bstack11l1l11lll_opy_ = json.load(f)
    bstack11l1l11lll_opy_.append(bstack11ll11111_opy_)
    with open(bstack11l1l111l1_opy_, bstack11lll_opy_ (u"࠭ࡷࠨዏ")) as f:
        json.dump(bstack11l1l11lll_opy_, f)
  except Exception as e:
    logger.warn(bstack11lll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡵࡳࡧࡵࡴࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥዐ").format(e))
def bstack11ll111l1_opy_(bstack1l1llll1l_opy_, name, logger):
  try:
    bstack11ll11111_opy_ = {bstack11lll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ዑ"): name, bstack11lll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨዒ"): bstack1l1llll1l_opy_, bstack11lll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩዓ"): str(threading.current_thread()._name)}
    return bstack11ll11111_opy_
  except Exception as e:
    logger.warn(bstack11lll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡢࡦࡪࡤࡺࡪࠦࡦࡶࡰࡱࡩࡱࠦࡤࡢࡶࡤ࠾ࠥࢁࡽࠣዔ").format(e))
  return
def bstack11l11ll1l1_opy_():
    return platform.system() == bstack11lll_opy_ (u"ࠬ࡝ࡩ࡯ࡦࡲࡻࡸ࠭ዕ")