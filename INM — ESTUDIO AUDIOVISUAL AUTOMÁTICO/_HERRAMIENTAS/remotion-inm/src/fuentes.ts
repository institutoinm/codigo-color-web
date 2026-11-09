import {staticFile} from 'remotion';
import {loadFont} from './cargarFuente';
export const cargarMontserrat = () => {
  loadFont('Montserrat Black', staticFile('Montserrat-Black.ttf'));
  loadFont('Montserrat SemiBold', staticFile('Montserrat-SemiBold.ttf'));
};
