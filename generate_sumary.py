from openai import OpenAI
import encrypt
import pandas as pd

def generate_summary_dataframe(dataframe):
    # Tạo prompt từ dữ liệu DataFrame
    prompt = "Here are some video details:\n"
    for index, row in dataframe.iterrows():
        prompt += f"Video title: {row['video_title']}\n"
        prompt += f"Channel name: {row['channel_name']}\n"
        prompt += f"View count: {row['view_count']}\n"
        prompt += f"Like count: {row['like_count']}\n"
        prompt += f"Dislike count: {row['dislike_count']}\n"
        prompt += f"Published at: {row['publishedAt']}\n\n"
    prompt += "Please summarize the information above."

    # Cấu hình API Key của bạn
    openai_api_key = encrypt.decrypt('xp-jXagRaRDIPvg4Z41dkbEY3GqgpKOrg3R4x8YCer8kQ0wQJvs',5)
    client = OpenAI(api_key=openai_api_key)

    # Gửi prompt đến API sử dụng model GPT-3.5 Turbo và nhận câu trả lời
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])

    # Trích xuất tin nhắn từ câu trả lời
    msg = response.choices[0].message.content

    return msg