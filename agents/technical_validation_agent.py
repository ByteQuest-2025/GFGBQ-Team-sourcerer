class TechnicalValidationAgent:
    """
    Validates whether the user's issue qualifies as a legitimate product issue.
    """

    def validate(self, user_message: str, product_data: dict) -> dict:
        if not product_data:
            return {
                "is_valid": False,
                "reason": "Product not identified."
            }

        defect_keywords = [
            "not working",
            "broken",
            "damaged",
            "defect",
            "issue",
            "faulty"
        ]

        if any(k in user_message.lower() for k in defect_keywords):
            return {
                "is_valid": True,
                "reason": "Issue matches known defect patterns."
            }

        return {
            "is_valid": False,
            "reason": "No technical defect detected."
        }