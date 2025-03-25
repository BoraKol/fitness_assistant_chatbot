from api_reader import FITNESS_CHATBOT_GEMINI_API_KEY 
import gradio as gr 
import google.generativeai as genai
from fpdf import FPDF
import tempfile 
import os

genai.configure(api_key=FITNESS_CHATBOT_GEMINI_API_KEY)

model = genai.GenerativeModel(model_name = "tunedModels/fitnessasistantchatbot-c18nkd3ca8cw")
    
def get_program(cinsiyet, yas, boy, kilo, hedef ,calisma_stili , 
spor_gecmisi , saglik_problemi , saglik_durumu): 
    # Fitness planı için kullanıcı bilgilerini içeren bir prompt oluştur
    prompt = f"""Cinsiyet: {cinsiyet}, Yaş: {yas}, Boy: {boy} cm, Kilo: {kilo} kg, Hedef: {hedef} ,   çalışma şekli : {calisma_stili} , sporcu seviyesi : {spor_gecmisi} , sağlık problemi : {saglik_problemi} , sağlık durumu : {saglik_durumu}. 
    Bu bilgilere göre kullanıcıya haftalık antrenman programı(7 günlük program) hazırla. Bu programı hazırlarken her gün yapılacak hareketler için set sayısı x tekrar sayılarını belirt.Kullanıcıya karbonhidrat ve protein ağırlıklı beslenmeler önerebilirsin(kilosuna göre). Bu beslenme önerilerini sunarken şunları göz önünde bulundur: Kilosuna göre bir sporcunun alması gereken karbonhidrat miktarı yaklaşık olarak kilosu başına 5-10 gram/kg , protein miktarı 1.2 - 2 gram / kg , yağ miktarı ise 0.8 - 1.2 gram/kg şeklindedir. """

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
    pdf.add_font("Times New Roman", "", "c:\\Windows\\Fonts\\times.ttf", uni=True)
    pdf.set_font("Times New Roman", size=12)
    
    # Add title
    pdf.set_font("Times New Roman", size=16)
    pdf.cell(200, 10, txt="Fitness Training Program", ln=True, align='C')
    pdf.ln(10)
    
    # Add content
    pdf.set_font("Times New Roman", size=12)
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
    background-image: url('https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=1470&auto=format&fit=crop') !important;
    background-size: cover !important;
    background-position: center !important;
    background-repeat: no-repeat !important;
    color: white !important;
 }
 h1 {
    text-align: center !important;
    color: white !important;
    font-size: 3em !important;
    font-weight: bold !important;
    text-shadow: 4px 2px 2px rgba(0, 0, 0, 0.7) !important;
 }
 .gradio-row {
    background-color: rgba(0, 0, 0, 0.7) !important;
    padding: 20px !important;
    border-radius: 10px !important;
    margin: 10px !important;
 }

 footer {
    text-align: center !important;
    background-color: black !important;
    color: orange !important;
 }

"""

def show_textbox(has_health_issue) : 
    if has_health_issue : 
        return gr.update(visible=True) ## var ise textbox gorunur yap
    else : 
        return gr.update(visible=False , value = "") ## yoksa textbox'ı gizle ve içeriği temizle

with gr.Blocks(theme=gr.themes.Citrus() , css = custom_css) as demo:
    gr.HTML("<h1> 🏋 Fitness Danışmanı </h1>")
    
    with gr.Row():
        with gr.Column():
            cinsiyet = gr.Dropdown(choices=["Female", "Male"], label="Gender")
            yas = gr.Slider(minimum=18, maximum=50, step=1, value=20 , label="Age")
            boy = gr.Slider(minimum=150, maximum=200, step=1, value = 160 , label="Height (cm)")
            kilo = gr.Slider(minimum=50, maximum=120, step=1, value = 60 , label="Weight (kg)")
            calisma_stili = gr.Dropdown(choices = ["Home office" , "Hybrid" , "Office"] ,
            label = "Work type")
            spor_gecmisi = gr.Dropdown(choices=["Beginner" , "Intermediate" , "Advanced"] ,
            label = "Fitness Level")
            hedef = gr.Dropdown(choices=["Muscle Gain", "Strength", "Flexibility", "Fat Loss" , "Endurance"], label="Sport Goal")
            saglik_problemi = gr.Checkbox(label = "Please select if you have chronic health problems/injuries")
            saglik_durumu = gr.Dropdown(choices = ["Diabetes" , "Heart Disease" , "Hypertension" , "Asthma"] , label = "Please inform us about your health problems/injuries here" , visible = False)
            submit_btn = gr.Button("Antrenman Programı Oluştur")
            clear_btn = gr.Button("Temizle")
        with gr.Column():
            output = gr.Textbox(label="Antrenman Programı", lines=5, placeholder="output")
            pdf_output = gr.File(label = "Pdf File")
    
    gr.HTML("""<footer>
     All rights reserved. Created by Alper Sancılı - Bora Kol  
     </footer>""")

    saglik_problemi.change(
        show_textbox , ## function
        saglik_problemi , ## input
        saglik_durumu ## output
    ) 
    submit_btn.click(
        get_program, 
        [cinsiyet, yas, boy, kilo, hedef ,calisma_stili, saglik_problemi , saglik_durumu , spor_gecmisi], 
        [output , pdf_output]
    ) 
    clear_btn.click(
        lambda: (None, None, None, None, None , None , None , None , None , None , None), 
        [], 
        [cinsiyet, yas, boy, kilo, hedef, calisma_stili , spor_gecmisi , output , pdf_output]
    )

if __name__ == "__main__": 
    demo.launch(show_error=True)
