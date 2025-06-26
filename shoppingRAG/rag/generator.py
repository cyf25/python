import openai

# 直接在此处填写你的API Key和API Base（仅供本地测试，生产环境请用环境变量！）
DEEPSEEK_API_KEY = "key"
DEEPSEEK_API_BASE = "https://api.deepseek.com"

openai.api_key = DEEPSEEK_API_KEY
openai.base_url = DEEPSEEK_API_BASE

PROMPT_TEMPLATE = """
你是一位专业的电商智能客服，请根据以下知识库内容和用户问题，给出详细、准确、友好的回复。

知识库内容：
{context}

用户问题：
{question}

请用中文回答。
"""

def generate_answer(question, docs):
    context = "\n".join(docs)
    prompt = PROMPT_TEMPLATE.format(context=context, question=question)
    response = openai.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=512
    )
    return response.choices[0].message.content.strip() 