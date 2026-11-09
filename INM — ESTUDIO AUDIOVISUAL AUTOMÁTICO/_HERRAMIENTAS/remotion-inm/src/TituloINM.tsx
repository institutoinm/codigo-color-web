import React from 'react';
import {AbsoluteFill, Audio, interpolate, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {cargarMontserrat} from './fuentes';
cargarMontserrat();

export const esquemaTitulo = {
  titulo: 'ESTUDIO INM',
  subtitulo: 'Remotion · prueba de render',
  segundaEscena: 'PRUEBA OK',
  colorPrimario: '#0D2B4E',   // PROVISIONAL: sustituir por los HEX oficiales del INM
  colorSecundario: '#2F6DB5', // PROVISIONAL
  colorResalte: '#8FC3FF',    // PROVISIONAL
  transparente: false,
  sonido: true,
};
type Props = typeof esquemaTitulo;

const Texto: React.FC<{texto: string; tam: number; color: string; y: number; inicio: number; familia?: string}> = ({texto, tam, color, y, inicio, familia = 'Montserrat Black'}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame: frame - inicio, fps, config: {damping: 14, stiffness: 140}});
  const blur = interpolate(s, [0, 1], [14, 0]);
  return (
    <div style={{position: 'absolute', top: y, width: '100%', textAlign: 'center', fontFamily: familia, fontSize: tam, color,
      transform: `scale(${interpolate(s, [0, 1], [0.6, 1])})`, opacity: s, filter: `blur(${blur}px)`,
      textShadow: '0 4px 18px rgba(0,0,0,.45)', letterSpacing: 1}}>{texto}</div>
  );
};

export const TituloINM: React.FC<Props> = (p) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const corte = Math.round(durationInFrames * 0.48);
  // Transición: barrido diagonal de la escena 2 sobre la escena 1 (18 fotogramas)
  const barrido = interpolate(frame, [corte - 9, corte + 9], [-30, 130], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const salida = interpolate(frame, [durationInFrames - 8, durationInFrames], [1, 0], {extrapolateLeft: 'clamp'});
  return (
    <AbsoluteFill style={{background: p.transparente ? 'transparent' : `linear-gradient(180deg, ${p.colorPrimario}, ${p.colorSecundario})`}}>
      <AbsoluteFill style={{opacity: p.transparente ? salida : 1}}>
        <Texto texto={p.titulo} tam={120} color="#FFFFFF" y={820} inicio={4} />
        {p.subtitulo ? <Texto texto={p.subtitulo} tam={54} color={p.colorResalte} y={990} inicio={14} familia="Montserrat SemiBold" /> : null}
      </AbsoluteFill>
      {!p.transparente && (
        <AbsoluteFill style={{clipPath: `polygon(0 0, ${barrido}% 0, ${barrido - 30}% 100%, 0 100%)`, background: '#08182C'}}>
          <Sequence from={corte}><Texto texto={p.segundaEscena} tam={110} color="#FFFFFF" y={860} inicio={4} /></Sequence>
        </AbsoluteFill>
      )}
      {p.sonido && <Sequence from={2}><Audio src={staticFile('pop.wav')} volume={0.7} /></Sequence>}
      {p.sonido && !p.transparente && <Sequence from={corte - 9}><Audio src={staticFile('whoosh.wav')} /></Sequence>}
    </AbsoluteFill>
  );
};
