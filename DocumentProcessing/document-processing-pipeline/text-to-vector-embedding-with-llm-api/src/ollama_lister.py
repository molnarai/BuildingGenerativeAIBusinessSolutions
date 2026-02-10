#!/usr/bin/env python3
"""
Ollama model lister.
Uses the same environment variables and configuration as processor.py.
"""

import os
import logging
from typing import Any, Dict, List, Optional

import requests

logger = logging.getLogger(__name__)


class OllamaModelLister:
	"""Lists available Ollama models and checks for a target model."""

	def __init__(self) -> None:
		self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
		self.ollama_api_key = os.getenv("OLLAMA_API_KEY")
		self.ollama_generation_model = os.getenv("OLLAMA_GENERATION_MODEL")
		self.ollama_embedding_model = os.getenv("OLLAMA_EMBEDDING_MODEL_NAME")
		self.use_ollama = bool(self.ollama_base_url)

	def list_models(self) -> Dict[str, Any]:
		"""
		List available models and indicate if OLLAMA_GENERATION_MODEL is present.

		Returns:
			A dict with models, target model, and availability status.
		"""
		result: Dict[str, Any] = {
			"ollama_configured": self.use_ollama,
			"base_url": self.ollama_base_url,
			"models": [],
			"target_model": self.ollama_generation_model,
			"target_model_available": False,
			"error": None,
		}

		if not self.use_ollama:
			result["error"] = "Ollama not configured (missing OLLAMA_BASE_URL)"
			return result

		headers = {"Content-Type": "application/json"}
		if self.ollama_api_key:
			headers["Authorization"] = f"Bearer {self.ollama_api_key}"

		try:
			response = requests.get(
				f"{self.ollama_base_url}/api/tags",
				headers=headers,
				timeout=30,
			)
		except requests.RequestException as exc:
			logger.error("Failed to contact Ollama: %s", str(exc))
			result["error"] = "Failed to contact Ollama server"
			return result

		if response.status_code != 200:
			logger.error("Ollama API error: %s - %s", response.status_code, response.text)
			result["error"] = f"API error: {response.status_code}"
			return result

		payload = response.json()
		models = payload.get("models", [])
		model_names: List[str] = []
		for model in models:
			name = model.get("name")
			if name:
				model_names.append(name)

		result["models"] = model_names
		if self.ollama_generation_model:
			result["target_model_available"] = self.ollama_generation_model in model_names

		return result
