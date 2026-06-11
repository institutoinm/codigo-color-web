<?php
/**
 * Schema JSON-LD (Fase 4 §E). Datos confirmados 10/06/2026.
 *
 * Se imprime en la landing. Organization, Person (Cristina Barriga con sameAs
 * confirmados), Service con OfferCatalog (180/590/1290 €), WebSite, Breadcrumb
 * y FAQPage con las preguntas priorizadas.
 *
 * Guardrails: sin tipos médicos; el INM no aparece como sameAs visible.
 *
 * @package codigo-color-child
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

function cc_schema_jsonld() {
	if ( ! cc_is_landing() ) {
		return;
	}

	$home = trailingslashit( home_url( '/' ) );
	$org  = $home . '#organization';
	$per  = $home . '#cristina-barriga';

	$faqs = array(
		array( '¿Qué es la colorimetría?', 'La colorimetría es el análisis que identifica los colores que favorecen a cada persona según su rostro: subtono, temperatura, contraste, luminosidad e intensidad. Construye una paleta personal aplicable a maquillaje, ropa, cabello e imagen profesional con criterio.' ),
		array( '¿Qué es el análisis cromático personal?', 'El análisis cromático personal es el proceso de observar el rostro real y compararlo con telas profesionales para determinar qué colores armonizan con la persona, valorando subtono, contraste, luminosidad e intensidad antes de definir la paleta.' ),
		array( '¿Cómo saber qué colores me favorecen?', 'Para saberlo se analiza el subtono (cálido o frío), el contraste facial, la luminosidad y la intensidad, y se contrasta el rostro con telas de distintos colores. Los tonos que iluminan la piel y unifican el rostro son los que favorecen.' ),
		array( '¿Cómo es un análisis de colorimetría paso a paso?', 'Sigue cinco pasos: observación del rostro, comparación con telas profesionales, diagnóstico de subtono, contraste, luminosidad e intensidad, construcción de la paleta personal y aplicación a maquillaje, ropa y cabello.' ),
		array( '¿Cuáles son las estaciones cromáticas?', 'Son cuatro familias de color: primavera (cálida y clara), verano (fría y suave), otoño (cálida y profunda) e invierno (frío e intenso). Cada persona armoniza con una, con subtipos según contraste e intensidad.' ),
		array( '¿Qué es el subtono de la piel?', 'El subtono es la tonalidad de fondo de la piel, independiente del bronceado: cálido (dorado), frío (rosado), neutro u oliva. Determinarlo es el primer paso de la colorimetría.' ),
		array( '¿Qué diferencia hay entre colorimetría y armocromía?', 'Nombran lo mismo: el análisis de los colores que favorecen a una persona. «Armocromía» es el término italiano popularizado en redes; «colorimetría» y «análisis cromático personal» son las denominaciones profesionales en español.' ),
		array( '¿La colorimetría sirve para el maquillaje?', 'Sí. La paleta personal se traduce al maquillaje real: bases que respetan el subtono, correctores, labiales, sombras, coloretes e intensidad según el contraste y la armonía facial. El maquillaje deja de corregir y empieza a favorecer.' ),
		array( '¿El diagnóstico se puede hacer online?', 'Sí. Código Color realiza el diagnóstico online o presencial en Madrid. La modalidad online requiere buena luz natural y fotografías correctas, y adapta el análisis y la entrega de recomendaciones al formato elegido.' ),
		array( '¿Cuánto cuesta un diagnóstico de colorimetría en Código Color?', 'Código Color tiene tres modalidades: Online Express por 180 €, Código Color Signature presencial en Madrid por 590 € y Código Color Elite por 1.290 €. También hay tarjeta regalo desde 590 €.' ),
		array( '¿Cuánto dura una sesión de diagnóstico?', 'Depende de la modalidad: Online Express dura 60-90 minutos por videollamada; Código Color Signature, de 3 a 4 horas presenciales en Madrid; y Código Color Elite se desarrolla en dos sesiones.' ),
		array( '¿Quién dirige Código Color?', 'Código Color está dirigido por Cristina Barriga, especialista en colorimetría e imagen personal, con formación en Asesoría Integral de Imagen Personal, certificados IMPE0209 (Maquillaje Integral) e IMPE0210 (Tratamientos Estéticos) y más de una década de análisis facial.' ),
		array( '¿La colorimetría funciona en piel madura, oscura o con canas?', 'Sí. La colorimetría analiza subtono, contraste e intensidad, presentes en cualquier piel y edad. En piel madura, oscura o con canas se ajusta la aplicación de la paleta al contraste actual del rostro, sin etiquetas rígidas.' ),
	);

	$main_entity = array();
	foreach ( $faqs as $f ) {
		$main_entity[] = array(
			'@type'          => 'Question',
			'name'           => $f[0],
			'acceptedAnswer' => array(
				'@type' => 'Answer',
				'text'  => $f[1],
			),
		);
	}

	$graph = array(
		array(
			'@type'         => 'Organization',
			'@id'           => $org,
			'name'          => 'Código Color',
			'url'           => $home,
			'description'   => 'Método de colorimetría y asesoría integral de imagen personal dirigido por Cristina Barriga.',
			'founder'       => array( '@id' => $per ),
			'areaServed'    => array( 'Madrid', 'España', 'Online' ),
			'knowsLanguage' => array( 'es', 'en', 'it' ),
			'email'         => 'contacto@cristinabarriga.com',
			'telephone'     => '+34 682 17 26 21',
		),
		array(
			'@type'         => 'Person',
			'@id'           => $per,
			'name'          => 'Cristina Pilar Barriga Ramos',
			'alternateName' => 'Cristina Barriga',
			'jobTitle'      => 'Directora de Código Color · especialista en colorimetría e imagen personal',
			'homeLocation'  => array(
				'@type' => 'Place',
				'name'  => 'Madrid, España',
			),
			'knowsAbout'    => array(
				'Colorimetría', 'Asesoría Integral de Imagen Personal', 'Diagnóstico cromático',
				'Maquillaje Integral', 'Tratamientos Estéticos', 'Análisis visual', 'Visagismo',
				'Armonía facial', 'Imagen profesional', 'Estética avanzada', 'Docencia',
			),
			'sameAs'        => array(
				'https://cristinabarriga.com/',
				'https://cristinabarriga.com/bio/',
				'https://www.linkedin.com/in/cristina-barriga/',
				'https://www.amazon.com/author/cristinabarriga',
			),
		),
		array(
			'@type'          => 'Service',
			'@id'            => $home . '#servicio-diagnostico',
			'name'           => 'Diagnóstico cromático Código Color',
			'serviceType'    => 'Colorimetría y asesoría integral de imagen personal',
			'provider'       => array( '@id' => $org ),
			'areaServed'     => array( 'Madrid', 'Online' ),
			'description'    => 'Análisis cromático e imagen personal que estudia subtono, contraste facial, luminosidad e intensidad para construir una paleta personal aplicable a maquillaje, ropa, cabello e imagen profesional.',
			'hasOfferCatalog' => array(
				'@type'           => 'OfferCatalog',
				'name'            => 'Servicios Código Color',
				'itemListElement' => array(
					array(
						'@type'       => 'Offer',
						'name'        => 'Online Express',
						'price'       => '180',
						'priceCurrency' => 'EUR',
						'description' => 'Diagnóstico de color por videollamada (60-90 min): análisis preliminar, paleta orientativa, recomendaciones de color y PDF resumen.',
					),
					array(
						'@type'       => 'Offer',
						'name'        => 'Código Color Signature',
						'price'       => '590',
						'priceCurrency' => 'EUR',
						'description' => 'Sesión presencial en Madrid (3-4 h): colorimetría completa, visagismo, estudio facial, paleta personalizada, carta digital, recomendaciones de maquillaje, cabello y accesorios e informe personalizado.',
					),
					array(
						'@type'       => 'Offer',
						'name'        => 'Código Color Elite',
						'price'       => '1290',
						'priceCurrency' => 'EUR',
						'description' => 'Dos sesiones: todo lo de Signature más estilo personal, silueta, vestuario, personal shopping estratégico, revisión de armario y dossier premium.',
					),
				),
			),
		),
		array(
			'@type'      => 'WebSite',
			'@id'        => $home . '#website',
			'url'        => $home,
			'name'       => 'Código Color',
			'inLanguage' => 'es-ES',
			'publisher'  => array( '@id' => $org ),
		),
		array(
			'@type'           => 'BreadcrumbList',
			'itemListElement' => array(
				array(
					'@type'    => 'ListItem',
					'position' => 1,
					'name'     => 'Inicio',
					'item'     => $home,
				),
			),
		),
		array(
			'@type'      => 'FAQPage',
			'@id'        => $home . '#faq',
			'mainEntity' => $main_entity,
		),
	);

	$data = array(
		'@context' => 'https://schema.org',
		'@graph'   => $graph,
	);

	echo '<script type="application/ld+json">'
		. wp_json_encode( $data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE )
		. '</script>' . "\n";
}
add_action( 'wp_head', 'cc_schema_jsonld', 20 );
