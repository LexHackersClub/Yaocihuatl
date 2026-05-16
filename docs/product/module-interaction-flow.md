# Flujo e Interaccion Entre Modulos

Este documento describe como conviven Tlachia, Machiyotl, Chimalli y el portal publico dentro del ecosistema de Yaocihuatl. Su funcion es dar contexto producto-tecnico sobre interfaces, responsabilidades y flujo institucional, sin sustituir los contratos API ni la arquitectura de despliegue.

Yaocihuatl no es una aplicacion comercial de descarga libre para el publico general. Es una plataforma civica institucional bajo un paradigma B2G, disenada para ser desplegada, operada y gobernada por Organismos Publicos Locales Electorales (OPLEs) bajo su infraestructura, su marco de responsabilidad legal y sus obligaciones de proteccion de datos personales.

## Formas De Existencia

El sistema se organiza en tres experiencias principales conectadas a una API backend unificada:

```text
                     +------------------------------+
                     |   Landing page principal     |
                     |      yaocihuatl.com          |
                     +--------------+---------------+
                                    |
         +--------------------------+--------------------------+
         |                          |                          |
         v                          v                          v
+-----------------+       +-------------------+       +--------------------+
| Dashboard OPLE  |       | PWA protegida     |       | Portal publico     |
| Tlachia         |       | Machiyotl+Chimalli|       | Observatorio       |
+-----------------+       +-------------------+       +--------------------+
```

Estas experiencias no significan tres backends separados. Comparten identidad, auditoria, expedientes transversales y base de datos, pero cada modulo mantiene limites claros de responsabilidad.

## 1. Dashboard De Operacion Para OPLEs

**Modulo principal:** Tlachia.  
**Usuarios:** analistas de la Unidad Tecnica de lo Contencioso Electoral o area institucional equivalente.  
**Estado actual:** interfaz demo, tablas PostgreSQL y seed sintetico. API real pendiente.

El dashboard de operacion es una aplicacion web interna para personal autorizado. Su objetivo es mostrar alertas, senales explicables y patrones que requieren revision humana.

Responsabilidades:

- visualizar alertas por nivel de riesgo asistivo;
- mostrar senales que justifican la alerta;
- revisar menciones sanitizadas o autorizadas;
- auditar, descartar, pausar o escalar una alerta;
- vincular una alerta revisada con un expediente `core.cases`;
- notificar a la mujer protegida cuando proceda.

Limites:

- Tlachia no confirma VPMRG;
- no sustituye criterio de autoridad;
- no debe usar scraping invasivo;
- no debe acceder a comunicaciones privadas;
- no debe almacenar datos reales sin fuente, autorizacion, minimizacion y retencion documentadas.

## 2. PWA Para Mujeres Protegidas

**Modulos principales:** Machiyotl + Chimalli + guia de cese inmediato.  
**Usuarios:** mujeres protegidas incorporadas por una institucion responsable.  
**Estado actual:** pantallas demo y Chimalli backend funcional; Machiyotl real/PWA offline-first pendiente.

La experiencia de la mujer protegida debe vivir en una sola PWA. Separar el sello forense, la guia de reporte y la canalizacion legal en aplicaciones distintas fragmentaria un flujo que ocurre en momentos de urgencia.

La PWA debe poder abrirse desde navegador moderno y, cuando el navegador lo permita, instalarse en la pantalla de inicio. El objetivo de la instalacion no es crear una app comercial, sino habilitar una experiencia mas rapida, responsiva y eventualmente offline-first.

### Flujo Interno

1. **Machiyotl: sello de evidencia**

   La usuaria captura una pantalla, adjunta un archivo autorizado o registra un enlace. El objetivo productivo es que el hash SHA-256 se genere localmente en el navegador mediante Web Crypto API antes de subir contenido al servidor.

   Estado actual: existe modelo de datos y seed sintetico de evidencia. La implementacion real de hash local, carga segura y PWA offline-first esta pendiente.

2. **Cese inmediato en plataforma**

   Despues del sellado, la PWA debe guiar a la usuaria hacia reportes ante la plataforma correspondiente. El orden es importante: primero preservar evidencia, despues intentar mitigar el dano activo.

   Yaocihuatl no elimina contenido ni modera plataformas. Solo guia a la persona protegida para usar mecanismos oficiales de reporte.

3. **Chimalli: canalizacion asistida**

   Chimalli ordena la narrativa, extrae datos explicitos, aplica un test VPMRG asistivo y sugiere rutas preliminares para revision humana.

   Estado actual: Chimalli cuenta con endpoints MVP para chat, extraccion, test asistivo, sugerencia de jurisdiccion, RAG local y expediente HTML borrador.

4. **Boton de panico**

   La PWA debe mantener una accion visible para salir rapidamente a una pagina neutral y reducir exposicion en situaciones de riesgo fisico. Cualquier limpieza de cache o almacenamiento local debe documentarse cuidadosamente para no destruir evidencia ya sellada sin consentimiento ni registro.

## 3. Portal Publico De Verificacion Y Observatorio

**Modulos principales:** Observatory + verificacion Machiyotl.  
**Usuarios:** sociedad civil, academia, prensa, personas juzgadoras o revisoras autorizadas segun flujo.  
**Estado actual:** pantalla demo, tabla `observatory.aggregate_metrics` y seed sintetico.

El portal publico tiene dos funciones diferenciadas:

- publicar metricas agregadas y anonimizadas;
- permitir verificacion de hashes sin revelar contenido sensible.

El observatorio nunca debe exponer nombres, cuentas, URLs, contenido de evidencia, identificadores de agresores o informacion que permita reidentificar a una mujer protegida.

La verificacion de hash debe demostrar integridad, no abrir evidencia privada. El flujo objetivo es que una persona pueda ingresar un SHA-256 o escanear un QR de reporte forense y recibir una respuesta sobre coincidencia, estado y metadatos seguros.

## Landing Page Principal

La landing page en `yaocihuatl.com` funciona como entrada institucional y demostracion publica del proyecto. Tambien debe enrutar claramente hacia experiencias por rol.

Componentes recomendados:

- **Probar aplicacion:** selector de roles para entrar como mujer protegida, autoridad electoral, persona revisora u observacion ciudadana en modo demo.
- **Repositorio de GitHub:** enlace al codigo abierto y a la portabilidad Docker/on-premise.
- **Evidencia y marco normativo:** seccion que explique el corpus legal/RAG disponible, distinguiendo fuentes demo de corpus validado.
- **Validador de hashes:** entrada de hash demo o simulacion de QR para explicar integridad sin revelar datos.

La landing no debe prometer capacidades no implementadas. Debe distinguir entre prototipo desplegado, flujo objetivo y funciones pendientes de especificacion.

## Flujo Institucional Completo

```text
1. Observacion
   Tlachia detecta senales publicas o autorizadas.

2. Revision humana
   Analista OPLE revisa senales, contexto y limites.

3. Notificacion
   Si procede, se avisa a la mujer protegida o se abre expediente interno.

4. Sello
   Machiyotl preserva evidencia y registra hash/custodia.

5. Cese inmediato
   La PWA guia reportes oficiales ante plataformas.

6. Canalizacion
   Chimalli ordena narrativa, fuentes y ruta preliminar.

7. Expediente
   Core vincula alerta, evidencia, narrativa y asignaciones.

8. Revision institucional
   Autoridad competente evalua, corrige, descarta o continua.

9. Transparencia
   Observatory publica solo metricas agregadas y seguras.
```

## Contratos Entre Modulos

### Tlachia -> Core

Una alerta revisada puede originar o alimentar un caso transversal.

Datos esperados:

- `alert_id`;
- nivel de riesgo asistivo;
- senales explicables;
- menciones sanitizadas;
- estado de revision humana;
- actor institucional.

### Core -> Machiyotl

Un caso puede tener evidencias asociadas.

Datos esperados:

- `case_id`;
- `evidence_id`;
- `sha256_hash`;
- estado de evidencia;
- eventos de custodia.

### Machiyotl -> Chimalli

Chimalli puede recibir referencias a evidencia sellada, no necesariamente el contenido.

Datos esperados:

- hashes;
- estado de custodia;
- tipo de evidencia;
- plataforma o fuente declarada;
- notas autorizadas.

### Chimalli -> Core

Chimalli puede generar un borrador revisable para el expediente.

Datos esperados:

- narrativa estructurada;
- entidades extraidas;
- resultado asistivo del test;
- ruta preliminar;
- fuentes RAG consultadas;
- aviso de revision humana.

### Core/Audit -> Todos

Toda accion sensible debe registrar actor, momento, entidad afectada, resultado y metadata minima.

## Criterios De Implementacion

- Mantener una sola API versionada en `/api/v1`.
- Proteger rutas por rol antes de datos reales.
- Registrar auditoria por acceso a evidencia y cambios de estado.
- No mezclar datos demo con datos reales.
- No usar IA como decision final.
- No inventar fuentes legales.
- No romper separacion entre observacion, evidencia y canalizacion.
- Documentar cualquier integracion externa antes de activarla.

## Relacion Con Otros Documentos

- `ARCHITECTURE.md`: arquitectura general y despliegue.
- `docs/technical/architecture.md`: detalle tecnico por runtime y servicios.
- `docs/technical/api-contracts.md`: endpoints actuales y contratos pendientes.
- `docs/technical/data-model.md`: tablas y esquemas PostgreSQL.
- `docs/technical/deployment.md`: operacion Docker/AWS.
- `docs/product/Yaocihuatl_Propuesta_Final_v3.md`: propuesta producto amplia.
