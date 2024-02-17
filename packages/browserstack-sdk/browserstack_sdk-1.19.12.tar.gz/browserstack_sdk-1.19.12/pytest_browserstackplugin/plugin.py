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
import atexit
import datetime
import inspect
import logging
import os
import signal
import sys
import threading
from uuid import uuid4
from bstack_utils.percy_sdk import PercySDK
import tempfile
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1l1lll1lll_opy_, bstack1llll1111l_opy_, update, bstack111l1lll1_opy_,
                                       bstack11l11111l_opy_, bstack1l1lllll1l_opy_, bstack1l1l1l1l_opy_, bstack1111l1l11_opy_,
                                       bstack11l11l111_opy_, bstack111l111l1_opy_, bstack1l11l11l1_opy_, bstack1l1ll111l_opy_,
                                       bstack1l1ll1l1ll_opy_, getAccessibilityResults, getAccessibilityResultsSummary)
from browserstack_sdk.bstack11llllll_opy_ import bstack11l1lll1_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack11lll1ll_opy_
from bstack_utils.capture import bstack1l11l11ll1_opy_
from bstack_utils.config import Config
from bstack_utils.constants import bstack1111111ll_opy_, bstack1l111llll_opy_, bstack11111l111_opy_, \
    bstack1lll1l1lll_opy_
from bstack_utils.helper import bstack11ll1l1ll_opy_, bstack1ll1llll_opy_, bstack11l11l111l_opy_, bstack1ll1ll1lll_opy_, \
    bstack11l11l1l11_opy_, \
    bstack11l1ll1ll1_opy_, bstack1l1111l1_opy_, bstack1ll111ll11_opy_, bstack11l11l1l1l_opy_, bstack1lll1lll1l_opy_, Notset, \
    bstack1lll111l1_opy_, bstack11l1ll11ll_opy_, bstack11l11l1lll_opy_, Result, bstack11l111lll1_opy_, bstack11l1lll111_opy_, bstack1l111l1ll1_opy_, \
    bstack1lllllll1l_opy_, bstack1l1l1lllll_opy_, bstack1lll111l1l_opy_, bstack11l11ll1l1_opy_
from bstack_utils.bstack11l1111lll_opy_ import bstack11l111111l_opy_
from bstack_utils.messages import bstack1ll1llll11_opy_, bstack1lll11l111_opy_, bstack111lll11l_opy_, bstack11lll1ll1_opy_, bstack111lll1ll_opy_, \
    bstack1llll11l1l_opy_, bstack1l1l11l11_opy_, bstack1l1l11ll11_opy_, bstack1l1ll11111_opy_, bstack11l1ll1ll_opy_, \
    bstack1l1l11l1l_opy_, bstack11llll11l_opy_
from bstack_utils.proxy import bstack1l11l1ll_opy_, bstack111111ll_opy_
from bstack_utils.bstack1ll1lll1ll_opy_ import bstack11111l11ll_opy_, bstack11111l1l1l_opy_, bstack11111ll11l_opy_, bstack11111l1lll_opy_, \
    bstack11111l1l11_opy_, bstack11111l11l1_opy_, bstack11111ll111_opy_, bstack1llll111l_opy_, bstack11111lll11_opy_
from bstack_utils.bstack1l1ll111l1_opy_ import bstack1111l1l1l_opy_
from bstack_utils.bstack1ll111ll1l_opy_ import bstack1ll111llll_opy_, bstack11ll1l11_opy_, bstack11l1ll111_opy_, \
    bstack111l1l11_opy_, bstack11lll111l_opy_
from bstack_utils.bstack1l11111ll1_opy_ import bstack1l1111llll_opy_
from bstack_utils.bstack1lll1l1ll1_opy_ import bstack1l111l11_opy_
import bstack_utils.bstack1ll11ll111_opy_ as bstack1l11lll1_opy_
bstack1lll11l1l_opy_ = None
bstack1llll1ll1_opy_ = None
bstack11llll1l_opy_ = None
bstack1llll1l1l1_opy_ = None
bstack1l1ll1llll_opy_ = None
bstack1ll1111l1l_opy_ = None
bstack11l1llll1_opy_ = None
bstack1ll111l11l_opy_ = None
bstack1l111l1l1_opy_ = None
bstack1ll1l11l_opy_ = None
bstack1llll1lll1_opy_ = None
bstack1111ll1l1_opy_ = None
bstack1llllllll1_opy_ = None
bstack1lll11lll_opy_ = bstack11lll_opy_ (u"ࠩࠪᖀ")
CONFIG = {}
bstack1llll1ll1l_opy_ = False
bstack1l1ll1l1l_opy_ = bstack11lll_opy_ (u"ࠪࠫᖁ")
bstack1lllll1ll1_opy_ = bstack11lll_opy_ (u"ࠫࠬᖂ")
bstack1ll11ll1ll_opy_ = False
bstack1l11lllll1_opy_ = []
bstack1lllllllll_opy_ = bstack1111111ll_opy_
bstack1llll11ll1l_opy_ = bstack11lll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᖃ")
bstack1lll1llll1l_opy_ = False
bstack1ll11l11l1_opy_ = {}
logger = bstack11lll1ll_opy_.get_logger(__name__, bstack1lllllllll_opy_)
store = {
    bstack11lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᖄ"): []
}
bstack1lll1llll11_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1l1111lll1_opy_ = {}
current_test_uuid = None
def bstack1l1l1111_opy_(page, bstack1l1lll11_opy_):
    try:
        page.evaluate(bstack11lll_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣᖅ"),
                      bstack11lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬᖆ") + json.dumps(
                          bstack1l1lll11_opy_) + bstack11lll_opy_ (u"ࠤࢀࢁࠧᖇ"))
    except Exception as e:
        print(bstack11lll_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽࠣᖈ"), e)
def bstack1llllll11l_opy_(page, message, level):
    try:
        page.evaluate(bstack11lll_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧᖉ"), bstack11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪᖊ") + json.dumps(
            message) + bstack11lll_opy_ (u"࠭ࠬࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠩᖋ") + json.dumps(level) + bstack11lll_opy_ (u"ࠧࡾࡿࠪᖌ"))
    except Exception as e:
        print(bstack11lll_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡࡽࢀࠦᖍ"), e)
def pytest_configure(config):
    bstack1ll11l1ll_opy_ = Config.bstack111llll1l_opy_()
    config.args = bstack1l111l11_opy_.bstack1lllll11ll1_opy_(config.args)
    bstack1ll11l1ll_opy_.bstack1ll11lll_opy_(bstack1lll111l1l_opy_(config.getoption(bstack11lll_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᖎ"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1llll1l1l11_opy_ = item.config.getoption(bstack11lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᖏ"))
    plugins = item.config.getoption(bstack11lll_opy_ (u"ࠦࡵࡲࡵࡨ࡫ࡱࡷࠧᖐ"))
    report = outcome.get_result()
    bstack1llll11111l_opy_(item, call, report)
    if bstack11lll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡴࡱࡻࡧࡪࡰࠥᖑ") not in plugins or bstack1lll1lll1l_opy_():
        return
    summary = []
    driver = getattr(item, bstack11lll_opy_ (u"ࠨ࡟ࡥࡴ࡬ࡺࡪࡸࠢᖒ"), None)
    page = getattr(item, bstack11lll_opy_ (u"ࠢࡠࡲࡤ࡫ࡪࠨᖓ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1lll1llllll_opy_(item, report, summary, bstack1llll1l1l11_opy_)
    if (page is not None):
        bstack1lll1ll1l1l_opy_(item, report, summary, bstack1llll1l1l11_opy_)
def bstack1lll1llllll_opy_(item, report, summary, bstack1llll1l1l11_opy_):
    if report.when == bstack11lll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᖔ") and report.skipped:
        bstack11111lll11_opy_(report)
    if report.when in [bstack11lll_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᖕ"), bstack11lll_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᖖ")]:
        return
    if not bstack11l11l111l_opy_():
        return
    try:
        if (str(bstack1llll1l1l11_opy_).lower() != bstack11lll_opy_ (u"ࠫࡹࡸࡵࡦࠩᖗ")):
            item._driver.execute_script(
                bstack11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪᖘ") + json.dumps(
                    report.nodeid) + bstack11lll_opy_ (u"࠭ࡽࡾࠩᖙ"))
        os.environ[bstack11lll_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪᖚ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack11lll_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧ࠽ࠤࢀ࠶ࡽࠣᖛ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11lll_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦᖜ")))
    bstack1l1l1l11ll_opy_ = bstack11lll_opy_ (u"ࠥࠦᖝ")
    bstack11111lll11_opy_(report)
    if not passed:
        try:
            bstack1l1l1l11ll_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack11lll_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦᖞ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1l1l1l11ll_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack11lll_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢᖟ")))
        bstack1l1l1l11ll_opy_ = bstack11lll_opy_ (u"ࠨࠢᖠ")
        if not passed:
            try:
                bstack1l1l1l11ll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11lll_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢᖡ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1l1l1l11ll_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack11lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡩࡧࡴࡢࠤ࠽ࠤࠬᖢ")
                    + json.dumps(bstack11lll_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠣࠥᖣ"))
                    + bstack11lll_opy_ (u"ࠥࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠨᖤ")
                )
            else:
                item._driver.execute_script(
                    bstack11lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡦࡤࡸࡦࠨ࠺ࠡࠩᖥ")
                    + json.dumps(str(bstack1l1l1l11ll_opy_))
                    + bstack11lll_opy_ (u"ࠧࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠣᖦ")
                )
        except Exception as e:
            summary.append(bstack11lll_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡦࡴ࡮ࡰࡶࡤࡸࡪࡀࠠࡼ࠲ࢀࠦᖧ").format(e))
def bstack1lll1lll11l_opy_(test_name, error_message):
    try:
        bstack1lll1lll1l1_opy_ = []
        bstack1l111l1l_opy_ = os.environ.get(bstack11lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᖨ"), bstack11lll_opy_ (u"ࠨ࠲ࠪᖩ"))
        bstack11ll11111_opy_ = {bstack11lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᖪ"): test_name, bstack11lll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᖫ"): error_message, bstack11lll_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪᖬ"): bstack1l111l1l_opy_}
        bstack1lll1ll1ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack11lll_opy_ (u"ࠬࡶࡷࡠࡲࡼࡸࡪࡹࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪᖭ"))
        if os.path.exists(bstack1lll1ll1ll1_opy_):
            with open(bstack1lll1ll1ll1_opy_) as f:
                bstack1lll1lll1l1_opy_ = json.load(f)
        bstack1lll1lll1l1_opy_.append(bstack11ll11111_opy_)
        with open(bstack1lll1ll1ll1_opy_, bstack11lll_opy_ (u"࠭ࡷࠨᖮ")) as f:
            json.dump(bstack1lll1lll1l1_opy_, f)
    except Exception as e:
        logger.debug(bstack11lll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡩࡷࡹࡩࡴࡶ࡬ࡲ࡬ࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡴࡾࡺࡥࡴࡶࠣࡩࡷࡸ࡯ࡳࡵ࠽ࠤࠬᖯ") + str(e))
def bstack1lll1ll1l1l_opy_(item, report, summary, bstack1llll1l1l11_opy_):
    if report.when in [bstack11lll_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᖰ"), bstack11lll_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᖱ")]:
        return
    if (str(bstack1llll1l1l11_opy_).lower() != bstack11lll_opy_ (u"ࠪࡸࡷࡻࡥࠨᖲ")):
        bstack1l1l1111_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11lll_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨᖳ")))
    bstack1l1l1l11ll_opy_ = bstack11lll_opy_ (u"ࠧࠨᖴ")
    bstack11111lll11_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1l1l1l11ll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11lll_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨᖵ").format(e)
                )
        try:
            if passed:
                bstack11lll111l_opy_(getattr(item, bstack11lll_opy_ (u"ࠧࡠࡲࡤ࡫ࡪ࠭ᖶ"), None), bstack11lll_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣᖷ"))
            else:
                error_message = bstack11lll_opy_ (u"ࠩࠪᖸ")
                if bstack1l1l1l11ll_opy_:
                    bstack1llllll11l_opy_(item._page, str(bstack1l1l1l11ll_opy_), bstack11lll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤᖹ"))
                    bstack11lll111l_opy_(getattr(item, bstack11lll_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪᖺ"), None), bstack11lll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᖻ"), str(bstack1l1l1l11ll_opy_))
                    error_message = str(bstack1l1l1l11ll_opy_)
                else:
                    bstack11lll111l_opy_(getattr(item, bstack11lll_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬᖼ"), None), bstack11lll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᖽ"))
                bstack1lll1lll11l_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack11lll_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡵࡱࡦࡤࡸࡪࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࡽ࠳ࢁࠧᖾ").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack11lll_opy_ (u"ࠤ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨᖿ"), default=bstack11lll_opy_ (u"ࠥࡊࡦࡲࡳࡦࠤᗀ"), help=bstack11lll_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡩࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠥᗁ"))
    parser.addoption(bstack11lll_opy_ (u"ࠧ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦᗂ"), default=bstack11lll_opy_ (u"ࠨࡆࡢ࡮ࡶࡩࠧᗃ"), help=bstack11lll_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡪࡥࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠨᗄ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack11lll_opy_ (u"ࠣ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠥᗅ"), action=bstack11lll_opy_ (u"ࠤࡶࡸࡴࡸࡥࠣᗆ"), default=bstack11lll_opy_ (u"ࠥࡧ࡭ࡸ࡯࡮ࡧࠥᗇ"),
                         help=bstack11lll_opy_ (u"ࠦࡉࡸࡩࡷࡧࡵࠤࡹࡵࠠࡳࡷࡱࠤࡹ࡫ࡳࡵࡵࠥᗈ"))
def bstack1l111l1l11_opy_(log):
    if not (log[bstack11lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᗉ")] and log[bstack11lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᗊ")].strip()):
        return
    active = bstack1l11l11lll_opy_()
    log = {
        bstack11lll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᗋ"): log[bstack11lll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᗌ")],
        bstack11lll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᗍ"): datetime.datetime.utcnow().isoformat() + bstack11lll_opy_ (u"ࠪ࡞ࠬᗎ"),
        bstack11lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᗏ"): log[bstack11lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᗐ")],
    }
    if active:
        if active[bstack11lll_opy_ (u"࠭ࡴࡺࡲࡨࠫᗑ")] == bstack11lll_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᗒ"):
            log[bstack11lll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᗓ")] = active[bstack11lll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᗔ")]
        elif active[bstack11lll_opy_ (u"ࠪࡸࡾࡶࡥࠨᗕ")] == bstack11lll_opy_ (u"ࠫࡹ࡫ࡳࡵࠩᗖ"):
            log[bstack11lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᗗ")] = active[bstack11lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᗘ")]
    bstack1l111l11_opy_.bstack1ll1lllll1_opy_([log])
def bstack1l11l11lll_opy_():
    if len(store[bstack11lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᗙ")]) > 0 and store[bstack11lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᗚ")][-1]:
        return {
            bstack11lll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᗛ"): bstack11lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨᗜ"),
            bstack11lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᗝ"): store[bstack11lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᗞ")][-1]
        }
    if store.get(bstack11lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᗟ"), None):
        return {
            bstack11lll_opy_ (u"ࠧࡵࡻࡳࡩࠬᗠ"): bstack11lll_opy_ (u"ࠨࡶࡨࡷࡹ࠭ᗡ"),
            bstack11lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᗢ"): store[bstack11lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᗣ")]
        }
    return None
bstack1l111l1111_opy_ = bstack1l11l11ll1_opy_(bstack1l111l1l11_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        global bstack1lll1llll1l_opy_
        item._1lll1lll1ll_opy_ = True
        bstack1l111l111_opy_ = bstack1l11lll1_opy_.bstack1llll11l_opy_(CONFIG, bstack11l1ll1ll1_opy_(item.own_markers))
        item._a11y_test_case = bstack1l111l111_opy_
        if bstack1lll1llll1l_opy_:
            driver = getattr(item, bstack11lll_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬᗤ"), None)
            item._a11y_started = bstack1l11lll1_opy_.bstack1l1lll111_opy_(driver, bstack1l111l111_opy_)
        if not bstack1l111l11_opy_.on() or bstack1llll11ll1l_opy_ != bstack11lll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᗥ"):
            return
        global current_test_uuid, bstack1l111l1111_opy_
        bstack1l111l1111_opy_.start()
        bstack1l1111ll1l_opy_ = {
            bstack11lll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᗦ"): uuid4().__str__(),
            bstack11lll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᗧ"): datetime.datetime.utcnow().isoformat() + bstack11lll_opy_ (u"ࠨ࡜ࠪᗨ")
        }
        current_test_uuid = bstack1l1111ll1l_opy_[bstack11lll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᗩ")]
        store[bstack11lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᗪ")] = bstack1l1111ll1l_opy_[bstack11lll_opy_ (u"ࠫࡺࡻࡩࡥࠩᗫ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1l1111lll1_opy_[item.nodeid] = {**_1l1111lll1_opy_[item.nodeid], **bstack1l1111ll1l_opy_}
        bstack1llll111ll1_opy_(item, _1l1111lll1_opy_[item.nodeid], bstack11lll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᗬ"))
    except Exception as err:
        print(bstack11lll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡣࡢ࡮࡯࠾ࠥࢁࡽࠨᗭ"), str(err))
def pytest_runtest_setup(item):
    global bstack1lll1llll11_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11l11l1l1l_opy_():
        atexit.register(bstack111llllll_opy_)
        if not bstack1lll1llll11_opy_:
            try:
                bstack1llll11l111_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11l11ll1l1_opy_():
                    bstack1llll11l111_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1llll11l111_opy_:
                    signal.signal(s, bstack1lll1lllll1_opy_)
                bstack1lll1llll11_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack11lll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡵࡩ࡬࡯ࡳࡵࡧࡵࠤࡸ࡯ࡧ࡯ࡣ࡯ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶࡸࡀࠠࠣᗮ") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack11111l11ll_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack11lll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᗯ")
    try:
        if not bstack1l111l11_opy_.on():
            return
        bstack1l111l1111_opy_.start()
        uuid = uuid4().__str__()
        bstack1l1111ll1l_opy_ = {
            bstack11lll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᗰ"): uuid,
            bstack11lll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᗱ"): datetime.datetime.utcnow().isoformat() + bstack11lll_opy_ (u"ࠫ࡟࠭ᗲ"),
            bstack11lll_opy_ (u"ࠬࡺࡹࡱࡧࠪᗳ"): bstack11lll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᗴ"),
            bstack11lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᗵ"): bstack11lll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ᗶ"),
            bstack11lll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬᗷ"): bstack11lll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᗸ")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack11lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨᗹ")] = item
        store[bstack11lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᗺ")] = [uuid]
        if not _1l1111lll1_opy_.get(item.nodeid, None):
            _1l1111lll1_opy_[item.nodeid] = {bstack11lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᗻ"): [], bstack11lll_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩᗼ"): []}
        _1l1111lll1_opy_[item.nodeid][bstack11lll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᗽ")].append(bstack1l1111ll1l_opy_[bstack11lll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᗾ")])
        _1l1111lll1_opy_[item.nodeid + bstack11lll_opy_ (u"ࠪ࠱ࡸ࡫ࡴࡶࡲࠪᗿ")] = bstack1l1111ll1l_opy_
        bstack1llll111l1l_opy_(item, bstack1l1111ll1l_opy_, bstack11lll_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᘀ"))
    except Exception as err:
        print(bstack11lll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡹࡥࡵࡷࡳ࠾ࠥࢁࡽࠨᘁ"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack1ll11l11l1_opy_
        if CONFIG.get(bstack11lll_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬᘂ"), False):
            if CONFIG.get(bstack11lll_opy_ (u"ࠧࡱࡧࡵࡧࡾࡉࡡࡱࡶࡸࡶࡪࡓ࡯ࡥࡧࠪᘃ"), bstack11lll_opy_ (u"ࠣࡣࡸࡸࡴࠨᘄ")) == bstack11lll_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦᘅ"):
                bstack1llll1111ll_opy_ = bstack11ll1l1ll_opy_(threading.current_thread(), bstack11lll_opy_ (u"ࠪࡴࡪࡸࡣࡺࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᘆ"), None)
                bstack11ll11l1l_opy_ = bstack1llll1111ll_opy_ + bstack11lll_opy_ (u"ࠦ࠲ࡺࡥࡴࡶࡦࡥࡸ࡫ࠢᘇ")
                driver = getattr(item, bstack11lll_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭ᘈ"), None)
                PercySDK.screenshot(driver, bstack11ll11l1l_opy_)
        if getattr(item, bstack11lll_opy_ (u"࠭࡟ࡢ࠳࠴ࡽࡤࡹࡴࡢࡴࡷࡩࡩ࠭ᘉ"), False):
            bstack11l1lll1_opy_.bstack1111ll11l_opy_(getattr(item, bstack11lll_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨᘊ"), None), bstack1ll11l11l1_opy_, logger, item)
        if not bstack1l111l11_opy_.on():
            return
        bstack1l1111ll1l_opy_ = {
            bstack11lll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᘋ"): uuid4().__str__(),
            bstack11lll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᘌ"): datetime.datetime.utcnow().isoformat() + bstack11lll_opy_ (u"ࠪ࡞ࠬᘍ"),
            bstack11lll_opy_ (u"ࠫࡹࡿࡰࡦࠩᘎ"): bstack11lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᘏ"),
            bstack11lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᘐ"): bstack11lll_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫᘑ"),
            bstack11lll_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫᘒ"): bstack11lll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫᘓ")
        }
        _1l1111lll1_opy_[item.nodeid + bstack11lll_opy_ (u"ࠪ࠱ࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᘔ")] = bstack1l1111ll1l_opy_
        bstack1llll111l1l_opy_(item, bstack1l1111ll1l_opy_, bstack11lll_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᘕ"))
    except Exception as err:
        print(bstack11lll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࠺ࠡࡽࢀࠫᘖ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1l111l11_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack11111l1lll_opy_(fixturedef.argname):
        store[bstack11lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡪࡶࡨࡱࠬᘗ")] = request.node
    elif bstack11111l1l11_opy_(fixturedef.argname):
        store[bstack11lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡥ࡯ࡥࡸࡹ࡟ࡪࡶࡨࡱࠬᘘ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack11lll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᘙ"): fixturedef.argname,
            bstack11lll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᘚ"): bstack11l11l1l11_opy_(outcome),
            bstack11lll_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬᘛ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack11lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨᘜ")]
        if not _1l1111lll1_opy_.get(current_test_item.nodeid, None):
            _1l1111lll1_opy_[current_test_item.nodeid] = {bstack11lll_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᘝ"): []}
        _1l1111lll1_opy_[current_test_item.nodeid][bstack11lll_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨᘞ")].append(fixture)
    except Exception as err:
        logger.debug(bstack11lll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡴࡧࡷࡹࡵࡀࠠࡼࡿࠪᘟ"), str(err))
if bstack1lll1lll1l_opy_() and bstack1l111l11_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _1l1111lll1_opy_[request.node.nodeid][bstack11lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᘠ")].bstack1lllllll11l_opy_(id(step))
        except Exception as err:
            print(bstack11lll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲ࠽ࠤࢀࢃࠧᘡ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _1l1111lll1_opy_[request.node.nodeid][bstack11lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᘢ")].bstack1l111l1l1l_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack11lll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡴࡶࡨࡴࡤ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠨᘣ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack1l11111ll1_opy_: bstack1l1111llll_opy_ = _1l1111lll1_opy_[request.node.nodeid][bstack11lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᘤ")]
            bstack1l11111ll1_opy_.bstack1l111l1l1l_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack11lll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡶࡸࡪࡶ࡟ࡦࡴࡵࡳࡷࡀࠠࡼࡿࠪᘥ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1llll11ll1l_opy_
        try:
            if not bstack1l111l11_opy_.on() or bstack1llll11ll1l_opy_ != bstack11lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫᘦ"):
                return
            global bstack1l111l1111_opy_
            bstack1l111l1111_opy_.start()
            if not _1l1111lll1_opy_.get(request.node.nodeid, None):
                _1l1111lll1_opy_[request.node.nodeid] = {}
            bstack1l11111ll1_opy_ = bstack1l1111llll_opy_.bstack1lllll1l11l_opy_(
                scenario, feature, request.node,
                name=bstack11111l11l1_opy_(request.node, scenario),
                bstack1l11l1l1ll_opy_=bstack1ll1ll1lll_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack11lll_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪᘧ"),
                tags=bstack11111ll111_opy_(feature, scenario)
            )
            _1l1111lll1_opy_[request.node.nodeid][bstack11lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᘨ")] = bstack1l11111ll1_opy_
            bstack1llll1l1l1l_opy_(bstack1l11111ll1_opy_.uuid)
            bstack1l111l11_opy_.bstack1l11111l1l_opy_(bstack11lll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᘩ"), bstack1l11111ll1_opy_)
        except Exception as err:
            print(bstack11lll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰ࠼ࠣࡿࢂ࠭ᘪ"), str(err))
def bstack1llll11l11l_opy_(bstack1llll111111_opy_):
    if bstack1llll111111_opy_ in store[bstack11lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᘫ")]:
        store[bstack11lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᘬ")].remove(bstack1llll111111_opy_)
def bstack1llll1l1l1l_opy_(bstack1lll1lll111_opy_):
    store[bstack11lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᘭ")] = bstack1lll1lll111_opy_
    threading.current_thread().current_test_uuid = bstack1lll1lll111_opy_
@bstack1l111l11_opy_.bstack1lllll111l1_opy_
def bstack1llll11111l_opy_(item, call, report):
    global bstack1llll11ll1l_opy_
    bstack1lll11ll1l_opy_ = bstack1ll1ll1lll_opy_()
    if hasattr(report, bstack11lll_opy_ (u"ࠨࡵࡷࡳࡵ࠭ᘮ")):
        bstack1lll11ll1l_opy_ = bstack11l111lll1_opy_(report.stop)
    if hasattr(report, bstack11lll_opy_ (u"ࠩࡶࡸࡦࡸࡴࠨᘯ")):
        bstack1lll11ll1l_opy_ = bstack11l111lll1_opy_(report.start)
    try:
        if getattr(report, bstack11lll_opy_ (u"ࠪࡻ࡭࡫࡮ࠨᘰ"), bstack11lll_opy_ (u"ࠫࠬᘱ")) == bstack11lll_opy_ (u"ࠬࡩࡡ࡭࡮ࠪᘲ"):
            bstack1l111l1111_opy_.reset()
        if getattr(report, bstack11lll_opy_ (u"࠭ࡷࡩࡧࡱࠫᘳ"), bstack11lll_opy_ (u"ࠧࠨᘴ")) == bstack11lll_opy_ (u"ࠨࡥࡤࡰࡱ࠭ᘵ"):
            if bstack1llll11ll1l_opy_ == bstack11lll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᘶ"):
                _1l1111lll1_opy_[item.nodeid][bstack11lll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᘷ")] = bstack1lll11ll1l_opy_
                bstack1llll111ll1_opy_(item, _1l1111lll1_opy_[item.nodeid], bstack11lll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᘸ"), report, call)
                store[bstack11lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᘹ")] = None
            elif bstack1llll11ll1l_opy_ == bstack11lll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥᘺ"):
                bstack1l11111ll1_opy_ = _1l1111lll1_opy_[item.nodeid][bstack11lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᘻ")]
                bstack1l11111ll1_opy_.set(hooks=_1l1111lll1_opy_[item.nodeid].get(bstack11lll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᘼ"), []))
                exception, bstack1l11ll1ll1_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1l11ll1ll1_opy_ = [call.excinfo.exconly(), getattr(report, bstack11lll_opy_ (u"ࠩ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠨᘽ"), bstack11lll_opy_ (u"ࠪࠫᘾ"))]
                bstack1l11111ll1_opy_.stop(time=bstack1lll11ll1l_opy_, result=Result(result=getattr(report, bstack11lll_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬᘿ"), bstack11lll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᙀ")), exception=exception, bstack1l11ll1ll1_opy_=bstack1l11ll1ll1_opy_))
                bstack1l111l11_opy_.bstack1l11111l1l_opy_(bstack11lll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᙁ"), _1l1111lll1_opy_[item.nodeid][bstack11lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᙂ")])
        elif getattr(report, bstack11lll_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭ᙃ"), bstack11lll_opy_ (u"ࠩࠪᙄ")) in [bstack11lll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᙅ"), bstack11lll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᙆ")]:
            bstack11lllllll1_opy_ = item.nodeid + bstack11lll_opy_ (u"ࠬ࠳ࠧᙇ") + getattr(report, bstack11lll_opy_ (u"࠭ࡷࡩࡧࡱࠫᙈ"), bstack11lll_opy_ (u"ࠧࠨᙉ"))
            if getattr(report, bstack11lll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᙊ"), False):
                hook_type = bstack11lll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᙋ") if getattr(report, bstack11lll_opy_ (u"ࠪࡻ࡭࡫࡮ࠨᙌ"), bstack11lll_opy_ (u"ࠫࠬᙍ")) == bstack11lll_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᙎ") else bstack11lll_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᙏ")
                _1l1111lll1_opy_[bstack11lllllll1_opy_] = {
                    bstack11lll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᙐ"): uuid4().__str__(),
                    bstack11lll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᙑ"): bstack1lll11ll1l_opy_,
                    bstack11lll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᙒ"): hook_type
                }
            _1l1111lll1_opy_[bstack11lllllll1_opy_][bstack11lll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᙓ")] = bstack1lll11ll1l_opy_
            bstack1llll11l11l_opy_(_1l1111lll1_opy_[bstack11lllllll1_opy_][bstack11lll_opy_ (u"ࠫࡺࡻࡩࡥࠩᙔ")])
            bstack1llll111l1l_opy_(item, _1l1111lll1_opy_[bstack11lllllll1_opy_], bstack11lll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᙕ"), report, call)
            if getattr(report, bstack11lll_opy_ (u"࠭ࡷࡩࡧࡱࠫᙖ"), bstack11lll_opy_ (u"ࠧࠨᙗ")) == bstack11lll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᙘ"):
                if getattr(report, bstack11lll_opy_ (u"ࠩࡲࡹࡹࡩ࡯࡮ࡧࠪᙙ"), bstack11lll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᙚ")) == bstack11lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᙛ"):
                    bstack1l1111ll1l_opy_ = {
                        bstack11lll_opy_ (u"ࠬࡻࡵࡪࡦࠪᙜ"): uuid4().__str__(),
                        bstack11lll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᙝ"): bstack1ll1ll1lll_opy_(),
                        bstack11lll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᙞ"): bstack1ll1ll1lll_opy_()
                    }
                    _1l1111lll1_opy_[item.nodeid] = {**_1l1111lll1_opy_[item.nodeid], **bstack1l1111ll1l_opy_}
                    bstack1llll111ll1_opy_(item, _1l1111lll1_opy_[item.nodeid], bstack11lll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᙟ"))
                    bstack1llll111ll1_opy_(item, _1l1111lll1_opy_[item.nodeid], bstack11lll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᙠ"), report, call)
    except Exception as err:
        print(bstack11lll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡡࡲ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥࢁࡽࠨᙡ"), str(err))
def bstack1llll111l11_opy_(test, bstack1l1111ll1l_opy_, result=None, call=None, bstack11111lll_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack1l11111ll1_opy_ = {
        bstack11lll_opy_ (u"ࠫࡺࡻࡩࡥࠩᙢ"): bstack1l1111ll1l_opy_[bstack11lll_opy_ (u"ࠬࡻࡵࡪࡦࠪᙣ")],
        bstack11lll_opy_ (u"࠭ࡴࡺࡲࡨࠫᙤ"): bstack11lll_opy_ (u"ࠧࡵࡧࡶࡸࠬᙥ"),
        bstack11lll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᙦ"): test.name,
        bstack11lll_opy_ (u"ࠩࡥࡳࡩࡿࠧᙧ"): {
            bstack11lll_opy_ (u"ࠪࡰࡦࡴࡧࠨᙨ"): bstack11lll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫᙩ"),
            bstack11lll_opy_ (u"ࠬࡩ࡯ࡥࡧࠪᙪ"): inspect.getsource(test.obj)
        },
        bstack11lll_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᙫ"): test.name,
        bstack11lll_opy_ (u"ࠧࡴࡥࡲࡴࡪ࠭ᙬ"): test.name,
        bstack11lll_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨ᙭"): bstack1l111l11_opy_.bstack1l11l11111_opy_(test),
        bstack11lll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ᙮"): file_path,
        bstack11lll_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬᙯ"): file_path,
        bstack11lll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᙰ"): bstack11lll_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭ᙱ"),
        bstack11lll_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫᙲ"): file_path,
        bstack11lll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᙳ"): bstack1l1111ll1l_opy_[bstack11lll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᙴ")],
        bstack11lll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᙵ"): bstack11lll_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪᙶ"),
        bstack11lll_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡖࡪࡸࡵ࡯ࡒࡤࡶࡦࡳࠧᙷ"): {
            bstack11lll_opy_ (u"ࠬࡸࡥࡳࡷࡱࡣࡳࡧ࡭ࡦࠩᙸ"): test.nodeid
        },
        bstack11lll_opy_ (u"࠭ࡴࡢࡩࡶࠫᙹ"): bstack11l1ll1ll1_opy_(test.own_markers)
    }
    if bstack11111lll_opy_ in [bstack11lll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨᙺ"), bstack11lll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᙻ")]:
        bstack1l11111ll1_opy_[bstack11lll_opy_ (u"ࠩࡰࡩࡹࡧࠧᙼ")] = {
            bstack11lll_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬᙽ"): bstack1l1111ll1l_opy_.get(bstack11lll_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭ᙾ"), [])
        }
    if bstack11111lll_opy_ == bstack11lll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭ᙿ"):
        bstack1l11111ll1_opy_[bstack11lll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ ")] = bstack11lll_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᚁ")
        bstack1l11111ll1_opy_[bstack11lll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᚂ")] = bstack1l1111ll1l_opy_[bstack11lll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᚃ")]
        bstack1l11111ll1_opy_[bstack11lll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᚄ")] = bstack1l1111ll1l_opy_[bstack11lll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᚅ")]
    if result:
        bstack1l11111ll1_opy_[bstack11lll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᚆ")] = result.outcome
        bstack1l11111ll1_opy_[bstack11lll_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧᚇ")] = result.duration * 1000
        bstack1l11111ll1_opy_[bstack11lll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᚈ")] = bstack1l1111ll1l_opy_[bstack11lll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᚉ")]
        if result.failed:
            bstack1l11111ll1_opy_[bstack11lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨᚊ")] = bstack1l111l11_opy_.bstack11lll1l11l_opy_(call.excinfo.typename)
            bstack1l11111ll1_opy_[bstack11lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᚋ")] = bstack1l111l11_opy_.bstack1lllll11l1l_opy_(call.excinfo, result)
        bstack1l11111ll1_opy_[bstack11lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᚌ")] = bstack1l1111ll1l_opy_[bstack11lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᚍ")]
    if outcome:
        bstack1l11111ll1_opy_[bstack11lll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᚎ")] = bstack11l11l1l11_opy_(outcome)
        bstack1l11111ll1_opy_[bstack11lll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᚏ")] = 0
        bstack1l11111ll1_opy_[bstack11lll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᚐ")] = bstack1l1111ll1l_opy_[bstack11lll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᚑ")]
        if bstack1l11111ll1_opy_[bstack11lll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᚒ")] == bstack11lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᚓ"):
            bstack1l11111ll1_opy_[bstack11lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᚔ")] = bstack11lll_opy_ (u"࠭ࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠧᚕ")  # bstack1llll11llll_opy_
            bstack1l11111ll1_opy_[bstack11lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᚖ")] = [{bstack11lll_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᚗ"): [bstack11lll_opy_ (u"ࠩࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷ࠭ᚘ")]}]
        bstack1l11111ll1_opy_[bstack11lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᚙ")] = bstack1l1111ll1l_opy_[bstack11lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᚚ")]
    return bstack1l11111ll1_opy_
def bstack1lll1ll1lll_opy_(test, bstack1l11l111l1_opy_, bstack11111lll_opy_, result, call, outcome, bstack1llll11l1ll_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1l11l111l1_opy_[bstack11lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ᚛")]
    hook_name = bstack1l11l111l1_opy_[bstack11lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩ᚜")]
    hook_data = {
        bstack11lll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ᚝"): bstack1l11l111l1_opy_[bstack11lll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭᚞")],
        bstack11lll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ᚟"): bstack11lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨᚠ"),
        bstack11lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᚡ"): bstack11lll_opy_ (u"ࠬࢁࡽࠨᚢ").format(bstack11111l1l1l_opy_(hook_name)),
        bstack11lll_opy_ (u"࠭ࡢࡰࡦࡼࠫᚣ"): {
            bstack11lll_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬᚤ"): bstack11lll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᚥ"),
            bstack11lll_opy_ (u"ࠩࡦࡳࡩ࡫ࠧᚦ"): None
        },
        bstack11lll_opy_ (u"ࠪࡷࡨࡵࡰࡦࠩᚧ"): test.name,
        bstack11lll_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫᚨ"): bstack1l111l11_opy_.bstack1l11l11111_opy_(test, hook_name),
        bstack11lll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨᚩ"): file_path,
        bstack11lll_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨᚪ"): file_path,
        bstack11lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᚫ"): bstack11lll_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩᚬ"),
        bstack11lll_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧᚭ"): file_path,
        bstack11lll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᚮ"): bstack1l11l111l1_opy_[bstack11lll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᚯ")],
        bstack11lll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᚰ"): bstack11lll_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨᚱ") if bstack1llll11ll1l_opy_ == bstack11lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫᚲ") else bstack11lll_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨᚳ"),
        bstack11lll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᚴ"): hook_type
    }
    bstack1lll1ll11ll_opy_ = bstack1l111l11ll_opy_(_1l1111lll1_opy_.get(test.nodeid, None))
    if bstack1lll1ll11ll_opy_:
        hook_data[bstack11lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡯ࡤࠨᚵ")] = bstack1lll1ll11ll_opy_
    if result:
        hook_data[bstack11lll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᚶ")] = result.outcome
        hook_data[bstack11lll_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ᚷ")] = result.duration * 1000
        hook_data[bstack11lll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᚸ")] = bstack1l11l111l1_opy_[bstack11lll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᚹ")]
        if result.failed:
            hook_data[bstack11lll_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᚺ")] = bstack1l111l11_opy_.bstack11lll1l11l_opy_(call.excinfo.typename)
            hook_data[bstack11lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᚻ")] = bstack1l111l11_opy_.bstack1lllll11l1l_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack11lll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᚼ")] = bstack11l11l1l11_opy_(outcome)
        hook_data[bstack11lll_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬᚽ")] = 100
        hook_data[bstack11lll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᚾ")] = bstack1l11l111l1_opy_[bstack11lll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᚿ")]
        if hook_data[bstack11lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᛀ")] == bstack11lll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᛁ"):
            hook_data[bstack11lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨᛂ")] = bstack11lll_opy_ (u"࡙ࠪࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠫᛃ")  # bstack1llll11llll_opy_
            hook_data[bstack11lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᛄ")] = [{bstack11lll_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᛅ"): [bstack11lll_opy_ (u"࠭ࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠪᛆ")]}]
    if bstack1llll11l1ll_opy_:
        hook_data[bstack11lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᛇ")] = bstack1llll11l1ll_opy_.result
        hook_data[bstack11lll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩᛈ")] = bstack11l1ll11ll_opy_(bstack1l11l111l1_opy_[bstack11lll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᛉ")], bstack1l11l111l1_opy_[bstack11lll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᛊ")])
        hook_data[bstack11lll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᛋ")] = bstack1l11l111l1_opy_[bstack11lll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᛌ")]
        if hook_data[bstack11lll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᛍ")] == bstack11lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᛎ"):
            hook_data[bstack11lll_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᛏ")] = bstack1l111l11_opy_.bstack11lll1l11l_opy_(bstack1llll11l1ll_opy_.exception_type)
            hook_data[bstack11lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᛐ")] = [{bstack11lll_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᛑ"): bstack11l11l1lll_opy_(bstack1llll11l1ll_opy_.exception)}]
    return hook_data
def bstack1llll111ll1_opy_(test, bstack1l1111ll1l_opy_, bstack11111lll_opy_, result=None, call=None, outcome=None):
    bstack1l11111ll1_opy_ = bstack1llll111l11_opy_(test, bstack1l1111ll1l_opy_, result, call, bstack11111lll_opy_, outcome)
    driver = getattr(test, bstack11lll_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬᛒ"), None)
    if bstack11111lll_opy_ == bstack11lll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᛓ") and driver:
        bstack1l11111ll1_opy_[bstack11lll_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬᛔ")] = bstack1l111l11_opy_.bstack1l111llll1_opy_(driver)
    if bstack11111lll_opy_ == bstack11lll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨᛕ"):
        bstack11111lll_opy_ = bstack11lll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᛖ")
    bstack11llllllll_opy_ = {
        bstack11lll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ᛗ"): bstack11111lll_opy_,
        bstack11lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬᛘ"): bstack1l11111ll1_opy_
    }
    bstack1l111l11_opy_.bstack1l111l1lll_opy_(bstack11llllllll_opy_)
def bstack1llll111l1l_opy_(test, bstack1l1111ll1l_opy_, bstack11111lll_opy_, result=None, call=None, outcome=None, bstack1llll11l1ll_opy_=None):
    hook_data = bstack1lll1ll1lll_opy_(test, bstack1l1111ll1l_opy_, bstack11111lll_opy_, result, call, outcome, bstack1llll11l1ll_opy_)
    bstack11llllllll_opy_ = {
        bstack11lll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᛙ"): bstack11111lll_opy_,
        bstack11lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴࠧᛚ"): hook_data
    }
    bstack1l111l11_opy_.bstack1l111l1lll_opy_(bstack11llllllll_opy_)
def bstack1l111l11ll_opy_(bstack1l1111ll1l_opy_):
    if not bstack1l1111ll1l_opy_:
        return None
    if bstack1l1111ll1l_opy_.get(bstack11lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᛛ"), None):
        return getattr(bstack1l1111ll1l_opy_[bstack11lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᛜ")], bstack11lll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᛝ"), None)
    return bstack1l1111ll1l_opy_.get(bstack11lll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᛞ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1l111l11_opy_.on():
            return
        places = [bstack11lll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᛟ"), bstack11lll_opy_ (u"ࠫࡨࡧ࡬࡭ࠩᛠ"), bstack11lll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧᛡ")]
        bstack1l111ll1l1_opy_ = []
        for bstack1llll111lll_opy_ in places:
            records = caplog.get_records(bstack1llll111lll_opy_)
            bstack1llll1l11ll_opy_ = bstack11lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᛢ") if bstack1llll111lll_opy_ == bstack11lll_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᛣ") else bstack11lll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᛤ")
            bstack1llll11l1l1_opy_ = request.node.nodeid + (bstack11lll_opy_ (u"ࠩࠪᛥ") if bstack1llll111lll_opy_ == bstack11lll_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᛦ") else bstack11lll_opy_ (u"ࠫ࠲࠭ᛧ") + bstack1llll111lll_opy_)
            bstack1lll1lll111_opy_ = bstack1l111l11ll_opy_(_1l1111lll1_opy_.get(bstack1llll11l1l1_opy_, None))
            if not bstack1lll1lll111_opy_:
                continue
            for record in records:
                if bstack11l1lll111_opy_(record.message):
                    continue
                bstack1l111ll1l1_opy_.append({
                    bstack11lll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨᛨ"): datetime.datetime.utcfromtimestamp(record.created).isoformat() + bstack11lll_opy_ (u"࡚࠭ࠨᛩ"),
                    bstack11lll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᛪ"): record.levelname,
                    bstack11lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ᛫"): record.message,
                    bstack1llll1l11ll_opy_: bstack1lll1lll111_opy_
                })
        if len(bstack1l111ll1l1_opy_) > 0:
            bstack1l111l11_opy_.bstack1ll1lllll1_opy_(bstack1l111ll1l1_opy_)
    except Exception as err:
        print(bstack11lll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡧࡴࡴࡤࡠࡨ࡬ࡼࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭᛬"), str(err))
def bstack1llll11111_opy_(sequence, driver_command, response=None):
    if sequence == bstack11lll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩ᛭"):
        if driver_command == bstack11lll_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨᛮ"):
            bstack1l111l11_opy_.bstack1lll1111l1_opy_({
                bstack11lll_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫᛯ"): response[bstack11lll_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬᛰ")],
                bstack11lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᛱ"): store[bstack11lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᛲ")]
            })
def bstack111llllll_opy_():
    global bstack1l11lllll1_opy_
    bstack1l111l11_opy_.bstack1l11l111ll_opy_()
    for driver in bstack1l11lllll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lll1lllll1_opy_(*args):
    global bstack1l11lllll1_opy_
    bstack1l111l11_opy_.bstack1l11l111ll_opy_()
    for driver in bstack1l11lllll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1l1ll1lll1_opy_(self, *args, **kwargs):
    bstack1l1l111l11_opy_ = bstack1lll11l1l_opy_(self, *args, **kwargs)
    bstack1l111l11_opy_.bstack1lll111ll_opy_(self)
    return bstack1l1l111l11_opy_
def bstack1l1111lll_opy_(framework_name):
    global bstack1lll11lll_opy_
    global bstack1l1l1l1ll_opy_
    bstack1lll11lll_opy_ = framework_name
    logger.info(bstack11llll11l_opy_.format(bstack1lll11lll_opy_.split(bstack11lll_opy_ (u"ࠩ࠰ࠫᛳ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack11l11l111l_opy_():
            Service.start = bstack1l1l1l1l_opy_
            Service.stop = bstack1111l1l11_opy_
            webdriver.Remote.__init__ = bstack1l11l11ll_opy_
            webdriver.Remote.get = bstack1lll11ll_opy_
            if not isinstance(os.getenv(bstack11lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡅࡗࡇࡌࡍࡇࡏࠫᛴ")), str):
                return
            WebDriver.close = bstack11l11l111_opy_
            WebDriver.quit = bstack1ll1l1l1l1_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.bstack11lll11l_opy_ = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.bstack111l1lll_opy_ = getAccessibilityResultsSummary
        if not bstack11l11l111l_opy_() and bstack1l111l11_opy_.on():
            webdriver.Remote.__init__ = bstack1l1ll1lll1_opy_
        bstack1l1l1l1ll_opy_ = True
    except Exception as e:
        pass
    bstack1l1ll1111_opy_()
    if os.environ.get(bstack11lll_opy_ (u"ࠫࡘࡋࡌࡆࡐࡌ࡙ࡒࡥࡏࡓࡡࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡉࡏࡕࡗࡅࡑࡒࡅࡅࠩᛵ")):
        bstack1l1l1l1ll_opy_ = eval(os.environ.get(bstack11lll_opy_ (u"࡙ࠬࡅࡍࡇࡑࡍ࡚ࡓ࡟ࡐࡔࡢࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡊࡐࡖࡘࡆࡒࡌࡆࡆࠪᛶ")))
    if not bstack1l1l1l1ll_opy_:
        bstack1l11l11l1_opy_(bstack11lll_opy_ (u"ࠨࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠡࡰࡲࡸࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠣᛷ"), bstack1l1l11l1l_opy_)
    if bstack1lll1ll1l1_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack11l1l11l1_opy_
        except Exception as e:
            logger.error(bstack1llll11l1l_opy_.format(str(e)))
    if bstack11lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᛸ") in str(framework_name).lower():
        if not bstack11l11l111l_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack11l11111l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1l1lllll1l_opy_
            Config.getoption = bstack111l1ll1_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1l1l11l11l_opy_
        except Exception as e:
            pass
def bstack1ll1l1l1l1_opy_(self):
    global bstack1lll11lll_opy_
    global bstack11l1l1lll_opy_
    global bstack1llll1ll1_opy_
    try:
        if bstack11lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ᛹") in bstack1lll11lll_opy_ and self.session_id != None and bstack11ll1l1ll_opy_(threading.current_thread(), bstack11lll_opy_ (u"ࠩࡷࡩࡸࡺࡓࡵࡣࡷࡹࡸ࠭᛺"), bstack11lll_opy_ (u"ࠪࠫ᛻")) != bstack11lll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ᛼"):
            bstack1ll11ll11l_opy_ = bstack11lll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ᛽") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭᛾")
            bstack1l1l1lllll_opy_(logger, True)
            if self != None:
                bstack111l1l11_opy_(self, bstack1ll11ll11l_opy_, bstack11lll_opy_ (u"ࠧ࠭ࠢࠪ᛿").join(threading.current_thread().bstackTestErrorMessages))
        item = store.get(bstack11lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬᜀ"), None)
        if item is not None and bstack1lll1llll1l_opy_:
            bstack11l1lll1_opy_.bstack1111ll11l_opy_(self, bstack1ll11l11l1_opy_, logger, item)
        threading.current_thread().testStatus = bstack11lll_opy_ (u"ࠩࠪᜁ")
    except Exception as e:
        logger.debug(bstack11lll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࠦᜂ") + str(e))
    bstack1llll1ll1_opy_(self)
    self.session_id = None
def bstack1l11l11ll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack11l1l1lll_opy_
    global bstack1ll1111ll1_opy_
    global bstack1ll11ll1ll_opy_
    global bstack1lll11lll_opy_
    global bstack1lll11l1l_opy_
    global bstack1l11lllll1_opy_
    global bstack1l1ll1l1l_opy_
    global bstack1lllll1ll1_opy_
    global bstack1lll1llll1l_opy_
    global bstack1ll11l11l1_opy_
    CONFIG[bstack11lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᜃ")] = str(bstack1lll11lll_opy_) + str(__version__)
    command_executor = bstack1ll111ll11_opy_(bstack1l1ll1l1l_opy_)
    logger.debug(bstack11lll1ll1_opy_.format(command_executor))
    proxy = bstack1l1ll1l1ll_opy_(CONFIG, proxy)
    bstack1l111l1l_opy_ = 0
    try:
        if bstack1ll11ll1ll_opy_ is True:
            bstack1l111l1l_opy_ = int(os.environ.get(bstack11lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᜄ")))
    except:
        bstack1l111l1l_opy_ = 0
    bstack1l1lll11ll_opy_ = bstack1l1lll1lll_opy_(CONFIG, bstack1l111l1l_opy_)
    logger.debug(bstack1l1l11ll11_opy_.format(str(bstack1l1lll11ll_opy_)))
    bstack1ll11l11l1_opy_ = CONFIG.get(bstack11lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᜅ"))[bstack1l111l1l_opy_]
    if bstack11lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᜆ") in CONFIG and CONFIG[bstack11lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᜇ")]:
        bstack11l1ll111_opy_(bstack1l1lll11ll_opy_, bstack1lllll1ll1_opy_)
    if desired_capabilities:
        bstack11ll1l1l_opy_ = bstack1llll1111l_opy_(desired_capabilities)
        bstack11ll1l1l_opy_[bstack11lll_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩᜈ")] = bstack1lll111l1_opy_(CONFIG)
        bstack11l1lll11_opy_ = bstack1l1lll1lll_opy_(bstack11ll1l1l_opy_)
        if bstack11l1lll11_opy_:
            bstack1l1lll11ll_opy_ = update(bstack11l1lll11_opy_, bstack1l1lll11ll_opy_)
        desired_capabilities = None
    if options:
        bstack111l111l1_opy_(options, bstack1l1lll11ll_opy_)
    if not options:
        options = bstack111l1lll1_opy_(bstack1l1lll11ll_opy_)
    if bstack1l11lll1_opy_.bstack1111l11l_opy_(CONFIG, bstack1l111l1l_opy_) and bstack1l11lll1_opy_.bstack1llll11lll_opy_(bstack1l1lll11ll_opy_, options):
        bstack1lll1llll1l_opy_ = True
        bstack1l11lll1_opy_.set_capabilities(bstack1l1lll11ll_opy_, CONFIG)
    if proxy and bstack1l1111l1_opy_() >= version.parse(bstack11lll_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪᜉ")):
        options.proxy(proxy)
    if options and bstack1l1111l1_opy_() >= version.parse(bstack11lll_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪᜊ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1l1111l1_opy_() < version.parse(bstack11lll_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫᜋ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1l1lll11ll_opy_)
    logger.info(bstack111lll11l_opy_)
    if bstack1l1111l1_opy_() >= version.parse(bstack11lll_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ᜌ")):
        bstack1lll11l1l_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l1111l1_opy_() >= version.parse(bstack11lll_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ᜍ")):
        bstack1lll11l1l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l1111l1_opy_() >= version.parse(bstack11lll_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨᜎ")):
        bstack1lll11l1l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1lll11l1l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack1llll1lll_opy_ = bstack11lll_opy_ (u"ࠩࠪᜏ")
        if bstack1l1111l1_opy_() >= version.parse(bstack11lll_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࡤ࠴ࠫᜐ")):
            bstack1llll1lll_opy_ = self.caps.get(bstack11lll_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦᜑ"))
        else:
            bstack1llll1lll_opy_ = self.capabilities.get(bstack11lll_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧᜒ"))
        if bstack1llll1lll_opy_:
            bstack1lllllll1l_opy_(bstack1llll1lll_opy_)
            if bstack1l1111l1_opy_() <= version.parse(bstack11lll_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭ᜓ")):
                self.command_executor._url = bstack11lll_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯᜔ࠣ") + bstack1l1ll1l1l_opy_ + bstack11lll_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦ᜕ࠧ")
            else:
                self.command_executor._url = bstack11lll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦ᜖") + bstack1llll1lll_opy_ + bstack11lll_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦ᜗")
            logger.debug(bstack1lll11l111_opy_.format(bstack1llll1lll_opy_))
        else:
            logger.debug(bstack1ll1llll11_opy_.format(bstack11lll_opy_ (u"ࠦࡔࡶࡴࡪ࡯ࡤࡰࠥࡎࡵࡣࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠧ᜘")))
    except Exception as e:
        logger.debug(bstack1ll1llll11_opy_.format(e))
    bstack11l1l1lll_opy_ = self.session_id
    if bstack11lll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ᜙") in bstack1lll11lll_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack11lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ᜚"), None)
        if item:
            bstack1llll11lll1_opy_ = getattr(item, bstack11lll_opy_ (u"ࠧࡠࡶࡨࡷࡹࡥࡣࡢࡵࡨࡣࡸࡺࡡࡳࡶࡨࡨࠬ᜛"), False)
            if not getattr(item, bstack11lll_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ᜜"), None) and bstack1llll11lll1_opy_:
                setattr(store[bstack11lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭᜝")], bstack11lll_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ᜞"), self)
        bstack1l111l11_opy_.bstack1lll111ll_opy_(self)
    bstack1l11lllll1_opy_.append(self)
    if bstack11lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᜟ") in CONFIG and bstack11lll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᜠ") in CONFIG[bstack11lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᜡ")][bstack1l111l1l_opy_]:
        bstack1ll1111ll1_opy_ = CONFIG[bstack11lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᜢ")][bstack1l111l1l_opy_][bstack11lll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᜣ")]
    logger.debug(bstack11l1ll1ll_opy_.format(bstack11l1l1lll_opy_))
def bstack1lll11ll_opy_(self, url):
    global bstack1l111l1l1_opy_
    global CONFIG
    try:
        bstack11ll1l11_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1l1ll11111_opy_.format(str(err)))
    try:
        bstack1l111l1l1_opy_(self, url)
    except Exception as e:
        try:
            bstack1l11llll_opy_ = str(e)
            if any(err_msg in bstack1l11llll_opy_ for err_msg in bstack11111l111_opy_):
                bstack11ll1l11_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1l1ll11111_opy_.format(str(err)))
        raise e
def bstack1lll1ll1_opy_(item, when):
    global bstack1111ll1l1_opy_
    try:
        bstack1111ll1l1_opy_(item, when)
    except Exception as e:
        pass
def bstack1l1l11l11l_opy_(item, call, rep):
    global bstack1llllllll1_opy_
    global bstack1l11lllll1_opy_
    name = bstack11lll_opy_ (u"ࠩࠪᜤ")
    try:
        if rep.when == bstack11lll_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᜥ"):
            bstack11l1l1lll_opy_ = threading.current_thread().bstackSessionId
            bstack1llll1l1l11_opy_ = item.config.getoption(bstack11lll_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᜦ"))
            try:
                if (str(bstack1llll1l1l11_opy_).lower() != bstack11lll_opy_ (u"ࠬࡺࡲࡶࡧࠪᜧ")):
                    name = str(rep.nodeid)
                    bstack1l1l11lll_opy_ = bstack1ll111llll_opy_(bstack11lll_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᜨ"), name, bstack11lll_opy_ (u"ࠧࠨᜩ"), bstack11lll_opy_ (u"ࠨࠩᜪ"), bstack11lll_opy_ (u"ࠩࠪᜫ"), bstack11lll_opy_ (u"ࠪࠫᜬ"))
                    os.environ[bstack11lll_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧᜭ")] = name
                    for driver in bstack1l11lllll1_opy_:
                        if bstack11l1l1lll_opy_ == driver.session_id:
                            driver.execute_script(bstack1l1l11lll_opy_)
            except Exception as e:
                logger.debug(bstack11lll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬᜮ").format(str(e)))
            try:
                bstack1llll111l_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack11lll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᜯ"):
                    status = bstack11lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᜰ") if rep.outcome.lower() == bstack11lll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᜱ") else bstack11lll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᜲ")
                    reason = bstack11lll_opy_ (u"ࠪࠫᜳ")
                    if status == bstack11lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧ᜴ࠫ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack11lll_opy_ (u"ࠬ࡯࡮ࡧࡱࠪ᜵") if status == bstack11lll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭᜶") else bstack11lll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭᜷")
                    data = name + bstack11lll_opy_ (u"ࠨࠢࡳࡥࡸࡹࡥࡥࠣࠪ᜸") if status == bstack11lll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ᜹") else name + bstack11lll_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠥࠥ࠭᜺") + reason
                    bstack1l1l1ll1l1_opy_ = bstack1ll111llll_opy_(bstack11lll_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭᜻"), bstack11lll_opy_ (u"ࠬ࠭᜼"), bstack11lll_opy_ (u"࠭ࠧ᜽"), bstack11lll_opy_ (u"ࠧࠨ᜾"), level, data)
                    for driver in bstack1l11lllll1_opy_:
                        if bstack11l1l1lll_opy_ == driver.session_id:
                            driver.execute_script(bstack1l1l1ll1l1_opy_)
            except Exception as e:
                logger.debug(bstack11lll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡩ࡯࡯ࡶࡨࡼࡹࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬ᜿").format(str(e)))
    except Exception as e:
        logger.debug(bstack11lll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡴࡢࡶࡨࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿࢂ࠭ᝀ").format(str(e)))
    bstack1llllllll1_opy_(item, call, rep)
notset = Notset()
def bstack111l1ll1_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1llll1lll1_opy_
    if str(name).lower() == bstack11lll_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪᝁ"):
        return bstack11lll_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥᝂ")
    else:
        return bstack1llll1lll1_opy_(self, name, default, skip)
def bstack11l1l11l1_opy_(self):
    global CONFIG
    global bstack11l1llll1_opy_
    try:
        proxy = bstack1l11l1ll_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack11lll_opy_ (u"ࠬ࠴ࡰࡢࡥࠪᝃ")):
                proxies = bstack111111ll_opy_(proxy, bstack1ll111ll11_opy_())
                if len(proxies) > 0:
                    protocol, bstack1lll1l111l_opy_ = proxies.popitem()
                    if bstack11lll_opy_ (u"ࠨ࠺࠰࠱ࠥᝄ") in bstack1lll1l111l_opy_:
                        return bstack1lll1l111l_opy_
                    else:
                        return bstack11lll_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣᝅ") + bstack1lll1l111l_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack11lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡵࡸ࡯ࡹࡻࠣࡹࡷࡲࠠ࠻ࠢࡾࢁࠧᝆ").format(str(e)))
    return bstack11l1llll1_opy_(self)
def bstack1lll1ll1l1_opy_():
    return (bstack11lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᝇ") in CONFIG or bstack11lll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᝈ") in CONFIG) and bstack1ll1llll_opy_() and bstack1l1111l1_opy_() >= version.parse(
        bstack1l111llll_opy_)
def bstack1ll111111_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1ll1111ll1_opy_
    global bstack1ll11ll1ll_opy_
    global bstack1lll11lll_opy_
    CONFIG[bstack11lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᝉ")] = str(bstack1lll11lll_opy_) + str(__version__)
    bstack1l111l1l_opy_ = 0
    try:
        if bstack1ll11ll1ll_opy_ is True:
            bstack1l111l1l_opy_ = int(os.environ.get(bstack11lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᝊ")))
    except:
        bstack1l111l1l_opy_ = 0
    CONFIG[bstack11lll_opy_ (u"ࠨࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᝋ")] = True
    bstack1l1lll11ll_opy_ = bstack1l1lll1lll_opy_(CONFIG, bstack1l111l1l_opy_)
    logger.debug(bstack1l1l11ll11_opy_.format(str(bstack1l1lll11ll_opy_)))
    if CONFIG.get(bstack11lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᝌ")):
        bstack11l1ll111_opy_(bstack1l1lll11ll_opy_, bstack1lllll1ll1_opy_)
    if bstack11lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᝍ") in CONFIG and bstack11lll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᝎ") in CONFIG[bstack11lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᝏ")][bstack1l111l1l_opy_]:
        bstack1ll1111ll1_opy_ = CONFIG[bstack11lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᝐ")][bstack1l111l1l_opy_][bstack11lll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᝑ")]
    import urllib
    import json
    bstack1lll1ll11l_opy_ = bstack11lll_opy_ (u"࠭ࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠨᝒ") + urllib.parse.quote(json.dumps(bstack1l1lll11ll_opy_))
    browser = self.connect(bstack1lll1ll11l_opy_)
    return browser
def bstack1l1ll1111_opy_():
    global bstack1l1l1l1ll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1ll111111_opy_
        bstack1l1l1l1ll_opy_ = True
    except Exception as e:
        pass
def bstack1lll1ll1l11_opy_():
    global CONFIG
    global bstack1llll1ll1l_opy_
    global bstack1l1ll1l1l_opy_
    global bstack1lllll1ll1_opy_
    global bstack1ll11ll1ll_opy_
    global bstack1lllllllll_opy_
    CONFIG = json.loads(os.environ.get(bstack11lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌ࠭ᝓ")))
    bstack1llll1ll1l_opy_ = eval(os.environ.get(bstack11lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ᝔")))
    bstack1l1ll1l1l_opy_ = os.environ.get(bstack11lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡊࡘࡆࡤ࡛ࡒࡍࠩ᝕"))
    bstack1l1ll111l_opy_(CONFIG, bstack1llll1ll1l_opy_)
    bstack1lllllllll_opy_ = bstack11lll1ll_opy_.bstack11l1l11ll_opy_(CONFIG, bstack1lllllllll_opy_)
    global bstack1lll11l1l_opy_
    global bstack1llll1ll1_opy_
    global bstack11llll1l_opy_
    global bstack1llll1l1l1_opy_
    global bstack1l1ll1llll_opy_
    global bstack1ll1111l1l_opy_
    global bstack1ll111l11l_opy_
    global bstack1l111l1l1_opy_
    global bstack11l1llll1_opy_
    global bstack1llll1lll1_opy_
    global bstack1111ll1l1_opy_
    global bstack1llllllll1_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1lll11l1l_opy_ = webdriver.Remote.__init__
        bstack1llll1ll1_opy_ = WebDriver.quit
        bstack1ll111l11l_opy_ = WebDriver.close
        bstack1l111l1l1_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack11lll_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭᝖") in CONFIG or bstack11lll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ᝗") in CONFIG) and bstack1ll1llll_opy_():
        if bstack1l1111l1_opy_() < version.parse(bstack1l111llll_opy_):
            logger.error(bstack1l1l11l11_opy_.format(bstack1l1111l1_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack11l1llll1_opy_ = RemoteConnection._get_proxy_url
            except Exception as e:
                logger.error(bstack1llll11l1l_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1llll1lll1_opy_ = Config.getoption
        from _pytest import runner
        bstack1111ll1l1_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack111lll1ll_opy_)
    try:
        from pytest_bdd import reporting
        bstack1llllllll1_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack11lll_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡴࠦࡲࡶࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࡸ࠭᝘"))
    bstack1lllll1ll1_opy_ = CONFIG.get(bstack11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ᝙"), {}).get(bstack11lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ᝚"))
    bstack1ll11ll1ll_opy_ = True
    bstack1l1111lll_opy_(bstack1lll1l1lll_opy_)
if (bstack11l11l1l1l_opy_()):
    bstack1lll1ll1l11_opy_()
@bstack1l111l1ll1_opy_(class_method=False)
def bstack1llll1l1111_opy_(hook_name, event, bstack1llll1111l1_opy_=None):
    if hook_name not in [bstack11lll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ᝛"), bstack11lll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭᝜"), bstack11lll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩ᝝"), bstack11lll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭᝞"), bstack11lll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪ᝟"), bstack11lll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧᝠ"), bstack11lll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ᝡ"), bstack11lll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪᝢ")]:
        return
    node = store[bstack11lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ᝣ")]
    if hook_name in [bstack11lll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩᝤ"), bstack11lll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭ᝥ")]:
        node = store[bstack11lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥ࡭ࡰࡦࡸࡰࡪࡥࡩࡵࡧࡰࠫᝦ")]
    elif hook_name in [bstack11lll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫᝧ"), bstack11lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨᝨ")]:
        node = store[bstack11lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡦࡰࡦࡹࡳࡠ࡫ࡷࡩࡲ࠭ᝩ")]
    if event == bstack11lll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩᝪ"):
        hook_type = bstack11111ll11l_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack1l11l111l1_opy_ = {
            bstack11lll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᝫ"): uuid,
            bstack11lll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᝬ"): bstack1ll1ll1lll_opy_(),
            bstack11lll_opy_ (u"ࠬࡺࡹࡱࡧࠪ᝭"): bstack11lll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᝮ"),
            bstack11lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᝯ"): hook_type,
            bstack11lll_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫᝰ"): hook_name
        }
        store[bstack11lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭᝱")].append(uuid)
        bstack1llll11ll11_opy_ = node.nodeid
        if hook_type == bstack11lll_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨᝲ"):
            if not _1l1111lll1_opy_.get(bstack1llll11ll11_opy_, None):
                _1l1111lll1_opy_[bstack1llll11ll11_opy_] = {bstack11lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᝳ"): []}
            _1l1111lll1_opy_[bstack1llll11ll11_opy_][bstack11lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ᝴")].append(bstack1l11l111l1_opy_[bstack11lll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ᝵")])
        _1l1111lll1_opy_[bstack1llll11ll11_opy_ + bstack11lll_opy_ (u"ࠧ࠮ࠩ᝶") + hook_name] = bstack1l11l111l1_opy_
        bstack1llll111l1l_opy_(node, bstack1l11l111l1_opy_, bstack11lll_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ᝷"))
    elif event == bstack11lll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨ᝸"):
        bstack11lllllll1_opy_ = node.nodeid + bstack11lll_opy_ (u"ࠪ࠱ࠬ᝹") + hook_name
        _1l1111lll1_opy_[bstack11lllllll1_opy_][bstack11lll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ᝺")] = bstack1ll1ll1lll_opy_()
        bstack1llll11l11l_opy_(_1l1111lll1_opy_[bstack11lllllll1_opy_][bstack11lll_opy_ (u"ࠬࡻࡵࡪࡦࠪ᝻")])
        bstack1llll111l1l_opy_(node, _1l1111lll1_opy_[bstack11lllllll1_opy_], bstack11lll_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ᝼"), bstack1llll11l1ll_opy_=bstack1llll1111l1_opy_)
def bstack1llll1l111l_opy_():
    global bstack1llll11ll1l_opy_
    if bstack1lll1lll1l_opy_():
        bstack1llll11ll1l_opy_ = bstack11lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫ᝽")
    else:
        bstack1llll11ll1l_opy_ = bstack11lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ᝾")
@bstack1l111l11_opy_.bstack1lllll111l1_opy_
def bstack1llll1l11l1_opy_():
    bstack1llll1l111l_opy_()
    if bstack1ll1llll_opy_():
        bstack1111l1l1l_opy_(bstack1llll11111_opy_)
    bstack11l1111lll_opy_ = bstack11l111111l_opy_(bstack1llll1l1111_opy_)
bstack1llll1l11l1_opy_()