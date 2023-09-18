from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import default_storage
import re
import fitz
import openai

# 토큰 수를 조절하는데 사용할 만한 방법들
# NLP 딥러닝에 사용될 수 있는 text 토큰화 방법
# text embeding -> 사용할 만한 모델이 openai 꺼라서 결국 애매
# 텍스트 전처리 <- 다양하게 고려할 수 있는데 방법이 많다

# 현재 정성록 playground api
# api가 계속 없어지는 에러가 발생해서 만약 에러가 발생하면 각자 api를 발행하거나 카톡으로 애기 주셈
openai.api_key = "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"

# 파일 업로드 처리를 django의 method에 의존
def handle_upload_file(f):
    file_path = default_storage.save(f.name, f)
    return file_path


# 가져온 pdf 파일을 저장하는 로직들 
def pdf_save(request):
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        pdf_file = request.FILES['pdf_file']
        pdf_content = pdf_file.read()
        pdf_text = extract_text(pdf_content)
        # openai와 통신을 통해 pdf 요약한 값
        response = get_completion(pdf_text)
        return render(request, 'pdf_viewer.html', {'pdf_text': pdf_text, 'response': response})
    
    return render(request, 'pdf_upload.html')


def preprocess_text(text):
    # 특수 문자 제거
    cleaned_text = re.sub(r'[^\w\s]', '', text)
    # 줄바꿈을 공백으로 대체
    cleaned_text = cleaned_text.replace('\n', '').replace('\r', '')
    return cleaned_text

# 글자 추출 메소드
def extract_text(pdf_content):
    pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
    text= ""

    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        page_text = page.get_text("text")
        cleaned_text = preprocess_text(page_text)
        text += cleaned_text

    pdf_document.close()
    return text

# openai api 하고 통신하는 부분
def get_completion(prompt):
    system_message = "You are a respected writer in the world You have a professional level of understanding of the text in each field no matter what field the content of the PDF is You can handle them very well"
    
    user_message = prompt + "PDF 내용을 가장 중요한 핵심내용으로 세줄 요약 해주십시오"
    max_tokens = 16000

    total_tokens = len(system_message.split()) + len(user_message.split())
    print(user_message)

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
    response = ""

    while total_tokens > 0:
        tokens_to_request = min(total_tokens, max_tokens)
        query = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo-16k-0613",
            messages = messages,
            max_tokens = tokens_to_request,
            temperature = 0.5,
        )
        response += query.choices[0].message["content"]
        total_tokens -= tokens_to_request

        if query.choices[0].finish_reason == "stop":
            break # 정상적으로 다하면 break
        elif query.choices[0].finish_reason == "error":
            break
    return response
    
def query_view(request):
    if request.method == "POST":
        prompt = request.POST.get('prompt')
        response = get_completion(prompt)
        return JsonResponse({'response': response})
    return render(request, 'pdf_viewer.html', {'pdf_text':None, 'response':None})