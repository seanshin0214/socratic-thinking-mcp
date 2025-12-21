"""
Problem Classifier
문제 유형 분석 및 방법론 추천 - Question Storming 항상 첫 번째
"""

from typing import List, Dict, Any
from .methods.templates import ALL_METHODS, CATEGORY_MAP


class ProblemClassifier:
    """문제 분류 및 방법론 추천"""

    KEYWORD_RULES = {
        "analytical": [
            "왜", "이유", "원인", "분석", "why", "cause", "reason",
            "근본", "root", "문제", "problem", "인과관계", "causal"
        ],
        "creative": [
            "창의적", "혁신", "새로운", "아이디어", "creative", "innovative",
            "idea", "brainstorm", "상상", "imagine"
        ],
        "strategic": [
            "전략", "미래", "계획", "목표", "strategy", "future", "plan",
            "비전", "vision", "장기", "long-term", "의사결정", "결정",
            "선택", "decision", "choice", "투자", "investment", "ROI",
            "BCG", "SWOT", "포터", "Porter", "경쟁", "competitive",
            "시장분석", "market analysis", "포트폴리오", "portfolio"
        ],
        "technical": [
            "기술", "제품", "시스템", "technical", "product", "system",
            "개발", "develop", "설계", "design"
        ],
        "product": [
            "제품", "서비스", "개선", "product", "service", "improve",
            "고객", "customer", "사용자", "user"
        ],
        "organizational": [
            "조직", "팀", "프로세스", "organization", "team", "process",
            "생산성", "productivity", "효율", "efficiency"
        ],
        "personal": [
            "개인", "자기", "personal", "self", "성장", "growth",
            "인생", "life", "경력", "career", "후회", "regret"
        ]
    }

    def classify(self, problem_description: str) -> Dict[str, Any]:
        category_scores = self._score_categories(problem_description)
        best_category = max(category_scores, key=category_scores.get)
        confidence = category_scores[best_category] / sum(category_scores.values()) \
            if sum(category_scores.values()) > 0 else 0.0

        recommended_methods = self._get_recommended_methods(
            best_category, problem_description
        )

        return {
            "category": best_category,
            "confidence": confidence,
            "recommended_methods": recommended_methods[:3],
            "reasoning": self._generate_reasoning(best_category, problem_description, confidence)
        }

    def _score_categories(self, text: str) -> Dict[str, float]:
        text_lower = text.lower()
        scores = {category: 0.0 for category in self.KEYWORD_RULES}
        for category, keywords in self.KEYWORD_RULES.items():
            for keyword in keywords:
                if keyword in text_lower:
                    scores[category] += 1.0
        return scores

    def _get_recommended_methods(
        self, category: str, problem_description: str
    ) -> List[Dict[str, Any]]:
        """카테고리에 맞는 방법론 추천 - Question Storming 항상 첫 번째"""
        recommendations = []

        # PRIMARY: Question Storming 항상 첫 번째
        if "question_storming" in ALL_METHODS:
            qs = ALL_METHODS["question_storming"]
            recommendations.append({
                "id": "question_storming",
                "name": qs["name"],
                "category": qs["category"],
                "best_for": qs["best_for"],
                "steps": qs["steps"]
            })

        method_ids = CATEGORY_MAP.get(category, [])
        additional_methods = self._get_additional_methods(problem_description)
        all_method_ids = [m for m in list(set(method_ids + additional_methods))
                         if m != "question_storming"]

        for method_id in all_method_ids[:4]:
            if method_id in ALL_METHODS:
                method = ALL_METHODS[method_id]
                recommendations.append({
                    "id": method_id,
                    "name": method["name"],
                    "category": method["category"],
                    "best_for": method["best_for"],
                    "steps": method["steps"]
                })

        return recommendations

    def _get_additional_methods(self, text: str) -> List[str]:
        text_lower = text.lower()
        additional = []

        if text_lower.count("왜") >= 2 or text_lower.count("why") >= 2:
            additional.append("five_whys")
        if "제품" in text_lower or "product" in text_lower:
            additional.append("scamper")
        if "미래" in text_lower or "future" in text_lower:
            additional.append("scenario_planning")
        if "팀" in text_lower or "조직" in text_lower:
            additional.append("six_hats")
        if "결정" in text_lower or "decision" in text_lower:
            additional.append("decision_tree")
        if "swot" in text_lower:
            additional.append("swot")
        if "원인" in text_lower or "cause" in text_lower:
            additional.append("fishbone")
        if "투자" in text_lower or "investment" in text_lower:
            additional.append("cost_benefit")
        if "리스크" in text_lower or "risk" in text_lower:
            additional.append("pre_mortem")
        if "후회" in text_lower or "regret" in text_lower:
            additional.append("regret_minimization")

        return additional

    def _generate_reasoning(self, category: str, problem: str, confidence: float) -> str:
        category_names = {
            "analytical": "분석적 접근",
            "creative": "창의적 사고",
            "strategic": "전략적 계획",
            "technical": "기술적 혁신",
            "product": "제품 개선",
            "organizational": "조직 개선",
            "personal": "개인 성장"
        }
        category_name = category_names.get(category, category)
        confidence_level = "높음" if confidence > 0.5 else "중간" if confidence > 0.3 else "낮음"
        return f"귀하의 문제는 '{category_name}'이 필요합니다. (신뢰도: {confidence_level})"

    def format_recommendations(self, classification: Dict[str, Any]) -> str:
        output = "🎯 문제 분석 완료\n\n"
        output += f"분류: {classification['reasoning']}\n\n"
        output += "📋 추천 방법론:\n"

        for i, method in enumerate(classification["recommended_methods"], 1):
            output += f"{i}. {method['name']}\n"
            output += f"   - 적합한 상황: {method['best_for']}\n"
            output += f"   - 단계 수: {method['steps']}\n"

        output += "\n방법 선택: /{번호} (예: /1, /2, /3) 또는 /auto (AI 자동 선택)"
        return output


classifier = ProblemClassifier()
