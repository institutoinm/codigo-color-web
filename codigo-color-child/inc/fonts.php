<?php
/**
 * Fuentes: Cormorant Garamond + DM Sans.
 *
 * Estado final (Fase 0/1): fuentes servidas localmente desde /assets/fonts.
 * Puente V1: si aún no se han subido los woff2, se cargan desde Google Fonts
 *            para no romper la estética premium. Documentado en MANTENIMIENTO.md.
 *
 * @package codigo-color-child
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/** Detecta si las fuentes locales ya están disponibles. */
function cc_fonts_are_local() {
	return cc_has( '/assets/fonts/cormorant-garamond-500.woff2' );
}

function cc_fonts() {
	if ( cc_fonts_are_local() ) {
		// Estado final: @font-face local (assets/css/cc-fonts.css).
		wp_enqueue_style( 'cc-fonts', CC_URI . '/assets/css/cc-fonts.css', array(), cc_v( '/assets/css/cc-fonts.css' ) );
	} else {
		// Puente temporal V1.
		wp_enqueue_style(
			'cc-google-fonts',
			'https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=DM+Sans:wght@400;500&display=swap',
			array(),
			null
		);
	}
}
add_action( 'wp_enqueue_scripts', 'cc_fonts', 5 );

/** Preconnect solo mientras se use el puente de Google Fonts. */
add_action(
	'wp_head',
	function () {
		if ( ! cc_fonts_are_local() ) {
			echo '<link rel="preconnect" href="https://fonts.googleapis.com">' . "\n";
			echo '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>' . "\n";
		}
	},
	1
);
