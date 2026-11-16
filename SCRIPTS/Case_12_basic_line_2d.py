import os
import sys
import time
import openmc
from datetime import datetime

print("[INFO] Cargando motor OpenMC de alta fidelidad - Ensayo 12 Unificado (Multilibrería)...")
print("[CONFIG] Modelo industrial compacto: 50 millones de partículas por librería / Manto 150 cm.")

# 1. RUTAS DE LIBRERÍAS BLINDADAS
# Ajustar a las rutas locales de las librerías HDF5 procesadas para OpenMC
ruta_base_fendl = "/run/media/tato/unadetres/e-lab/2ª PARTE GenTechnionB/Librerias FENDL 3-ENDF B8/fendl32/fendl-3.2-hdf5/cross_sections.xml"
ruta_base_endf = "/run/media/tato/unadetres/e-lab/2ª PARTE GenTechnionB/Librerias FENDL 3-ENDF B8/ENDF-B VIII.0 - endfb80-lowtemp/endfb80-lowtemp/cross_sections.xml"

if not os.path.exists(ruta_base_fendl):
    print(f"\n[ERROR] No se detecta la ruta de secciones eficaces: {ruta_base_fendl}")
    sys.exit(1)

# Inicialización de librería base para expansión isotópica de elementos
openmc.config['cross_sections'] = ruta_base_fendl

librerias = {
    "FENDL-3.2": ruta_base_fendl,
    "ENDF-B-VIII.0": ruta_base_endf
}

carpeta_resultados = "/run/media/tato/unadetres/e-lab/2ª PARTE GenTechnionB/Resultados"
os.makedirs(carpeta_resultados, exist_ok=True)

# Variables de Control - Geometría Ensayo 12
pct_li6 = 90.0
pct_li7 = 10.0
espesor_pared = 1.0
grosor_tapas = 50.0
radio_exterior_manto = 150.0

# 2. MATERIALES
lipb = openmc.Material(name='LiPb')
lipb.add_nuclide('Li6', pct_li6, 'ao')
lipb.add_nuclide('Li7', pct_li7, 'ao')
lipb.add_element('Pb', 83.0)
lipb.set_density('g/cm3', 9.0)

lead = openmc.Material(name='Lead')
lead.add_element('Pb', 1.0)
lead.set_density('g/cm3', 11.34)

iron = openmc.Material(name='Iron')
iron.add_element('Fe', 1.0)
iron.set_density('g/cm3', 7.87)

mats = openmc.Materials([lipb, lead, iron])
mats.export_to_xml()

# 3. GEOMETRÍA COMPACTA OPTIMIZADA (CSG)
r0 = 50.0
r1 = 51.0
r2 = 130.0
r3 = radio_exterior_manto  # 150.0 cm
r4 = 190.0
r5 = 220.0
z_h = 300.0

surf_r0 = openmc.ZCylinder(r=r0)
surf_r1 = openmc.ZCylinder(r=r1)
surf_r2 = openmc.ZCylinder(r=r2)
surf_r3 = openmc.ZCylinder(r=r3)
surf_r4 = openmc.ZCylinder(r=r4)
surf_r5 = openmc.ZCylinder(r=r5, boundary_type='vacuum')

surf_z_pos = openmc.ZPlane(z0=z_h)
surf_z_neg = openmc.ZPlane(z0=-z_h)
surf_cap_pos = openmc.ZPlane(z0=z_h + grosor_tapas, boundary_type='vacuum')
surf_cap_neg = openmc.ZPlane(z0=-(z_h + grosor_tapas), boundary_type='vacuum')

universe = openmc.Universe(cells=[
    openmc.Cell(region=-surf_r0 & -surf_z_pos & +surf_z_neg),
    openmc.Cell(region=+surf_r0 & -surf_r1 & -surf_z_pos & +surf_z_neg, fill=iron),
    openmc.Cell(region=+surf_r1 & -surf_r2 & -surf_z_pos & +surf_z_neg, fill=lead),
    openmc.Cell(region=+surf_r2 & -surf_r3 & -surf_z_pos & +surf_z_neg, fill=lipb),
    openmc.Cell(region=+surf_r3 & -surf_r4 & -surf_z_pos & +surf_z_neg, fill=iron),
    openmc.Cell(region=+surf_r4 & -surf_r5 & -surf_z_pos & +surf_z_neg, fill=lead),
    openmc.Cell(region=-surf_r5 & +surf_z_pos & -surf_cap_pos, fill=lipb),
    openmc.Cell(region=-surf_r5 & -surf_z_neg & +surf_cap_neg, fill=lipb)
])

geometry = openmc.Geometry(universe)
geometry.export_to_xml()

# 4. CONFIGURACIÓN DEL ENSAYO INDUSTRIAL (714,285 neutrones x 70 lotes = ~50M historias/librería)
settings = openmc.Settings()
settings.run_mode = 'fixed source'
settings.particles = 714285
settings.batches = 70
settings.inactive = 0
settings.max_lost_particles = 2000
settings.verbosity = 7

source = openmc.IndependentSource()
source.space = openmc.stats.Point((0, 0, 0))
source.energy = openmc.stats.Discrete([14.1e6], [1.0])
settings.source = source
settings.export_to_xml()

# 5. TALLIES UNIFICADOS: TBR (n,Xt) y Multiplicación en Plomo (n,2n)
tallies = openmc.Tallies()

tbr_tally = openmc.Tally(name='TBR_Global')
tbr_tally.scores = ['(n,Xt)']
tallies.append(tbr_tally)

n2n_tally = openmc.Tally(name='Multiplicacion_Pb')
n2n_tally.filters = [openmc.MaterialFilter([lead, lipb])]
n2n_tally.scores = ['(n,2n)']
tallies.append(n2n_tally)

tallies.export_to_xml()

# 6. EJECUCIÓN MULTILIBRERÍA Y EXPORTACIÓN DE REPORTE
archivos_salida = [
    "12_resultado_industrial_compacto.txt",
    os.path.join(carpeta_resultados, "12_resultado_industrial_compacto.txt")
]
ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for ruta_rep in archivos_salida:
    with open(ruta_rep, "w") as f:
        f.write("=========================================================================\n")
        f.write(" REPORTE AUTOMÁTICO DE ENSAYO NEUTRÓNICO INDUSTRIAL COMPACTO (ENSAYO 12)\n")
        f.write(f" Fecha/Hora de inicio: {ahora}\n")
        f.write(f" Configuración: Li6 al {pct_li6}% | Radio Manto: {radio_exterior_manto} cm | Tapas: {grosor_tapas} cm\n")
        f.write(" Estadística: 50,000,000 Partículas por librería (70 lotes x 714,285)\n")
        f.write("=========================================================================\n")

for nombre_lib, ruta_xs in librerias.items():
    print(f"\n-------------------------------------------------------------------------")
    print(f" >>> EJECUTANDO ENSAYO 12 COMPACTO CON LIBRERÍA: {nombre_lib}")
    print(f"-------------------------------------------------------------------------")

    for archivo_viejo in ['summary.h5', 'tallies.out', 'statepoint.70.h5']:
        if os.path.exists(archivo_viejo):
            os.remove(archivo_viejo)

    openmc.config['cross_sections'] = ruta_xs
    t0 = time.time()
    openmc.run()
    t1 = time.time()

    sp = openmc.StatePoint('statepoint.70.h5')
    tbr_media = sp.get_tally(name='TBR_Global').mean.flatten()[0]
    tbr_std = sp.get_tally(name='TBR_Global').std_dev.flatten()[0]

    n2n_media = sp.get_tally(name='Multiplicacion_Pb').mean.flatten()[0]
    n2n_std = sp.get_tally(name='Multiplicacion_Pb').std_dev.flatten()[0]

    leakage_data = sp.global_tallies[sp.global_tallies['name'] == b'leakage']
    leak_media = leakage_data['mean'][0]
    leak_std = leakage_data['std_dev'][0]

    bloque_res = (
        f"\n ---> LIBRERÍA: [{nombre_lib}] (Tiempo: {t1 - t0:.2f} s)\n"
        f" -> TBR Global (n,Xt):              {tbr_media:.5f} +/- {tbr_std:.5f}\n"
        f" -> Multiplicación Pb Global (n,2n):{n2n_media:.5f} +/- {n2n_std:.5f}\n"
        f" -> Fracción de Fuga (Leakage):     {leak_media:.5f} +/- {leak_std:.5f}\n"
        f"-------------------------------------------------------------------------\n"
    )
    print(bloque_res)
    for ruta_rep in archivos_salida:
        with open(ruta_rep, "a") as f:
            f.write(bloque_res)

print("\n[ÉXITO] Ensayo 12 Unificado finalizado.\n")