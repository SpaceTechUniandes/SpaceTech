/**
 * carousel.js — Carruseles de tarjetas (historia, benchmark).
 *
 * Cada carrusel es un [data-carousel] con una pista [data-carousel-track]
 * y tarjetas .card. Los controles y el contador se ocultan solos cuando hay
 * una tarjeta o ninguna, para que un carrusel a medio llenar no se vea roto.
 */
(function () {
  'use strict';

  var carruseles = Array.prototype.slice.call(document.querySelectorAll('[data-carousel]'));
  if (!carruseles.length) return;

  var sinMovimiento = window.matchMedia('(prefers-reduced-motion: reduce)');

  carruseles.forEach(function (carrusel) {
    var pista = carrusel.querySelector('[data-carousel-track]');
    var tarjetas = Array.prototype.slice.call(carrusel.querySelectorAll('.card'));
    var anterior = carrusel.querySelector('[data-carousel-prev]');
    var siguiente = carrusel.querySelector('[data-carousel-next]');
    var contador = carrusel.querySelector('[data-carousel-count]');
    var controles = carrusel.querySelector('[data-carousel-controls]');

    if (!pista) return;

    // Sin tarjetas o con una sola, los controles sobran
    if (tarjetas.length < 2) {
      if (controles) controles.hidden = true;
      if (contador && tarjetas.length === 1) contador.textContent = '01 / 01';
      // Un carrusel vacío no debe ocupar espacio: deja sitio al marco reservado
      if (!tarjetas.length) {
        var envoltorio = pista.closest('.carousel');
        if (envoltorio) envoltorio.hidden = true;
      }
      return;
    }

    var indice = 0;

    var formatear = function (n) {
      return String(n).padStart(2, '0');
    };

    var pintar = function () {
      if (contador) {
        contador.textContent = formatear(indice + 1) + ' / ' + formatear(tarjetas.length);
      }
      if (anterior) anterior.disabled = indice === 0;
      if (siguiente) siguiente.disabled = indice === tarjetas.length - 1;
    };

    var ir = function (nuevo) {
      indice = Math.max(0, Math.min(nuevo, tarjetas.length - 1));
      // scrollIntoView dentro de la pista: respeta el ancho real de la tarjeta
      // sin depender de cálculos de gap ni de márgenes.
      pista.scrollTo({
        left: tarjetas[indice].offsetLeft - pista.offsetLeft,
        behavior: sinMovimiento.matches ? 'auto' : 'smooth'
      });
      pintar();
    };

    if (anterior) {
      anterior.addEventListener('click', function () { ir(indice - 1); });
    }
    if (siguiente) {
      siguiente.addEventListener('click', function () { ir(indice + 1); });
    }

    // Flechas del teclado cuando el foco está dentro del carrusel
    carrusel.addEventListener('keydown', function (event) {
      if (event.key === 'ArrowLeft') { event.preventDefault(); ir(indice - 1); }
      if (event.key === 'ArrowRight') { event.preventDefault(); ir(indice + 1); }
    });

    // Si el usuario desliza con el dedo o el trackpad, el índice se resincroniza
    var esperando = false;
    pista.addEventListener('scroll', function () {
      if (esperando) return;
      esperando = true;
      window.requestAnimationFrame(function () {
        esperando = false;
        var centro = pista.scrollLeft + pista.clientWidth / 2;
        var cercana = 0;
        var menor = Infinity;
        tarjetas.forEach(function (tarjeta, i) {
          var medio = tarjeta.offsetLeft - pista.offsetLeft + tarjeta.offsetWidth / 2;
          var d = Math.abs(medio - centro);
          if (d < menor) { menor = d; cercana = i; }
        });
        if (cercana !== indice) {
          indice = cercana;
          pintar();
        }
      });
    }, { passive: true });

    pintar();
  });
})();
