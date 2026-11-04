# GenTechnionB v1.0 — 3D Neutronic Validation and Geometric Robustness of Compact LiPb Breeding Blankets under Industrial Penetrations

[![ORCID](https://img.shields.io/badge/ORCID-0009-0000-6912-3955-A6CE39?logo=orcid&logoColor=white)](https://orcid.org/0009-0000-6912-3955)
[![OpenMC](https://img.shields.io/badge/OpenMC-v0.15.3-0b3c5d)](https://openmc.org/)
[![Nuclear Data](https://img.shields.io/badge/Libraries-FENDL--3.2%20%7C%20ENDF%2FB--VIII.0-e67e22)]()

**Author / Autor:** José Luis González Quintana (jlgonzalezq01@gmail.com)  
**ORCID iD:** [https://orcid.org/0009-0000-6912-3955](https://orcid.org/0009-0000-6912-3955)  
**Official Repository / Repositorio Oficial:** [https://github.com/jlgonzalezq01-svg/GenTechnionB-Compact-LiPb-Blanket](https://github.com/jlgonzalezq01-svg/GenTechnionB-Compact-LiPb-Blanket) 
Official Zenodo DOI: https://doi.org/10.5281/zenodo.23883962
**Transport Engine / Motor de Transporte:** OpenMC v0.15.3 (Constructive Solid Geometry — CSG)  
**Evaluated Nuclear Data Libraries / Librerías Nucleares:** FENDL-3.2 (IAEA) & ENDF/B-VIII.0  

---

## 1. Overview / Resumen del Proyecto `[EN / ES]`

* **`[EN]`** This repository contains the complete source code (`SCRIPTS/`), multi-library statistical transport reports (`RESULTADOS_ENSAYOS_12, 17-28/`), spatial radial profiles (`FIGURAS_Estadisticas_y_Curvas/`), and plant integration documentation (`ANEXO_I_Concepcion_Visual/`) for the three-dimensional neutronic and thermodynamic validation of the **GenTechnionB v1.0** compact modular fusion reactor (HCLL architecture). Cross-validated with **FENDL-3.2** and **ENDF/B-VIII.0** up to an ultra-high statistics regime of **200 million cumulative particle histories** in the full 3D industrial configuration (**Case 28**), the system sustains a global Tritium Breeding Ratio (**TBR**) of **1.26766 ± 0.00010** (FENDL-3.2) and **1.26733 ± 0.00011** (ENDF/B-VIII.0) under severe structural penetrations (two orthogonal equatorial ports and a physical basal W/CuCrZr/H₂O divertor cassette), while bounding residual nuclear heating in the capillary-cooled superconducting magnets between **414.94 ± 3.16** and **482.80 ± 3.45 eV/source particle** with zero peripheral radial leakage (**0.00000 ± 0.00000**).
* **`[ES]`** Este repositorio contiene el código fuente completo (`SCRIPTS/`), los reportes estadísticos multilibrería (`RESULTADOS_ENSAYOS_12, 17-28/`), los perfiles espaciales radiales (`FIGURAS_Estadisticas_y_Curvas/`) y la memoria técnica de integración en planta (`ANEXO_I_Concepcion_Visual/`) correspondientes a la validación neutrónica y termodinámica tridimensional del reactor de fusión modular compacto **GenTechnionB v1.0** (arquitectura HCLL). Evaluado mediante validación cruzada con **FENDL-3.2** y **ENDF/B-VIII.0** hasta un régimen de ultra-alta estadística de **200 millones de historias acumuladas** en el modelo industrial 3D completo (**Ensayo 28**), el sistema sostiene un **TBR global** de **1.26766 ± 0.00010** (FENDL-3.2) y **1.26733 ± 0.00011** (ENDF/B-VIII.0) frente a penetraciones industriales severas (dos puertos ecuatoriales ortogonales y cassette divertor basal físico de W/CuCrZr/H₂O), acotando el calentamiento nuclear en los imanes superconductores refrigerados por red capilar entre **414.94 ± 3.16** y **482.80 ± 3.45 eV/partícula fuente** con fuga radial periférica nula (**0.00000 ± 0.00000**).

---

## 2. Repository Structure & File Traceability / Estructura y Trazabilidad de Archivos

| Case / Ensayo | OpenMC Python Script (`SCRIPTS/`) | Statistical Reports (`RESULTADOS_ENSAYOS_12, 17-28/`) | Figures & Radial Curves (`FIGURAS_Estadisticas_y_Curvas/`) | Global TBR (FENDL-3.2 / ENDF/B-VIII.0) |
| :--- | :--- | :--- | :--- | :--- |
| **12** | `12_base_2d.py` | `12_resultado_base_2d.txt` | — | `1.29755 ± 0.00020` / `1.29894 ± 0.00020` |
| **17** | `17_open_3d_baseline.py` | `17_resultado_linea_base_3d_<lib>.txt` | `17_TBR_Comparativa.png`, `17_curva_tbr_radial_<lib>.png`, `17_curva_n2n_calor_radial_<lib>.png` | `0.85855 ± 0.00079` / `0.85892 ± 0.00067` |
| **18** | `18_reflective_confinement.py` | `18_resultado_reflectivo_<lib>.txt` | `18_TBR_Comparativa.png`, `18_curva_tbr_radial_<lib>.png`, `18_curva_n2n_calor_radial_<lib>.png` | `1.39364 ± 0.00079` / `1.39495 ± 0.00064` |
| **19** | `19_blanket_optimization.py` | `19_resultado_optimizado_<lib>.txt` | `19_TBR_Comparativa.png`, `19_curva_tbr_radial_<lib>.png`, `19_curva_n2n_calor_radial_<lib>.png` | `1.56458 ± 0.00065` / `1.56501 ± 0.00066` |
| **20** | `20_hcll_helium_channel.py` | `20_resultado_hcll_<lib>.txt` | `20_TBR_Comparativa.png`, `20_curva_tbr_radial_<lib>.png`, `20_curva_n2n_calor_radial_<lib>.png` | `1.56577 ± 0.00065` / `1.56415 ± 0.00050` |
| **21** | `21_graphite_radial_port.py` | `21_resultado_puerto_grafito_<lib>.txt` | `21_TBR_Comparativa.png`, `21_curva_tbr_radial_<lib>.png`, `21_curva_n2n_calor_radial_<lib>.png` | `1.55862 ± 0.00068` / `1.55726 ± 0.00045` |
| **22** | `22_monolithic_structural_arm.py` | `22_resultado_brazo_estructural_<lib>.txt` | `22_TBR_Comparativa.png`, `22_curva_tbr_radial_<lib>.png`, `22_curva_n2n_calor_radial_<lib>.png` | `1.50736 ± 0.00060` / `1.50712 ± 0.00059` |
| **23** | `23_hybrid_structural_arm.py` | `23_resultado_brazo_hibrido_<lib>.txt` | `23_TBR_Comparativa.png`, `23_curva_tbr_radial_<lib>.png`, `23_curva_n2n_calor_radial_<lib>.png` | `1.50487 ± 0.00068` / `1.50392 ± 0.00059` |
| **24** | `24_directional_shielding_plug.py` | `24_resultado_tapon_blindaje_direccional_<lib>.txt` | `24_TBR_Comparativa.png`, `24_curva_tbr_radial_<lib>.png`, `24_curva_n2n_calor_radial_<lib>.png` | `1.50523 ± 0.00068` / `1.50426 ± 0.00059` |
| **25** | `25_heterogeneous_blanket.py` | `25_resultado_manto_heterogeneo_<lib>.txt` | `25_TBR_Comparativa.png`, `25_curva_tbr_radial_<lib>.png`, `25_curva_n2n_calor_radial_<lib>.png` | `1.50111 ± 0.00074` / `1.50105 ± 0.00074` |
| **26** | `26_tungsten_armor.py` | `26_resultado_armadura_wolframio_<lib>.txt` | `26_TBR_Comparativa.png`, `26_curva_tbr_radial_<lib>.png`, `26_curva_n2n_calor_radial_<lib>.png` | `1.52264 ± 0.00052` / `1.52276 ± 0.00052` |
| **27** | `27_advanced_shield.py` | `27_resultado_blindaje_b4c_agua_<lib>.txt` | `27_TBR_Comparativa.png`, `27_curva_tbr_radial_<lib>.png`, `27_curva_n2n_calor_radial_<lib>.png` | `1.52236 ± 0.00053` / `1.52272 ± 0.00052` |
| **28** | `28_industrial_3d.py` | `28_resultado_industrial_3d_<lib>.txt` | `28_TBR_Comparativa.png`, `28_curva_tbr_radial_<lib>.png`, `28_curva_n2n_calor_radial_<lib>.png`, `28_geometria_corte_xy.png`, `28_geometria_corte_xz.png` | `1.26766 ± 0.00010` / `1.26733 ± 0.00011` |

*(Note: `<lib>` denotes both `fendl32` and `endfbviii0` evaluated files).*

---

## 3. Reproducibility & Execution / Reproducibilidad y Ejecución

1. Install **OpenMC v0.15.3** (`conda install -c conda-forge openmc=0.15.3`) alongside `numpy` and `matplotlib`.
2. Download the official HDF5 cross-section distributions for **FENDL-3.2** (`fendl-3.2-hdf5`) and **ENDF/B-VIII.0** (`endfb80-lowtemp`), and update the `librerias` dictionary path in the corresponding script.
3. Run any simulation case from the terminal:
   ```bash
   python3 SCRIPTS/28_industrial_3d.py
   ```

---

## 4. Official Repository & Authorship Priority / Repositorio Oficial y Prioridad de Autoría

* **Author:** José Luis González Quintana — ORCID: [https://orcid.org/0009-0000-6912-3955](https://orcid.org/0009-0000-6912-3955)
* **Repository URL:** [https://github.com/jlgonzalezq01-svg/GenTechnionB-Compact-LiPb-Blanket](https://github.com/jlgonzalezq01-svg/GenTechnionB-Compact-LiPb-Blanket)
* **Clone command:**
  ```bash
  git clone https://github.com/jlgonzalezq01-svg/GenTechnionB-Compact-LiPb-Blanket.git
  ```
* **Authorship & Intellectual Priority / Autoría y Prioridad Intelectual:**  
  All 3D Constructive Solid Geometry (CSG) architectures, radial/axial shielding configurations, capillary-cooled magnet protection schemes, and multi-library OpenMC validation workflows contained in this repository are the original work of **José Luis González Quintana** (`jlgonzalezq01@gmail.com`, ORCID: `0009-0000-6912-3955`).
