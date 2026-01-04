from utils.gemini_client import call_gemini_api


class LangGraphOrchestrator:
    def __init__(self, gemini_api_key, system_prompt=None, model_params=None):
        self.gemini_api_key = gemini_api_key
        self.system_prompt = system_prompt
        self.model_params = model_params or {}
        self.agent = None

    def run(self, user_input):
        return call_gemini_api(
            prompt=user_input,
            api_key=self.gemini_api_key,
            system_prompt=self.system_prompt,
            model_params=self.model_params,
        )
