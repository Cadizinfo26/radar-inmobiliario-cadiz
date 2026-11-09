# Radar Inmobiliario Cádiz — prototipo gratuito

**Estado:** primera versión de descubrimiento indirecto. NO rastrea de forma exhaustiva los portales, NO verifica anuncios y NO identifica automáticamente precios, ocupación ni rentabilidad.

## Instalación desde GitHub
1. Sube los archivos y carpetas de este paquete a la raíz de tu repositorio público, conservando las rutas (`.github/workflows/busqueda.yml`, `data/results.json`, etc.).
2. En **Actions**, abre **Buscar pistas inmobiliarias** y pulsa **Run workflow** para la primera prueba. Puede requerir habilitar Actions.
3. En **Settings → Pages**, elige **Deploy from a branch**, rama `main`, carpeta `/ (root)` y guarda. La web aparecerá en `https://TU-USUARIO.github.io/radar-inmobiliario-cadiz/` cuando se publique.
4. GitHub Actions intentará ejecutar la búsqueda diariamente; los horarios programados pueden retrasarse y el proveedor del índice puede bloquear consultas o no ofrecer resultados. Comprueba el registro en Actions.

## Qué hace realmente
- Ejecuta 65 consultas de descubrimiento (13 fuentes × 5 municipios) a un buscador externo (RSS de Bing).
- Solo conserva URLs cuyo dominio coincide con la fuente buscada.
- Guarda resultados en `data/results.json`, con historial de primera y última detección.
- Registra errores y ausencia de resultados sin afirmar que no existen inmuebles.
- Muestra pistas con enlaces en el panel HTML.

## Limitaciones y siguientes pasos
- Un resultado indexado **no** equivale a un anuncio vigente, ni su presencia garantiza cobertura.
- El RSS de Bing puede dejar de funcionar o limitar las consultas sin aviso. La ejecución registra errores, pero el método no tiene garantías.
- La publicación es **pública**: no añadas contraseñas, datos personales ni claves privadas al repositorio.
- Para búsqueda real, hay que crear y validar conectores específicos por portal respetando sus condiciones y las restricciones técnicas; para alertas hace falta integrar un canal de notificación.
