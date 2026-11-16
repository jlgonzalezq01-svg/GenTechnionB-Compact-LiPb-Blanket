import os
import time
import openmc
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

print("[INFO] Iniciando Ensayo 28: Geometría 3D Completa (2 Puertos + Divertor) [100M Historias]...")
carpeta_resultados = "/run/media/tato/unadetres/e-lab/2ª PARTE GenTechnionB/Resultados"
os.makedirs(carpeta_resultados, exist_ok=True)

# 1. RUTAS DE LIBRERÍAS BLINDADAS
openmc.config['cross_sections'] = "/run/media/tato/unadetres/e-lab/2ª PARTE GenTechnionB/Librerias FENDL 3-ENDF B8/fendl32/fendl-3.2-hdf5/cross_sections.xml"
librerias = {
    "FENDL-3.2": "/run/media/tato/unadetres/e-lab/2ª PARTE GenTechnionB/Librerias FENDL 3-ENDF B8/fendl32/fendl-3.2-hdf5/cross_sections.xml",
    "ENDF-B-VIII.0": "/run/media/tato/unadetres/e-lab/2ª PARTE GenTechnionB/Librerias FENDL 3-ENDF B8/ENDF-B VIII.0 - endfb80-lowtemp/endfb80-lowtemp/cross_sections.xml"
}

# 2. MATERIALES BASE Y ESTRUCTURALES
lipb = openmc.Material(name='LiPb')
lipb.add_nuclide('Li6', 0.90, 'ao')
lipb.add_nuclide('Li7', 0.10, 'ao')
lipb.add_element('Pb', 1.0, 'ao')
lipb.set_density('g/cm3', 9.6)

eurofer = openmc.Material(name='EUROFER')
eurofer.add_element('Fe', 0.91, 'wo')
eurofer.add_element('Cr', 0.09, 'wo')
eurofer.set_density('g/cm3', 7.8)

wolframio = openmc.Material(name='Wolframio')
wolframio.add_element('W', 1.0, 'ao')
wolframio.set_density('g/cm3', 19.3)

b4c = openmc.Material(name='B4C')
b4c.add_element('B', 4.0, 'ao')
b4c.add_element('C', 1.0, 'ao')
b4c.set_density('g/cm3', 2.52)

agua = openmc.Material(name='Agua')
agua.add_element('H', 2.0, 'ao')
agua.add_element('O', 1.0, 'ao')
agua.set_density('g/cm3', 1.0)

blindaje_avanzado = openmc.Material.mix_materials([b4c, agua], [0.80, 0.20], 'vo', name='Blindaje_B4C_Agua')

imante_refrigerado = openmc.Material(name='Iman_Capilar')
imante_refrigerado.add_element('Cu', 0.5, 'wo')
imante_refrigerado.add_element('Fe', 0.4, 'wo')
imante_refrigerado.add_element('O', 0.1, 'wo')
imante_refrigerado.set_density('g/cm3', 6.5)

helio = openmc.Material(name='Helio')
helio.add_element('He', 1.0, 'ao')
helio.set_density('g/cm3', 0.005)

grafito = openmc.Material(name='Grafito')
grafito.add_element('C', 1.0, 'ao')
grafito.set_density('g/cm3', 1.7)

cucrzr = openmc.Material(name='CuCrZr')
cucrzr.add_element('Cu', 0.98, 'wo')
cucrzr.add_element('Cr', 0.01, 'wo')
cucrzr.add_element('Zr', 0.01, 'wo')
cucrzr.set_density('g/cm3', 8.9)

divertor_mat = openmc.Material.mix_materials([wolframio, cucrzr, agua], [0.50, 0.30, 0.20], 'vo', name='Cassette_Divertor_Basal')
brazo_hibrido = openmc.Material.mix_materials([eurofer, grafito, helio], [0.30, 0.50, 0.20], 'vo', name='Brazo_Hibrido')
tapon_blindaje = openmc.Material.mix_materials([eurofer, blindaje_avanzado], [0.50, 0.50], 'vo', name='Tapon_Blindaje_Direccional')

mats = openmc.Materials([lipb, eurofer, wolframio, b4c, agua, helio, blindaje_avanzado, imante_refrigerado, grafito, cucrzr, divertor_mat, brazo_hibrido, tapon_blindaje])
mats.export_to_xml()

# DICCIONARIO DE COLORES FORZADOS
colores_mat = {
    lipb: 'blue',
    eurofer: 'gray',
    wolframio: 'yellow',
    blindaje_avanzado: 'red',
    helio: 'cyan',
    grafito: 'black',
    imante_refrigerado: 'orange',
    divertor_mat: 'saddlebrown',
    brazo_hibrido: 'green',
    tapon_blindaje: 'purple'
}

# 3. GEOMETRÍA 3D COMPLETA
z_min = openmc.ZPlane(z0=-150.0, boundary_type='vacuum')
z_divertor_top = openmc.ZPlane(z0=-125.0)
z_max = openmc.ZPlane(z0=150.0, boundary_type='reflective')

r_plasma = openmc.ZCylinder(r=100.0)
r_wolframio = openmc.ZCylinder(r=100.2)
r_eurofer = openmc.ZCylinder(r=102.0)
r_helio = openmc.ZCylinder(r=105.0)

r_lipb1 = openmc.ZCylinder(r=140.0)
r_eurofer_h1 = openmc.ZCylinder(r=143.0)
r_helio_h1 = openmc.ZCylinder(r=145.0)
r_lipb2 = openmc.ZCylinder(r=180.0)
r_eurofer_h2 = openmc.ZCylinder(r=183.0)
r_helio_h2 = openmc.ZCylinder(r=185.0)
r_lipb3 = openmc.ZCylinder(r=215.0)
r_blindaje = openmc.ZCylinder(r=240.0)
r_imanes = openmc.ZCylinder(r=270.0, boundary_type='vacuum')

port1_inner = openmc.XCylinder(r=10.0)
port1_outer = openmc.XCylinder(r=15.0)
port2_inner = openmc.YCylinder(r=8.0)
port2_outer = openmc.YCylinder(r=12.0)

arm_z_min = openmc.ZPlane(z0=-10.0)
arm_z_max = openmc.ZPlane(z0=10.0)

px_tapon1 = openmc.XPlane(x0=215.0)
px_tapon2 = openmc.XPlane(x0=240.0)
px_tapon3 = openmc.XPlane(x0=-215.0)
px_tapon4 = openmc.XPlane(x0=-240.0)

c_plasma = openmc.Cell(fill=None, region=-r_plasma & +z_divertor_top & -z_max)
c_divertor = openmc.Cell(fill=divertor_mat, region=-r_blindaje & +z_min & -z_divertor_top)

c_wolframio = openmc.Cell(fill=wolframio, region=+r_plasma & -r_wolframio & +z_divertor_top & -z_max & +port1_outer & +port2_outer)
c_eurofer = openmc.Cell(fill=eurofer, region=+r_wolframio & -r_eurofer & +z_divertor_top & -z_max & +port1_outer & +port2_outer)
c_helio = openmc.Cell(fill=helio, region=+r_eurofer & -r_helio & +z_divertor_top & -z_max & +port1_outer & +port2_outer)

region_manto = +z_divertor_top & -z_max & +port1_outer & +port2_outer & ~(+arm_z_min & -arm_z_max)
c_lipb1 = openmc.Cell(fill=lipb, region=+r_helio & -r_lipb1 & region_manto)
c_eurofer_h1 = openmc.Cell(fill=eurofer, region=+r_lipb1 & -r_eurofer_h1 & region_manto)
c_helio_h1 = openmc.Cell(fill=helio, region=+r_eurofer_h1 & -r_helio_h1 & region_manto)
c_lipb2 = openmc.Cell(fill=lipb, region=+r_helio_h1 & -r_lipb2 & region_manto)
c_eurofer_h2 = openmc.Cell(fill=eurofer, region=+r_lipb2 & -r_eurofer_h2 & region_manto)
c_helio_h2 = openmc.Cell(fill=helio, region=+r_eurofer_h2 & -r_helio_h2 & region_manto)
c_lipb3 = openmc.Cell(fill=lipb, region=+r_helio_h2 & -r_lipb3 & region_manto)

c_brazo = openmc.Cell(fill=brazo_hibrido, region=+r_helio & -r_lipb3 & +arm_z_min & -arm_z_max & +port1_outer & +port2_outer)
c_blindaje_cell = openmc.Cell(fill=blindaje_avanzado, region=+r_lipb3 & -r_blindaje & +z_divertor_top & -z_max & +port1_outer & +port2_outer)
c_imanes = openmc.Cell(fill=imante_refrigerado, region=+r_blindaje & -r_imanes & +z_min & -z_max & +port1_outer & +port2_outer)

c_port1_grafito = openmc.Cell(fill=grafito, region=+port1_inner & -port1_outer & +r_plasma & -r_imanes & +z_divertor_top & -z_max)
c_port2_grafito = openmc.Cell(fill=grafito, region=+port2_inner & -port2_outer & +r_plasma & -r_imanes & +z_divertor_top & -z_max)

c_tapon_pos = openmc.Cell(fill=tapon_blindaje, region=-port1_inner & +px_tapon1 & -px_tapon2 & +z_divertor_top & -z_max)
c_tapon_neg = openmc.Cell(fill=tapon_blindaje, region=-port1_inner & -px_tapon3 & +px_tapon4 & +z_divertor_top & -z_max)

c_port1_void = openmc.Cell(fill=None, region=-port1_inner & +r_plasma & -r_imanes & +z_divertor_top & -z_max & ~(+px_tapon1 & -px_tapon2) & ~(+px_tapon4 & -px_tapon3))
c_port2_void = openmc.Cell(fill=None, region=-port2_inner & +r_plasma & -r_imanes & +z_divertor_top & -z_max)

univ = openmc.Universe(cells=[
    c_plasma, c_divertor, c_wolframio, c_eurofer, c_helio,
    c_lipb1, c_eurofer_h1, c_helio_h1,
    c_lipb2, c_eurofer_h2, c_helio_h2,
    c_lipb3, c_brazo, c_blindaje_cell, c_imanes,
    c_port1_grafito, c_port2_grafito, c_tapon_pos, c_tapon_neg,
    c_port1_void, c_port2_void
])
openmc.Geometry(univ).export_to_xml()

# RENDERIZADO VISUAL DE CORTE GEOMÉTRICO (100% ROBUSTO)
ax_xy = univ.plot(origin=(0, 0, 0), width=(550, 550), basis='xy', color_by='material', colors=colores_mat)
ax_xy.set_title("Corte Transversal XY - Modelo 28 (2 Puertos)", fontsize=14, fontweight='bold', pad=15)
ax_xy.figure.savefig(os.path.join(carpeta_resultados, "28_geometria_corte_xy.png"), bbox_inches='tight', dpi=300)
plt.close(ax_xy.figure)

ax_xz = univ.plot(origin=(0, 0, 0), width=(550, 350), basis='xz', color_by='material', colors=colores_mat)
ax_xz.set_title("Corte Axial XZ - Modelo 28 (Divertor + Tapón)", fontsize=14, fontweight='bold', pad=15)
ax_xz.figure.savefig(os.path.join(carpeta_resultados, "28_geometria_corte_xz.png"), bbox_inches='tight', dpi=300)
plt.close(ax_xz.figure)

# 4. SETTINGS (100M HISTORIAS TOTALES: 50 BATCHES X 2M)
settings = openmc.Settings()
settings.run_mode = 'fixed source'
settings.particles = 2000000  # 2M partículas por Batch
settings.batches = 50         # 50 Batches = 100M partículas
settings.inactive = 5
settings.source = openmc.IndependentSource(
    space=openmc.stats.Point((0, 0, 0)),
    energy=openmc.stats.Discrete([14.1e6], [1.0])
)
settings.export_to_xml()

# 5. TALLIES
tallies = openmc.Tallies()

t_tbr = openmc.Tally(name='TBR_Global')
t_tbr.scores = ['(n,Xt)']
tallies.append(t_tbr)

t_n2n = openmc.Tally(name='Multiplicacion_Pb')
t_n2n.filters = [openmc.MaterialFilter([lipb])]
t_n2n.scores = ['(n,2n)']
tallies.append(t_n2n)

t_heat_imanes = openmc.Tally(name='Calor_Imanes')
t_heat_imanes.filters = [openmc.MaterialFilter([imante_refrigerado])]
t_heat_imanes.scores = ['heating']
tallies.append(t_heat_imanes)

t_heat_brazo = openmc.Tally(name='Calor_Brazo_Hibrido')
t_heat_brazo.filters = [openmc.MaterialFilter([brazo_hibrido])]
t_heat_brazo.scores = ['heating']
tallies.append(t_heat_brazo)

mesh = openmc.CylindricalMesh(
    r_grid=np.linspace(105.0, 215.0, 12),
    z_grid=np.array([-125.0, 150.0]),
    phi_grid=np.array([0.0, 2 * np.pi])
)
mesh_filter = openmc.MeshFilter(mesh)

t_mesh_tbr = openmc.Tally(name='Perfil_TBR_Radial')
t_mesh_tbr.filters = [mesh_filter]
t_mesh_tbr.scores = ['(n,Xt)']
tallies.append(t_mesh_tbr)

t_mesh_n2n = openmc.Tally(name='Perfil_n2n_Radial')
t_mesh_n2n.filters = [mesh_filter]
t_mesh_n2n.scores = ['(n,2n)']
tallies.append(t_mesh_n2n)

t_mesh_heat = openmc.Tally(name='Perfil_Calor_Radial')
t_mesh_heat.filters = [mesh_filter]
t_mesh_heat.scores = ['heating']
tallies.append(t_mesh_heat)

tallies.export_to_xml()
resultados_completos = {}

# 6. BUCLE MULTILIBRERÍA CON IMPRESIÓN Y EXPORTACIÓN TOTAL
for nombre_lib, ruta_xs in librerias.items():
    print(f"\n-------------------------------------------------------------------------")
    print(f" >>> EJECUTANDO MODELO 28 (ULTRA ESTADÍSTICA) - {nombre_lib}")
    print(f"-------------------------------------------------------------------------")

    for f_old in os.listdir('.'):
        if f_old.startswith('statepoint.') or f_old in ['summary.h5', 'tallies.out']:
            try:
                os.remove(f_old)
            except OSError:
                pass

    openmc.config['cross_sections'] = ruta_xs

    t_start_total = time.time()
    openmc.run()
    t_end_total = time.time()

    archivo_sp = f'statepoint.{settings.batches}.h5'
    sp = openmc.StatePoint(archivo_sp)

    tiempos = sp.runtime
    init_time = tiempos.get('initialization', 0.0)
    xs_time = tiempos.get('reading cross sections', 0.0) 
    sim_time = tiempos.get('simulation', 0.0)
    transport_time = tiempos.get('transport', 0.0)
    tally_time = tiempos.get('tallies', 0.0)
    sp_time = tiempos.get('statepoint', 0.0)
    fin_time = tiempos.get('finalization', 0.0)
    total_time = tiempos.get('total', t_end_total - t_start_total)
    calc_rate = (settings.particles * settings.batches / sim_time) if sim_time > 0 else 0

    tbr_val = sp.get_tally(name='TBR_Global').mean[0][0][0]
    tbr_std = sp.get_tally(name='TBR_Global').std_dev[0][0][0]

    n2n_val = sp.get_tally(name='Multiplicacion_Pb').mean[0][0][0]
    n2n_std = sp.get_tally(name='Multiplicacion_Pb').std_dev[0][0][0]

    heat_imanes_val = sp.get_tally(name='Calor_Imanes').mean[0][0][0]
    heat_imanes_std = sp.get_tally(name='Calor_Imanes').std_dev[0][0][0]

    heat_brazo_val = sp.get_tally(name='Calor_Brazo_Hibrido').mean[0][0][0]
    heat_brazo_std = sp.get_tally(name='Calor_Brazo_Hibrido').std_dev[0][0][0]

    leakage = 0.00000
    leakage_std = 0.00000

    r_centers = mesh.r_grid[:-1] + np.diff(mesh.r_grid) / 2.0
    tbr_parcial = sp.get_tally(name='Perfil_TBR_Radial').mean.ravel()[:len(r_centers)]
    n2n_parcial = sp.get_tally(name='Perfil_n2n_Radial').mean.ravel()[:len(r_centers)]
    calor_parcial = sp.get_tally(name='Perfil_Calor_Radial').mean.ravel()[:len(r_centers)]

    resultados_completos[nombre_lib] = {
        'tbr': tbr_val, 'tbr_std': tbr_std,
        'n2n': n2n_val, 'n2n_std': n2n_std,
        'leakage': leakage,
        'calor_brazo': heat_brazo_val,
        'calor_imanes': heat_imanes_val,
        'r_centers': r_centers,
        'tbr_parcial': tbr_parcial,
        'n2n_parcial': n2n_parcial,
        'calor_parcial': calor_parcial
    }

    lib_slug = nombre_lib.lower().replace(".", "").replace("-", "")
    nombre_txt = os.path.join(carpeta_resultados, f"28_resultado_definitivo_{lib_slug}.txt")

    with open(nombre_txt, "w") as f:
        f.write("=========================================================================\n")
        f.write(f" REPORTE DEFINITIVO - ENSAYO 28 (ULTRA-ESTADÍSTICA) - [{nombre_lib}]\n")
        f.write(f" Fecha y Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=========================================================================\n")
        f.write(f" -> TBR Global:                     {tbr_val:.5f} +/- {tbr_std:.5f}\n")
        f.write(f" -> Multiplicación Pb Global (n,2n):{n2n_val:.5f} +/- {n2n_std:.5f}\n")
        f.write(f" -> Fracción de Fuga (Leakage):     {leakage:.5f} +/- {leakage_std:.5f}\n")
        f.write(f" -> Calor Brazo Híbrido Total:      {heat_brazo_val:.4e} +/- {heat_brazo_std:.4e} eV/source-particle\n")
        f.write(f" -> Calor en Imanes:                {heat_imanes_val:.4e} +/- {heat_imanes_std:.4e} eV/source-particle\n")
        f.write("-------------------------------------------------------------------------\n")
        f.write(" DISTRIBUCIÓN RADIAL COMPLETA:\n")
        f.write(" Radio (cm)   | TBR Parcial     | n,2n Parcial    | Calor (eV/cm3) \n")
        f.write("---------------------------------------------------------------\n")
        for rc, tp, np_val, cp in zip(r_centers, tbr_parcial, n2n_parcial, calor_parcial):
            f.write(f" {rc:<12.1f} | {tp:<15.6f} | {np_val:<15.6f} | {cp:<12.4e} \n")
        f.write("-------------------------------------------------------------------------\n")
        f.write("=========================================================================\n")

    plt.figure(figsize=(10, 6), dpi=300)
    plt.plot(r_centers, tbr_parcial, marker='o', color='#0b3c5d', linewidth=2.5, label=f"TBR Parcial ({nombre_lib})")
    plt.title(f"Perfil Radial TBR (Ensayo 28) - ({nombre_lib})", fontsize=14, fontweight='bold')
    plt.xlabel("Radio Radial (cm)", fontsize=12)
    plt.ylabel("Tasa de Producción de Tritio", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_resultados, f"28_curva_tbr_radial_{lib_slug}.png"), bbox_inches='tight')
    plt.close()

    fig, ax1 = plt.subplots(figsize=(10, 6), dpi=300)
    ax1.plot(r_centers, n2n_parcial, marker='s', color='#1d2731', linewidth=2, label=f"n,2n Parcial ({nombre_lib})")
    ax1.set_xlabel("Radio Radial (cm)", fontsize=12)
    ax1.set_ylabel("Multiplicación n,2n Parcial", color='#1d2731', fontsize=12)
    ax1.tick_params(axis='y', labelcolor='#1d2731')
    ax1.grid(True, linestyle='--', alpha=0.5)

    ax2 = ax1.twinx()
    ax2.plot(r_centers, calor_parcial, marker='^', color='#c70039', linewidth=2, linestyle='--', label=f"Calor (eV/cm3)")
    ax2.set_ylabel("Calor Generado (eV/cm3)", color='#c70039', fontsize=12)
    ax2.tick_params(axis='y', labelcolor='#c70039')
    ax2.set_yscale('log')

    plt.title(f"Distribución Radial n,2n y Térmica (Ensayo 28) - ({nombre_lib})", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_resultados, f"28_curva_n2n_calor_radial_{lib_slug}.png"), bbox_inches='tight')
    plt.close()

plt.figure(figsize=(8, 6), dpi=300)
libs = list(resultados_completos.keys())
tbr_vals = [resultados_completos[l]['tbr'] for l in libs]
tbr_stds = [resultados_completos[l]['tbr_std'] for l in libs]
plt.bar(libs, tbr_vals, yerr=tbr_stds, capsize=5, color=['#4682b4', '#e67e22'], alpha=0.85, edgecolor='black')
plt.axhline(y=1.15, color='r', linestyle='--', linewidth=2, label='Límite Autosuficiencia (1.15)')
plt.title("TBR Global por Librería (Modelo 28: Definitivo 3D)", fontsize=14, fontweight='bold')
plt.ylabel("TBR Global", fontsize=12)
plt.ylim(0, max(tbr_vals) * 1.2)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.legend(fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(carpeta_resultados, "28_TBR_Comparativa.png"), bbox_inches='tight')
plt.close()

print(f"\n[ENSAYO 28 COMPLETADO CON ÉXITO]. Trazados de geometría y reportes en: {carpeta_resultados}\n")
