# Estado del arte en procesamiento de señales (2026)

Oct 20, 2026 · @Jesús

## Panorama general

El procesamiento de señales (PS) ha pasado de una disciplina centrada en modelos (Fourier, filtrado lineal, estimación estadística) a un campo híbrido que combina modelos matemáticos clásicos y aprendizaje automático.

Los fundamentos clásicos (muestreo, transformadas, filtrado, estimación, detección) siguen siendo la base. La investigación actual se concentra en integrarlos con métodos basados en datos de forma eficiente, interpretable y fiable.

## Líneas de investigación principales

1. **Aprendizaje profundo guiado por modelos (*model-based deep learning*).** Algoritmos iterativos (ISTA, ADMM, filtro de Kalman) se "desenrollan" como capas de una red entrenable. El resultado son redes con menos parámetros, más interpretables y que necesitan menos datos: LISTA, KalmanNet, *algorithm unrolling*.
2. **Modelos fundacionales para señales.** Se preentrenan modelos a gran escala sobre señales. En neurociencia surgen los *Brain Foundation Models*, preentrenados con grandes volúmenes de datos neuronales. En comunicaciones, la IEEE Signal Processing Society impulsa modelos fundacionales inalámbricos para 6G que conectan con el análisis tiempo-frecuencia y los modelos estadísticos. En audio, el ICASSP 2026 dedicó una plenaria a cómo los LLM han cambiado el procesamiento de audio.
3. **Modelos generativos y problemas inversos.** Los modelos de difusión y basados en *score* sirven como *priors* para eliminar ruido, superresolución, reconstrucción en MRI y TC, separación de fuentes y síntesis de canal. Desplazan en parte a la regularización clásica por dispersión.
4. **Detección y comunicación integradas (ISAC) y 6G.** Comunicación y percepción del entorno comparten espectro y hardware en un marco unificado. Se estudian formas de onda nuevas (OTFS, AFDM), MIMO de muy gran escala, superficies inteligentes reconfigurables y la extensión a detección, comunicación y computación integradas (ISCC).
5. **Procesamiento de señales sobre grafos (GSP).** Generaliza Fourier, filtrado y muestreo a datos sobre redes irregulares: sensores, redes cerebrales, redes sociales. Es la base teórica de las redes neuronales sobre grafos.
6. **Muestreo compresivo, dispersión y baja dimensión.** El *compressed sensing* sigue vigente, ahora con *priors* aprendidos. Destacan el muestreo sub-Nyquist, la conversión A/D de pocos bits y el muestreo *modulo* (*unlimited sampling*).
7. **Métodos tensoriales y de alta dimensión.** Descomposiciones CP y Tucker para análisis multimodal, MIMO y quimiometría.
8. **PS eficiente, en el borde y neuromórfico.** Algoritmos de bajo consumo para IoT y vestibles: cuantización de redes, procesamiento por eventos y redes neuronales de impulsos (*spiking*).
9. **Fusión multimodal.** Audio, vídeo, radar, lidar y texto en sistemas unificados, por ejemplo en conducción autónoma y salud digital.
10. **Fiabilidad y cuantificación de incertidumbre.** Robustez, privacidad (aprendizaje federado), interpretabilidad y estimación de incertidumbre (métodos bayesianos, predicción conformal) para aplicaciones críticas como medicina y radar.

## Tendencias transversales

- Los algoritmos clásicos se convierten en arquitecturas de aprendizaje, y el aprendizaje se interpreta con herramientas de PS.
- Los datos y los modelos preentrenados pesan cada vez más que el diseño manual de características.
- La eficiencia (latencia, energía) importa tanto como la precisión.
- Ámbitos más activos: comunicaciones 6G, radar automotriz, biomedicina (EEG, ECG, imagen), audio y voz, teledetección.

## Referencias bibliográficas esenciales

Treinta y una referencias en siete bloques, de los fundamentos a los temas de frontera. Formato IEEE. Conviene verificar ediciones y autores antes de citarlas formalmente.

### Fundamentos (libros de texto)

&#91;1\] A. V. Oppenheim, A. S. Willsky, and S. H. Nawab, *Signals and Systems*, 2nd ed. Upper Saddle River, NJ, USA: Prentice Hall, 1997.

&#91;2\] A. V. Oppenheim and R. W. Schafer, *Discrete-Time Signal Processing*, 3rd ed. Upper Saddle River, NJ, USA: Pearson, 2010.

&#91;3\] J. G. Proakis and D. G. Manolakis, *Digital Signal Processing: Principles, Algorithms, and Applications*, 4th ed. Upper Saddle River, NJ, USA: Pearson Prentice Hall, 2007.

&#91;4\] M. Vetterli, J. Kovačević, and V. K. Goyal, *Foundations of Signal Processing*. Cambridge, U.K.: Cambridge Univ. Press, 2014.

&#91;5\] R. G. Lyons, *Understanding Digital Signal Processing*, 3rd ed. Upper Saddle River, NJ, USA: Prentice Hall, 2010.

### Procesamiento estadístico, adaptativo y espectral

&#91;6\] S. M. Kay, *Fundamentals of Statistical Signal Processing*, vol. I: *Estimation Theory* (1993); vol. II: *Detection Theory* (1998); vol. III: *Practical Algorithm Development* (2013). Upper Saddle River, NJ, USA: Prentice Hall.

&#91;7\] S. Haykin, *Adaptive Filter Theory*, 5th ed. Harlow, U.K.: Pearson, 2014.

&#91;8\] A. H. Sayed, *Adaptive Filters*. Hoboken, NJ, USA: Wiley-IEEE Press, 2008.

&#91;9\] P. Stoica and R. Moses, *Spectral Analysis of Signals*. Upper Saddle River, NJ, USA: Pearson Prentice Hall, 2005.

&#91;10\] H. L. Van Trees, *Optimum Array Processing*. New York, NY, USA: Wiley, 2002.

&#91;11\] S. Särkkä and L. Svensson, *Bayesian Filtering and Smoothing*, 2nd ed. Cambridge, U.K.: Cambridge Univ. Press, 2023.

### Representaciones, dispersión y muestreo

&#91;12\] S. Mallat, *A Wavelet Tour of Signal Processing: The Sparse Way*, 3rd ed. Burlington, MA, USA: Academic Press, 2009.

&#91;13\] D. L. Donoho, "Compressed sensing," *IEEE Trans. Inf. Theory*, vol. 52, no. 4, pp. 1289–1306, Apr. 2006.

&#91;14\] E. J. Candès, J. Romberg, and T. Tao, "Robust uncertainty principles: Exact signal reconstruction from highly incomplete frequency information," *IEEE Trans. Inf. Theory*, vol. 52, no. 2, pp. 489–509, Feb. 2006.

&#91;15\] S. Foucart and H. Rauhut, *A Mathematical Introduction to Compressive Sensing*. New York, NY, USA: Birkhäuser, 2013.

&#91;16\] Y. C. Eldar, *Sampling Theory: Beyond Bandlimited Systems*. Cambridge, U.K.: Cambridge Univ. Press, 2015.

### Optimización y aprendizaje

&#91;17\] S. Boyd and L. Vandenberghe, *Convex Optimization*. Cambridge, U.K.: Cambridge Univ. Press, 2004.

&#91;18\] D. P. Palomar and Y. C. Eldar, Eds., *Convex Optimization in Signal Processing and Communications*. Cambridge, U.K.: Cambridge Univ. Press, 2010.

&#91;19\] S. Theodoridis, *Machine Learning: A Bayesian and Optimization Perspective*, 2nd ed. London, U.K.: Academic Press, 2020.

&#91;20\] N. D. Sidiropoulos *et al.*, "Tensor decomposition for signal processing and machine learning," *IEEE Trans. Signal Process.*, vol. 65, no. 13, pp. 3551–3582, Jul. 2017.

### PS y aprendizaje profundo

&#91;21\] K. Gregor and Y. LeCun, "Learning fast approximations of sparse coding," in *Proc. 27th Int. Conf. Mach. Learn. (ICML)*, Haifa, Israel, 2010, pp. 399–406.

&#91;22\] V. Monga, Y. Li, and Y. C. Eldar, "Algorithm unrolling: Interpretable, efficient deep learning for signal and image processing," *IEEE Signal Process. Mag.*, vol. 38, no. 2, pp. 18–44, Mar. 2021.

&#91;23\] N. Shlezinger, J. Whang, Y. C. Eldar, and A. G. Dimakis, "Model-based deep learning," *Proc. IEEE*, vol. 111, no. 5, pp. 465–499, May 2023.

&#91;24\] J. Ho, A. Jain, and P. Abbeel, "Denoising diffusion probabilistic models," in *Adv. Neural Inf. Process. Syst. (NeurIPS)*, vol. 33, 2020, pp. 6840–6851.

&#91;25\] Y. Song *et al.*, "Score-based generative modeling through stochastic differential equations," in *Proc. Int. Conf. Learn. Represent. (ICLR)*, 2021.

&#91;26\] X. Zhou *et al.*, "Brain foundation models: A survey on advancements in neural signal processing and brain discovery," 2025, [arXiv:2503.00580](https://arxiv.org/html/2503.00580v2) (verificar primer autor).

### PS sobre grafos

&#91;27\] D. I. Shuman, S. K. Narang, P. Frossard, A. Ortega, and P. Vandergheynst, "The emerging field of signal processing on graphs," *IEEE Signal Process. Mag.*, vol. 30, no. 3, pp. 83–98, May 2013.

&#91;28\] A. Ortega, P. Frossard, J. Kovačević, J. M. F. Moura, and P. Vandergheynst, "Graph signal processing: Overview, challenges, and applications," *Proc. IEEE*, vol. 106, no. 5, pp. 808–828, May 2018.

### ISAC y 6G

&#91;29\] F. Liu *et al.*, "Integrated sensing and communications: Toward dual-functional wireless networks for 6G and beyond," *IEEE J. Sel. Areas Commun.*, vol. 40, no. 6, pp. 1728–1767, Jun. 2022.

&#91;30\] D. Zhang *et al.*, "Integrated sensing and communications over the years: An evolution perspective," 2025, [arXiv:2504.06830](https://arxiv.org/abs/2504.06830).

&#91;31\] "Sensing with communication signals: From information theory to signal processing," *IEEE J. Sel. Areas Commun.*, vol. 44, 2026, doi: 10.1109/JSAC.2025.3614025.

### Para estar al día

- **Revistas:** *IEEE Signal Processing Magazine* (tutoriales, ideal para empezar), *IEEE Transactions on Signal Processing*, *IEEE Journal of Selected Topics in Signal Processing*, *Signal Processing* (Elsevier), *EURASIP Journal on Advances in Signal Processing*.
- **Congresos:** ICASSP, EUSIPCO, IEEE SSP, CAMSAP, SPAWC.
- **Preprints:** arXiv, categoría eess.SP.

## Fuentes consultadas

- [Brain Foundation Models: A Survey (arXiv 2503.00580)](https://arxiv.org/html/2503.00580v2)
- [Call for Papers – Wireless Foundation Models for AI-native 6G (IEEE SPS)](https://signalprocessingsociety.org/events/call-papers-wireless-foundation-models-ai-native-6g-and-beyond-wfmab)
- [ICASSP 2026 – Plenarias](https://2026.ieeeicassp.org/?p=4704)
- [Integrated Sensing and Communication – Chalmers, 2026](https://research.chalmers.se/en/publication/552990)
- [ISAC: A Survey of Recent Progress Toward 5G-A and 6G](https://scholar.hit.edu.cn/en/publications/integrated-sensing-and-communications-a-survey-of-recent-progress/)
- [A Survey on Integrated Sensing, Communication, and Computation (arXiv 2408.08074)](https://arxiv.org/pdf/2408.08074)
- [MDPI Electronics – Visual Recognition and Signal Processing](https://www.mdpi.com/journal/electronics/special_issues/7C1SZ65Q1G)
- [ISAC Over the Years (arXiv 2504.06830)](https://arxiv.org/abs/2504.06830)
- [Sensing With Communication Signals (IEEE JSAC, 2026)](https://www.weizmann.ac.il/math/yonina/sites/math.yonina/files/Sensing%20With%20Communication%20Signals_0.pdf)
