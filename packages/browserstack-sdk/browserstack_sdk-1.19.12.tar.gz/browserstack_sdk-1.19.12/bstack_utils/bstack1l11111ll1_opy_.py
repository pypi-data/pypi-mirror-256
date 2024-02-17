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
from uuid import uuid4
from bstack_utils.helper import bstack1ll1ll1lll_opy_, bstack11l1ll11ll_opy_
from bstack_utils.bstack1ll1lll1ll_opy_ import bstack11111ll1ll_opy_
class bstack1l11ll1111_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack1l11l1l1ll_opy_=None, framework=None, tags=[], scope=[], bstack1llllll11l1_opy_=None, bstack1llllll1l11_opy_=True, bstack1llllll1ll1_opy_=None, bstack11111lll_opy_=None, result=None, duration=None, bstack1l11l1l111_opy_=None, meta={}):
        self.bstack1l11l1l111_opy_ = bstack1l11l1l111_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1llllll1l11_opy_:
            self.uuid = uuid4().__str__()
        self.bstack1l11l1l1ll_opy_ = bstack1l11l1l1ll_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1llllll11l1_opy_ = bstack1llllll11l1_opy_
        self.bstack1llllll1ll1_opy_ = bstack1llllll1ll1_opy_
        self.bstack11111lll_opy_ = bstack11111lll_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
    def bstack1l11l11l11_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1lllllll1ll_opy_(self):
        bstack1lllll1llll_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack11lll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬᑡ"): bstack1lllll1llll_opy_,
            bstack11lll_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬᑢ"): bstack1lllll1llll_opy_,
            bstack11lll_opy_ (u"ࠫࡻࡩ࡟ࡧ࡫࡯ࡩࡵࡧࡴࡩࠩᑣ"): bstack1lllll1llll_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack11lll_opy_ (u"࡛ࠧ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷ࠾ࠥࠨᑤ") + key)
            setattr(self, key, val)
    def bstack1llllll111l_opy_(self):
        return {
            bstack11lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᑥ"): self.name,
            bstack11lll_opy_ (u"ࠧࡣࡱࡧࡽࠬᑦ"): {
                bstack11lll_opy_ (u"ࠨ࡮ࡤࡲ࡬࠭ᑧ"): bstack11lll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩᑨ"),
                bstack11lll_opy_ (u"ࠪࡧࡴࡪࡥࠨᑩ"): self.code
            },
            bstack11lll_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫᑪ"): self.scope,
            bstack11lll_opy_ (u"ࠬࡺࡡࡨࡵࠪᑫ"): self.tags,
            bstack11lll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᑬ"): self.framework,
            bstack11lll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᑭ"): self.bstack1l11l1l1ll_opy_
        }
    def bstack1lllll1ll11_opy_(self):
        return {
         bstack11lll_opy_ (u"ࠨ࡯ࡨࡸࡦ࠭ᑮ"): self.meta
        }
    def bstack1llllll1l1l_opy_(self):
        return {
            bstack11lll_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡔࡨࡶࡺࡴࡐࡢࡴࡤࡱࠬᑯ"): {
                bstack11lll_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠧᑰ"): self.bstack1llllll11l1_opy_
            }
        }
    def bstack1lllll1l1ll_opy_(self, bstack1lllll1lll1_opy_, details):
        step = next(filter(lambda st: st[bstack11lll_opy_ (u"ࠫ࡮ࡪࠧᑱ")] == bstack1lllll1lll1_opy_, self.meta[bstack11lll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᑲ")]), None)
        step.update(details)
    def bstack1lllllll11l_opy_(self, bstack1lllll1lll1_opy_):
        step = next(filter(lambda st: st[bstack11lll_opy_ (u"࠭ࡩࡥࠩᑳ")] == bstack1lllll1lll1_opy_, self.meta[bstack11lll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᑴ")]), None)
        step.update({
            bstack11lll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᑵ"): bstack1ll1ll1lll_opy_()
        })
    def bstack1l111l1l1l_opy_(self, bstack1lllll1lll1_opy_, result, duration=None):
        bstack1llllll1ll1_opy_ = bstack1ll1ll1lll_opy_()
        if bstack1lllll1lll1_opy_ is not None and self.meta.get(bstack11lll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᑶ")):
            step = next(filter(lambda st: st[bstack11lll_opy_ (u"ࠪ࡭ࡩ࠭ᑷ")] == bstack1lllll1lll1_opy_, self.meta[bstack11lll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᑸ")]), None)
            step.update({
                bstack11lll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᑹ"): bstack1llllll1ll1_opy_,
                bstack11lll_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨᑺ"): duration if duration else bstack11l1ll11ll_opy_(step[bstack11lll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᑻ")], bstack1llllll1ll1_opy_),
                bstack11lll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᑼ"): result.result,
                bstack11lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᑽ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1llllll1lll_opy_):
        if self.meta.get(bstack11lll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᑾ")):
            self.meta[bstack11lll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᑿ")].append(bstack1llllll1lll_opy_)
        else:
            self.meta[bstack11lll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᒀ")] = [ bstack1llllll1lll_opy_ ]
    def bstack1llllll11ll_opy_(self):
        return {
            bstack11lll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᒁ"): self.bstack1l11l11l11_opy_(),
            **self.bstack1llllll111l_opy_(),
            **self.bstack1lllllll1ll_opy_(),
            **self.bstack1lllll1ll11_opy_()
        }
    def bstack1llllll1111_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack11lll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᒂ"): self.bstack1llllll1ll1_opy_,
            bstack11lll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩᒃ"): self.duration,
            bstack11lll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᒄ"): self.result.result
        }
        if data[bstack11lll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᒅ")] == bstack11lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᒆ"):
            data[bstack11lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᒇ")] = self.result.bstack11lll1l11l_opy_()
            data[bstack11lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᒈ")] = [{bstack11lll_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᒉ"): self.result.bstack11l1ll1111_opy_()}]
        return data
    def bstack1lllllll1l1_opy_(self):
        return {
            bstack11lll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᒊ"): self.bstack1l11l11l11_opy_(),
            **self.bstack1llllll111l_opy_(),
            **self.bstack1lllllll1ll_opy_(),
            **self.bstack1llllll1111_opy_(),
            **self.bstack1lllll1ll11_opy_()
        }
    def bstack1l111lll1l_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack11lll_opy_ (u"ࠩࡖࡸࡦࡸࡴࡦࡦࠪᒋ") in event:
            return self.bstack1llllll11ll_opy_()
        elif bstack11lll_opy_ (u"ࠪࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᒌ") in event:
            return self.bstack1lllllll1l1_opy_()
    def bstack1l11111111_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1llllll1ll1_opy_ = time if time else bstack1ll1ll1lll_opy_()
        self.duration = duration if duration else bstack11l1ll11ll_opy_(self.bstack1l11l1l1ll_opy_, self.bstack1llllll1ll1_opy_)
        if result:
            self.result = result
class bstack1l1111llll_opy_(bstack1l11ll1111_opy_):
    def __init__(self, hooks=[], bstack1l111ll111_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack1l111ll111_opy_ = bstack1l111ll111_opy_
        super().__init__(*args, **kwargs, bstack11111lll_opy_=bstack11lll_opy_ (u"ࠫࡹ࡫ࡳࡵࠩᒍ"))
    @classmethod
    def bstack1lllll1l11l_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11lll_opy_ (u"ࠬ࡯ࡤࠨᒎ"): id(step),
                bstack11lll_opy_ (u"࠭ࡴࡦࡺࡷࠫᒏ"): step.name,
                bstack11lll_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨᒐ"): step.keyword,
            })
        return bstack1l1111llll_opy_(
            **kwargs,
            meta={
                bstack11lll_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࠩᒑ"): {
                    bstack11lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᒒ"): feature.name,
                    bstack11lll_opy_ (u"ࠪࡴࡦࡺࡨࠨᒓ"): feature.filename,
                    bstack11lll_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᒔ"): feature.description
                },
                bstack11lll_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧᒕ"): {
                    bstack11lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᒖ"): scenario.name
                },
                bstack11lll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᒗ"): steps,
                bstack11lll_opy_ (u"ࠨࡧࡻࡥࡲࡶ࡬ࡦࡵࠪᒘ"): bstack11111ll1ll_opy_(test)
            }
        )
    def bstack1lllll1l1l1_opy_(self):
        return {
            bstack11lll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᒙ"): self.hooks
        }
    def bstack1lllllll111_opy_(self):
        if self.bstack1l111ll111_opy_:
            return {
                bstack11lll_opy_ (u"ࠪ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠩᒚ"): self.bstack1l111ll111_opy_
            }
        return {}
    def bstack1lllllll1l1_opy_(self):
        return {
            **super().bstack1lllllll1l1_opy_(),
            **self.bstack1lllll1l1l1_opy_()
        }
    def bstack1llllll11ll_opy_(self):
        return {
            **super().bstack1llllll11ll_opy_(),
            **self.bstack1lllllll111_opy_()
        }
    def bstack1l11111111_opy_(self):
        return bstack11lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ᒛ")
class bstack1l11l1lll1_opy_(bstack1l11ll1111_opy_):
    def __init__(self, hook_type, *args, **kwargs):
        self.hook_type = hook_type
        super().__init__(*args, **kwargs, bstack11111lll_opy_=bstack11lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᒜ"))
    def bstack1l1111ll11_opy_(self):
        return self.hook_type
    def bstack1lllll1ll1l_opy_(self):
        return {
            bstack11lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᒝ"): self.hook_type
        }
    def bstack1lllllll1l1_opy_(self):
        return {
            **super().bstack1lllllll1l1_opy_(),
            **self.bstack1lllll1ll1l_opy_()
        }
    def bstack1llllll11ll_opy_(self):
        return {
            **super().bstack1llllll11ll_opy_(),
            **self.bstack1lllll1ll1l_opy_()
        }
    def bstack1l11111111_opy_(self):
        return bstack11lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࠩᒞ")