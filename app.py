import streamlit as st
import pandas as pd
from collections import Counter

st.set_page_config(page_title="Nostradamus", page_icon="📜", layout="centered")

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

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800&display=swap');
        .stApp { background-color: #000000; color: #ffffff; font-family: 'Montserrat', sans-serif; }
        h1, h2, h3 { text-align: center; font-family: 'Montserrat', sans-serif; color: #D4AF37; }
        div[data-baseweb="input"] { border-radius: 10px; border: 2px solid #D4AF37; background-color: #111111; }
        div[data-baseweb="input"] input { font-size: 2rem !important; text-align: center !important; font-weight: bold; color: white; }
        .stTabs [data-baseweb="tab-list"] { background-color: #111111; border-radius: 10px; padding: 5px; }
        .stTabs [data-baseweb="tab"] { color: #ffffff; font-weight: bold; }
        .stTabs [aria-selected="true"] { background-color: #D4AF37 !important; color: #000000 !important; border-radius: 5px; }
        .caja-resultado { background-color: #151515; border: 1px solid #333; border-radius: 12px; padding: 15px; text-align: center; margin-bottom: 15px; box-shadow: 0px 4px 10px rgba(0,0,0,0.5); }
        .caja-numero { font-size: 1.8rem; font-weight: 800; color: #D4AF37; }
        .caja-emoji { font-size: 2.5rem; display: block; margin-bottom: 5px; }
        .caja-texto { font-size: 0.9rem; color: #aaaaaa; }
        
        /* Estilo especial para la alerta de Sinergia */
        .caja-sinergia {
            background: linear-gradient(45deg, #1a0000, #4d0000);
            border: 2px solid #ff4b4b;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0px 0px 15px rgba(255, 75, 75, 0.4);
        }
    </style>
""", unsafe_allow_html=True)

st.title("📜 NOSTRADAMUS 🔍")
st.markdown("<p style='text-align: center; color: #888;'>Panel de Control Estratégico (Modo Tripletas)</p>", unsafe_allow_html=True)

archivo_subido = st.file_uploader("", type=["xlsx", "csv"])

if archivo_subido is not None:
    st.markdown("<p style='text-align: center; color: #D4AF37; font-weight: bold;'>¿Dónde están los números MÁS RECIENTES en tu Excel?</p>", unsafe_allow_html=True)
    orden_datos = st.radio("", ["⬇️ Al final de la lista (Abajo)", "⬆️ Al principio de la lista (Arriba)"], horizontal=True)

    try:
        if archivo_subido.name.endswith('.csv'):
            df = pd.read_csv(archivo_subido, header=None, dtype=str)
        else:
            df = pd.read_excel(archivo_subido, header=None, dtype=str)
            
        raw_data = df[df.columns[0]].dropna().tolist()
        todos_los_datos = []
        
        for x in raw_data:
            num_str = str(x).strip()
            if num_str == '00' or num_str.startswith('00'):
                todos_los_datos.append('00')
            else:
                try:
                    val = float(num_str.replace(',', '.'))
                    todos_los_datos.append(str(int(val)))
                except ValueError:
                    todos_los_datos.append(num_str)
        
        if "Arriba" in orden_datos:
            todos_los_datos.reverse()
            
        total_historial = len(todos_los_datos)
        st.success(f"✅ Data cargada y sincronizada: {total_historial} sorteos listos.")
        st.divider()

        # ==========================================
        # CÁLCULO GLOBAL DE CALIENTES (Para la Sinergia)
        # ==========================================
        ventana_caliente = 800
        if total_historial < ventana_caliente:
            datos_recientes = todos_los_datos
        else:
            datos_recientes = todos_los_datos[-ventana_caliente:]
            
        conteo_general = Counter(datos_recientes)
        top_5_global = conteo_general.most_common(5)
        numeros_calientes_globales = [x[0] for x in top_5_global]
        
        tab1, tab2, tab3 = st.tabs(["🔍 Cacería de Tripletas", "🚨 Radar de Atrasos", "🔥 Top 5 Calientes"])
        
        with tab1:
            st.markdown("<h3>DETECCIÓN DE PARES UNIDOS</h3>", unsafe_allow_html=True)
            st.markdown("<p style='text-align:center; color:#888;'>Detecta el detonante y busca triangulación.</p>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                par1 = st.text_input("Primer Número", placeholder="Ej: 21")
            with col2:
                par2 = st.text_input("Segundo Número", placeholder="Ej: 13")
                
            if par1 and par2:
                par1 = par1.strip()
                par2 = par2.strip()
                
                inmediatos = []
                siguientes_12 = []
                
                for i in range(total_historial - 1):
                    condicion_directa = (todos_los_datos[i] == par1 and todos_los_datos[i+1] == par2)
                    condicion_inversa = (todos_los_datos[i] == par2 and todos_los_datos[i+1] == par1)
                    
                    if condicion_directa or condicion_inversa:
                        if i + 2 < total_historial:
                            inmediatos.append(todos_los_datos[i+2])
                            limite = min(i + 2 + 12, total_historial)
                            siguientes_12.extend(todos_los_datos[i+2 : limite])
                            
                apariciones_par = len(inmediatos)
                
                if apariciones_par == 0:
                    st.warning(f"⚠️ El par {par1} y {par2} nunca han salido juntos en el historial.")
                else:
                    st.info(f"📊 El detonante [{par1} ↔️ {par2}] ha estallado {apariciones_par} veces.")
                    
                    # Cálculos para la ventana de 12
                    conteo_12 = Counter(siguientes_12)
                    top_12_par = conteo_12.most_common(3)
                    numeros_top_12 = [x[0] for x in top_12_par]
                    
                    # 🔥 CRUCE DE SEÑALES (Sinergia) 🔥
                    sinergias = set(numeros_top_12).intersection(set(numeros_calientes_globales))
                    
                    if sinergias:
                        st.markdown("<div class='caja-sinergia'>", unsafe_allow_html=True)
                        st.markdown("<h3 style='color: #ff4b4b; margin-top: 0;'>🚨 ¡ALERTA DE SINERGIA! 🚨</h3>", unsafe_allow_html=True)
                        st.markdown("<p style='color: white;'>Estos animales dominan los 12 sorteos del par y TAMBIÉN son los más calientes de la temporada. <b>Bala fija para la tripleta:</b></p>", unsafe_allow_html=True)
                        
                        cols_sinergia = st.columns(len(sinergias))
                        for idx, num_sin in enumerate(sinergias):
                            nom_sin, emo_sin = animales.get(num_sin, ('?', '❓'))
                            with cols_sinergia[idx]:
                                st.markdown(f"<span style='font-size: 3rem;'>{emo_sin}</span><br><span style='font-size: 1.5rem; font-weight: bold; color: #D4AF37;'>{num_sin} - {nom_sin}</span>", unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.success("👀 No hay sinergia directa con el Top 5 Global. Guíate por la matemática pura del detonante de abajo.")

                    # Mostrar los 3 que más salen en las 12 horas
                    st.markdown("<h4>🎯 Frecuencia Pura (Próximos 12 Sorteos)</h4>", unsafe_allow_html=True)
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
                            
                    # El inmediato
                    conteo_inm = Counter(inmediatos)
                    top_inm = conteo_inm.most_common(1)[0]
                    nom_inm, emo_inm = animales.get(top_inm[0], ('?', '❓'))
                    
                    st.markdown("<h4>⚡ El Inmediato (El Gatillo Rápido)</h4>", unsafe_allow_html=True)
                    st.markdown(f"""
                        <div class='caja-resultado'>
                            <span class='caja-emoji'>{emo_inm}</span>
                            <span class='caja-numero'>{top_inm[0]} - {nom_inm}</span><br>
                            <span class='caja-texto'>Salió {top_inm[1]} veces justo después del par.</span>
                        </div>
                    """, unsafe_allow_html=True)

        with tab2:
            st.markdown("<h3>🚨 NÚMEROS DESAPARECIDOS</h3>", unsafe_allow_html=True)
            st.markdown("<p style='text-align:center; color:#888;'>Tiempo que ha pasado sin que salga cada número.</p>", unsafe_allow_html=True)
            
            sorteos_diarios = 12
            
            atrasos = {}
            lista_inversa = todos_los_datos[::-1]
            for num_str in animales.keys():
                try:
                    sorteos_atras = lista_inversa.index(num_str)
                    atrasos[num_str] = sorteos_atras
                except ValueError:
                    atrasos[num_str] = total_historial
                    
            atrasos_ordenados = sorted(atrasos.items(), key=lambda x: x[1], reverse=True)[:5]
            
            for num_atr, sorteos in atrasos_ordenados:
                dias_aprox = sorteos // sorteos_diarios
                nom_atr, emo_atr = animales.get(num_atr, ('?', '❓'))
                st.markdown(f"""
                    <div class='caja-resultado' style='border-left: 5px solid #ff4b4b; text-align: left; display: flex; align-items: center;'>
                        <div style='font-size: 2.5rem; margin-right: 15px;'>{emo_atr}</div>
                        <div>
                            <span class='caja-numero' style='color: #ff4b4b;'>{num_atr} - {nom_atr}</span><br>
                            <span style='color: white; font-weight: bold;'>{sorteos} sorteos sin salir</span><br>
                            <span style='color: #aaaaaa; font-size: 0.85rem;'>⏱️ Aprox. <b>{dias_aprox} días</b> de atraso</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

        with tab3:
            st.markdown("<h3>🔥 TOP 5 DEL MOMENTO</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:center; color:#888;'>Los que más han salido en los últimos {ventana_caliente} sorteos.</p>", unsafe_allow_html=True)
            
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
        2
