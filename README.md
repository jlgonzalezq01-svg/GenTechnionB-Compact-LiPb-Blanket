# GenTechnionB v1.0 — 3D Neutronic Validation and Geometric Robustness of Compact LiPb Breeding Blankets under Industrial Penetrations

[![ORCID](https://img.shields.io/badge/ORCID-0009-0000-6912-3955-A6CE39?logo=orcid&logoColor=white)](https://orcid.org/0009-0000-6912-3955)
[![OpenMC](https://img.shields.io/badge/OpenMC-v0.15.3-0b3c5d)](https://openmc.org/)
[![Nuclear Data](https://img.shields.io/badge/Libraries-FENDL--3.2%20%7C%20ENDF%2FB--VIII.0-e67e22)]()

**Author / Autor:** José Luis González Quintana (jlgonzalezq01@gmail.com)  
**ORCID iD:** [https://orcid.org/0009-0000-6912-3955](https://orcid.org/0009-0000-6912-3955)  
**Official Repository / Repositorio Oficial:** [https://github.com/jlgonzalezq01-svg/GenTechnionB-Compact-LiPb-Blanket](https://github.com/jlgonzalezq01-svg/GenTechnionB-Compact-LiPb-Blanket) 
/ Official Zenodo DOI: https://doi.org/10.5281/zenodo.23883962
**Transport Engine / Motor de Transporte:** OpenMC v0.15.3 (Constructive Solid Geometry — CSG)  
**Evaluated Nuclear Data Libraries / Librerías Nucleares:** FENDL-3.2 (IAEA) & ENDF/B-VIII.0  
> **NOTE / NOTA:**  
> **EN:** Those who downloaded the documents prior to 04/11/2026 at 17:00h, please take into account that the previously provided DOI was erroneous. The correct DOI is the one currently listed (`https://doi.org/10.5281/zenodo.23883962`).  
> **ES:** Quienes hayan descargado los documentos antes del día 04/11/2026 a las 17:00h, por favor tengan en cuenta que el DOI proporcionado era erróneo. El DOI correcto es el que figura actualmente (`https://doi.org/10.5281/zenodo.23883962`).

---

## 1. Overview / Resumen del Proyecto `[EN / ES]`

* **`[EN]`** This repository contains the complete source code (`SCRIPTS/`), multi-library statistical transport reports (`RESULTS_Cases_12_17-28/`), spatial radial profiles (`FIGURES_Statistics_and_Curves/`), and plant integration documentation (`DOCUMENTS/`) for the three-dimensional neutronic and thermodynamic validation of the **GenTechnionB v1.0** compact modular fusion reactor (HCLL architecture). Cross-validated with **FENDL-3.2** and **ENDF/B-VIII.0** up to an ultra-high statistics regime of **200 million cumulative particle histories** in the full 3D industrial configuration (**Case 28**), the system sustains a global Tritium Breeding Ratio (**TBR**) of **1.26766 ± 0.00010** (FENDL-3.2) and **1.26733 ± 0.00011** (ENDF/B-VIII.0) under severe structural penetrations (two orthogonal equatorial ports and a physical basal W/CuCrZr/H₂O divertor cassette), while bounding residual nuclear heating in the capillary-cooled superconducting magnets between **414.94 ± 3.16** and **482.80 ± 3.45 eV/source particle** with zero peripheral radial leakage (**0.00000 ± 0.00000**).
* **`[ES]`** Este repositorio contiene el código fuente completo (`SCRIPTS/`), los reportes estadísticos multilibrería (`RESULTS_Cases_12_17-28/`), los perfiles espaciales radiales (`FIGURES_Statistics_and_Curves/`) y la memoria técnica de integración en planta (`DOCUMENTS/`) correspondientes a la validación neutrónica y termodinámica tridimensional del reactor de fusión modular compacto **GenTechnionB v1.0** (arquitectura HCLL). Evaluado mediante validación cruzada con **FENDL-3.2** y **ENDF/B-VIII.0** hasta un régimen de ultra-alta estadística de **200 millones de historias acumuladas** en el modelo industrial 3D completo (**Ensayo 28**), el sistema sostiene un **TBR global** de **1.26766 ± 0.00010** (FENDL-3.2) y **1.26733 ± 0.00011** (ENDF/B-VIII.0) frente a penetraciones industriales severas (dos puertos ecuatoriales ortogonales y cassette divertor basal físico de W/CuCrZr/H₂O), acotando el calentamiento nuclear en los imanes superconductores refrigerados por red capilar entre **414.94 ± 3.16** y **482.80 ± 3.45 eV/partícula fuente** con fuga radial periférica nula (**0.00000 ± 0.00000**).

---

## 2. Repository Structure & File Traceability / Estructura y Trazabilidad de Archivos

| Case / Ensayo | OpenMC Python Script (`SCRIPTS/`) | Statistical Reports (`RESULTS_Cases_12_17-28/`) | Figures & Radial Curves (`FIGURES_Statistics_and_Curves/`) | Global TBR (FENDL-3.2 / ENDF/B-VIII.0) |
| :--- | :--- | :--- | :--- | :--- |
| **12** | `Case_12_basic_line_2d.py` | `Case_12_basic_line_2d.txt` | — | `1.29755 ± 0.00020` / `1.29894 ± 0.00020` |
| **17** | `Case_17_open_3d_basic_line.py` | `Case_17_open_3d_basic_line_<lib>.txt` | `Case_17_TBR_Comparison.png`, `Case_17_Radial_TBR_Curve_<lib>.png`, `Case_17_Radial_n2n_Thermal_Curve_<lib>.png` | `0.85855 ± 0.00079` / `0.85892 ± 0.00067` |
| **18** | `Case_18_reflective_confinement.py` | `Case_18_reflective_axial_<lib>.txt` | `Case_18_TBR_Comparison_Reflective.png`, `Case_18_Radial_TBR_Curve_Reflective_<lib>.png`, `Case_18_Radial_n2n_Thermal_Curve_<lib>.png` | `1.39364 ± 0.00079` / `1.39495 ± 0.00064` |
| **19** | `Case_19_blanket_optimization.py` | `Case_19_optimized_radial_<lib>.txt` | `Case_19_TBR_Comparison_Optimized.png`, `Case_19_Radial_TBR_Curve_Optimized_<lib>.png`, `Case_19_Radial_n2n_Thermal_Curve_<lib>.png` | `1.56458 ± 0.00065` / `1.56501 ± 0.00066` |
| **20** | `Case_20_hcll_helium_channel.py` | `Case_20_hcll_channel_<lib>.txt` | `Case_20_TBR_Comparison_HCLL.png`, `Case_20_Radial_TBR_Curve_HCLL_<lib>.png`, `Case_20_Radial_n2n_Thermal_Curve_<lib>.png` | `1.56577 ± 0.00065` / `1.56415 ± 0.00050` |
| **21** | `Case_21_graphite_radial_port.py` | `Case_21_graphite_port_<lib>.txt` | `Case_21_TBR_Comparison_Graphite_Port.png`, `Case_21_Radial_TBR_Curve_Graphite_Port_<lib>.png`, `Case_21_Radial_n2n_Thermal_Curve_<lib>.png` | `1.55862 ± 0.00068` / `1.55726 ± 0.00045` |
| **22** | `Case_22_monolithic_structural_arm.py` | `Case_22_monolithic_arm_<lib>.txt` | `Case_22_TBR_Comparison_Structural_Arm.png`, `Case_22_Radial_TBR_Curve_Structural_Arm_<lib>.png`, `Case_22_Radial_n2n_Thermal_Curve_<lib>.png` | `1.50736 ± 0.00060` / `1.50712 ± 0.00059` |
| **23** | `Case_23_hybrid_structural_arm.py` | `Case_23_hybrid_arm_<lib>.txt` | `Case_23_TBR_Comparison_Hybrid_Arm.png`, `Case_23_Radial_TBR_Curve_<lib>.png`, `Case_23_Radial_n2n_Thermal_Curve_<lib>.png` | `1.50487 ± 0.00068` / `1.50392 ± 0.00059` |
| **24** | `Case_24_directional_shielding_plug.py` | `Case_24_directional_shielding_plug_<lib>.txt` | `Case_24_TBR_Comparison_Shielding_Plug.png`, `Case_24_Radial_TBR_Curve_Shielding_Plug_<lib>.png`, `Case_24_Radial_n2n_Thermal_Curve_<lib>.png` | `1.50523 ± 0.00068` / `1.50426 ± 0.00059` |
| **25** | `Case_25_heterogeneous_blanket.py` | `Case_25_heterogeneous_blanket_<lib>.txt` | `Case_25_TBR_Comparison.png`, `Case_25_Radial_TBR_Curve_<lib>.png`, `Case_25_Radial_n2n_Thermal_Curve_<lib>.png` | `1.50111 ± 0.00074` / `1.50105 ± 0.00074` |
| **26** | `Case_26_tungsten_armor.py` | `Case_26_tungsten_armor_<lib>.txt` | `Case_26_TBR_Comparison.png`, `Case_26_Radial_TBR_Curve_<lib>.png`, `Case_26_Radial_n2n_Thermal_Curve_<lib>.png` | `1.52264 ± 0.00052` / `1.52276 ± 0.00052` |
| **27** | `Case_27_b4c_h2o_shield.py` | `Case_27_b4c_h2o_shield_<lib>.txt` | `Case_27_TBR_Comparison.png`, `Case_27_Radial_TBR_Curve_<lib>.png`, `Case_27_Radial_n2n_Thermal_Curve_<lib>.png` | `1.52236 ± 0.00053` / `1.52272 ± 0.00052` |
| **28** | `Case_28_full_3d_industrial.py` | `Case_28_full_3d_industrial_<lib>.txt` | `Case_28_TBR_Comparison.png`, `Case_28_Radial_TBR_Curve_<lib>.png`, `Case_28_Radial_n2n_Thermal_Curve_<lib>.png`, `Case_28_Geometry_XY_Cross_Section.png`, `Case_28_Geometry_XZ_Cross_Section.png` | `1.26766 ± 0.00010` / `1.26733 ± 0.00011` |

*(Note: `<lib>` denotes both `fendl32` and `endfbviii0` evaluated files).*

---

## 3. Reproducibility & Execution / Reproducibilidad y Ejecución

1. Install **OpenMC v0.15.3** (`conda install -c conda-forge openmc=0.15.3`) alongside `numpy` and `matplotlib`.
2. Download the official HDF5 cross-section distributions for **FENDL-3.2** (`fendl-3.2-hdf5`) and **ENDF/B-VIII.0** (`endfb80-lowtemp`), and update the `librerias` dictionary path in the corresponding script.
3. Run any simulation case from the terminal:
   ```bash
   python3 SCRIPTS/Case_28_full_3d_industrial.py
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
