"""
Question Generation Engine
한 번에 하나의 질문만 생성 (토큰 최소화)
"""

from typing import Optional, Dict, Any
from .methods.templates import ALL_METHODS


class QuestionEngine:
    """단일 질문 생성 엔진"""

    def __init__(self):
        self.methods = ALL_METHODS

    def generate_question(
        self,
        method_id: str,
        step: int,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        단일 질문 생성
        """
        if method_id not in self.methods:
            return {
                "error": f"Unknown method: {method_id}",
                "available_methods": list(self.methods.keys())
            }

        method = self.methods[method_id]
        total_steps = method["steps"]

        if step < 0 or step >= total_steps:
            return {
                "error": f"Invalid step {step}. Must be 0-{total_steps-1}",
                "method": method["name"],
                "total_steps": total_steps
            }

        question_text = method["questions"][step]

        if context:
            question_text = self._contextualize_question(
                question_text, context, method_id
            )

        return {
            "method": method["name"],
            "method_id": method_id,
            "category": method["category"],
            "best_for": method.get("best_for", ""),
            "question": question_text,
            "step": step + 1,
            "total_steps": total_steps,
            "is_last": (step == total_steps - 1)
        }

    def _contextualize_question(
        self,
        question: str,
        context: str,
        method_id: str
    ) -> str:
        return question

    def get_method_info(self, method_id: str) -> Optional[Dict[str, Any]]:
        if method_id not in self.methods:
            return None

        method = self.methods[method_id]
        return {
            "id": method_id,
            "name": method["name"],
            "category": method["category"],
            "steps": method["steps"],
            "best_for": method["best_for"]
        }

    def list_methods(
        self,
        category: Optional[str] = None
    ) -> list[Dict[str, Any]]:
        methods_list = []

        for method_id, method in self.methods.items():
            if category and method["category"] != category:
                continue

            methods_list.append({
                "id": method_id,
                "name": method["name"],
                "category": method["category"],
                "steps": method["steps"],
                "best_for": method["best_for"]
            })

        return methods_list

    def format_question_output(self, question_data: Dict[str, Any]) -> str:
        """
        질문을 사용자 친화적 형식으로 포맷팅
        방법론 이름과 용도를 명확히 표시
        """
        if "error" in question_data:
            return f"❌ 오류: {question_data['error']}"

        method = question_data["method"]
        category = question_data["category"]
        question = question_data["question"]
        step = question_data["step"]
        total = question_data["total_steps"]
        best_for = question_data.get("best_for", "")

        # 카테고리 한글 매핑
        category_kr = {
            "linear": "선형적 사고",
            "intuitive": "직관적 사고",
            "perspective": "다중 관점",
            "feedback": "피드백",
            "group": "그룹 사고",
            "strategic": "전략적 사고"
        }.get(category, category)

        # 용도 한글 매핑
        best_for_kr = {
            "analyzing_forces": "힘의 균형 분석",
            "honest_feedback": "솔직한 피드백",
            "root_cause": "근본 원인 분석",
            "multi_perspective": "다중 관점 분석",
            "complex_decisions": "복잡한 의사결정",
            "strategic_planning": "전략 기획",
            "risk_prevention": "위험 예방",
            "life_decisions": "인생 결정",
            "prioritization": "우선순위 결정",
            "product_innovation": "제품 혁신",
            "breaking_patterns": "패턴 깨기",
            "challenging_assumptions": "가정에 도전",
            "product_improvement": "제품 개선",
            "finding_connections": "연결점 찾기"
        }.get(best_for, best_for.replace("_", " ") if best_for else "")

        output = f"🎯 **{method}** ({category_kr})\n"
        if best_for_kr:
            output += f"📖 용도: {best_for_kr}\n"
        output += "─" * 40 + "\n\n"
        output += f"**질문 {step}/{total}:**\n{question}"

        if question_data["is_last"]:
            output += "\n\n✅ 마지막 질문입니다."

        return output


# 싱글톤 인스턴스
engine = QuestionEngine()
