import gradio as ui; import requests, logging, os, json; from io import BytesIO
from requests.exceptions import *; logging.basicConfig(level=logging.DEBUG)

def queue(img, context, length_a, length_b, mode, genre, lang):
    if length_a == 'Pilihan sendiri':
        length = int(length_b)
    else:
        length = int(length_a)
        
    if mode == 'Standard': mode = 'Standard'
    if mode == 'Kompleks': mode = 'Complex'
    if mode == 'Kreatif': mode = 'Creative'
    if mode == 'Ringkas': mode = 'Simple'
    if genre == 'Fiksyen': genre = 'science fiction'
    if genre == 'Misteri': genre = 'mystery'
    if genre == 'Fantasi': genre = 'fantasy'
    if genre == 'Penjelasan': genre = 'Descriptive'
    if lang == 'Bahasa Melayu': lang = 'ms'
    if lang == 'Bahasa Inggeris': lang = 'en'
    if lang == 'Bahasa Mandarin': lang = 'zh-cn'
    if lang == 'Bahasa Tamil': lang = 'ta'
    
    return translate(expand(f'(Additional context for story direction: {context} and write the story using "{lang}" language code) {describe(img)}', length, mode, genre), lang), ui.TextArea(visible=True), img

def describe(input_img):
    image_bytes = BytesIO()
    input_img.save(image_bytes, format='jpeg')
    
    payload = {'model_version': (None, '1')}; data = [('image',('_describe.jpg', image_bytes.getvalue(), 'image/jpeg'))]
    key = {'bearer': os.getenv('bearer')}
    
    try:
        response = requests.post(os.getenv('describe'), headers=key, data=payload, files=data, timeout=30)
        result = response.text.split(',', 1)
        described = result[0]
        print(f"Image description -> {described}")
        return described
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def expand(source, length, mode, genre):
    head = {'Content-Type': 'application/json'}
    body = json.dumps({"topic": source, "word_count": length, "writing_mode": mode, "story_genre": genre})
    try: return requests.post(os.getenv('gpt4'), headers=head, data=body, timeout=30).json()['story']
    except Exception as e: print(f"Expansion error: {e}"); return None

def translate(fusion, lang):
    try:
        print(f'Expanded story -> {fusion}')
        if lang == 'en': return fusion #en&q=
        else: return requests.get(f"{os.getenv('fusion')}{lang}&q={fusion}", timeout=30).json()[0][0]
    except Exception as e: print(f"Error translating: {e}"); return fusion

def custom(i: ui.SelectData):
    if i.value == 'Pilihan sendiri': return ui.Number(visible=True)
    else: return ui.Number(visible=False)
    
def reset():
    return ui.TextArea(visible=False)

thx = ui.themes.Default(
    font=[ui.themes.GoogleFont('Myriad Pro')], font_mono=[ui.themes.GoogleFont('Myriad Pro')],
    text_size=ui.themes.Size(lg="18px", md="18px", sm="18px", xl="18px", xs="18px", xxl="18px", xxs="18px"),
    primary_hue='green', secondary_hue='green', neutral_hue='zinc')
    
css = '''
footer {display: none !important;}
.app.svelte-182fdeq.svelte-182fdeq {padding: 12px;}
::-webkit-scrollbar {display: none;}
::-webkit-scrollbar-button {display: none;}
.svelte-qbrfs .wrap:after {content: "(or Tap to open Camera)";}
'''