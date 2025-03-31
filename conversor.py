import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog, messagebox

def generar_jrxml(xml_input, output_file):
    try:
        tree = ET.parse(xml_input)
        root = tree.getroot()

        fields = []
        ids = []
        etiquetas = []

#items
        for item in root.findall(".//item"):
            item_id = item.get("id")
            code = item.get("code")
            tipo = item.get("tipo")

            if item_id and code:
                ids.append(item_id)
                fields.append(f'''    <field name="{item_id}" class="java.lang.String">
        <fieldDescription><![CDATA[section[code/@code='{code}']/text]]></fieldDescription>
    </field>''')

#etiquetas
            if tipo == "ETIQUETA" and item.text:
                etiquetas.append(f')?("<style isBold=\\"true\\" pdfFontName=\\"Helvetica-Bold\\">{item.text}\\n\\n</style>"):("")) +')

#plantilla
        if ids:
            inicio = '((' + ' || '.join([f'$F{{{i}}}!=null' for i in ids]) + ')?("<style isBold=\\"true\\" pdfFontName=\\"Helvetica-Bold\\">¿Tuvo la enfermedad injerto contra huésped (GvHD)?\\n\\n</style>"):("")) +\n'
            cuerpo = '\n'.join([f'(($F{{{i}}}==null)?("") : ("<style isBold=\\"true\\" pdfFontName=\\"Helvetica-Bold\\"></style>" + $F{{{i}}} + "\\n")) +' for i in ids])
            cierre = '($F{' + '}!=null || $F{'.join(ids) + '}!=null?"\\n\\n":"") +'
            plantilla = inicio + cuerpo + "\n" + cierre
        else:
            plantilla = ""

#generar contenidos
        jrxml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<jasperReport>
{'\n'.join(fields)}

    <textFieldExpression><![CDATA[
{plantilla}
    ]]></textFieldExpression>

{'\n'.join(etiquetas)}

</jasperReport>
'''

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(jrxml_content)

        messagebox.showinfo("Éxito", f"Tu JRXML se ha generado correctamente: {output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"No se ha podido procesar el XML\n{str(e)}")

def seleccionar_archivo():
    file_path = filedialog.askopenfilename(filetypes=[("Archivos XML", "*.xml")])
    if file_path:
        guardar_archivo(file_path)

def guardar_archivo(xml_file):
    output_file = filedialog.asksaveasfilename(defaultextension=".jrxml", filetypes=[("Archivos JRXML", "*.jrxml")])
    if output_file:
        generar_jrxml(xml_file, output_file)

#crear interfaz
root = tk.Tk()
root.title("Conversor de JRXML")
root.geometry("400x200")

tk.Label(root, text="Selecciona un archivo XML:").pack(pady=10)
tk.Button(root, text="Buscar XML", command=seleccionar_archivo).pack(pady=10)

root.mainloop()
