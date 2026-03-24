import streamlit as st
import pandas as pd
from collections import Counter
import itertools

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
        
        /* Estilo para los Selectores Multibles */
        div[data-baseweb="select"] { border-radius: 10px; border: 2px solid #ff4b4b; background-color: #1a0000; }
        span[data-baseweb="tag"] { background-color: #ff4b4b !important; color: white !important; font-weight: bold; font-size: 1rem; }
        
        .stTabs [data-baseweb="tab-list"] { background-color: #111111; border-radius: 10px; padding: 5px; }
        .stTabs [data-baseweb="tab"] { color: #ffffff; font-weight: bold; }
        .stTabs [aria-selected="true"] { background-color: #D4AF37 !important; color: #000000 !important; border-radius: 5px; }
        .caja-resultado { background-color: #151515; border: 1px solid #333; border-radius: 12px; padding: 15px; text-align: center; margin-bottom: 15px; box-shadow: 0px 4px 10px rgba(0,0,0,0.5); }
        .caja-numero { font-size: 1.8rem; font-weight: 800; color: #D4AF37; }
        .caja-emoji { font-size: 2.5rem; display: block; margin-bottom: 5px; }
        .caja-texto { font-size: 0.9rem; color: #aaaaaa; }
        .caja-sinergia { background: linear-gradient(45deg, #1a0000, #4d0000); border: 2px solid #ff4b4b; border-radius: 12px; padding: 20px; text-align: center; margin-bottom: 20px; box-shadow: 0px 0px 15px rgba(255, 75, 75, 0.4); }
        .caja-tripleta { background: linear-gradient(90deg, #151515, #222); border-left: 5px solid #D4AF37; border-radius: 10px; padding: 15px; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0px 4px 10px rgba(0,0,0,0.5); }
        .caja-tripleta-fuego { background: linear-gradient(90deg, #2b0000, #151515); border-left: 5px solid #ff4b4b; border-radius: 10px; padding: 15px; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0px 4px 10px rgba(255,75,75,0.3); }
        .animal-tripleta { text-align: center; margin: 0 5px; }
        .stats-tripleta { text-align: right; color: #00ff00; font-weight: bold; font-size: 1.1rem; min-width: 80px;}
    </style>
""", unsafe_allow_html=True)

st.title("📜 NOSTRADAMUS 🔍")
st.markdown("<p style='text-align: center; color: #888;'>Panel de Control Estratégico</p>", unsafe_allow_html=True)

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
        # CÁLCULOS GLOBALES
        # ==========================================
        ventana_caliente = 800
        if total_historial < ventana_caliente:
            datos_recientes = todos_los_datos
        else:
            datos_recientes = todos_los_datos[-ventana_caliente:]
            
        conteo_general = Counter(datos_recientes)
        top_5_global = conteo_general.most_common(5)
        numeros_calientes_globales = [x[0] for x in top_5_global]

        atrasos_globales = {}
        lista_inversa = todos_los_datos[::-1]
        for num_str in animales.keys():
            try:
                atrasos_globales[num_str] = lista_inversa.index(num_str)
            except ValueError:
                atrasos_globales[num_str] = total_historial
                
        top_10_frios = sorted(atrasos_globales.items(), key=lambda x: x[1], reverse=True)[:10]
        numeros_frios_globales = [x[0] for x in top_10_frios]
        
        tab1, tab2, tab3, tab4 = st.tabs(["🔍 Cacería", "🚨 Atrasos", "🔥 Calientes", "⏱️ Laboratorio VIP"])
        
        # --- Pestañas 1, 2 y 3 intactas ---
        with tab1:
            st.markdown("<h3>DETECCIÓN DE PARES UNIDOS</h3>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                par1 = st.text_input("Primer Número", placeholder="Ej: 21", key="t1_p1")
            with col2:
                par2 = st.text_input("Segundo Número", placeholder="Ej: 13", key="t1_p2")
                
            if par1 and par2:
                par1 = par1.strip()
                par2 = par2.strip()
                inmediatos = []
                siguientes_12 = []
                
                for i in range(total_historial - 1):
                    if (todos_los_datos[i] == par1 and todos_los_datos[i+1] == par2) or (todos_los_datos[i] == par2 and todos_los_datos[i+1] == par1):
                        if i + 2 < total_historial:
                            inmediatos.append(todos_los_datos[i+2])
                            limite = min(i + 2 + 12, total_historial)
                            siguientes_12.extend(todos_los_datos[i+2 : limite])
                            
                if len(inmediatos) == 0:
                    st.warning(f"⚠️ El par {par1} y {par2} nunca han salido juntos.")
                else:
                    st.info(f"📊 El detonante [{par1} ↔️ {par2}] ha estallado {len(inmediatos)} veces.")
                    conteo_12 = Counter(siguientes_12)
                    top_12_par = conteo_12.most_common(3)
                    numeros_top_12 = [x[0] for x in top_12_par]
                    sinergias = set(numeros_top_12).intersection(set(numeros_calientes_globales))
                    
                    if sinergias:
                        st.markdown("<div class='caja-sinergia'><h3 style='color: #ff4b4b; margin-top: 0;'>🚨 ¡ALERTA DE SINERGIA! 🚨</h3><p style='color: white;'>Estos animales dominan los 12 sorteos del par y TAMBIÉN son los más calientes. <b>Bala fija:</b></p>", unsafe_allow_html=True)
                        cols_sinergia = st.columns(len(sinergias))
                        for idx, num_sin in enumerate(sinergias):
                            nom_sin, emo_sin = animales.get(num_sin, ('?', '❓'))
                            with cols_sinergia[idx]:
                                st.markdown(f"<span style='font-size: 3rem;'>{emo_sin}</span><br><span style='font-size: 1.5rem; font-weight: bold; color: #D4AF37;'>{num_sin} - {nom_sin}</span>", unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)

                    st.markdown("<h4>🎯 Frecuencia Pura Individual (Próximos 12)</h4>", unsafe_allow_html=True)
                    c1, c2, c3 = st.columns(3)
                    cols = [c1, c2, c3]
                    for idx, (num_cal, freq_cal) in enumerate(top_12_par):
                        nom_cal, emo_cal = animales.get(num_cal, ('?', '❓'))
                        with cols[idx]:
                            st.markdown(f"<div class='caja-resultado' style='padding: 10px;'><span class='caja-emoji' style='font-size: 2rem;'>{emo_cal}</span><span class='caja-numero' style='font-size: 1.2rem;'>{num_cal}</span><br><span class='caja-texto' style='font-size: 0.8rem;'>{freq_cal} veces</span></div>", unsafe_allow_html=True)

        with tab2:
            st.markdown("<h3>🚨 NÚMEROS DESAPARECIDOS</h3>", unsafe_allow_html=True)
            sorteos_diarios = 12
            atrasos_ordenados = sorted(atrasos_globales.items(), key=lambda x: x[1], reverse=True)[:5]
            for num_atr, sorteos in atrasos_ordenados:
                dias_aprox = sorteos // sorteos_diarios
                nom_atr, emo_atr = animales.get(num_atr, ('?', '❓'))
                st.markdown(f"<div class='caja-resultado' style='border-left: 5px solid #ff4b4b; text-align: left; display: flex; align-items: center;'><div style='font-size: 2.5rem; margin-right: 15px;'>{emo_atr}</div><div><span class='caja-numero' style='color: #ff4b4b;'>{num_atr} - {nom_atr}</span><br><span style='color: white; font-weight: bold;'>{sorteos} sorteos sin salir</span><br><span style='color: #aaaaaa; font-size: 0.85rem;'>⏱️ Aprox. <b>{dias_aprox} días</b> de atraso</span></div></div>", unsafe_allow_html=True)

        with tab3:
            st.markdown("<h3>🔥 TOP 5 DEL MOMENTO</h3>", unsafe_allow_html=True)
            for num_glob, freq_glob in top_5_global:
                nom_glob, emo_glob = animales.get(num_glob, ('?', '❓'))
                st.markdown(f"<div class='caja-resultado' style='border-left: 5px solid #00ff00; text-align: left; display: flex; align-items: center;'><div style='font-size: 2.5rem; margin-right: 15px;'>{emo_glob}</div><div><span class='caja-numero' style='color: #00ff00;'>{num_glob} - {nom_glob}</span><br><span style='color: white;'>Ha salido <b>{freq_glob} veces</b> recientemente.</span></div></div>", unsafe_allow_html=True)

        # ==========================================
        # PESTAÑA 4: LABORATORIO VIP MULTIPLE
        # ==========================================
        with tab4:
            st.markdown("<h3>⏱️ LABORATORIO VIP DE TRIPLETAS</h3>", unsafe_allow_html=True)
            st.markdown("<p style='text-align:center; color:#888;'>Caza las combinaciones de oro. Elige hasta 3 animales calientes para armar tu base y filtra la historia pura.</p>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                par1_bt = st.text_input("Detonante 1", placeholder="Ej: 5", key="t4_p1")
            with col2:
                par2_bt = st.text_input("Detonante 2", placeholder="Ej: 36", key="t4_p2")
                
            if par1_bt and par2_bt:
                par1_bt = par1_bt.strip()
                par2_bt = par2_bt.strip()
                
                ventanas_validas = []
                for i in range(total_historial - 1):
                    if (todos_los_datos[i] == par1_bt and todos_los_datos[i+1] == par2_bt) or (todos_los_datos[i] == par2_bt and todos_los_datos[i+1] == par1_bt):
                        if i + 2 < total_historial:
                            limite = min(i + 2 + 12, total_historial)
                            ventanas_validas.append(todos_los_datos[i+2 : limite])
                
                if not ventanas_validas:
                    st.warning("⚠️ Este par no tiene historial suficiente.")
                else:
                    conteo_tripletas = Counter()
                    def ordenar_animales(x):
                        return -1 if x == '00' else int(x)

                    for ventana in ventanas_validas:
                        animales_unicos = list(set(ventana))
                        if len(animales_unicos) >= 3:
                            combos_de_3 = list(itertools.combinations(sorted(animales_unicos, key=ordenar_animales), 3))
                            for combo in combos_de_3:
                                conteo_tripletas[combo] += 1
                                
                    if not conteo_tripletas:
                        st.warning("No se lograron formar tripletas completas.")
                    else:
                        st.divider()
                        
                        # --- MULTI-SELECTOR VIP DE ANIMALES CALIENTES ---
                        opciones_menu = []
                        for num_cal in numeros_calientes_globales:
                            nombre, emoji = animales.get(num_cal, ('?', '❓'))
                            opciones_menu.append(f"{num_cal} - {nombre} {emoji}")
                            
                        st.markdown("<h4 style='color: #ff4b4b;'>🔥 Arma tu Base VIP (Elige 1, 2 o 3 calientes):</h4>", unsafe_allow_html=True)
                        seleccion_usuario = st.multiselect(
                            "Toca aquí y escoge tus animales favoritos del Top 5:",
                            opciones_menu,
                            max_selections=3  # Bloqueamos en 3 porque una tripleta solo aguanta 3
                        )
                        
                        if not seleccion_usuario:
                            st.info("👆 Agrega al menos un animal caliente en la caja de arriba para empezar a buscar las tripletas doradas.")
                        else:
                            # Extraemos solo los números de lo que seleccionaste
                            animales_base_elegidos = [sel.split(" ")[0] for sel in seleccion_usuario]
                            
                            # --- FILTRADO EN TIEMPO REAL MULTIPLE ---
                            tripletas_filtradas = []
                            for tripleta, reps in conteo_tripletas.items():
                                # Verificamos si TODOS los animales que elegiste están metidos en esa tripleta
                                tiene_los_elegidos = all(animal in tripleta for animal in animales_base_elegidos)
                                tiene_frio = any(num in numeros_frios_globales for num in tripleta)
                                
                                # Regla de oro: Tiene que tener la base completa y NADA de muertos
                                if tiene_los_elegidos and not tiene_frio:
                                    tripletas_filtradas.append((tripleta, reps))
                                    
                            top_10_filtrado = sorted(tripletas_filtradas, key=lambda x: x[1], reverse=True)[:10]
                            
                            def formato_animal(num):
                                _, emoji = animales.get(num, ('?', '❓'))
                                es_base = num in animales_base_elegidos
                                color = "#ff4b4b" if es_base else "#ffffff"
                                icono = "🔥" if es_base else "" 
                                return f"<div class='animal-tripleta'><span style='font-size: 2rem;'>{emoji}</span><br><b style='color: {color};'>{num} {icono}</b></div>"

                            # Títulos dinámicos dependiendo de cuántos metiste
                            if len(animales_base_elegidos) == 1:
                                msj = f"Tripletas purificadas que contienen al firme: {animales_base_elegidos[0]}"
                            elif len(animales_base_elegidos) == 2:
                                msj = f"Tripletas purificadas que amarran el súper par: {animales_base_elegidos[0]} y {animales_base_elegidos[1]}"
                            else:
                                msj = f"¿Habrá salido la tripleta perfecta de fuego puro? {animales_base_elegidos[0]} - {animales_base_elegidos[1]} - {animales_base_elegidos[2]}"

                            st.markdown(f"<h4 style='color: #ff4b4b; margin-top: 20px;'>🏆 TOP 10 EXCLUSIVO DE TU BASE</h4>", unsafe_allow_html=True)
                            st.markdown(f"<p style='color: #aaaaaa; font-size: 0.85rem;'>{msj}</p>", unsafe_allow_html=True)
                            
                            if not top_10_filtrado:
                                st.error(f"❌ Mano, la estadística es fría: esa combinación exacta no ha reventado nunca sin números atrasados estorbando. Intenta quitar un animal o armar otro combo en el buscador de arriba.")
                            else:
                                for idx, (tripleta, repeticiones) in enumerate(top_10_filtrado):
                                    n1, n2, n3 = tripleta
                                    st.markdown(f"""
                                        <div class='caja-tripleta-fuego'>
                                            <div style='display: flex; align-items: center;'>
                                                <div style='font-size: 1.5rem; margin-right: 15px; color: #ff4b4b;'><b>#{idx+1}</b></div>
                                                {formato_animal(n1)}
                                                {formato_animal(n2)}
                                                {formato_animal(n3)}
                                            </div>
                                            <div class='stats-tripleta' style='color: #ff4b4b;'>
                                                🎯 {repeticiones}x
                                            </div>
                                        </div>
                                    """, unsafe_allow_html=True)

                        # Histórico plegable
                        with st.expander("Ver Top 10 Histórico General (Sin Filtros)"):
                            top_10_historico = conteo_tripletas.most_common(10)
                            for idx, (tripleta, repeticiones) in enumerate(top_10_historico):
                                n1, n2, n3 = tripleta
                                _, e1 = animales.get(n1, ('?', '❓'))
                                _, e2 = animales.get(n2, ('?', '❓'))
                                _, e3 = animales.get(n3, ('?', '❓'))
                                st.markdown(f"<div class='caja-tripleta'><div style='display: flex; align-items: center;'><div style='font-size: 1.5rem; margin-right: 15px; color: #D4AF37;'><b>#{idx+1}</b></div><div class='animal-tripleta'><span style='font-size: 2rem;'>{e1}</span><br><b>{n1}</b></div><div class='animal-tripleta'><span style='font-size: 2rem;'>{e2}</span><br><b>{n2}</b></div><div class='animal-tripleta'><span style='font-size: 2rem;'>{e3}</span><br><b>{n3}</b></div></div><div class='stats-tripleta'>🎯 {repeticiones}x</div></div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Error procesando el archivo: {e}")
