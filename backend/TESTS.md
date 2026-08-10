### Tests

Run the backend unit tests (a simple smoke test that uses the MockLLM):

```bash
pip install -r requirements.txt
pytest -q
```

Note: the test suite uses the MockLLM via the `USE_MOCK_LLM` environment
variable (set to `true` in `.env.example`).
