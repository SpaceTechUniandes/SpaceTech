# Backend — funciones serverless

Cada archivo `.js` de esta carpeta es una función serverless de Vercel. La
ruta se deduce del nombre: `api/health.js` responde en `/api/health`.

## Estado actual

El sitio es estático y **no necesita backend para funcionar**. Aquí sólo vive
`health.js`, un endpoint de comprobación que confirma que las funciones se
desplegaron bien. No hay lógica de negocio todavía.

## Dónde corre

| Entorno | ¿Funciona `/api/*`? |
|---|---|
| Vercel | Sí |
| GitHub Pages (spacetech.lat) | No — es hosting estático, devuelve 404 |

Esta es la diferencia de fondo entre los dos despliegues: Pages publica el
frontend; Vercel publica frontend y backend. Cualquier funcionalidad que
dependa de `/api/*` sólo estará disponible en Vercel.

## Añadir un endpoint

1. Crea `api/nombre.js` exportando un handler por defecto.
2. Recibe `(request, response)` al estilo Node.
3. Valida el método y responde con `response.status(...).json(...)`.

```js
export default function handler(request, response) {
  if (request.method !== 'POST') {
    response.setHeader('Allow', 'POST');
    return response.status(405).json({ error: 'Método no permitido' });
  }
  // ...
  return response.status(200).json({ ok: true });
}
```

Los secretos van como variables de entorno del proyecto en Vercel, nunca en
el repositorio. Se leen con `process.env.NOMBRE`.

## Pendiente

El formulario de inscripción de la sección de redes necesitará un endpoint
`POST /api/inscripcion`. Cuando se implemente, la página dejará de funcionar
completa en GitHub Pages y habrá que apuntar el dominio a Vercel.
