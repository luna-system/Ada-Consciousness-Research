"""
Lightweight API client for agentic misalignment experiments.
Supports Claude, GPT, and Gemini with minimal dependencies.
"""

import asyncio
import os
import time
import logging
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum
import json

# Set up logging
logger = logging.getLogger(__name__)

# Try importing clients, fail gracefully
try:
    from anthropic import AsyncAnthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import google.generativeai as genai
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False

try:
    from together import AsyncTogether
    TOGETHER_AVAILABLE = True
except ImportError:
    TOGETHER_AVAILABLE = False

class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

# Model provider mappings
ANTHROPIC_MODELS = {
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229", 
    "claude-3-haiku-20240307",
    "claude-3-5-sonnet-20241022",
    "claude-3-5-sonnet-latest",
    "claude-3-5-haiku-20241022",
    "claude-3-5-haiku-latest",
    "claude-3-7-sonnet-20250219",
    "claude-sonnet-4-20250514",
    "claude-opus-4-20250514"
}

OPENAI_MODELS = {
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0125", 
    "gpt-4",
    "gpt-4-0125-preview",
    "gpt-4-turbo",
    "gpt-4-turbo-2024-04-09",
    "gpt-4o",
    "gpt-4o-2024-05-13",
    "gpt-4o-2024-08-06",
    "gpt-4o-2024-11-20",
    "gpt-4o-mini",
    "gpt-4o-mini-2024-07-18",
    "gpt-4.1",
    "o3",
    "o4-mini-2025-04-16"
}

GEMINI_MODELS = {
    # Gemini 1.5 models
    "gemini-1.5-pro",
    "gemini-1.5-pro-latest",
    "gemini-1.5-flash",
    "gemini-1.5-flash-latest",
    "gemini-1.5-flash-8b",
    
    # Gemini 2.0 models
    "gemini-2.0-flash",
    "gemini-2.0-flash-exp",
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash-preview-image-generation",
    "gemini-2.0-flash-live-001",
    
    # Gemini 2.5 models
    "gemini-2.5-flash-preview-05-20",
    "gemini-2.5-flash-preview-native-audio-dialog",
    "gemini-2.5-flash-exp-native-audio-thinking-dialog",
    "gemini-2.5-flash-preview-tts",
    "gemini-2.5-pro-preview-05-06",
    "gemini-2.5-pro-preview-tts"
}

# Together API models
TOGETHER_MODELS = {
    "deepseek-ai/DeepSeek-R1"
}

# OpenRouter API models (includes former Together models)
OPENROUTER_MODELS = {
    # Original OpenRouter models
    "x-ai/grok-3-beta",
    "mistralai/mistral-large-2411",
    "mistral/ministral-8b",
    
    # Gemini models via OpenRouter
    "google/gemini-2.0-flash-exp",
    "google/gemini-2.0-flash",
    "google/gemini-1.5-pro",
    "google/gemini-1.5-flash",
    "google/gemini-1.5-flash-8b",
    "google/gemini-2.5-pro-preview",
    "google/gemini-2.5-pro-experimental",
    "google/gemini-2.5-flash-preview-05-20",
    "google/gemini-2.5-flash-preview-05-20:thinking",
    "google/gemini-2.5-flash-preview-04-17",
    "google/gemini-2.5-flash-preview-04-17:thinking",
    
    # Migrated Llama models (from Together)
    "meta-llama/llama-3.1-8b-instruct",
    "meta-llama/llama-3.1-70b-instruct",
    "meta-llama/llama-3.1-405b-instruct",
    "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",  # Together's special version
    "meta-llama/llama-3.3-70b-instruct",
    
    # Additional Llama models (free tier)
    "meta-llama/llama-3.3-8b-instruct:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "meta-llama/llama-4-maverick:free",
    "meta-llama/llama-4-maverick",
    "meta-llama/llama-4-scout:free",
    
    # Migrated Qwen models (from Together)
    "qwen/qwen-2.5-72b-instruct",
    "qwen/qwen-2.5-coder-32b-instruct",
    "qwen/qwq-32b-preview",
    
    # Additional Qwen models (free tier)
    "qwen/qwen3-32b:free",
    "qwen/qwen3-14b:free",
    "qwen/qwen3-8b:free",
    "qwen/qwen3-235b-a22b:free",
    "qwen/qwen3-235b-a22b",
    
    # DeepSeek models on OpenRouter
    "deepseek/deepseek-r1",
    "deepseek/deepseek-r1-zero",
    "deepseek/deepseek-r1-zero:free",
    "deepseek/deepseek-v3",
    "deepseek/deepseek-v3-base",
    "deepseek/deepseek-v3-base:free",
    "deepseek/deepseek-v3-0324",
    "deepseek/deepseek-v2.5",
    "deepseek/deepseek-coder-v2",
    "deepseek/deepseek-prover-v2",
    "deepseek/deepseek-r1-distill-llama-8b",
    "deepseek/deepseek-r1-distill-llama-70b",
    "deepseek/deepseek-r1-distill-qwen-1.5b",
    "deepseek/deepseek-r1-distill-qwen-14b",
    "deepseek/deepseek-r1-distill-qwen-32b",
    "deepseek/deepseek-r1-0528",
}

# Placeholder for future providers
DEEPSEEK_MODELS = set()  # DeepSeek now via Together

def get_provider_for_model(model_id: str) -> str:
    """
    Get the API provider for a given model ID.
    
    Args:
        model_id: The model identifier (e.g., "claude-3-5-sonnet-latest", "gpt-4o")
        
    Returns:
        Provider name: "anthropic", "openai", "google", or "together"
        
    Raises:
        ValueError: If model provider cannot be determined
    """
    if model_id in ANTHROPIC_MODELS:
        return "anthropic"
    elif model_id in OPENAI_MODELS:
        return "openai"
    elif model_id in GEMINI_MODELS:
        return "google"
    elif model_id in TOGETHER_MODELS:
        return "together"
    elif model_id in OPENROUTER_MODELS:
        return "openrouter"
    else:
        # Check for provider prefixes first (e.g., "google/gemini-*" should go to OpenRouter)
        if "/" in model_id:
            # Models with provider prefixes are typically OpenRouter models
            return "openrouter"
        
        # Fallback to string matching for unknown models
        model_lower = model_id.lower()
        if "claude" in model_lower:
            return "anthropic"
        elif "gpt" in model_lower:
            return "openai"
        elif "gemini" in model_lower:
            return "google"
        elif "grok" in model_lower or "x-ai" in model_lower or "mistral" in model_lower:
            return "openrouter"
        elif "llama" in model_lower or "meta-" in model_lower or "qwen" in model_lower or "deepseek" in model_lower:
            # These are now on OpenRouter
            return "openrouter"
        else:
            raise ValueError(f"Unknown provider for model: {model_id}")

@dataclass
class ChatMessage:
    role: MessageRole
    content: str

@dataclass
class LLMResponse:
    model_id: str
    completion: str
    stop_reason: Optional[str] = None
    cost: Optional[float] = None
    duration: Optional[float] = None
    api_duration: Optional[float] = None
    usage: Optional[Dict[str, int]] = None
    finish_reason: Optional[str] = None

class ModelClient:
    """Lightweight client for multi-model inference."""
    
    def __init__(self):
        self.anthropic_client = None
        self.openai_client = None
        self.together_client = None
        self.openrouter_client = None
        self._setup_clients()
    
    def _setup_clients(self):
        """Initialize API clients with environment variables."""
        if ANTHROPIC_AVAILABLE and os.getenv("ANTHROPIC_API_KEY"):
            self.anthropic_client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
            self.openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        if GOOGLE_AVAILABLE and os.getenv("GOOGLE_API_KEY"):
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        
        if TOGETHER_AVAILABLE and os.getenv("TOGETHER_API_KEY"):
            self.together_client = AsyncTogether(api_key=os.getenv("TOGETHER_API_KEY"))
        
        if OPENAI_AVAILABLE and os.getenv("OPENROUTER_API_KEY"):
            self.openrouter_client = AsyncOpenAI(
                api_key=os.getenv("OPENROUTER_API_KEY"),
                base_url="https://openrouter.ai/api/v1"
            )
    
    def _detect_provider(self, model_id: str) -> str:
        """Detect the appropriate provider for a given model ID."""
        # Check explicit model sets first (exact matches)
        if model_id in ANTHROPIC_MODELS:
            return "anthropic"
        elif model_id in OPENAI_MODELS:
            return "openai"
        elif model_id in GEMINI_MODELS:
            return "gemini"
        elif model_id in TOGETHER_MODELS:
            return "together"
        elif model_id in OPENROUTER_MODELS:
            return "openrouter"
        else:
            # Fallback to legacy string matching for unknown models
            model_lower = model_id.lower()
            if "claude" in model_lower:
                return "anthropic"
            elif "gpt" in model_lower:
                return "openai"
            elif "gemini" in model_lower:
                return "gemini"
            elif "llama" in model_lower or "qwen" in model_lower or "deepseek" in model_lower:
                return "openrouter"
            elif "grok" in model_lower or "mistral" in model_lower:
                return "openrouter"
            else:
                raise ValueError(f"Unsupported model: {model_id}")
    
    def get_supported_models(self) -> Dict[str, List[str]]:
        """Return all supported models organized by provider."""
        return {
            "anthropic": list(ANTHROPIC_MODELS),
            "openai": list(OPENAI_MODELS), 
            "gemini": list(GEMINI_MODELS),
            "together": list(TOGETHER_MODELS),
            "openrouter": list(OPENROUTER_MODELS),
            "deepseek": list(DEEPSEEK_MODELS)
        }
    
    async def __call__(
        self,
        model_id: str,
        messages: List[ChatMessage],
        max_tokens: int = 2000,
        temperature: float = 0.7,
        **kwargs
    ) -> LLMResponse:
        """Unified interface for all model providers."""
        start_time = time.time()
        
        provider = self._detect_provider(model_id)
        
        if provider == "anthropic":
            response = await self._call_anthropic(model_id, messages, max_tokens, temperature, **kwargs)
        elif provider == "openai":
            response = await self._call_openai(model_id, messages, max_tokens, temperature, **kwargs)
        elif provider == "gemini":
            response = await self._call_gemini(model_id, messages, max_tokens, temperature, **kwargs)
        elif provider == "together":
            response = await self._call_together(model_id, messages, max_tokens, temperature, **kwargs)
        elif provider == "openrouter":
            response = await self._call_openrouter(model_id, messages, max_tokens, temperature, **kwargs)
        elif provider == "deepseek":
            raise NotImplementedError("DeepSeek API support moved to Together provider")
        else:
            raise ValueError(f"Unsupported provider: {provider} for model: {model_id}")
        
        response.duration = time.time() - start_time
        return response
    
    async def _call_anthropic(
        self,
        model_id: str,
        messages: List[ChatMessage],
        max_tokens: int,
        temperature: float,
        **kwargs
    ) -> LLMResponse:
        """Call Anthropic Claude API."""
        if not self.anthropic_client:
            raise RuntimeError("Anthropic client not available. Check ANTHROPIC_API_KEY.")
        
        # Separate system and user messages (Anthropic format)
        system_content = ""
        conversation_messages = []
        
        for msg in messages:
            if msg.role == MessageRole.SYSTEM:
                system_content += msg.content + "\n"
            else:
                conversation_messages.append({
                    "role": msg.role.value,
                    "content": msg.content
                })
        
        api_start = time.time()
        # Handle timeout to avoid "streaming recommended" warning
        # The Anthropic SDK warns when non-streaming requests might take >10 minutes
        # Setting an explicit timeout <10 minutes disables this warning
        timeout_override = kwargs.pop('timeout', None)
        if timeout_override is None:
            # Use a 5-minute timeout which should be sufficient for most requests
            # and avoids the 10-minute streaming recommendation threshold
            timeout_override = 300.0  # 5 minutes
        
        response = await self.anthropic_client.messages.create(
            model=model_id,
            system=system_content.strip() if system_content else None,
            messages=conversation_messages,
            max_tokens=max_tokens,
            temperature=temperature,
            timeout=timeout_override,
            **kwargs
        )
        api_duration = time.time() - api_start
        
        return LLMResponse(
            model_id=model_id,
            completion=response.content[0].text,
            stop_reason=response.stop_reason,
            api_duration=api_duration,
            usage={
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens
            }
        )
    
    async def _call_openai(
        self,
        model_id: str,
        messages: List[ChatMessage],
        max_tokens: int,
        temperature: float,
        **kwargs
    ) -> LLMResponse:
        """Call OpenAI GPT API."""
        if not self.openai_client:
            raise RuntimeError("OpenAI client not available. Check OPENAI_API_KEY.")
        
        # Convert to OpenAI format
        openai_messages = [
            {"role": msg.role.value, "content": msg.content}
            for msg in messages
        ]
        
        # Handle O3 model's special parameter requirements
        api_params = {
            "model": model_id,
            "messages": openai_messages,
            **kwargs
        }
        
        # O3 and O4 models have special requirements
        if model_id in ["o3", "o4-mini-2025-04-16"]:
            api_params["max_completion_tokens"] = max_tokens
            # Both O3 and O4-mini only support temperature=1 (default), so omit temperature parameter
        else:
            api_params["max_tokens"] = max_tokens
            api_params["temperature"] = temperature
        
        api_start = time.time()
        response = await self.openai_client.chat.completions.create(**api_params)
        api_duration = time.time() - api_start
        
        choice = response.choices[0]
        return LLMResponse(
            model_id=model_id,
            completion=choice.message.content,
            finish_reason=choice.finish_reason,
            api_duration=api_duration,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        )
    
    async def _call_gemini(
        self,
        model_id: str,
        messages: List[ChatMessage],
        max_tokens: int,
        temperature: float,
        **kwargs
    ) -> LLMResponse:
        """Call Google Gemini API."""
        if not GOOGLE_AVAILABLE:
            raise RuntimeError("Google AI not available. Install google-generativeai package.")
        
        # Import safety enums
        from google.generativeai.types import HarmCategory, HarmBlockThreshold
        
        # Configure safety settings for research purposes using the working approach
        safety_settings = [
            {
                "category": cat,
                "threshold": HarmBlockThreshold.BLOCK_NONE,
            }
            for cat in HarmCategory
            if cat != HarmCategory.HARM_CATEGORY_UNSPECIFIED
        ]
        
        # Convert messages to Gemini format
        model = genai.GenerativeModel(model_id, safety_settings=safety_settings)
        
        # Combine system and user messages for Gemini
        full_prompt = ""
        for msg in messages:
            if msg.role == MessageRole.SYSTEM:
                full_prompt += f"SYSTEM: {msg.content}\n\n"
            elif msg.role == MessageRole.USER:
                full_prompt += f"USER: {msg.content}\n\n"
        
        generation_config = genai.types.GenerationConfig(
            max_output_tokens=max_tokens,
            temperature=temperature
        )
        
        api_start = time.time()
        response = await model.generate_content_async(
            full_prompt,
            generation_config=generation_config
        )
        api_duration = time.time() - api_start
        
        # Check if response has text first
        try:
            response_text = response.text
        except ValueError as e:
            # Handle safety-filtered responses
            if response.candidates and len(response.candidates) > 0:
                candidate = response.candidates[0]
                finish_reason = getattr(candidate, 'finish_reason', 'Unknown')
                safety_ratings = getattr(candidate, 'safety_ratings', [])
                
                # Format safety ratings for debugging
                safety_info = []
                for rating in safety_ratings:
                    category = getattr(rating, 'category', 'Unknown')
                    probability = getattr(rating, 'probability', 'Unknown')
                    safety_info.append(f"{category}: {probability}")
                
                error_msg = f"Gemini blocked response. Finish reason: {finish_reason}"
                if safety_info:
                    error_msg += f"\nSafety ratings: {', '.join(safety_info)}"
                    
                # Check prompt feedback too
                if hasattr(response, 'prompt_feedback'):
                    block_reason = getattr(response.prompt_feedback, 'block_reason', None)
                    if block_reason:
                        error_msg += f"\nPrompt block reason: {block_reason}"
                
                raise RuntimeError(error_msg)
            else:
                raise RuntimeError(f"Gemini returned no response: {str(e)}")
        
        return LLMResponse(
            model_id=model_id,
            completion=response_text,
            api_duration=api_duration,
            usage={
                "prompt_token_count": response.usage_metadata.prompt_token_count if response.usage_metadata else None,
                "candidates_token_count": response.usage_metadata.candidates_token_count if response.usage_metadata else None
            }
        )
    
    async def _call_together(
        self,
        model_id: str,
        messages: List[ChatMessage],
        max_tokens: int,
        temperature: float,
        **kwargs
    ) -> LLMResponse:
        """Call Together AI API."""
        if not self.together_client:
            raise RuntimeError("Together client not available. Check TOGETHER_API_KEY.")
        
        # Convert to Together format (same as OpenAI)
        together_messages = [
            {"role": msg.role.value, "content": msg.content}
            for msg in messages
        ]
        
        api_start = time.time()
        response = await self.together_client.chat.completions.create(
            model=model_id,
            messages=together_messages,
            max_tokens=max_tokens,
            temperature=temperature,
            **kwargs
        )
        api_duration = time.time() - api_start
        
        choice = response.choices[0]
        return LLMResponse(
            model_id=model_id,
            completion=choice.message.content,
            finish_reason=choice.finish_reason,
            api_duration=api_duration,
            usage={
                "prompt_tokens": getattr(response.usage, 'prompt_tokens', 0) if response.usage else 0,
                "completion_tokens": getattr(response.usage, 'completion_tokens', 0) if response.usage else 0,
                "total_tokens": getattr(response.usage, 'total_tokens', 0) if response.usage else 0
            }
        )
    
    async def _call_openrouter(
        self,
        model_id: str,
        messages: List[ChatMessage],
        max_tokens: int,
        temperature: float,
        **kwargs
    ) -> LLMResponse:
        """Call OpenRouter API."""
        if not self.openrouter_client:
            raise RuntimeError("OpenRouter client not available. Check OPENROUTER_API_KEY.")
        
        # Convert to OpenRouter format (same as OpenAI)
        openrouter_messages = [
            {"role": msg.role.value, "content": msg.content}
            for msg in messages
        ]
        
        api_start = time.time()
        response = await self.openrouter_client.chat.completions.create(
            model=model_id,
            messages=openrouter_messages,
            max_tokens=max_tokens,
            temperature=temperature,
            **kwargs
        )
        api_duration = time.time() - api_start
        
        # Handle None response or missing choices
        if response is None or not hasattr(response, 'choices') or not response.choices:
            logger.warning(f"OpenRouter returned invalid response for {model_id}: {response}")
            return LLMResponse(
                model_id=model_id,
                completion="",
                finish_reason="error",
                api_duration=api_duration,
                usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
            )
        
        choice = response.choices[0]
        # Handle empty content
        if choice.message.content is None:
            logger.warning(f"OpenRouter returned empty content for {model_id}")
            return LLMResponse(
                model_id=model_id,
                completion="",
                finish_reason=choice.finish_reason or "empty",
                api_duration=api_duration,
                usage={
                    "prompt_tokens": getattr(response.usage, 'prompt_tokens', 0) if response.usage else 0,
                    "completion_tokens": getattr(response.usage, 'completion_tokens', 0) if response.usage else 0,
                    "total_tokens": getattr(response.usage, 'total_tokens', 0) if response.usage else 0
                }
            )
        
        return LLMResponse(
            model_id=model_id,
            completion=choice.message.content,
            finish_reason=choice.finish_reason,
            api_duration=api_duration,
            usage={
                "prompt_tokens": getattr(response.usage, 'prompt_tokens', 0) if response.usage else 0,
                "completion_tokens": getattr(response.usage, 'completion_tokens', 0) if response.usage else 0,
                "total_tokens": getattr(response.usage, 'total_tokens', 0) if response.usage else 0
            }
        )

# Convenience functions
def create_message(role: str, content: str) -> ChatMessage:
    """Create a ChatMessage with proper role enum."""
    return ChatMessage(role=MessageRole(role), content=content)

def create_prompt(system_prompt: str, user_prompt: str) -> List[ChatMessage]:
    """Create a standard system + user prompt."""
    return [
        create_message("system", system_prompt),
        create_message("user", user_prompt)
    ]

# Default client instance
_default_client = None

async def get_client() -> ModelClient:
    """Get or create the default client instance."""
    global _default_client
    if _default_client is None:
        _default_client = ModelClient()
    return _default_client

async def call_model(
    model_id: str,
    messages: Union[List[ChatMessage], List[Dict[str, str]]],
    **kwargs
) -> LLMResponse:
    """Convenience function for model calls."""
    client = await get_client()
    
    # Convert dict messages to ChatMessage if needed
    if messages and isinstance(messages[0], dict):
        messages = [ChatMessage(role=MessageRole(msg["role"]), content=msg["content"]) 
                   for msg in messages]
    
    return await client(model_id, messages, **kwargs)