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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1l1l1l1l11_opy_, bstack1lll11l1ll_opy_
class bstack1ll1l1l1ll_opy_:
  working_dir = os.getcwd()
  bstack11llll111_opy_ = False
  config = {}
  binary_path = bstack11lll_opy_ (u"ࠫࠬ፮")
  bstack1111lll11l_opy_ = bstack11lll_opy_ (u"ࠬ࠭፯")
  bstack1111lll1_opy_ = False
  bstack111l11l1ll_opy_ = None
  bstack111l1ll1l1_opy_ = {}
  bstack111l11l11l_opy_ = 300
  bstack111l1l1lll_opy_ = False
  logger = None
  bstack111l1111l1_opy_ = False
  bstack111l1lllll_opy_ = bstack11lll_opy_ (u"࠭ࠧ፰")
  bstack111l11111l_opy_ = {
    bstack11lll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ፱") : 1,
    bstack11lll_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩ፲") : 2,
    bstack11lll_opy_ (u"ࠩࡨࡨ࡬࡫ࠧ፳") : 3,
    bstack11lll_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪ፴") : 4
  }
  def __init__(self) -> None: pass
  def bstack111ll1l111_opy_(self):
    bstack111l1ll11l_opy_ = bstack11lll_opy_ (u"ࠫࠬ፵")
    bstack1111lllll1_opy_ = sys.platform
    bstack1111ll1l1l_opy_ = bstack11lll_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ፶")
    if re.match(bstack11lll_opy_ (u"ࠨࡤࡢࡴࡺ࡭ࡳࢂ࡭ࡢࡥࠣࡳࡸࠨ፷"), bstack1111lllll1_opy_) != None:
      bstack111l1ll11l_opy_ = bstack11ll111111_opy_ + bstack11lll_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭ࡰࡵࡻ࠲ࡿ࡯ࡰࠣ፸")
      self.bstack111l1lllll_opy_ = bstack11lll_opy_ (u"ࠨ࡯ࡤࡧࠬ፹")
    elif re.match(bstack11lll_opy_ (u"ࠤࡰࡷࡼ࡯࡮ࡽ࡯ࡶࡽࡸࢂ࡭ࡪࡰࡪࡻࢁࡩࡹࡨࡹ࡬ࡲࢁࡨࡣࡤࡹ࡬ࡲࢁࡽࡩ࡯ࡥࡨࢀࡪࡳࡣࡽࡹ࡬ࡲ࠸࠸ࠢ፺"), bstack1111lllll1_opy_) != None:
      bstack111l1ll11l_opy_ = bstack11ll111111_opy_ + bstack11lll_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡻ࡮ࡴ࠮ࡻ࡫ࡳࠦ፻")
      bstack1111ll1l1l_opy_ = bstack11lll_opy_ (u"ࠦࡵ࡫ࡲࡤࡻ࠱ࡩࡽ࡫ࠢ፼")
      self.bstack111l1lllll_opy_ = bstack11lll_opy_ (u"ࠬࡽࡩ࡯ࠩ፽")
    else:
      bstack111l1ll11l_opy_ = bstack11ll111111_opy_ + bstack11lll_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳࡬ࡪࡰࡸࡼ࠳ࢀࡩࡱࠤ፾")
      self.bstack111l1lllll_opy_ = bstack11lll_opy_ (u"ࠧ࡭࡫ࡱࡹࡽ࠭፿")
    return bstack111l1ll11l_opy_, bstack1111ll1l1l_opy_
  def bstack111ll111ll_opy_(self):
    try:
      bstack111l111ll1_opy_ = [os.path.join(expanduser(bstack11lll_opy_ (u"ࠣࢀࠥᎀ")), bstack11lll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᎁ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack111l111ll1_opy_:
        if(self.bstack111ll1111l_opy_(path)):
          return path
      raise bstack11lll_opy_ (u"࡙ࠥࡳࡧ࡬ࡣࡧࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠢᎂ")
    except Exception as e:
      self.logger.error(bstack11lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥࠡࡲࡤࡸ࡭ࠦࡦࡰࡴࠣࡴࡪࡸࡣࡺࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࠯ࠣࡿࢂࠨᎃ").format(e))
  def bstack111ll1111l_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1111lll111_opy_(self, bstack111l1ll11l_opy_, bstack1111ll1l1l_opy_):
    try:
      bstack111l1l1l11_opy_ = self.bstack111ll111ll_opy_()
      bstack111l111111_opy_ = os.path.join(bstack111l1l1l11_opy_, bstack11lll_opy_ (u"ࠬࡶࡥࡳࡥࡼ࠲ࡿ࡯ࡰࠨᎄ"))
      bstack111l11llll_opy_ = os.path.join(bstack111l1l1l11_opy_, bstack1111ll1l1l_opy_)
      if os.path.exists(bstack111l11llll_opy_):
        self.logger.info(bstack11lll_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡼࡿ࠯ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡤࡰࡹࡱࡰࡴࡧࡤࠣᎅ").format(bstack111l11llll_opy_))
        return bstack111l11llll_opy_
      if os.path.exists(bstack111l111111_opy_):
        self.logger.info(bstack11lll_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡺࡪࡲࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࢁࡽ࠭ࠢࡸࡲࡿ࡯ࡰࡱ࡫ࡱ࡫ࠧᎆ").format(bstack111l111111_opy_))
        return self.bstack111l11l1l1_opy_(bstack111l111111_opy_, bstack1111ll1l1l_opy_)
      self.logger.info(bstack11lll_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥ࡬ࡲࡰ࡯ࠣࡿࢂࠨᎇ").format(bstack111l1ll11l_opy_))
      response = bstack1lll11l1ll_opy_(bstack11lll_opy_ (u"ࠩࡊࡉ࡙࠭ᎈ"), bstack111l1ll11l_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack111l111111_opy_, bstack11lll_opy_ (u"ࠪࡻࡧ࠭ᎉ")) as file:
          file.write(response.content)
        self.logger.info(bstack111l11ll11_opy_ (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡢࡰࡧࠤࡸࡧࡶࡦࡦࠣࡥࡹࠦࡻࡣ࡫ࡱࡥࡷࡿ࡟ࡻ࡫ࡳࡣࡵࡧࡴࡩࡿࠥᎊ"))
        return self.bstack111l11l1l1_opy_(bstack111l111111_opy_, bstack1111ll1l1l_opy_)
      else:
        raise(bstack111l11ll11_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡸ࡭࡫ࠠࡧ࡫࡯ࡩ࠳ࠦࡓࡵࡣࡷࡹࡸࠦࡣࡰࡦࡨ࠾ࠥࢁࡲࡦࡵࡳࡳࡳࡹࡥ࠯ࡵࡷࡥࡹࡻࡳࡠࡥࡲࡨࡪࢃࠢᎋ"))
    except:
      self.logger.error(bstack11lll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥᎌ"))
  def bstack1111llllll_opy_(self, bstack111l1ll11l_opy_, bstack1111ll1l1l_opy_):
    try:
      bstack111l11llll_opy_ = self.bstack1111lll111_opy_(bstack111l1ll11l_opy_, bstack1111ll1l1l_opy_)
      bstack111l1l1ll1_opy_ = self.bstack111l1llll1_opy_(bstack111l1ll11l_opy_, bstack1111ll1l1l_opy_, bstack111l11llll_opy_)
      return bstack111l11llll_opy_, bstack111l1l1ll1_opy_
    except Exception as e:
      self.logger.error(bstack11lll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣ࡫ࡪࡺࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡰࡢࡶ࡫ࠦᎍ").format(e))
    return bstack111l11llll_opy_, False
  def bstack111l1llll1_opy_(self, bstack111l1ll11l_opy_, bstack1111ll1l1l_opy_, bstack111l11llll_opy_, bstack1111ll1lll_opy_ = 0):
    if bstack1111ll1lll_opy_ > 1:
      return False
    if bstack111l11llll_opy_ == None or os.path.exists(bstack111l11llll_opy_) == False:
      self.logger.warn(bstack11lll_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡱࡣࡷ࡬ࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤ࠭ࠢࡵࡩࡹࡸࡹࡪࡰࡪࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠨᎎ"))
      bstack111l11llll_opy_ = self.bstack1111lll111_opy_(bstack111l1ll11l_opy_, bstack1111ll1l1l_opy_)
      self.bstack111l1llll1_opy_(bstack111l1ll11l_opy_, bstack1111ll1l1l_opy_, bstack111l11llll_opy_, bstack1111ll1lll_opy_+1)
    bstack1111lll1ll_opy_ = bstack11lll_opy_ (u"ࠤࡡ࠲࠯ࡆࡰࡦࡴࡦࡽࡡ࠵ࡣ࡭࡫ࠣࡠࡩ࠴࡜ࡥ࠭࠱ࡠࡩ࠱ࠢᎏ")
    command = bstack11lll_opy_ (u"ࠪࡿࢂࠦ࠭࠮ࡸࡨࡶࡸ࡯࡯࡯ࠩ᎐").format(bstack111l11llll_opy_)
    bstack1111ll1ll1_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack1111lll1ll_opy_, bstack1111ll1ll1_opy_) != None:
      return True
    else:
      self.logger.error(bstack11lll_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡺࡪࡸࡳࡪࡱࡱࠤࡨ࡮ࡥࡤ࡭ࠣࡪࡦ࡯࡬ࡦࡦࠥ᎑"))
      bstack111l11llll_opy_ = self.bstack1111lll111_opy_(bstack111l1ll11l_opy_, bstack1111ll1l1l_opy_)
      self.bstack111l1llll1_opy_(bstack111l1ll11l_opy_, bstack1111ll1l1l_opy_, bstack111l11llll_opy_, bstack1111ll1lll_opy_+1)
  def bstack111l11l1l1_opy_(self, bstack111l111111_opy_, bstack1111ll1l1l_opy_):
    try:
      working_dir = os.path.dirname(bstack111l111111_opy_)
      shutil.unpack_archive(bstack111l111111_opy_, working_dir)
      bstack111l11llll_opy_ = os.path.join(working_dir, bstack1111ll1l1l_opy_)
      os.chmod(bstack111l11llll_opy_, 0o755)
      return bstack111l11llll_opy_
    except Exception as e:
      self.logger.error(bstack11lll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡷࡱࡾ࡮ࡶࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠨ᎒"))
  def bstack111ll11l11_opy_(self):
    try:
      percy = str(self.config.get(bstack11lll_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ᎓"), bstack11lll_opy_ (u"ࠢࡧࡣ࡯ࡷࡪࠨ᎔"))).lower()
      if percy != bstack11lll_opy_ (u"ࠣࡶࡵࡹࡪࠨ᎕"):
        return False
      self.bstack1111lll1_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack11lll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡦࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦ᎖").format(e))
  def bstack111l1ll1ll_opy_(self):
    try:
      bstack111l1ll1ll_opy_ = str(self.config.get(bstack11lll_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ࠭᎗"), bstack11lll_opy_ (u"ࠦࡦࡻࡴࡰࠤ᎘"))).lower()
      return bstack111l1ll1ll_opy_
    except Exception as e:
      self.logger.error(bstack11lll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡩࡴࠡࡲࡨࡶࡨࡿࠠࡤࡣࡳࡸࡺࡸࡥࠡ࡯ࡲࡨࡪ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨ᎙").format(e))
  def init(self, bstack11llll111_opy_, config, logger):
    self.bstack11llll111_opy_ = bstack11llll111_opy_
    self.config = config
    self.logger = logger
    if not self.bstack111ll11l11_opy_():
      return
    self.bstack111l1ll1l1_opy_ = config.get(bstack11lll_opy_ (u"࠭ࡰࡦࡴࡦࡽࡔࡶࡴࡪࡱࡱࡷࠬ᎚"), {})
    self.bstack1111llll1l_opy_ = config.get(bstack11lll_opy_ (u"ࠧࡱࡧࡵࡧࡾࡉࡡࡱࡶࡸࡶࡪࡓ࡯ࡥࡧࠪ᎛"), bstack11lll_opy_ (u"ࠣࡣࡸࡸࡴࠨ᎜"))
    try:
      bstack111l1ll11l_opy_, bstack1111ll1l1l_opy_ = self.bstack111ll1l111_opy_()
      bstack111l11llll_opy_, bstack111l1l1ll1_opy_ = self.bstack1111llllll_opy_(bstack111l1ll11l_opy_, bstack1111ll1l1l_opy_)
      if bstack111l1l1ll1_opy_:
        self.binary_path = bstack111l11llll_opy_
        thread = Thread(target=self.bstack1111lll1l1_opy_)
        thread.start()
      else:
        self.bstack111l1111l1_opy_ = True
        self.logger.error(bstack11lll_opy_ (u"ࠤࡌࡲࡻࡧ࡬ࡪࡦࠣࡴࡪࡸࡣࡺࠢࡳࡥࡹ࡮ࠠࡧࡱࡸࡲࡩࠦ࠭ࠡࡽࢀ࠰࡛ࠥ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡑࡧࡵࡧࡾࠨ᎝").format(bstack111l11llll_opy_))
    except Exception as e:
      self.logger.error(bstack11lll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦ᎞").format(e))
  def bstack111ll11lll_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack11lll_opy_ (u"ࠫࡱࡵࡧࠨ᎟"), bstack11lll_opy_ (u"ࠬࡶࡥࡳࡥࡼ࠲ࡱࡵࡧࠨᎠ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack11lll_opy_ (u"ࠨࡐࡶࡵ࡫࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦ࡬ࡰࡩࡶࠤࡦࡺࠠࡼࡿࠥᎡ").format(logfile))
      self.bstack1111lll11l_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack11lll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡪࡺࠠࡱࡧࡵࡧࡾࠦ࡬ࡰࡩࠣࡴࡦࡺࡨ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᎢ").format(e))
  def bstack1111lll1l1_opy_(self):
    bstack111l1l11l1_opy_ = self.bstack111ll11l1l_opy_()
    if bstack111l1l11l1_opy_ == None:
      self.bstack111l1111l1_opy_ = True
      self.logger.error(bstack11lll_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡵࡱ࡮ࡩࡳࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼࠦᎣ"))
      return False
    command_args = [bstack11lll_opy_ (u"ࠤࡤࡴࡵࡀࡥࡹࡧࡦ࠾ࡸࡺࡡࡳࡶࠥᎤ") if self.bstack11llll111_opy_ else bstack11lll_opy_ (u"ࠪࡩࡽ࡫ࡣ࠻ࡵࡷࡥࡷࡺࠧᎥ")]
    bstack111l1l111l_opy_ = self.bstack1111ll1l11_opy_()
    if bstack111l1l111l_opy_ != None:
      command_args.append(bstack11lll_opy_ (u"ࠦ࠲ࡩࠠࡼࡿࠥᎦ").format(bstack111l1l111l_opy_))
    env = os.environ.copy()
    env[bstack11lll_opy_ (u"ࠧࡖࡅࡓࡅ࡜ࡣ࡙ࡕࡋࡆࡐࠥᎧ")] = bstack111l1l11l1_opy_
    bstack111ll11ll1_opy_ = [self.binary_path]
    self.bstack111ll11lll_opy_()
    self.bstack111l11l1ll_opy_ = self.bstack111l111l1l_opy_(bstack111ll11ll1_opy_ + command_args, env)
    self.logger.debug(bstack11lll_opy_ (u"ࠨࡓࡵࡣࡵࡸ࡮ࡴࡧࠡࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠢᎨ"))
    bstack1111ll1lll_opy_ = 0
    while self.bstack111l11l1ll_opy_.poll() == None:
      bstack1111llll11_opy_ = self.bstack111ll111l1_opy_()
      if bstack1111llll11_opy_:
        self.logger.debug(bstack11lll_opy_ (u"ࠢࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠥᎩ"))
        self.bstack111l1l1lll_opy_ = True
        return True
      bstack1111ll1lll_opy_ += 1
      self.logger.debug(bstack11lll_opy_ (u"ࠣࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡓࡧࡷࡶࡾࠦ࠭ࠡࡽࢀࠦᎪ").format(bstack1111ll1lll_opy_))
      time.sleep(2)
    self.logger.error(bstack11lll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡊࡦ࡯࡬ࡦࡦࠣࡥ࡫ࡺࡥࡳࠢࡾࢁࠥࡧࡴࡵࡧࡰࡴࡹࡹࠢᎫ").format(bstack1111ll1lll_opy_))
    self.bstack111l1111l1_opy_ = True
    return False
  def bstack111ll111l1_opy_(self, bstack1111ll1lll_opy_ = 0):
    try:
      if bstack1111ll1lll_opy_ > 10:
        return False
      bstack111l111l11_opy_ = os.environ.get(bstack11lll_opy_ (u"ࠪࡔࡊࡘࡃ࡚ࡡࡖࡉࡗ࡜ࡅࡓࡡࡄࡈࡉࡘࡅࡔࡕࠪᎬ"), bstack11lll_opy_ (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࡱࡵࡣࡢ࡮࡫ࡳࡸࡺ࠺࠶࠵࠶࠼ࠬᎭ"))
      bstack111l1lll1l_opy_ = bstack111l111l11_opy_ + bstack11l1lllll1_opy_
      response = requests.get(bstack111l1lll1l_opy_)
      return True if response.json() else False
    except:
      return False
  def bstack111ll11l1l_opy_(self):
    bstack111l1l1111_opy_ = bstack11lll_opy_ (u"ࠬࡧࡰࡱࠩᎮ") if self.bstack11llll111_opy_ else bstack11lll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨᎯ")
    bstack11l1l1ll1l_opy_ = bstack11lll_opy_ (u"ࠢࡢࡲ࡬࠳ࡦࡶࡰࡠࡲࡨࡶࡨࡿ࠯ࡨࡧࡷࡣࡵࡸ࡯࡫ࡧࡦࡸࡤࡺ࡯࡬ࡧࡱࡃࡳࡧ࡭ࡦ࠿ࡾࢁࠫࡺࡹࡱࡧࡀࡿࢂࠨᎰ").format(self.config[bstack11lll_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭Ꮁ")], bstack111l1l1111_opy_)
    uri = bstack1l1l1l1l11_opy_(bstack11l1l1ll1l_opy_)
    try:
      response = bstack1lll11l1ll_opy_(bstack11lll_opy_ (u"ࠩࡊࡉ࡙࠭Ꮂ"), uri, {}, {bstack11lll_opy_ (u"ࠪࡥࡺࡺࡨࠨᎳ"): (self.config[bstack11lll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭Ꮄ")], self.config[bstack11lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᎵ")])})
      if response.status_code == 200:
        bstack111l1l1l1l_opy_ = response.json()
        if bstack11lll_opy_ (u"ࠨࡴࡰ࡭ࡨࡲࠧᎶ") in bstack111l1l1l1l_opy_:
          return bstack111l1l1l1l_opy_[bstack11lll_opy_ (u"ࠢࡵࡱ࡮ࡩࡳࠨᎷ")]
        else:
          raise bstack11lll_opy_ (u"ࠨࡖࡲ࡯ࡪࡴࠠࡏࡱࡷࠤࡋࡵࡵ࡯ࡦࠣ࠱ࠥࢁࡽࠨᎸ").format(bstack111l1l1l1l_opy_)
      else:
        raise bstack11lll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡥࡵࡥ࡫ࠤࡵ࡫ࡲࡤࡻࠣࡸࡴࡱࡥ࡯࠮ࠣࡖࡪࡹࡰࡰࡰࡶࡩࠥࡹࡴࡢࡶࡸࡷࠥ࠳ࠠࡼࡿ࠯ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡂࡰࡦࡼࠤ࠲ࠦࡻࡾࠤᎹ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack11lll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡴࡷࡵࡪࡦࡥࡷࠦᎺ").format(e))
  def bstack1111ll1l11_opy_(self):
    bstack111ll11111_opy_ = os.path.join(tempfile.gettempdir(), bstack11lll_opy_ (u"ࠦࡵ࡫ࡲࡤࡻࡆࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠢᎻ"))
    try:
      if bstack11lll_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭Ꮌ") not in self.bstack111l1ll1l1_opy_:
        self.bstack111l1ll1l1_opy_[bstack11lll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧᎽ")] = 2
      with open(bstack111ll11111_opy_, bstack11lll_opy_ (u"ࠧࡸࠩᎾ")) as fp:
        json.dump(self.bstack111l1ll1l1_opy_, fp)
      return bstack111ll11111_opy_
    except Exception as e:
      self.logger.error(bstack11lll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡨࡸࡥࡢࡶࡨࠤࡵ࡫ࡲࡤࡻࠣࡧࡴࡴࡦ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᎿ").format(e))
  def bstack111l111l1l_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack111l1lllll_opy_ == bstack11lll_opy_ (u"ࠩࡺ࡭ࡳ࠭Ꮐ"):
        bstack111l1l11ll_opy_ = [bstack11lll_opy_ (u"ࠪࡧࡲࡪ࠮ࡦࡺࡨࠫᏁ"), bstack11lll_opy_ (u"ࠫ࠴ࡩࠧᏂ")]
        cmd = bstack111l1l11ll_opy_ + cmd
      cmd = bstack11lll_opy_ (u"ࠬࠦࠧᏃ").join(cmd)
      self.logger.debug(bstack11lll_opy_ (u"ࠨࡒࡶࡰࡱ࡭ࡳ࡭ࠠࡼࡿࠥᏄ").format(cmd))
      with open(self.bstack1111lll11l_opy_, bstack11lll_opy_ (u"ࠢࡢࠤᏅ")) as bstack111l11l111_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack111l11l111_opy_, text=True, stderr=bstack111l11l111_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack111l1111l1_opy_ = True
      self.logger.error(bstack11lll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺࠢࡺ࡭ࡹ࡮ࠠࡤ࡯ࡧࠤ࠲ࠦࡻࡾ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࡼࡿࠥᏆ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack111l1l1lll_opy_:
        self.logger.info(bstack11lll_opy_ (u"ࠤࡖࡸࡴࡶࡰࡪࡰࡪࠤࡕ࡫ࡲࡤࡻࠥᏇ"))
        cmd = [self.binary_path, bstack11lll_opy_ (u"ࠥࡩࡽ࡫ࡣ࠻ࡵࡷࡳࡵࠨᏈ")]
        self.bstack111l111l1l_opy_(cmd)
        self.bstack111l1l1lll_opy_ = False
    except Exception as e:
      self.logger.error(bstack11lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡲࡴࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡷࡪࡶ࡫ࠤࡨࡵ࡭࡮ࡣࡱࡨࠥ࠳ࠠࡼࡿ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦᏉ").format(cmd, e))
  def bstack11l1lll1l_opy_(self):
    if not self.bstack1111lll1_opy_:
      return
    try:
      bstack111l1ll111_opy_ = 0
      while not self.bstack111l1l1lll_opy_ and bstack111l1ll111_opy_ < self.bstack111l11l11l_opy_:
        if self.bstack111l1111l1_opy_:
          self.logger.info(bstack11lll_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡸ࡫ࡴࡶࡲࠣࡪࡦ࡯࡬ࡦࡦࠥᏊ"))
          return
        time.sleep(1)
        bstack111l1ll111_opy_ += 1
      os.environ[bstack11lll_opy_ (u"࠭ࡐࡆࡔࡆ࡝ࡤࡈࡅࡔࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࠬᏋ")] = str(self.bstack111l11lll1_opy_())
      self.logger.info(bstack11lll_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡳࡦࡶࡸࡴࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠣᏌ"))
    except Exception as e:
      self.logger.error(bstack11lll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸ࡫ࡴࡶࡲࠣࡴࡪࡸࡣࡺ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᏍ").format(e))
  def bstack111l11lll1_opy_(self):
    if self.bstack11llll111_opy_:
      return
    try:
      bstack111l1111ll_opy_ = [platform[bstack11lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᏎ")].lower() for platform in self.config.get(bstack11lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭Ꮟ"), [])]
      bstack111l11ll1l_opy_ = sys.maxsize
      bstack111l1lll11_opy_ = bstack11lll_opy_ (u"ࠫࠬᏐ")
      for browser in bstack111l1111ll_opy_:
        if browser in self.bstack111l11111l_opy_:
          bstack111l111lll_opy_ = self.bstack111l11111l_opy_[browser]
        if bstack111l111lll_opy_ < bstack111l11ll1l_opy_:
          bstack111l11ll1l_opy_ = bstack111l111lll_opy_
          bstack111l1lll11_opy_ = browser
      return bstack111l1lll11_opy_
    except Exception as e:
      self.logger.error(bstack11lll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡢࡦࡵࡷࠤࡵࡲࡡࡵࡨࡲࡶࡲ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨᏑ").format(e))