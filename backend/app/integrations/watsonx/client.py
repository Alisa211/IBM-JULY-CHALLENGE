from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai import Credentials

from app.core.config import settings

class WatsonxClient:
    def __init__(self):
        # Allow missing credentials during early local development
        if not settings.WATSONX_API_KEY:
            self.model = None
            return

        credentials = Credentials(
            url=settings.WATSONX_URL,
            api_key=settings.WATSONX_API_KEY
        )
        
        parameters = {
            GenParams.DECODING_METHOD: "greedy",
            GenParams.MAX_NEW_TOKENS: 2000,
            GenParams.TEMPERATURE: 0.7,
            GenParams.REPETITION_PENALTY: 1.0,
        }
        
        try:
            self.model = ModelInference(
                model_id=settings.WATSONX_MODEL_ID,
                params=parameters,
                credentials=credentials,
                project_id=settings.WATSONX_PROJECT_ID
            )
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning(f"Failed to initialize Watsonx client: {e}. Falling back to mock responses.")
            self.model = None

    def generate_text(self, prompt: str, model_id: str = None, workflow_run_id: str = None) -> str:
        """
        Sends a prompt to the Watsonx model and returns the raw string response.
        Records telemetry to ai_usage table if workflow_run_id is provided.
        """
        import time
        from app.models.ai_usage import AIUsage
        
        start_time = time.time()
        
        if not self.model:
            return '''[
                {
                    "title": "Mock Chola Concept",
                    "description": "A placeholder response since Watsonx API keys are missing.",
                    "rationale": "For local development and UI testing.",
                    "tags": ["mock", "test"]
                }
            ]'''
            
        # Re-initialize model if different model_id is requested
        current_model = self.model
        used_model_id = settings.WATSONX_MODEL_ID
        if model_id and model_id != settings.WATSONX_MODEL_ID:
            used_model_id = model_id
            parameters = {
                GenParams.DECODING_METHOD: "greedy",
                GenParams.MAX_NEW_TOKENS: 2000,
                GenParams.TEMPERATURE: 0.7,
                GenParams.REPETITION_PENALTY: 1.0,
            }
            credentials = Credentials(
                url=settings.WATSONX_URL,
                api_key=settings.WATSONX_API_KEY
            )
            try:
                current_model = ModelInference(
                    model_id=model_id,
                    params=parameters,
                    credentials=credentials,
                    project_id=settings.WATSONX_PROJECT_ID
                )
            except Exception as e:
                import logging
                logging.getLogger(__name__).warning(f"Failed to initialize Watsonx client for model {model_id}: {e}. Falling back to mock responses.")
                current_model = None

        if current_model:
            response = current_model.generate_text(prompt=prompt)
        else:
            response = '''[
                {
                    "title": "Mock Chola Concept",
                    "description": "A placeholder response since Watsonx API keys are missing.",
                    "rationale": "For local development and UI testing.",
                    "tags": ["mock", "test"]
                }
            ]'''
        latency = time.time() - start_time
        
        # Estimate tokens (approximate: 1 token = 4 chars)
        prompt_tokens = len(prompt) // 4
        response_tokens = len(response) // 4
        total_tokens = prompt_tokens + response_tokens
        
        if workflow_run_id:
            try:
                from app.core.database import AsyncSessionLocal
                async def save_usage():
                    async with AsyncSessionLocal() as db:
                        usage = AIUsage(
                            workflow_run_id=workflow_run_id,
                            model=used_model_id,
                            tokens=total_tokens,
                            latency=latency,
                            cost=total_tokens * 0.000001
                        )
                        db.add(usage)
                        await db.commit()
                import asyncio
                # since generate_text is synchronous, we run the save_usage in the event loop or block
                try:
                    loop = asyncio.get_running_loop()
                    loop.create_task(save_usage())
                except RuntimeError:
                    asyncio.run(save_usage())
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(f"Failed to record AI usage: {e}")
                
        return response
