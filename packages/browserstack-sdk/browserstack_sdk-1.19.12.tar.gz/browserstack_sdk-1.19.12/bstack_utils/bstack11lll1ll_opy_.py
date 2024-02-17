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
import sys
import logging
import tarfile
import io
import os
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11ll11111l_opy_
import tempfile
import json
bstack111lll11l1_opy_ = os.path.join(tempfile.gettempdir(), bstack11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡩ࡫ࡢࡶࡩ࠱ࡰࡴ࡭ࠧዸ"))
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack11lll_opy_ (u"࠭࡜࡯ࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫዹ"),
      datefmt=bstack11lll_opy_ (u"ࠧࠦࡊ࠽ࠩࡒࡀࠥࡔࠩዺ"),
      stream=sys.stdout
    )
  return logger
def bstack11l1l11ll_opy_(config, log_level):
  bstack111lll111l_opy_ = log_level
  if bstack11lll_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪዻ") in config:
    bstack111lll111l_opy_ = bstack11ll11111l_opy_[config[bstack11lll_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫዼ")]]
  if config.get(bstack11lll_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬዽ"), False):
    logging.getLogger().setLevel(bstack111lll111l_opy_)
    return bstack111lll111l_opy_
  global bstack111lll11l1_opy_
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
  bstack111ll1llll_opy_ = logging.Formatter(
    fmt=bstack11lll_opy_ (u"ࠫࡡࡴࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴࠩዾ"),
    datefmt=bstack11lll_opy_ (u"ࠬࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧዿ")
  )
  bstack111lll1111_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack111lll11l1_opy_)
  file_handler.setFormatter(bstack111ll1llll_opy_)
  bstack111lll1111_opy_.setFormatter(bstack111ll1llll_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack111lll1111_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack11lll_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠯ࡹࡨࡦࡩࡸࡩࡷࡧࡵ࠲ࡷ࡫࡭ࡰࡶࡨ࠲ࡷ࡫࡭ࡰࡶࡨࡣࡨࡵ࡮࡯ࡧࡦࡸ࡮ࡵ࡮ࠨጀ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack111lll1111_opy_.setLevel(bstack111lll111l_opy_)
  logging.getLogger().addHandler(bstack111lll1111_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack111lll111l_opy_
def bstack111llll1l1_opy_(config):
  try:
    bstack111lll1l1l_opy_ = set([
      bstack11lll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩጁ"), bstack11lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫጂ"), bstack11lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬጃ"), bstack11lll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧጄ"), bstack11lll_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸ࠭ጅ"),
      bstack11lll_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨጆ"), bstack11lll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡧࡳࡴࠩጇ"), bstack11lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨገ"), bstack11lll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴࠩጉ")
    ])
    bstack111llll111_opy_ = bstack11lll_opy_ (u"ࠩࠪጊ")
    with open(bstack11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ጋ")) as bstack111llll11l_opy_:
      bstack111lll1ll1_opy_ = bstack111llll11l_opy_.read()
      bstack111llll111_opy_ = re.sub(bstack11lll_opy_ (u"ࡶࠬࡤࠨ࡝ࡵ࠮࠭ࡄࠩ࠮ࠫࠦ࡟ࡲࠬጌ"), bstack11lll_opy_ (u"ࠬ࠭ግ"), bstack111lll1ll1_opy_, flags=re.M)
      bstack111llll111_opy_ = re.sub(
        bstack11lll_opy_ (u"ࡸࠧ࡟ࠪ࡟ࡷ࠰࠯࠿ࠩࠩጎ") + bstack11lll_opy_ (u"ࠧࡽࠩጏ").join(bstack111lll1l1l_opy_) + bstack11lll_opy_ (u"ࠨࠫ࠱࠮ࠩ࠭ጐ"),
        bstack11lll_opy_ (u"ࡴࠪࡠ࠷ࡀࠠ࡜ࡔࡈࡈࡆࡉࡔࡆࡆࡠࠫ጑"),
        bstack111llll111_opy_, flags=re.M | re.I
      )
    def bstack111lll1lll_opy_(dic):
      bstack111lll11ll_opy_ = {}
      for key, value in dic.items():
        if key in bstack111lll1l1l_opy_:
          bstack111lll11ll_opy_[key] = bstack11lll_opy_ (u"ࠪ࡟ࡗࡋࡄࡂࡅࡗࡉࡉࡣࠧጒ")
        else:
          if isinstance(value, dict):
            bstack111lll11ll_opy_[key] = bstack111lll1lll_opy_(value)
          else:
            bstack111lll11ll_opy_[key] = value
      return bstack111lll11ll_opy_
    bstack111lll11ll_opy_ = bstack111lll1lll_opy_(config)
    return {
      bstack11lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧጓ"): bstack111llll111_opy_,
      bstack11lll_opy_ (u"ࠬ࡬ࡩ࡯ࡣ࡯ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨጔ"): json.dumps(bstack111lll11ll_opy_)
    }
  except Exception as e:
    return {}
def bstack1ll1lllll1_opy_(config):
  global bstack111lll11l1_opy_
  try:
    if config.get(bstack11lll_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨጕ"), False):
      return
    uuid = os.getenv(bstack11lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ጖"))
    if not uuid or uuid == bstack11lll_opy_ (u"ࠨࡰࡸࡰࡱ࠭጗"):
      return
    bstack111lll1l11_opy_ = [bstack11lll_opy_ (u"ࠩࡵࡩࡶࡻࡩࡳࡧࡰࡩࡳࡺࡳ࠯ࡶࡻࡸࠬጘ"), bstack11lll_opy_ (u"ࠪࡔ࡮ࡶࡦࡪ࡮ࡨࠫጙ"), bstack11lll_opy_ (u"ࠫࡵࡿࡰࡳࡱ࡭ࡩࡨࡺ࠮ࡵࡱࡰࠫጚ"), bstack111lll11l1_opy_]
    output_file = os.path.join(tempfile.gettempdir(), bstack11lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠲ࡲ࡯ࡨࡵ࠱ࡸࡦࡸ࠮ࡨࡼࠪጛ"))
    with tarfile.open(output_file, bstack11lll_opy_ (u"ࠨࡷ࠻ࡩࡽࠦጜ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack111lll1l11_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack111llll1l1_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack111llll1ll_opy_ = data.encode()
        tarinfo.size = len(bstack111llll1ll_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack111llll1ll_opy_))
    bstack1lllll1ll_opy_ = MultipartEncoder(
      fields= {
        bstack11lll_opy_ (u"ࠧࡥࡣࡷࡥࠬጝ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack11lll_opy_ (u"ࠨࡴࡥࠫጞ")), bstack11lll_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯ࡹ࠯ࡪࡾ࡮ࡶࠧጟ")),
        bstack11lll_opy_ (u"ࠪࡧࡱ࡯ࡥ࡯ࡶࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬጠ"): uuid
      }
    )
    response = requests.post(
      bstack11lll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡻࡰ࡭ࡱࡤࡨ࠲ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡥ࡯࡭ࡪࡴࡴ࠮࡮ࡲ࡫ࡸ࠵ࡵࡱ࡮ࡲࡥࡩࠨጡ"),
      data=bstack1lllll1ll_opy_,
      headers={bstack11lll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫጢ"): bstack1lllll1ll_opy_.content_type},
      auth=(config[bstack11lll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨጣ")], config[bstack11lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪጤ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack11lll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡶࡲ࡯ࡳࡦࡪࠠ࡭ࡱࡪࡷ࠿ࠦࠧጥ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack11lll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡲࡩ࡯࡮ࡨࠢ࡯ࡳ࡬ࡹ࠺ࠨጦ") + str(e))
  finally:
    os.remove(bstack111lll11l1_opy_)