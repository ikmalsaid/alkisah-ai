from alkisah_data import *

with ui.Blocks(title='Alkisah AI', theme=thx, css=css, analytics_enabled=False) as alkisah:
    ui.HTML(value='''
            <center>
                <h2>📸 Alkisah AI Web App 📝</h2>
                <p>Sebuah aplikasi web menulis cerita berdasarkan foto dan konteks menggunakan AI</p>
            </center>
            ''')
    
    with ui.Row(equal_height=True):
        with ui.Column(min_width=512, variant='panel'):
            input_image = ui.Image(label='Gambar Input', type='pil', sources=['webcam', 'upload'], height=640)
            story_output = ui.Textbox(label='Hasil janaan:', show_copy_button=True, visible=False)
            context_add = ui.Textbox(label='Tambah konteks pada penceritaan:', placeholder='Masa, tempat atau keadaan...')
            length_choice = ui.Dropdown(label='Bilangan perkataan yang diingini:', choices=['60', '150', '300', 'Pilihan sendiri'], value='60')
            length_custom = ui.Number(label='Tentukan bilangan perkataan:', value=60, maximum=2000, visible=False)
            story_mode = ui.Dropdown(label='Mod penghasilan cerita:', choices=['Standard', 'Kompleks', 'Kreatif', 'Ringkas'], value='Standard')
            story_genre = ui.Dropdown(label='Genre yang diingini:', choices=['Fiksyen', 'Misteri', 'Fantasi', 'Penjelasan'], value='Penjelasan')
            story_lang = ui.Dropdown(label='Bahasa yang dipilih:', choices=['Bahasa Melayu', 'Bahasa Inggeris', 'Bahasa Mandarin', 'Bahasa Tamil'], value='Bahasa Melayu')
            
            with ui.Group():
                with ui.Row():
                    story_reset = ui.ClearButton(value='Set Semula', components=[input_image, story_output])
                    story_stop = ui.Button('Batal')
                    story_init = ui.Button('Hantar', variant='primary')
    
    process = story_init.click(fn=queue, inputs=[input_image, context_add, length_choice, length_custom, story_mode, story_genre, story_lang], outputs=[story_output, story_output, input_image])
    length_choice.select(fn=custom, inputs=None, outputs=[length_custom])
    story_reset.click(fn=reset, inputs=None, outputs=[story_output])
    story_stop.click(fn=None, inputs=None, outputs=None, cancels=[process])
    
    ui.HTML(value='''
            <center>
                <h2>Dibangunkan oleh Ikmal Said (<a href='https://twitter.com/ikmalsaid'>@ikmalsaid</a>) untuk #GodamSahur 2024</h2>
            </center>
            ''')

if __name__ == "__main__":
    alkisah.queue(default_concurrency_limit=100).launch(inbrowser=True, favicon_path="favicon.ico")