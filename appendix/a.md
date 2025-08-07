# A: Configuring API Keys for AI Integration

## A.1 Creating an OpenAI API Key

If you want to use the models from OpenAI, you need to set up an API key on openai.com. After logging into your account at OpenAI, please visit to generate one API key for use the AI models from OpenAI.

To use OpenAI's models, you need to set up an API key on their platform. First, log in to your account on the OpenAI website (https://openai.com). Then, navigate to the API keys page (https://platform.openai.com/api-keys) to generate a new API key. This key will allow you to securely access and interact with OpenAI's AI models in your applications and workflows.

```{figure} ./images/a/image2.png
:label: figure-a-1
:alt: openai
:align: center
:width: 100%
```
In the OpenAI platform, you can generate an API key by clicking the green `Create new secret key` button located at the top right of the API keys page. Note that you may be required to add a payment method before you can access the API key. Keep in mind that each API key is displayed only once, so it's important to save it in a secure location for future use.
After creating the API key, the OpenAI API is powered by a diverse set of commonly used models with different capabilities and prices:
- gpt-4o: OpenAI's high-intelligence flagship model for complex, multi-step tasks
- gpt-4o-mini: An affordable and intelligent small model for fast, lightweight tasks
- gpt-3.5-turbo: A fast, inexpensive model for simple tasks
- chatgpt-4o-latest: A model version that continuously points to the version of GPT-4o used in ChatGPT, and is updated frequently

## A.2 Creating an NVIDIA API Key

### Option 1:

NVIDIA provides new users with 1,000 credits upon account creation, allowing you to explore and experiment with these powerful models and services without initial cost.

To quickly generate an API for NVIDIA NIM usage, just go to the exploration package of the AI models (https://build.nvidia.com/explore/discover) and enter one of them to start chatting and create an API key. 
For example, let's choose the Llama3.1 model (https://build.nvidia.com/meta/llama-3_1-405b-instruct) and enter the page. In this page, you can easily generate an API key after signing up and logging in. Just click the Get API Key on the right side of the page.

```{figure} ./images/a/image1.png
:label: figure-a-2
:alt: nvidia
:align: center
:width: 100%
```
### Option 2:

To access NVIDIA's foundation models and AI services, you first need to set up an NVIDIA NGC (NVIDIA GPU Cloud) API Key. Begin by signing in to your account on the NVIDIA NGC website (https://ngc.nvidia.com/signin). If you don’t have an account yet, you’ll need to create one. Once logged in, navigate to the NGC Setup page (https://org.ngc.nvidia.com/setup) to configure your account for API access. Here, you will find the option to generate personal key. Click on the button to create a personal API key, and make sure to securely store it as it will only be shown once.


```{figure} ./images/a/image3.png
:label: figure-a-2
:alt: nvidia
:align: center
:width: 100%
```

This API key will allow you to interact with NVIDIA’s powerful AI and foundation models, providing you with access to a range of AI services tailored for various applications, including natural language processing, computer vision, and digital content creation. With the API key set up, you can now explore the models available on the NVIDIA NGC platform by visiting the Explore page (https://build.nvidia.com/explore/discover) and select the model you want to use.
After creating your API key, you will gain access to a wide range of popular models offered by NVIDIA, spanning various AI and deep learning applications. 
- meta / llama-3.1-405b-instruct: Meta's most advanced LLM for synthetic data generation, distillation, and inference for chatbots, coding, and domain-specific tasks.
- meta / llama-3.1-8b-instruct: A relatively small model from Meta model with language understanding, superior reasoning, and text generation.
- mistralai / mixtral-8x22b-instruct-v0.1: an LLM from Mistral AI that follows instructions, completes requests, and generates creative text.