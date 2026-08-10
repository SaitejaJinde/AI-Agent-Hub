import os
from dotenv import load_dotenv

load_dotenv()

llm = None

class MockResponse:
    def __init__(self, content: str):
        self.content = content

    def __str__(self):
        return self.content


class MockLLM:
    """A very small mock LLM for local development and tests.

    It exposes an `invoke(prompt)` method and is callable so callers can use
    either `llm.invoke(prompt)` or `llm(prompt)`.
    """
    def invoke(self, prompt: str):
        return MockResponse(f"Mock response: {prompt}")

    def __call__(self, prompt: str):
        return self.invoke(prompt)


def get_llm():
    """Return a usable LLM object.

    Selection logic:
    - If `USE_MOCK_LLM` env var is set to a truthy value, return MockLLM.
    - If `GOOGLE_API_KEY` is present, attempt to construct ChatGoogleGenerativeAI.
    - If constructing the real LLM fails, fall back to MockLLM and print a warning.

    This function avoids raising on import or missing keys so the application can
    start in local/test environments and produce helpful warnings instead.
    """
    global llm

    if llm is not None:
        return llm

    use_mock = os.getenv("USE_MOCK_LLM", "false").lower() in ("1", "true", "yes")
    api_key = os.getenv("GOOGLE_API_KEY")

    if use_mock:
        llm = MockLLM()
        print("Using MockLLM because USE_MOCK_LLM is set.")
        return llm

    if not api_key:
        # No API key — fall back to mock but print a clear instruction.
        print("WARNING: GOOGLE_API_KEY is not set. Falling back to MockLLM.\n"
              "Set GOOGLE_API_KEY and unset USE_MOCK_LLM to use the real LLM.")
        llm = MockLLM()
        return llm

    try:
        # Import here to avoid import-time dependency errors for users who only
        # want to run the project locally without the real LLM packages installed.
        from langchain_google_genai import ChatGoogleGenerativeAI

        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            google_api_key=api_key
        )
        print("Initialized ChatGoogleGenerativeAI LLM.")
        return llm

    except Exception as e:
        print("Failed to initialize ChatGoogleGenerativeAI:", e)
        print("Falling back to MockLLM for continued operation.")
        llm = MockLLM()
        return llm
