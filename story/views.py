from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from api.utils import try_except_wrapper
from openai import OpenAI
import os
from story.models import Story, GeneratedStory
import requests
import json
from story import utils
import time

def define_story_by_search_openai(text_search, list_story):
    client = OpenAI(
        api_key=utils.get_token('OPEN_KEY'),
    )

    prompt = f"Người dùng đang tìm kiếm một câu chuyện lịch sử bằng cách search: {text_search}. Với danh sách các câu chuyện sau: {list_story} và những hiểu biết của bạn. Hãy đề xuất 1 câu chuyện phù hợp trong danh sách trên. Kết quả trả về là một ID (interger) duy nhất (Vui lòng không xin lỗi, không cảm ơn, không mô tả...)."

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    message_content = chat_completion.choices[0].message.content
    return message_content

def generate_story_openai(object, style, purpose, prev_session, cur_session):
    client = OpenAI(
        api_key=utils.get_token('OPEN_KEY'),
    )

    prompt = f"Tôi đang thuyết minh lịch sử cho {object} với phong cách kể {style} nhằm mục đích {purpose}. {'Nối tiếp phần sau của câu chuyện: {prev_session}, hãy' if prev_session else 'Hãy'} giúp tôi viết 1 đoạn thuyết minh ngắn gọn (không quá 100 từ) nhưng đầy đủ theo cốt chuyện lịch sử sau (giữ nguyên các mốc lịch sử: năm, thế kỷ, giai đoạn..., không viết tắt): {cur_session}. Kết quả trả về chỉ là đoạn văn bản thuyết minh."

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    message_content = chat_completion.choices[0].message.content
    return message_content

def create_questionaire_openai(content, prev_questions = None):
    client = OpenAI(
        api_key=utils.get_token('OPEN_KEY'),
    )

    prompt = f'Với nội dung lịch sử Việt Nam như sau: {content}. YÊU CẦU: Hãy tạo giúp tôi một câu hỏi trắc nghiệm để kiểm tra kiến thức về nội dung lịch sử trên{" mà không trùng với các câu hỏi: {prev_questions}" if prev_questions else ""}. Kết quả trả về có dạng: "question": question, "options": [option1, option2, option3, option4], "answer": INDEX'
    # print(prompt)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    message_content = chat_completion.choices[0].message.content
    return message_content

def genarate_new_text_openai(content, style, object, purpose):
    client = OpenAI(
        api_key=utils.get_token('OPEN_KEY'),
    )

    prompt = f'Viết lại đoạn sau theo phong cách {style} dành cho đối tượng {object} nhằm mục đích {purpose}: {content}'
    # print(prompt)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    message_content = chat_completion.choices[0].message.content
    return message_content

def pick_img_openai(content, list_img):
    client = OpenAI(
        api_key=utils.get_token('OPEN_KEY'),
    )

    prompt = f'Với danh sách các hình ảnh và mô tả của mỗi hình ảnh: {list_img}. hãy chọn giúp tôi một hình ảnh phù hợp cho đoạn văn: {content}. YÊU CẦU: Kết quả trả về là một số nguyên biểu diễn "INDEX" (start=0, không chứa nội dung khác).'
    # print(prompt)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    message_content = chat_completion.choices[0].message.content
    return message_content

def text_to_speech(text):
    url = os.getenv('FPTAI_URL')

    payload = text
    headers = {
        'api-key': utils.get_token('FPTAI_KEY'),
        'speed': '',
        'voice': os.getenv('FPTAI_VOICE')
    }

    response = requests.request(
        'POST',
        url, data=payload.encode('utf-8'),
        headers=headers
    )

    return response.text

def text_to_image(describe):
    client = OpenAI(
        api_key=utils.get_token('OPEN_KEY'),
    )

    prompt = f"Hãy tạo hình ảnh mô tả sự kiện dưới đây với các yếu tố như cảnh chiến, các nhân vật chính và cảnh vật xung quanh: {describe}"

    response = client.images.generate(
        model="dall-e-2",
        prompt=prompt,
        n=1,
        size="1024x1024"
    )

    image_data_list = response.data

    if image_data_list:
        image_url = image_data_list[0].url
        return image_url
    else:
        return None

class StoryApi(ViewSet):
    @action(
        detail=False,
        methods=["POST"],
        url_path="generate",
        url_name="generate",
    )
    @try_except_wrapper
    def generate(self, request):
        text_search = request.data['text_search']
        object = request.data['object']
        style = request.data['style']
        purpose = request.data['purpose']

        stories = Story.objects.all().values_list('id', 'title', 'historical_figures', 'period')
        id = int(define_story_by_search_openai(text_search=text_search, list_story=stories))

        story = Story.objects.filter(pk=id).first()
        related_images = story.story_imgs.all().values_list("url", "description")
        story_images_list = list(related_images)

        img_list = []

        if story:
            data = []

            story_paragraphs = story.content.split('\n')

            for paragraph in story_paragraphs:
                img_idx = pick_img_openai(paragraph, story_images_list)
                print(img_idx)
                img_url = story_images_list[int(img_idx)][0]

                story_images_list.pop(int(img_idx))
                img_list.append(img_url)
                print(img_url)

                text = generate_story_openai(
                    object=object,
                    style=style,
                    purpose=purpose,
                    prev_session=data[-1]['text'] if len(data) else None,
                    cur_session=paragraph
                )

                fpt_url = json.loads(text_to_speech(text))['async']

                while True:
                    response = requests.get(fpt_url)
                    if response.status_code == 200:
                        break
                    print("Pulling...")
                    time.sleep(3)

                voice_url = utils.upload_file(
                    id,
                    fpt_url
                )

                duration = utils.fetch_and_check_audio_length(fpt_url)

                item = {
                    "text": text,
                    "voice_url": voice_url,
                    "fpt_url": fpt_url,
                    "img_url": img_url,
                    "duration": duration,
                    "start_time": data[-1]['end_time'] if len(data) else 0,
                    "end_time": data[-1]['end_time'] + duration if len(data) else duration,
                }

                data.append(item)

            # CREATE QUESTIONAIRE
            prev_questions = ''
            questionaire = []
            for _ in range(5):
                data_question = create_questionaire_openai(
                    story.content,
                    prev_questions
                )

                data_question = json.loads(data_question)

                prev_questions += data_question['question']
                questionaire.append(data_question)


            context = genarate_new_text_openai(story.context, style, object, purpose)
            historical_significance = genarate_new_text_openai(story.historical_significance, style, object, purpose)
            main_happenings = genarate_new_text_openai(story.main_happenings, style, object, purpose)
            result = genarate_new_text_openai(story.result, style, object, purpose)

            data_object = {
                "content": data,
                "imgs": img_list,
                "questionaire": questionaire,
                "summary": {
                    "context": context,
                    "historical_significance": historical_significance,
                    "main_happenings": main_happenings,
                    "result": result,
                }
            }

            generated_story = GeneratedStory.objects.create(
                story=story,
                object=object,
                style=style,
                purpose=purpose,
                data=data_object
            )
            generated_story.save()

        return Response(
            data=data_object,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=["POST"],
        url_path="create-story",
        url_name="create-story",
    )
    @try_except_wrapper
    def create_story(self, request):
        text_search = request.data['text_search']
        object = request.data['object']
        style = request.data['style']
        purpose = request.data['purpose']

        stories = Story.objects.all().values_list('id', 'title', 'historical_figures', 'period')
        id = int(define_story_by_search_openai(text_search=text_search, list_story=stories))

        story = GeneratedStory.objects.filter(story=id).last()

        return Response(
            data=story.data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=["GET"],
        url_path="get-all",
        url_name="get-all",
    )
    @try_except_wrapper
    def get_all(self, request):
        generated_stories = GeneratedStory.objects.all()

        data = []

        for story in generated_stories:
            item = story.data
            item['imgs'] = utils.shuffle_array(item['imgs'])

            data.append(item)

        return Response(
            data=data,
            status=status.HTTP_200_OK,
        )
