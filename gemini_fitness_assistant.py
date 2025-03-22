from api_reader import FITNESS_CHATBOT_GEMINI_API_KEY 
import gradio as gr 
import google.generativeai as genai

genai.configure(api_key=FITNESS_CHATBOT_GEMINI_API_KEY)

model = genai.GenerativeModel(model_name = "tunedModels/fitnessassistant-2aljrbsv6o10")
    
def get_program(cinsiyet, yas, boy, kilo, hedef): 
    # Fitness planı için kullanıcı bilgilerini içeren bir prompt oluştur
    prompt = f"""Cinsiyet: {cinsiyet}, Yaş: {yas}, Boy: {boy} cm, Kilo: {kilo} kg, Hedef: {hedef}. 
    Bu bilgilere göre kullanıcıya haftalık antrenman programı(7 günlük program) hazırla. Bu programı hazırlarken her gün yapılacak hareketler için set sayısı x tekrar sayılarını belirt.Kullanıcıya karbonhidrat ve protein ağırlıklı beslenmeler önerebilirsin(kilosuna göre) ve ek olarak günlük içmesi gereken su miktarını belirt => 0.35 ml/kg . 
    Kilosuna göre bir sporcunun alması gereken karbonhidrat miktarı yaklaşık olarak kilosu başına; 5-10 gram/kg , 
    protein miktarı 1.2 - 2 gram / kg , yağ miktarı ise 0.8 - 1.2 gram/kg şeklindedir. """

    # Modelden yanıt al
    response = model.generate_content(prompt)

    # Yanıtı döndür
    if response:
        return response.text.strip()
    else:
        return "Üzgünüm, şu anda yardımcı olamıyorum..." 

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

    submit_btn.click(
        get_program, 
        [cinsiyet, yas, boy, kilo, hedef], 
        [output]
    ) 
    clear_btn.click(
        lambda: (None, None, None, None, None , None), 
        [], 
        [cinsiyet, yas, boy, kilo, hedef, output]
    )

if __name__ == "__main__": 
    demo.launch(show_error=True)