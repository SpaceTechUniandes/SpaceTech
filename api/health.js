/**
 * GET /api/health
 *
 * Comprobación de estado del backend. Sirve para verificar que las funciones
 * serverless quedaron desplegadas y responden.
 *
 * Sólo existe en Vercel: GitHub Pages es hosting estático y no ejecuta
 * funciones, así que en spacetech.lat esta ruta devuelve 404.
 */
export default function handler(request, response) {
  if (request.method !== 'GET') {
    response.setHeader('Allow', 'GET');
    return response.status(405).json({ error: 'Método no permitido' });
  }

  return response.status(200).json({
    service: 'spacetech-aess',
    status: 'ok',
    timestamp: new Date().toISOString(),
  });
}
