// Configuración de cámaras, fotogramas y resaltados por escena.
// Coordenadas en el sistema de Blender (Z arriba); clay-stage.js las convierte a glTF (Y arriba).
// Cada paso narrativo ("step") mapea su tramo de scroll a un rango de fotogramas
// de la animación stop motion exportada desde Blender (24 fps, poses cada 2).

export const SCENES = {
  "adn-del-color": {
    end: 120,
    fov: 30,
    steps: [
      { frames: [0, 40], cam: [-7.5, -14, 4.2], target: [0, 0, 2.9] },
      { frames: [40, 60], cam: [-5.0, -8.0, 2.0], target: [0, 0, 2.0], highlight: { dimension: "subtono" } },
      { frames: [60, 80], cam: [6.0, -8.0, 4.0], target: [0, 0, 3.2], highlight: { dimension: "valor" } },
      { frames: [80, 100], cam: [-2.0, -7.5, 0.9], target: [0, 0, 3.0], highlight: { dimension: "intensidad" } },
      { frames: [100, 120], cam: [3.0, -8.0, 6.5], target: [0, 0, 2.6], highlight: { dimension: "contraste" } },
      { frames: [120, 120], cam: [-4.2, -12.2, 3.4], target: [0, 0, 2.9] },
    ],
  },
  "capas-de-la-piel": {
    end: 144,
    fov: 30,
    steps: [
      { frames: [0, 8], cam: [-3.6, -12.0, 5.2], target: [0, 0, 1.55] },
      { frames: [8, 8], cam: [-5.5, -9.0, 3.0], target: [0, -1, 1.3], highlight: { names: ["Epidermis", "Dermis", "Hipodermis"] } },
      { frames: [8, 92], cam: [-1.2, -6.8, 3.2], target: [-0.2, -1.1, 2.0], highlight: { names: ["Franja_objetivo", "Gota_0", "Gota_1", "Gota_2"] } },
      { frames: [92, 144], cam: [2.8, -6.6, 2.3], target: [1.3, -1.1, 1.5], highlight: { names: ["Gota_3"] } },
      { frames: [144, 144], cam: [-1.4, -10.6, 4.4], target: [0, 0, 1.6] },
    ],
  },
  "neutralizacion-del-color": {
    end: 120,
    fov: 30,
    steps: [
      { frames: [0, 10], cam: [0.0, -9.5, 5.6], target: [0, 0, 0.4] },
      { frames: [10, 40], cam: [-3.0, -6.5, 6.5], target: [0, 0, 0.3], highlight: { names: ["Eje_complementario", "Gota_gris_azulada", "Gota_naranja"] } },
      { frames: [40, 84], cam: [1.5, -5.5, 3.2], target: [0, 0, 0.6] },
      { frames: [84, 120], cam: [0.8, -4.4, 2.0], target: [0, 0, 0.9], highlight: { names: ["Gota_neutra"] } },
      { frames: [120, 120], cam: [1.2, -7.6, 3.6], target: [0, 0, 0.4] },
    ],
  },
};

// Textos breves para el panel que aparece al tocar una pieza (datos "extras" de Blender).
export const HOTSPOTS = {
  subtono: "Subtono: temperatura de la piel. Cálido (dorado) o frío (rosado-azulado).",
  valor: "Valor: luminosidad. Lo claro u oscuro de piel, cabello y ojos.",
  intensidad: "Intensidad: saturación. Colores brillantes y limpios o suaves y empolvados.",
  contraste: "Contraste: diferencia de valor entre piel, cabello y ojos.",
  correcta: "Profundidad correcta: el pigmento queda en la franja superficial de la dermis y se mantiene nítido.",
  excesiva: "Demasiado profundo: el pigmento se difumina y puede verse gris azulado.",
  "pigmento virado": "Pigmento antiguo virado a gris azulado.",
  corrector: "Corrector anaranjado: el complementario del azul en el círculo cromático.",
  "resultado neutro": "Resultado: un marrón neutro y estable.",
};
