import streamlit as st
import pandas as pd
from collections import Counter

# 1 y 2. Nombre y Emoji (Pergamino y Lupa)
st.set_page_config(page_title="Nostradamus", page_icon="📜", layout="centered")

# Diccionario para asociar el número con su animal y emoji visual
animales = {
    '0': ('Delfín', '🐬'), '00': ('Ballena', '🐳'), '1': ('Carnero', '🐏'),
    '2': ('Toro', '🐂'), '3': ('Ciempiés', '🐛'), '4': ('Alacrán', '🦂'),
    '5': ('León', '🦁'), '6': ('Rana', '🐸'), '7': ('Perico', '🦜'),
    '8': ('Ratón', '🐁'), '9': ('Águila', '🦅'), '10': ('Tigre', '🐅'),
    '11': ('Gato', '🐈'), '12': ('Caballo', '🐎'), '13': ('Mono', '🐒'),
    '14': ('Paloma', '🕊️'), '15': ('Zorro', '🦊'), '16': ('Oso', '🐻'),
    '17': ('Pavo', '🦃'), '18': ('Burro', '🐴'), '19': ('Chivo', '🐐'),
    '20': ('Cochino', '🐖'), '21': ('Gallo', '🐓'), '22': ('Camello', '🐪'),
    '23': ('Cebra', '🦓'), '24': ('Iguana', '🦎'), '25': ('Gallina', '🐔'),
    '26': ('Vaca', '🐄'), '27': ('Perro', '🐕'), '28': ('Zamuro', '🦅'),
    '29': ('Elefante', '🐘'), '30': ('Caimán', '🐊'), '31': ('Lapa', '🦦'),
    '32': ('Ardilla', '🐿️'), '33': ('Pescado', '🐟'), '34': ('Venado', '🦌'),
    '35': ('Jirafa', '🦒'), '36': ('Culebra', '🐍')
}

# 3, 5 y 6. Inyección de CSS para Diseño Premium (Fondo negro, input central gigante)
st.markdown("""
    <style>
        /* Importar fuente premium */
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800&display=swap');
        
        /* Fondo negro y texto blanco */
        .stApp {
            background-color: #000000;
            color: #ffffff;
            font-family: 'Montserrat', sans-serif;
        }
        
        /* Títulos centrados */
        h1, h2, h3 {
            font-family: 'Montserrat', sans-serif;
            text-align: center;
        }

        /* Input gigante e intuitivo en el centro */
        div[data-baseweb="input"] {
            border-radius: 15px;
            border: 2px solid #D4AF37; /* Borde doradito premium */
            background-color: #111111;
        }
        div[data-baseweb="input"] input {
            font-size: 3rem !important; /* Número gigante */
            text-align: center !important;
            font-weight: 800;
            color: #ffffff;
            padding: 20px;
        }
        
        /* Cajas de resultados */
        .caja-resultado {
            background-color: #151515;
            border: 1px solid #333;
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            margin-bottom: 15px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.5);
        }
        .caja-numero {
            font-size: 2rem;
            font-weight: 800;
            color: #D4AF37; /* Dorado */
        }
        .caja-emoji {
            font-size: 3rem;
            display: block;
            margin-bottom: 5px;
        }
        .caja-texto {
            font-size: 1rem;
            color: #aaaaaa;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📜 NOSTRADAMUS 🔍")
st.markdown("<p style='text-align: center; font-size: 1.1rem; color: #888;'>Sube tu historial y deja que la matemática hable.</p>", unsafe_allow_html=True)

archivo_subido = st.file_uploader("", type=["xlsx", "csv"])

if archivo_subido is not None:
    try:
        if archivo_subido.name.endswith('.csv'):
            df = pd.read_csv(archivo_subido, header=None)
        else:
            df = pd.read_excel(archivo_subido, header=None)
            
        todos_los_datos = df[0].astype(str).str.strip().tolist()
        ventana_sorteos = 800
        datos_recientes = todos_los_datos[-ventana_sorteos:]
        
        st.success(f"✅ Historial activo: {len(datos_recientes)} sorteos.")
        st.divider()
        
        st.markdown("<h3>INGRESA EL NÚMERO AQUÍ</h3>", unsafe_allow_html=True)
        objetivo = st.text_input("", placeholder="Ej: 15")
        
        if objetivo:
            objetivo = objetivo.strip()
            apariciones = datos_recientes.count(objetivo)
            
            if apariciones == 0:
                st.warning(f"⚠️ El número {objetivo} no ha salido recientemente.")
            else:
                siguientes_2 = []
                siguientes_12 = []
                
                for i in range(len(datos_recientes)):
                    if datos_recientes[i] == objetivo:
                        siguientes_2.extend(datos_recientes[i+1 : i+1+2])
                        siguientes_12.extend(datos_recientes[i+1 : i+1+12])
                
                st.divider()
                
                # --- EL FIJO (Próximos 2) ---
                conteo_2 = Counter(siguientes_2)
                fijo = conteo_2.most_common(1)
                
                st.markdown("<h3>🎯 EL FIJO (Próximos 2 Sorteos)</h3>", unsafe_allow_html=True)
                if fijo:
                    num_fijo = fijo[0][0]
                    freq_fijo = fijo[0][1]
                    nombre, emoji = animales.get(num_fijo, ('Desconocido', '❓'))
                    
                    st.markdown(f"""
                        <div class='caja-resultado'>
                            <span class='caja-emoji'>{emoji}</span>
                            <span class='caja-numero'>{num_fijo} - {nombre}</span><br>
                            <span class='caja-texto'>Ha reventado {freq_fijo} veces cortico.</span>
                        </div>
                    """, unsafe_allow_html=True)
                
                # --- LOS CALIENTES (Próximos 12) ---
                conteo_12 = Counter(siguientes_12)
                top_12 = conteo_12.most_common(3)
                
                st.markdown("<h3>🔥 LOS 3 CALIENTES (Próximos 12 Sorteos)</h3>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                columnas = [col1, col2, col3]
                
                for idx, (num_cal, freq_cal) in enumerate(top_12):
                    nombre_cal, emoji_cal = animales.get(num_cal, ('Desconocido', '❓'))
                    with columnas[idx]:
                        st.markdown(f"""
                            <div class='caja-resultado' style='padding: 10px;'>
                                <span class='caja-emoji' style='font-size: 2rem;'>{emoji_cal}</span>
                                <span class='caja-numero' style='font-size: 1.5rem;'>{num_cal}</span><br>
                                <span class='caja-texto' style='font-size: 0.8rem;'>{freq_cal} veces</span>
                            </div>
                        """, unsafe_allow_html=True)
                
                # --- LA SORPRESA ---
                st.markdown("<h3>🎲 LA SORPRESA (Batacazo)</h3>", unsafe_allow_html=True)
                batacazos = [num for num, freq in conteo_12.items() if freq == 1]
                
                if batacazos:
                    num_bat = batacazos[-1]
                else:
                    num_bat = conteo_12.most_common()[-1][0]
                    
                nombre_bat, emoji_bat = animales.get(num_bat, ('Desconocido', '❓'))
                
                st.markdown(f"""
                    <div class='caja-resultado' style='border-color: #ff4b4b;'>
                        <span class='caja-emoji'>{emoji_bat}</span>
                        <span class='caja-numero' style='color: #ff4b4b;'>{num_bat} - {nombre_bat}</span><br>
                        <span class='caja-texto'>Está agazapado. Ojo con este.</span>
                    </div>
                """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Error leyendo el archivo: {e}")
2
