class ApprovalAgent:
    """
    Refund approval decision engine.

    IMPORTANT:
    - `is_refundable` is NOT a hard gate
    - It only indicates whether the product category normally allows refunds
    """

    def approve_refund(
        self,
        technical_result: dict,
        product_data: dict,
        user_profile: dict
    ) -> dict:

        decision = {
            "approved": False,
            "confidence": "low",
            "reason": "",
            "internal_notes": []
        }

        # 1️⃣ Technical validation (mandatory)
        if not technical_result.get("is_valid"):
            decision["reason"] = "Refund denied after issue validation."
            decision["internal_notes"].append("Technical issue not confirmed.")
            return decision

        risk_score = 0

        # 2️⃣ Product considerations
        if not product_data.get("is_refundable", True):
            risk_score += 2
            decision["internal_notes"].append("Non-standard refundable category.")

        if product_data.get("price", 0) >= 5000:
            risk_score += 2
            decision["internal_notes"].append("High-value product.")

        if product_data.get("product_type") == "durable":
            risk_score += 1
            decision["internal_notes"].append("Durable product.")

        # 3️⃣ User considerations
        if user_profile.get("rating", 5) < 2.5:
            risk_score += 2

        if user_profile.get("refund_requests", 0) >= 2:
            risk_score += 2

        if user_profile.get("total_orders", 1) <= 1:
            risk_score += 1

        # 4️⃣ Loyalty adjustment
        loyalty = user_profile.get("loyalty_level", "bronze")

        if loyalty == "gold":
            risk_score -= 2
        elif loyalty == "silver":
            risk_score -= 1

        # 5️⃣ Final decision
        if risk_score <= 1:
            decision.update({
                "approved": True,
                "confidence": "high",
                "reason": "Refund approved after review."
            })
        elif risk_score <= 3:
            decision.update({
                "approved": True,
                "confidence": "medium",
                "reason": "Refund approved as a goodwill exception."
            })
        else:
            decision["reason"] = "Refund denied based on assessment."

        return decision
