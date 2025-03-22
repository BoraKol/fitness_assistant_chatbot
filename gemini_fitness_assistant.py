from api_reader import FITNESS_CHATBOT_GEMINI_API_KEY 
import gradio as gr 
import google.generativeai as genai
from fpdf import FPDF
import tempfile 
import os

genai.configure(api_key=FITNESS_CHATBOT_GEMINI_API_KEY)

model = genai.GenerativeModel(model_name = "tunedModels/fitnessassistant-2aljrbsv6o10")
    
def get_program(cinsiyet, yas, boy, kilo, hedef): 
    # Fitness planı için kullanıcı bilgilerini içeren bir prompt oluştur
    prompt = f"""Cinsiyet: {cinsiyet}, Yaş: {yas}, Boy: {boy} cm, Kilo: {kilo} kg, Hedef: {hedef}. 
    Bu bilgilere göre kullanıcıya haftalık antrenman programı(7 günlük program) hazırla. Bu programı hazırlarken her gün yapılacak hareketler için set sayısı x tekrar sayılarını belirt.Kullanıcıya karbonhidrat ve protein ağırlıklı beslenmeler önerebilirsin(kilosuna göre) ve ek olarak günlük içmesi gereken su miktarını söyle , kg başına 0.35 ml kadar su içilmeli . 
    Kilosuna göre bir sporcunun alması gereken karbonhidrat miktarı yaklaşık olarak kilosu başına; 5-10 gram/kg , 
    protein miktarı 1.2 - 2 gram / kg , yağ miktarı ise 0.8 - 1.2 gram/kg şeklindedir. """

    # Modelden yanıt al
    response = model.generate_content(prompt)

    # Yanıtı döndür
    if response:
        text_output =  response.text.strip()
        pdf_path = create_pdf(text_output)
        return text_output , pdf_path
    else:
        return "Üzgünüm, şu anda yardımcı olamıyorum..." , None

def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    
    # Set font that supports Turkish characters
    pdf.add_font("Arial", "", "c:\\Windows\\Fonts\\arial.ttf", uni=True)
    pdf.set_font("Arial", size=12)
    
    # Add title
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt="Fitness Training Program", ln=True, align='C')
    pdf.ln(10)
    
    # Add content
    pdf.set_font("Arial", size=12)
    # Split text into lines and add to PDF
    for line in text.split('\n'):
        try:
            pdf.multi_cell(0, 10, txt=line, align='L')
        except Exception as e:
            # If there's an error, try to clean the text
            cleaned_line = ''.join(char for char in line if ord(char) < 128)
            pdf.multi_cell(0, 10, txt=cleaned_line, align='L')
    
    # Save to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        pdf.output(tmp.name)
        return tmp.name
             

custom_css = """
 .gradio-container {
    background-color : #FAEBD7 !important ; 
    color : white !important ;
 }
 h1 {
    text-align : center !important;
    color : orange !important ;
 }

"""

with gr.Blocks(theme=gr.themes.Citrus() , css = custom_css) as demo:
    gr.HTML("<h1> 🏋 Fitness Danışmanı </h1>")
    
    with gr.Row():
        with gr.Column():
            cinsiyet = gr.Dropdown(choices=["Female", "Male"], label="Gender")
            yas = gr.Slider(minimum=18, maximum=50, step=1, label="Age")
            boy = gr.Slider(minimum=150, maximum=200, step=1, label="Height (cm)")
            kilo = gr.Slider(minimum=50, maximum=120, step=1, label="Weight (kg)")
            hedef = gr.Dropdown(choices=["Muscle Gain", "Strength", "Flexibility", "Fat Loss" , "Endurance"], label="Sport Goal")
            submit_btn = gr.Button("Antrenman Programı Oluştur")
            clear_btn = gr.Button("Temizle")
        with gr.Column():
            output = gr.Textbox(label="Antrenman Programı", lines=5, placeholder="output")
            pdf_output = gr.File(label = "Pdf File")
    submit_btn.click(
        get_program, 
        [cinsiyet, yas, boy, kilo, hedef], 
        [output , pdf_output]
    ) 
    clear_btn.click(
        lambda: (None, None, None, None, None , None , None), 
        [], 
        [cinsiyet, yas, boy, kilo, hedef, output , pdf_output]
    )

if __name__ == "__main__": 
    demo.launch(show_error=True)
