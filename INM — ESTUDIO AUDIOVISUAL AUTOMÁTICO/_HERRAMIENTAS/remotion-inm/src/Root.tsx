import React from 'react';
import {Composition} from 'remotion';
import {TituloINM, esquemaTitulo} from './TituloINM';
import {Contador} from './Contador';

// Todas las composiciones son verticales 1080x1920 (Reels/TikTok/Shorts).
export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="TituloINM" component={TituloINM} durationInFrames={150} fps={30} width={1080} height={1920}
      defaultProps={esquemaTitulo} />
    <Composition id="TituloINMTransparente" component={TituloINM} durationInFrames={66} fps={30} width={1080} height={1920}
      defaultProps={{...esquemaTitulo, transparente: true, titulo: 'GANCHO', subtitulo: ''}} />
    <Composition id="Contador" component={Contador} durationInFrames={75} fps={30} width={1080} height={1920}
      defaultProps={{desde: 0, hasta: 100, sufijo: '%', etiqueta: 'DATO DE EJEMPLO', fuente: 'Fuente: pendiente', colorTexto: '#FFFFFF', colorResalte: '#8FC3FF'}} />
  </>
);
