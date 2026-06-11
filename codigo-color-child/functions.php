<?php
/**
 * Código Color — Child theme (Hello Elementor)
 *
 * Orquestador. Tres responsabilidades (Fase 1 A.3):
 *  1) Encolar el CSS versionado.
 *  2) Encolar el JS modular condicionalmente por página.
 *  3) Inyectar el schema JSON-LD.
 *
 * No contiene presentación ni contenido. Delega en /inc.
 *
 * @package codigo-color-child
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit; // Acceso directo no permitido.
}

define( 'CC_VER', '1.0.0' );
define( 'CC_DIR', get_stylesheet_directory() );
define( 'CC_URI', get_stylesheet_directory_uri() );

require_once CC_DIR . '/inc/helpers.php';
require_once CC_DIR . '/inc/fonts.php';
require_once CC_DIR . '/inc/enqueue.php';
require_once CC_DIR . '/inc/schema.php';
