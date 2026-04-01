import streamlit as st
import pandas as pd
from collections import Counter
import itertools
import numpy as np

st.set_page_config(page_title="Nostradamus 6.0", page_icon="📜", layout="centered")

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
        div[data-baseweb="select"] { border-radius: 10px; border: 2px solid #ff4b4b; background-color: #1a0000; }
        span[data-baseweb="tag"] { background-color: #ff4b4b !important; color: white !important; font-weight: bold; font-size: 1rem; }
        .stTabs [data-baseweb="tab-list"] { background-color: #111111; border-radius: 10px; padding: 5px; overflow-x: auto; }
        .stTabs [data-baseweb="tab"] { color: #ffffff; font-weight: bold; font-size: 0.9rem; }
        .stTabs [aria-selected="true"] { background-color: #D4AF37 !important; color: #000000 !important; border-radius: 5px; }
        .caja-resultado { background-color: #151515; border: 1px solid #333; border-radius: 12px; padding: 15px; text-align: center; margin-bottom: 15px; box-shadow: 0px 4px 10px rgba(0,0,0,0.5); }
        .caja-numero { font-size: 1.8rem; font-weight: 800; color: #D4AF37; }
        .caja-emoji { font-size: 2.5rem; display: block; margin-bottom: 5px; }
        .caja-tripleta-fuego { background: linear-gradient(90deg, #2b0000, #151515); border-left: 5px solid #ff4b4b; border-radius: 10px; padding: 15px; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0px 4px 10px rgba(255,75,75,0.3); }
        .animal-tripleta { text-align: center; margin: 0 5px; }
        .stats-tripleta { text-align: right; color: #00ff00; font-weight: bold; font-size: 1.1rem; min-width: 80px;}
        .alerta-zscore { border-left: 5px solid #ff00ff !important; background: linear-gradient(90deg, #2b002b, #151515) !important; }
    </style>
""", unsafe_allow_html=True)

st.title("📜 NOSTRADAMUS 6.0 🔍")
st.markdown("<p style='text-align: center; color: #888;'>Wall Street Edition - Algoritmos Avanzados</p>", unsafe_allow_html=True)

archivo_subido = st.file_uploader("", type=["xlsx", "csv"])

if archivo_subido is not None:
    orden_datos = st.radio("Orden del Excel:", ["⬇️ Datos nuevos abajo", "⬆️ Datos nuevos arriba"], horizontal=True)

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
                    todos_los_datos.append(str(int(float(num_str.replace(',', '.')))))
                except ValueError:
                    todos_los_datos.append(num_str)
        
        if "arriba" in orden_datos.lower():
            todos_los_datos.reverse()
            
        total_historial = len(todos_los_datos)
        st.success(f"✅ Data cargada: {total_historial} sorteos procesados.")
        
        # --- MATEMÁTICA GLOBAL ---
        ventana_caliente = 800
        datos_recientes = todos_los_datos[-ventana_caliente:] if total_historial >= ventana_caliente else todos_los_datos
        conteo_general = Counter(datos_recientes)
        top_5_global = conteo_general.most_common(5)
        numeros_calientes_globales = [x[0] for x in top_5_global]

        # --- CÁLCULO Z-SCORE (Reemplazo de Atrasos simples) ---
        z_scores_list = []
        for animal in animales.keys():
            indices = [i for i, x in enumerate(todos_los_datos) if x == animal]
            if len(indices) > 2:
                gaps = np.diff(indices)
                mean_gap = np.mean(gaps)
                std_gap = np.std(gaps)
                if std_gap > 0:
                    current_gap = (total_historial - 1) - indices[-1]
                    z_score = (current_gap - mean_gap) / std_gap
                    z_scores_list.append((animal, z_score, current_gap, int(mean_gap)))
        
        z_scores_ordenados = sorted(z_scores_list, key=lambda x: x[1], reverse=True)
        numeros_frios_z = [x[0] for x in z_scores_ordenados if x[1] > 1.0] # Animales extremadamente atrasados

        # --- PESTAÑAS ---
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔍 Cacería", "🎯 Radar Z-Score", "🔥 Calientes", "⏱️ Lab VIP", "🔗 Cadena Markov"])

        # PESTAÑA 1: CACERÍA BÁSICA
        with tab1:
            st.markdown("<h3>DETECCIÓN DE PARES UNIDOS</h3>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1: par1 = st.text_input("Primer Número", placeholder="Ej: 21", key="t1_p1")
            with col2: par2 = st.text_input("Segundo Número", placeholder="Ej: 13", key="t1_p2")
            if par1 and par2:
                par1, par2 = par1.strip(), par2.strip()
                inmediatos, siguientes_12 = [], []
                for i in range(total_historial - 1):
                    if (todos_los_datos[i] == par1 and todos_los_datos[i+1] == par2) or (todos_los_datos[i] == par2 and todos_los_datos[i+1] == par1):
                        if i + 2 < total_historial:
                            inmediatos.append(todos_los_datos[i+2])
                            siguientes_12.extend(todos_los_datos[i+2 : min(i + 2 + 12, total_historial)])
                
                if inmediatos:
                    st.info(f"📊 El detonante [{par1} ↔️ {par2}] ha estallado {len(inmediatos)} veces.")
                    cols = st.columns(3)
                    for idx, (num_cal, freq_cal) in enumerate(Counter(siguientes_12).most_common(3)):
                        nom_cal, emo_cal = animales.get(num_cal, ('?', '❓'))
                        with cols[idx]:
                            st.markdown(f"<div class='caja-resultado' style='padding: 10px;'><span class='caja-emoji' style='font-size: 2rem;'>{emo_cal}</span><span class='caja-numero' style='font-size: 1.2rem;'>{num_cal}</span><br><span class='caja-texto' style='font-size: 0.8rem;'>{freq_cal} veces</span></div>", unsafe_allow_html=True)

        # PESTAÑA 2: RADAR Z-SCORE (LA OLLA DE PRESIÓN)
        with tab2:
            st.markdown("<h3>🎯 RADAR Z-SCORE (Olla de Presión)</h3>", unsafe_allow_html=True)
            st.markdown("<p style='text-align:center; color:#888;'>Animales que superaron su límite matemático de ausencia y están por reventar por ley de gravedad estadística.</p>", unsafe_allow_html=True)
            
            for animal, z, gap_actual, media in z_scores_ordenados[:5]:
                nom, emo = animales.get(animal, ('?', '❓'))
                clase_extra = "alerta-zscore" if z > 1.5 else ""
                icono_alerta = "🚨 ¡A PUNTO DE REVENTAR!" if z > 1.5 else "⏳ Calentando..."
                
                st.markdown(f"""
                    <div class='caja-resultado {clase_extra}' style='text-align: left; display: flex; align-items: center;'>
                        <div style='font-size: 2.5rem; margin-right: 15px;'>{emo}</div>
                        <div>
                            <span class='caja-numero'>{animal} - {nom}</span><br>
                            <span style='color: white; font-weight: bold;'>{icono_alerta}</span><br>
                            <span style='color: #aaaaaa; font-size: 0.85rem;'>Normalmente sale cada <b>{media}</b> sorteos. Ahorita lleva <b>{gap_actual}</b> sin salir.<br>Nivel de Tensión (Z): <b>{z:.2f}</b></span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

        # PESTAÑA 3: CALIENTES
        with tab3:
            st.markdown("<h3>🔥 TOP 5 DEL MOMENTO</h3>", unsafe_allow_html=True)
            for num_glob, freq_glob in top_5_global:
                nom_glob, emo_glob = animales.get(num_glob, ('?', '❓'))
                st.markdown(f"<div class='caja-resultado' style='border-left: 5px solid #00ff00; text-align: left; display: flex; align-items: center;'><div style='font-size: 2.5rem; margin-right: 15px;'>{emo_glob}</div><div><span class='caja-numero' style='color: #00ff00;'>{num_glob} - {nom_glob}</span><br><span style='color: white;'>Ha salido <b>{freq_glob} veces</b> recientemente.</span></div></div>", unsafe_allow_html=True)

        # PESTAÑA 4: LABORATORIO VIP MULTIPLE
        with tab4:
            st.markdown("<h3>⏱️ LAB VIP MULTIPLE</h3>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1: par1_bt = st.text_input("Detonante 1", key="t4_p1")
            with col2: par2_bt = st.text_input("Detonante 2", key="t4_p2")
            if par1_bt and par2_bt:
                par1_bt, par2_bt = par1_bt.strip(), par2_bt.strip()
                ventanas_validas = []
                for i in range(total_historial - 1):
                    if (todos_los_datos[i] == par1_bt and todos_los_datos[i+1] == par2_bt) or (todos_los_datos[i] == par2_bt and todos_los_datos[i+1] == par1_bt):
                        if i + 2 < total_historial:
                            ventanas_validas.append(todos_los_datos[i+2 : min(i + 2 + 12, total_historial)])
                
                if ventanas_validas:
                    conteo_tripletas = Counter()
                    def ordenar_animales(x): return -1 if x == '00' else int(x)
                    for ventana in ventanas_validas:
                        animales_unicos = list(set(ventana))
                        if len(animales_unicos) >= 3:
                            for combo in itertools.combinations(sorted(animales_unicos, key=ordenar_animales), 3):
                                conteo_tripletas[combo] += 1
                                
                    opciones_menu = [f"{num} - {animales.get(num, ('?','❓'))[0]} {animales.get(num, ('?','❓'))[1]}" for num in numeros_calientes_globales]
                    st.markdown("<h4 style='color: #ff4b4b;'>🔥 Arma tu Base VIP (Elige hasta 3):</h4>", unsafe_allow_html=True)
                    seleccion_usuario = st.multiselect("", opciones_menu, max_selections=3)
                    
                    if seleccion_usuario:
                        animales_base = [sel.split(" ")[0] for sel in seleccion_usuario]
                        tripletas_filtradas = [(trip, reps) for trip, reps in conteo_tripletas.items() if all(a in trip for a in animales_base) and not any(f in trip for f in numeros_frios_z)]
                        top_10 = sorted(tripletas_filtradas, key=lambda x: x[1], reverse=True)[:10]
                        
                        if top_10:
                            for idx, (trip, reps) in enumerate(top_10):
                                divs = "".join([f"<div class='animal-tripleta'><span style='font-size: 2rem;'>{animales.get(n, ('?','❓'))[1]}</span><br><b style='color: {'#ff4b4b' if n in animales_base else '#fff'};'>{n} {'🔥' if n in animales_base else ''}</b></div>" for n in trip])
                                st.markdown(f"<div class='caja-tripleta-fuego'><div style='display: flex; align-items: center;'><div style='font-size: 1.5rem; margin-right: 15px; color: #ff4b4b;'><b>#{idx+1}</b></div>{divs}</div><div class='stats-tripleta' style='color: #ff4b4b;'>🎯 {reps}x</div></div>", unsafe_allow_html=True)
                        else:
                            st.error("No hay combinaciones puras con esos filtros.")

        # PESTAÑA 5: CADENAS DE MARKOV (EL SANTO GRIAL)
        with tab5:
            st.markdown("<h3>🔗 PREDICCIÓN EN CADENA (Markov)</h3>", unsafe_allow_html=True)
            st.markdown("<p style='text-align:center; color:#888;'>Mide el efecto dominó. ¿Quién sale seguido de quién de forma exacta?</p>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1: p1_mk = st.text_input("Detonante 1", key="t5_p1")
            with col2: p2_mk = st.text_input("Detonante 2", key="t5_p2")
            
            if p1_mk and p2_mk:
                p1_mk, p2_mk = p1_mk.strip(), p2_mk.strip()
                
                # Paso 1: Buscar C (El inmediato después del par)
                paso_1 = []
                for i in range(total_historial - 2):
                    if (todos_los_datos[i] == p1_mk and todos_los_datos[i+1] == p2_mk) or (todos_los_datos[i] == p2_mk and todos_los_datos[i+1] == p1_mk):
                        paso_1.append(todos_los_datos[i+2])
                
                if not paso_1:
                    st.warning("El par no tiene suficientes datos.")
                else:
                    animal_C = Counter(paso_1).most_common(1)[0][0]
                    nom_C, emo_C = animales.get(animal_C, ('?', '❓'))
                    
                    # Paso 2: Buscar D (El inmediato después de Par[2] + C)
                    paso_2 = []
                    for i in range(total_historial - 2):
                        if (todos_los_datos[i] == p2_mk and todos_los_datos[i+1] == animal_C):
                            paso_2.append(todos_los_datos[i+2])
                            
                    animal_D = Counter(paso_2).most_common(1)[0][0] if paso_2 else '?'
                    nom_D, emo_D = animales.get(animal_D, ('?', '❓'))

                    # Paso 3: Buscar E (El inmediato después de C + D)
                    paso_3 = []
                    for i in range(total_historial - 2):
                        if (todos_los_datos[i] == animal_C and todos_los_datos[i+1] == animal_D):
                            paso_3.append(todos_los_datos[i+2])
                            
                    animal_E = Counter(paso_3).most_common(1)[0][0] if paso_3 else '?'
                    nom_E, emo_E = animales.get(animal_E, ('?', '❓'))

                    st.markdown("<h4 style='color: #D4AF37; text-align: center;'>⚡ LA TRIPLETA EN EFECTO DOMINÓ ⚡</h4>", unsafe_allow_html=True)
                    st.markdown(f"""
                        <div style='display: flex; justify-content: center; align-items: center; background-color: #111; padding: 20px; border-radius: 15px; border: 2px dashed #D4AF37;'>
                            <div class='animal-tripleta'><span style='font-size: 2.5rem;'>{emo_C}</span><br><b style='color: #fff; font-size: 1.2rem;'>{animal_C}</b></div>
                            <div style='font-size: 2rem; color: #888; margin: 0 15px;'>➡️</div>
                            <div class='animal-tripleta'><span style='font-size: 2.5rem;'>{emo_D}</span><br><b style='color: #fff; font-size: 1.2rem;'>{animal_D}</b></div>
                            <div style='font-size: 2rem; color: #888; margin: 0 15px;'>➡️</div>
                            <div class='animal-tripleta'><span style='font-size: 2.5rem;'>{emo_E}</span><br><b style='color: #fff; font-size: 1.2rem;'>{animal_E}</b></div>
                        </div>
                        <p style='text-align: center; color: #aaaaaa; margin-top: 15px; font-size: 0.9rem;'>Esta es la ruta exacta que sigue la matriz matemática cuando explota tu par. El {animal_C} llama al {animal_D}, y el {animal_D} llama al {animal_E}.</p>
                    """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Error crítico: {e}")
