# Getting an OpenAI API Key

To use the Mind Companion chatbot, you'll need an OpenAI API key. Here's how to get one:

1. Go to [OpenAI's platform website](https://platform.openai.com/signup)
2. Create an account or sign in if you already have one
3. Navigate to the API keys section in your account settings
4. Generate a new API key
5. Copy the key and paste it in your `.env` file as follows:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Important Notes

- Keep your API key secure and do not share it publicly
- OpenAI provides free credits for new users, but after that, you'll need to add a payment method
- Monitor your usage to avoid unexpected charges

## Alternative LLM Options

If you prefer not to use OpenAI's API, you can modify the `response_generator.py` file to use alternative language models:

- [Hugging Face models](https://huggingface.co/)
- [Anthropic's Claude API](https://www.anthropic.com/product)
- Open-source models that can run locally

Follow the documentation for your chosen alternative to update the implementation.
