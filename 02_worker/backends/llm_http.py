import time, random
from typing import Any, Dict
from .base import BaseBackend

class LLMHTTPBackend(BaseBackend):
    def infer(self, payload: Dict[str, Any], params: Dict[str, Any] = None) -> Dict[str, Any]:
        # Simulated external API call
        time.sleep(random.uniform(1.0, 2.0))

        text = payload.get("text", "")
        tags = payload.get("tags", ["awesome", "trending"])
        p = params or {}
        lang = p.get("language", "ko")
        plat = p.get("platform", "instagram")
        tone = p.get("tone", "friendly")

        # Marketing Intelligence Logic
        prefix = {
            "professional": {"ko": "저희 브랜드의 새로운", "en": "Our latest", "jp": "私共の新しい"},
            "friendly": {"ko": "진짜 대박! 이번에 나온", "en": "Check this out!", "jp": "すごい！今回の"},
            "emotional": {"ko": "당신의 일상에 스며들", "en": "Bring joy to your life with", "jp": "日常に彩りを添える"}
        }

        platform_suffix = {
            "instagram": {"ko": "인친님들도 꼭 경험해보세요! 📸", "en": "A must-have for your feed! 📸", "jp": "インスタ映え間違いなし！📸"},
            "twitter": {"ko": "이거 진짜 물건입니다. #강추", "en": "This is it. #GameChanger", "jp": "これ、本当におすすめです。 #推し"},
            "blog": {"ko": "더 자세한 내용은 프로필 링크에서 확인 가능합니다.", "en": "Read more about it in our bio link.", "jp": "詳細はプロフィールのリンクから。"}
        }

        base_msg = prefix.get(tone, prefix["friendly"]).get(lang, "Check this out")
        suffix = platform_suffix.get(plat, platform_suffix["instagram"]).get(lang, "")

        ad_copy = f"{base_msg} {text}! {suffix}"

        lang_tags = {
            "ko": ["AI마케팅", "트렌드", "일상"],
            "en": ["AIMarketing", "Trend", "Daily"],
            "jp": ["AIマーケティング", "トレンド", "日常"]
        }

        hashtags = " ".join([f"#{t}" for t in tags] + [f"#{t}" for t in lang_tags.get(lang, lang_tags["ko"])])

        return {
            "model": self.model_name,
            "ad_copy": ad_copy,
            "hashtags": hashtags,
            "language": lang,
            "platform": plat,
            "tone": tone
        }

