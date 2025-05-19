# 🔍 Cálculo de Distribución Conjunta para Redes Bayesianas

Este proyecto permite calcular la **distribución conjunta** de una red bayesiana definida en un archivo JSON. Utiliza herramientas estándar de Python como `itertools`, `json` y `pandas`, y está diseñado para ser sencillo y fácil de entender.

![Demostración de uso](https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExYWp6anI2bWZsbHFqYjFqYml0amwxOGh0cnExNGIyd2Vja2Nib2hjdyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/GeimqsH0TLDt4tScGw/giphy.gif)

## 📁 Estructura esperada del archivo JSON

El archivo JSON debe tener la siguiente estructura:

```json
{
  "nodes": {
    "NombreNodo": {
      "values": ["valor1", "valor2", ...],
      "parents": ["Padre1", "Padre2", ...],
      "cpt": [
        {
          "when": { "Padre1": "valorA", ... },
          "then": { "valor1": 0.3, "valor2": 0.7 }
        }
      ]
    },
    ...
  }
}


