<?php
/**
 * Encolado condicional de CSS y JS (Fase 0 / Fase 5).
 *
 * - Base (tokens + base + JS ligero) siempre.
 * - CSS de módulos y JS de movimiento solo en la landing.
 * - GSAP/ScrollTrigger se encolan solo si están presentes en /assets/vendor
 *   (V1: la arquitectura está lista; al dejar caer los archivos, se activan).
 * - Three.js / Orbe Cromático: NO se encolan en V1 (reservado a V1.5).
 *
 * @package codigo-color-child
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

function cc_enqueue_assets() {

	// --- Base, siempre ---
	wp_enqueue_style( 'cc-tokens', CC_URI . '/assets/css/cc-tokens.css', array(), cc_v( '/assets/css/cc-tokens.css' ) );
	wp_enqueue_style( 'cc-base', CC_URI . '/assets/css/cc-base.css', array( 'cc-tokens' ), cc_v( '/assets/css/cc-base.css' ) );

	// JS base ligero (sin dependencias, en footer).
	wp_enqueue_script( 'cc-motion-config', CC_URI . '/assets/js/cc-motion-config.js', array(), cc_v( '/assets/js/cc-motion-config.js' ), true );
	wp_enqueue_script( 'cc-fallbacks', CC_URI . '/assets/js/cc-fallbacks.js', array(), cc_v( '/assets/js/cc-fallbacks.js' ), true );

	// Expone la URL del tema a JS (para la carga dinámica del Orbe en V1.5).
	wp_add_inline_script( 'cc-motion-config', 'window.CC_THEME_URI=' . wp_json_encode( esc_url_raw( CC_URI ) ) . ';', 'after' );

	if ( ! cc_is_landing() ) {
		return;
	}

	// --- CSS de módulos de la landing (Fase 5 F) ---
	$modules = array(
		'hero', 'manifesto', 'editorial', 'definition', 'service', 'palette-grid',
		'method', 'universe', 'season-card', 'dimensions', 'benefits', 'application',
		'reveal', 'video-frame', 'authority', 'for-who', 'pricing', 'training',
		'faq', 'cta', 'trust', 'footer-links',
	);
	foreach ( $modules as $m ) {
		$rel = "/assets/css/cc-{$m}.css";
		if ( cc_has( $rel ) ) {
			wp_enqueue_style( "cc-{$m}", CC_URI . $rel, array( 'cc-base' ), cc_v( $rel ) );
		}
	}

	// --- GSAP (opcional, local). Si no está, cc-scroll degrada con elegancia. ---
	$gsap_deps = array();
	if ( cc_has( '/assets/vendor/gsap.min.js' ) ) {
		wp_enqueue_script( 'cc-gsap', CC_URI . '/assets/vendor/gsap.min.js', array(), cc_v( '/assets/vendor/gsap.min.js' ), true );
		$gsap_deps[] = 'cc-gsap';
		if ( cc_has( '/assets/vendor/ScrollTrigger.min.js' ) ) {
			wp_enqueue_script( 'cc-scrolltrigger', CC_URI . '/assets/vendor/ScrollTrigger.min.js', array( 'cc-gsap' ), cc_v( '/assets/vendor/ScrollTrigger.min.js' ), true );
			$gsap_deps[] = 'cc-scrolltrigger';
		}
	}

	// --- JS de movimiento e interacción (footer, post-LCP) ---
	wp_enqueue_script( 'cc-scroll', CC_URI . '/assets/js/cc-scroll-animations.js', array_merge( array( 'cc-fallbacks', 'cc-motion-config' ), $gsap_deps ), cc_v( '/assets/js/cc-scroll-animations.js' ), true );
	wp_enqueue_script( 'cc-palette', CC_URI . '/assets/js/cc-palette-interactive.js', array( 'cc-fallbacks' ), cc_v( '/assets/js/cc-palette-interactive.js' ), true );
	wp_enqueue_script( 'cc-faq', CC_URI . '/assets/js/cc-faq-filter.js', array(), cc_v( '/assets/js/cc-faq-filter.js' ), true );
}
add_action( 'wp_enqueue_scripts', 'cc_enqueue_assets', 20 );
