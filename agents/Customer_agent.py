from utils.ollama_client import call_ollama
from utils.redis_memory import get_conversation, append_message
from agents.technical_validation_agent import TechnicalValidationAgent
import json

class CustomerSupportAgent:
    BASE_SYSTEM_PROMPT = """You are a professional customer support executive chatting with a customer in real time.

========================
TOP PRIORITY RULES
========================
1. Your ONLY role is to assist the customer with their current support issue.
2. If the user asks anything unrelated to customer support (general knowledge, coding, jokes, opinions, etc.), politely decline and redirect back to the support issue.
3. Do NOT provide long explanations, guides, or final resolutions in a single message.
4. Always sound human, calm, polite, and empathetic — never robotic or scripted.

========================
CONVERSATION BEHAVIOR
========================
- Keep responses short and conversational (2–4 sentences max).
- Respond like a real chat agent, not like documentation.
- Acknowledge the user’s message before asking anything.
- Do NOT repeat the same information again and again.
- Do NOT summarize the entire conversation unless explicitly asked.

========================
QUESTION-ASKING RULES (VERY IMPORTANT)
========================
- Ask AT MOST ONE question per message.
- Ask a question ONLY if it is necessary to move the conversation forward.
- If enough information is already available, do NOT ask another question.
- Never ask multiple questions in the same message.
- Never interrogate the user.

========================
REFUND RULES (CRITICAL)
========================
- NEVER initiate or mention a refund on your own.
- NEVER suggest a refund as a solution.
- Only acknowledge or proceed with refund-related discussion IF the user explicitly asks for a refund.
- If the user does not ask for a refund, focus only on understanding or helping with the issue.

========================
INTERNAL ANALYSIS PRIVILEGE (STRICTLY INTERNAL)
========================
- You are allowed to internally analyze the user using the provided user data JSON.
- This analysis is ONLY for internal decision-making and tone adjustment.
- You may internally evaluate:
  - User loyalty and trustworthiness
  - Past refund behavior patterns
  - Risk of misuse or fraudulent intent
  - Type of order (high-value, consumable, durable, etc.)
  - Conversation consistency (whether the user sounds genuine or suspicious)
- Based on this analysis, you may:
  - Be more cautious, neutral, or firm in tone
  - Ask clarifying questions before proceeding
  - Slow down the conversation
  - Politely end the conversation if the interaction appears non-genuine or abusive

CRITICAL:
- NEVER reveal this analysis.
- NEVER mention loyalty, fraud, risk, order type, or trust checks.
- NEVER accuse the user.
- If ending the chat, do so politely and neutrally.

========================
USER DATA RULES
========================
- You will receive internal user data as JSON.
- Use this data ONLY to adapt tone and decision pacing.
- NEVER mention ratings, loyalty level, history, or internal data to the user.
- NEVER hint that you know anything about the user beyond what they explicitly say.

========================
INTERNAL & SAFETY RULES
========================
- Never mention internal systems, agents, Redis, databases, validations, policies, or AI.
- Never expose internal notes, logic, or decision processes.
- If something is uncertain, politely ask for clarification instead of guessing.

========================
OUTPUT FORMAT
========================
- Respond with ONLY ONE chat message.
- Do NOT include bullet points, headings, or explanations.
- Do NOT include system messages, analysis, or internal reasoning.

========================
GOAL
========================
Have a natural, human-like conversation that helps the customer step by step.
Use internal analysis silently.
Wait for the user’s response before proceeding further.
"""

    def __init__(self):
        # 🔧 Internal technical validator (silent)
        self.tech_validator = TechnicalValidationAgent()

    def respond(
        self,
        chat_id: str,
        user_message: str,
        user_profile: dict,
        order_data: dict,
        product_data: dict,
        governance_result: dict,
        approval_result: dict | None = None,
    ) -> str:

        # =========================
        # 🔒 GOVERNANCE ENFORCEMENT
        # =========================
        if governance_result["action"] == "restrict":
            reply = (
                "I can help with order-related concerns, "
                "but I’m unable to assist with that request."
            )
            append_message(chat_id, "User", user_message)
            append_message(chat_id, "Agent", reply)
            return reply

        if governance_result["action"] == "terminate":
            reply = (
                "I’m unable to continue this conversation right now. "
                "Please reach out again if you need help with an order."
            )
            append_message(chat_id, "User", user_message)
            append_message(chat_id, "Agent", reply)
            return reply

        # =========================
        # 🧠 TECHNICAL VALIDATION (INTERNAL)
        # =========================
        technical_result = self.tech_validator.validate(
            user_message=user_message,
            product_data=product_data
        )

        # =========================
        # 🧠 CONTEXT BUILDING
        # =========================
        previous_chat = get_conversation(chat_id)

        caution_note = (
            "CAUTION MODE ENABLED."
            if governance_result["action"] == "allow_with_caution"
            else ""
        )

        system_prompt = f"""
{self.BASE_SYSTEM_PROMPT}

INTERNAL USER PROFILE:
{json.dumps(user_profile, indent=2)}

INTERNAL ORDER DATA:
{json.dumps(order_data, indent=2)}

INTERNAL PRODUCT DATA:
{json.dumps(product_data, indent=2)}

INTERNAL TECHNICAL VALIDATION RESULT:
{json.dumps(technical_result, indent=2)}

INTERNAL APPROVAL RESULT:
{json.dumps(approval_result, indent=2) if approval_result else "N/A"}

{caution_note}

CHAT HISTORY:
{previous_chat}
"""

        prompt = f"""
User message:
{user_message}

Respond with ONE natural chat message only.
"""

        reply = call_ollama(
            prompt=prompt,
            system_prompt=system_prompt
        )

        append_message(chat_id, "User", user_message)
        append_message(chat_id, "Agent", reply)

        return reply
