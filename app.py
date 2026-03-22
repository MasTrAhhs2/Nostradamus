simport streamlit as st
import pandas as pd
from collections import Counter

# Configuración de página
st.set_page_config(page_title="Nostradamus", page_icon="📜", layout="centered")

# Diccionario de animales y emojis
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
    '26': ('Vaca', '🐄'), '27': ('Perro', '🐕'), '28': ('Zamuro', '🦇'),
    '29': ('Elefante', '🐘'), '30': ('Caimán', '🐊'), '31': ('Lapa', '🐗'),
    '32': ('Ardilla', '🐿️'), '33': ('Pescado', '🐟'), '34': ('Venado', '🦌'),
    '35': ('Jirafa', '🦒'), '36': ('Culebra', '🐍')
}

# CSS para el diseño premium y fondo negro
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800&display=swap');
        .stApp { background-color: #000000; color: #ffffff; font-family: 'Montserrat', sans-serif; }
        h1, h2, h3 { text-align: center; font-family: 'Montserrat', sans-serif; color: #D4AF37; }
        
        /* Cajas de inputs dobles */
        div[data-baseweb="input"] { border-radius: 10px; border: 2px solid #D4AF37; background-color: #111111; }
        div[data-baseweb="input"] input { font-size: 2rem !important; text-align: center !important; font-weight: bold; color: white; }
        
        /* Pestañas (Tabs) */
        .stTabs [data-baseweb="tab-list"] { background-color: #111111; border-radius: 10px; padding: 5px; }
        .stTabs [data-baseweb="tab"] { color: #ffffff; font-weight: bold; }
        .stTabs [aria-selected="true"] { background-color: #D4AF37 !important; color: #000000 !important; border-radius: 5px; }

        .caja-resultado { background-color: #151515; border: 1px solid #333; border-radius: 12px; padding: 15px; text-align: center; margin-bottom: 15px; box-shadow: 0px 4px 10px rgba(0,0,0,0.5); }
        .caja-numero { font-size: 1.8rem; font-weight: 800; color: #D4AF37; }
        .caja-emoji { font-size: 2.5rem; display: block; margin-bottom: 5px; }
        .caja-texto { font-size: 0.9rem; color: #aaaaaa; }
    </style>
""", unsafe_allow_html=True)

st.title("📜 NOSTRADAMUS 🔍")
st.markdown("<p style='text-align: center; color: #888;'>Panel de Control Estratégico</p>", unsafe_allow_html=True)

archivo_subido = st.file_uploader("", type=["xlsx", "csv"])

if archivo_subido is not None:
    try:
        if archivo_subido.name.endswith('.csv'):
            df = pd.read_csv(archivo_subido, header=None)
        else:
            df = pd.read_excel(archivo_subido, header=None)
            
        todos_los_datos = df[0].astype(str).str.strip().tolist()
        total_historial = len(todos_los_datos)
        
        st.success(f"✅ Data cargada: {total_historial} sorteos disponibles.")
        st.divider()
        
        # Crear las tres pestañas de navegación
        tab1, tab2, tab3 = st.tabs(["🔍 Análisis de Pares", "🚨 Radar de Atrasos", "🔥 Top 5 Calientes"])
        
        # ==========================================
        # PESTAÑA 1: ANÁLISIS DEL PAR DETONANTE
        # ==========================================
        with tab1:
            st.markdown("<h3>DETECCIÓN DE PARES</h3>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                par1 = st.text_input("Primer Número", placeholder="Ej: 1")
            with col2:
                par2 = st.text_input("Segundo Número", placeholder="Ej: 12")
                
            if par1 and par2:
                par1 = par1.strip()
                par2 = par2.strip()
                
                inmediatos = []
                siguientes_12 = []
                
                # Buscar el par en TODO el historial (para tener datos suficientes)
                for i in range(total_historial - 1):
                    if todos_los_datos[i] == par1 and todos_los_datos[i+1] == par2:
                        # Si hay un número después del par, lo guardamos
                        if i + 2 < total_historial:
                            inmediatos.append(todos_los_datos[i+2])
                            # Guardamos los siguientes 12 después del par
                            limite = min(i + 2 + 12, total_historial)
                            siguientes_12.extend(todos_los_datos[i+2 : limite])
                            
                apariciones_par = len(inmediatos)
                
                if apariciones_par == 0:
                    st.warning(f"⚠️ El par {par1} seguido del {par2} nunca ha salido en el historial.")
                else:
                    st.info(f"📊 La secuencia [{par1} ➡️ {par2}] ha salido {apariciones_par} veces en la historia.")
                    
                    # El Inmediato
                    conteo_inm = Counter(inmediatos)
                    top_inm = conteo_inm.most_common(1)[0]
                    nom_inm, emo_inm = animales.get(top_inm[0], ('?', '❓'))
                    
                    st.markdown("<h4>⚡ El Inmediato Más Probable</h4>", unsafe_allow_html=True)
                    st.markdown(f"""
                        <div class='caja-resultado'>
                            <span class='caja-emoji'>{emo_inm}</span>
                            <span class='caja-numero'>{top_inm[0]} - {nom_inm}</span><br>
                            <span class='caja-texto'>Salió {top_inm[1]} veces justo después del par.</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Los próximos 12
                    conteo_12 = Counter(siguientes_12)
                    top_12_par = conteo_12.most_common(3)
                    
                    st.markdown("<h4>🎯 Mayor Probabilidad (Próximos 12 Sorteos)</h4>", unsafe_allow_html=True)
                    c1, c2, c3 = st.columns(3)
                    cols = [c1, c2, c3]
                    for idx, (num_cal, freq_cal) in enumerate(top_12_par):
                        nom_cal, emo_cal = animales.get(num_cal, ('?', '❓'))
                        with cols[idx]:
                            st.markdown(f"""
                                <div class='caja-resultado' style='padding: 10px;'>
                                    <span class='caja-emoji' style='font-size: 2rem;'>{emo_cal}</span>
                                    <span class='caja-numero' style='font-size: 1.2rem;'>{num_cal}</span><br>
                                    <span class='caja-texto' style='font-size: 0.8rem;'>{freq_cal} veces</span>
                                </div>
                            """, unsafe_allow_html=True)

        # ==========================================
        # PESTAÑA 2: RADAR DE ATRASOS (Ausencias)
        # ==========================================
        with tab2:
            st.markdown("<h3>🚨 NÚMEROS DESAPARECIDOS</h3>", unsafe_allow_html=True)
            st.markdown("<p style='text-align:center; color:#888;'>Sorteos que han pasado sin que salga cada número.</p>", unsafe_allow_html=True)
            
            atrasos = {}
            # Buscamos de atrás hacia adelante en la lista
            for num_str in animales.keys():
                # Reversar la lista para buscar la última aparición
                try:
                    # list.index busca la primera coincidencia, así que volteamos la lista
                    lista_inversa = todos_los_datos[::-1]
                    sorteos_atras = lista_inversa.index(num_str)
                    atrasos[num_str] = sorteos_atras
                except ValueError:
                    atrasos[num_str] = total_historial # Nunca ha salido
                    
            # Ordenamos los atrasos de mayor a menor
            atrasos_ordenados = sorted(atrasos.items(), key=lambda x: x[1], reverse=True)[:5]
            
            for num_atr, sorteos in atrasos_ordenados:
                nom_atr, emo_atr = animales.get(num_atr, ('?', '❓'))
                st.markdown(f"""
                    <div class='caja-resultado' style='border-left: 5px solid #ff4b4b; text-align: left; display: flex; align-items: center;'>
                        <div style='font-size: 2.5rem; margin-right: 15px;'>{emo_atr}</div>
                        <div>
                            <span class='caja-numero' style='color: #ff4b4b;'>{num_atr} - {nom_atr}</span><br>
                            <span style='color: white; font-weight: bold;'>{sorteos} sorteos sin salir</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

        # ==========================================
        # PESTAÑA 3: LOS MÁS CALIENTES
        # ==========================================
        with tab3:
            st.markdown("<h3>🔥 TOP 5 DEL MOMENTO</h3>", unsafe_allow_html=True)
            ventana_caliente = 800
            st.markdown(f"<p style='text-align:center; color:#888;'>Los que más han salido en los últimos {ventana_caliente} sorteos.</p>", unsafe_allow_html=True)
            
            datos_recientes = todos_los_datos[-ventana_caliente:]
            conteo_general = Counter(datos_recientes)
            top_5_global = conteo_general.most_common(5)
            
            for num_glob, freq_glob in top_5_global:
                nom_glob, emo_glob = animales.get(num_glob, ('?', '❓'))
                st.markdown(f"""
                    <div class='caja-resultado' style='border-left: 5px solid #00ff00; text-align: left; display: flex; align-items: center;'>
                        <div style='font-size: 2.5rem; margin-right: 15px;'>{emo_glob}</div>
                        <div>
                            <span class='caja-numero' style='color: #00ff00;'>{num_glob} - {nom_glob}</span><br>
                            <span style='color: white;'>Ha salido <b>{freq_glob} veces</b> recientemente.</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Error procesando el archivo: {e}")
                
