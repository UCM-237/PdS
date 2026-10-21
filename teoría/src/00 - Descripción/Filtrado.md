## Proceso seguido para la edición de la imagen

Voy a explicarlo **como lo haría en una asignatura de Procesamiento de Señales / Procesamiento de Imagen**, separando claramente las etapas y justificando cada una.

---

## 1. Eliminación del ruido sal y pimienta

### 1.1. Identificación del ruido
El ruido **sal y pimienta** se caracteriza por:
- Píxeles aislados con valores extremos (0 o 255 en escala de grises).
- Aparición aleatoria, no correlacionada espacialmente.
- Muy visible en zonas uniformes (fondo y piel).

Este tipo de ruido **no se elimina bien con filtros lineales** (media, gaussiano), porque:
- Difuminan bordes.
- No eliminan valores impulsivos extremos.

---

### 1.2. Filtro utilizado: **filtro mediana**
Se aplica un **filtro de mediana** porque:
- Es un filtro **no lineal**.
- Preserva bordes.
- Elimina eficazmente valores impulsivos.

#### Procedimiento:
1. Se trabaja en el dominio espacial.
2. Para cada píxel:
   - Se toma una ventana local (típicamente 3×3 o 5×5).
   - Se ordenan los valores.
   - Se sustituye el píxel central por la **mediana**.

📌 Resultado:
- Eliminación casi completa del ruido.
- Bordes faciales bien preservados (nariz, ojos, boca).

---

## 2. Eliminación de las gafas

Esta parte **no es un simple filtrado**, sino una **edición semántica de imagen**.

### 2.1. Detección de la región de las gafas
Internamente se realiza:
- Detección facial.
- Localización aproximada de:
  - Ojos
  - Puente nasal
- Identificación de objetos tipo “gafas” por forma y textura.

Esto equivale conceptualmente a una **segmentación por clases**:
- Cara
- Ojos
- Accesorios (gafas)

---

### 2.2. Eliminación y reconstrucción (inpainting)
Una vez detectadas las gafas:
1. Se crea una **máscara binaria** de las gafas.
2. Se eliminan los píxeles de esa región.
3. Se reconstruye la zona usando **inpainting**:
   - Se interpola textura y color desde las regiones vecinas.
   - Se respetan:
     - Iluminación local
     - Simetría facial
     - Continuidad de la piel

📌 Resultado:
- Desaparición natural de las gafas.
- Ojos y nariz coherentes, sin artefactos visibles.

---

## 3. Cambio del color de la barba a blanca

### 3.1. Segmentación de la barba
Se realiza una segmentación específica basada en:
- Posición facial (zona inferior del rostro).
- Textura característica (alta frecuencia, patrón piloso).
- Color original (tonos oscuros/marrones).

Esto es similar a una **segmentación por región + atributos**.

---

### 3.2. Transformación de color
Una vez aislada la barba:
1. Se cambia de espacio de color (conceptualmente a HSV o LAB).
2. Se modifica:
   - **Saturación → baja**
   - **Luminancia → alta**
3. Se conserva la textura:
   - No se “pinta” de blanco plano.
   - Se mantiene el relieve del pelo.

📌 Resultado:
- Barba blanca realista.
- Volumen y textura preservados.
- Integración natural con la piel.

---

## 4. Ajuste final y coherencia visual

Por último se hace un ajuste global:
- Suavizado leve para homogeneizar transiciones.
- Ajuste de contraste local para evitar zonas “plásticas”.
- Verificación de coherencia:
  - Iluminación
  - Sombras
  - Simetría facial

---

## Resumen en términos de Procesamiento de Señales

| Etapa | Técnica | Dominio |
|-----|-------|--------|
| Eliminación de ruido | Filtro mediana | Espacial |
| Quitar gafas | Segmentación + Inpainting | Semántico |
| Barba blanca | Segmentación + Transformación de color | Color |
| Ajuste final | Suavizado y realce leve | Espacial |

---

### Conversación con la IA

Para eliminar **únicamente el ruido** de la imagen utilizaría un **filtro de mediana en el dominio espacial**, ya que el ruido presente es claramente **sal y pimienta** (impulsivo): píxeles aislados con valores extremos que aparecen de forma aleatoria. Los filtros lineales como la media o el gaussiano no son adecuados en este caso porque los valores impulsivos contaminan el promedio y provocan un difuminado general de la imagen sin eliminar completamente el ruido.

El filtro de mediana es **no lineal** y sustituye cada píxel por la mediana de los valores en una ventana local (por ejemplo 5×5), lo que permite eliminar los impulsos sin degradar significativamente los bordes y detalles importantes de la imagen, como los rasgos faciales. Por eso es el método clásico más eficaz y conceptualmente correcto para este tipo de ruido.
