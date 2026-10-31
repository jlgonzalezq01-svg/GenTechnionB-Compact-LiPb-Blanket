import os
import openmc
import matplotlib.pyplot as plt
from datetime import datetime

print("[INFO] Iniciando Modelo 3D con Tallies y Refrigeración Capilar...")

# 1. RUTAS DE LIBRERÍAS BLINDADAS
# Asegúrate de ajustar las rutas a los directorios relativos correctos para el repositorio de GitHub si es necesario.
ruta_base_fendl = "/run/media/tato/unadetres/e-lab/2ª PARTE GenTechnionB/Librerias FENDL 3-ENDF B8/fendl32/fendl-3.2-hdf5/cross_sections.xml"
ruta_base_endf = "/run/media/tato/unadetres/e-lab/2ª PARTE GenTechnionB/Librerias FENDL 3-ENDF B8/ENDF-B VIII.0 - endfb80-lowtemp/endfb80-lowtemp/cross_sections.xml"

librerias = { 
    "FENDL-3.2": ruta_base_fendl, 
    "ENDF-B-VIII.0": ruta_base_endf 
}

openmc.config['cross_sections'] = ruta_base_fendl

# 2. MATERIALES
lipb = openmc.Material(name='LiPb') 
lipb.add_nuclide('Li6', 0.90, 'ao') 
lipb.add_nuclide('Li7', 0.10, 'ao') 
lipb.add_element('Pb', 1.0, 'ao') 
lipb.set_density('g/cm3', 9.0)

eurofer = openmc.Material(name='EUROFER') 
eurofer.add_element('Fe', 0.91, 'wo') 
eurofer.add_element('Cr', 0.09, 'wo') 
eurofer.set_density('g/cm3', 7.8)

boro = openmc.Material(name='Boro') 
boro.add_element('B', 1.0, 'wo') 
boro.set_density('g/cm3', 2.5)

imante_refrigerado = openmc.Material(name='Iman_Capilar') 
imante_refrigerado.add_element('Cu', 0.5, 'wo') 
imante_refrigerado.add_element('Fe', 0.4, 'wo') 
imante_refrigerado.add_element('O', 0.1, 'wo') 
imante_refrigerado.set_density('g/cm3', 6.5)

mats = openmc.Materials([lipb, eurofer, boro, imante_refrigerado]) 
mats.export_to_xml()

# 3. GEOMETRÍA 3D (Cilindros finitos coaxiales en Z)
z_min = openmc.ZPlane(z0=-150.0, boundary_type='vacuum') 
z_max = openmc.ZPlane(z0=150.0, boundary_type='vacuum')

r_plasma = openmc.ZCylinder(r=100.0) 
r_eurofer = openmc.ZCylinder(r=105.0) 
r_lipb = openmc.ZCylinder(r=200.0) 
r_boro = openmc.ZCylinder(r=230.0) 
r_imanes = openmc.ZCylinder(r=260.0, boundary_type='vacuum')

c_plasma = openmc.Cell(fill=None, region=-r_plasma & +z_min & -z_max) 
c_eurofer = openmc.Cell(fill=eurofer, region=+r_plasma & -r_eurofer & +z_min & -z_max) 
c_lipb = openmc.Cell(fill=lipb, region=+r_eurofer & -r_lipb & +z_min & -z_max) 
c_boro = openmc.Cell(fill=boro, region=+r_lipb & -r_boro & +z_min & -z_max) 
c_imanes = openmc.Cell(fill=imante_refrigerado, region=+r_boro & -r_imanes & +z_min & -z_max)

univ = openmc.Universe(cells=[c_plasma, c_eurofer, c_lipb, c_boro, c_imanes]) 
openmc.Geometry(univ).export_to_xml()

# 4. SETTINGS
settings = openmc.Settings() 
settings.run_mode = 'fixed source' 
settings.particles = 150000 
settings.batches = 25 
settings.inactive = 5 
settings.source = openmc.IndependentSource(space=openmc.stats.Point((0, 0, 0)), energy=openmc.stats.Discrete([14.1e6], [1.0])) 
settings.export_to_xml()

# 5. TALLIES 3D (TBR, Multiplicación y Calor en Imanes)
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

tallies.export_to_xml()

# 6. BUCLE DE EJECUCIÓN MULTILIBRERÍA 3D
for nombre_lib, ruta_xs in librerias.items(): 
    print(f"\n-------------------------------------------------------------------------") 
    print(f" >>> EJECUTANDO MODELO 3D CON LIBRERÍA: {nombre_lib}") 
    print(f"-------------------------------------------------------------------------")

    # Limpieza preventiva de archivos residuales HDF5
    for archivo_viejo in ['summary.h5', 'tallies.out', 'statepoint.25.h5']:
        if os.path.exists(archivo_viejo):
            os.remove(archivo_viejo)

    openmc.config['cross_sections'] = ruta_xs
    openmc.run()

    # Extracción de resultados
    sp = openmc.StatePoint('statepoint.25.h5')

    tbr_val = sp.get_tally(name='TBR_Global').mean[0][0][0]
    tbr_std = sp.get_tally(name='TBR_Global').std_dev[0][0][0]

    n2n_val = sp.get_tally(name='Multiplicacion_Pb').mean[0][0][0]
    n2n_std = sp.get_tally(name='Multiplicacion_Pb').std_dev[0][0][0]

    heat_val = sp.get_tally(name='Calor_Imanes').mean[0][0][0]
    heat_std = sp.get_tally(name='Calor_Imanes').std_dev[0][0][0]

    print(f"\n >>> RESULTADOS MODELO 3D ({nombre_lib}):")
    print(f" >>> TBR GLOBAL      = {tbr_val:.5f} +/- {tbr_std:.5f}")
    print(f" >>> MULTIPLICACIÓN  = {n2n_val:.5f} +/- {n2n_std:.5f}")
    print(f" >>> CALOR EN IMANES = {heat_val:.4e} +/- {heat_std:.4e} eV/source-particle")

print(f"\n[ÉXITO] Simulación del Modelo 3D completada para todas las librerías.\n")