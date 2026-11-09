import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import {cargarMontserrat} from './fuentes';
cargarMontserrat();

// Contador animado. REGLA INM: toda cifra necesita fuente verificada; si no, no se usa.
export const Contador: React.FC<{desde: number; hasta: number; sufijo: string; etiqueta: string; fuente: string; colorTexto: string; colorResalte: string}> = (p) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const v = interpolate(frame, [5, 45], [p.desde, p.hasta], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
  const s = spring({frame, fps, config: {damping: 15}});
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', fontFamily: 'Montserrat Black'}}>
      <div style={{fontSize: 220, color: p.colorTexto, transform: `scale(${s})`, textShadow: '0 6px 24px rgba(0,0,0,.5)'}}>{Math.round(v)}{p.sufijo}</div>
      <div style={{fontSize: 56, color: p.colorResalte, opacity: s}}>{p.etiqueta}</div>
      <div style={{fontFamily: 'Montserrat SemiBold', fontSize: 30, color: p.colorTexto, opacity: 0.8 * s, marginTop: 20}}>{p.fuente}</div>
    </AbsoluteFill>
  );
};
