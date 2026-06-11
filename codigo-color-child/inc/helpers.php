<?php
/**
 * Utilidades del tema.
 *
 * @package codigo-color-child
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * ¿Estamos en la landing (hub central)?
 * Los satélites futuros añadirán aquí sus propias condiciones.
 */
function cc_is_landing() {
	return is_front_page();
}

/**
 * Versión de un asset para cache busting (Fase 0).
 * Usa la fecha de modificación del archivo; si no existe, la versión del tema.
 *
 * @param string $rel Ruta relativa al tema, empezando por «/».
 * @return string|int
 */
function cc_v( $rel ) {
	$file = CC_DIR . $rel;
	return file_exists( $file ) ? filemtime( $file ) : CC_VER;
}

/**
 * ¿Existe un asset en el tema?
 *
 * @param string $rel Ruta relativa al tema.
 * @return bool
 */
function cc_has( $rel ) {
	return file_exists( CC_DIR . $rel );
}
