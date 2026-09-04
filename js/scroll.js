/**
 * scroll.js — Scroll suave, animaciones de entrada, sección activa y parallax.
 */
(function () {
  'use strict';

  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  /* --------------------------------------------------------
     Animaciones de entrada: .reveal → .is-visible
     -------------------------------------------------------- */
  var revealItems = document.querySelectorAll('.reveal');

  if (reducedMotion.matches) {
    // Sin animación: el contenido se muestra de inmediato
    revealItems.forEach(function (item) {
      item.classList.add('is-visible');
    });
  } else {
    var revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -10% 0px' });

    revealItems.forEach(function (item) {
      revealObserver.observe(item);
    });
  }

  /* --------------------------------------------------------
     Enlace activo del nav según la sección visible
     -------------------------------------------------------- */
  /* Sólo los enlaces a un ancla de esta misma página. En las páginas de
     división el nav apunta a "../index.html#seccion", que no es un selector
     CSS válido: pasarlo a querySelector lanzaría y cortaría el resto del
     script (animaciones, scroll suave y parallax). */
  var navLinks = Array.prototype.slice.call(document.querySelectorAll('.nav__link'))
    .filter(function (link) {
      var href = link.getAttribute('href') || '';
      return href.charAt(0) === '#' && href.length > 1;
    });

  var sections = navLinks
    .map(function (link) {
      return document.querySelector(link.getAttribute('href'));
    })
    .filter(Boolean);

  if (sections.length) {
    var setActive = function (id) {
      navLinks.forEach(function (link) {
        link.classList.toggle('nav__link--active', link.getAttribute('href') === '#' + id);
      });
    };

    var sectionObserver = new IntersectionObserver(function (entries) {
      // Gana la sección visible más cercana al tope del viewport
      var visible = entries
        .filter(function (entry) { return entry.isIntersecting; })
        .sort(function (a, b) { return a.boundingClientRect.top - b.boundingClientRect.top; })[0];

      if (visible) {
        setActive(visible.target.id);
      }
    }, { rootMargin: '-45% 0px -45% 0px' });

    sections.forEach(function (section) {
      sectionObserver.observe(section);
    });
  }

  /* --------------------------------------------------------
     Scroll suave para los enlaces ancla
     -------------------------------------------------------- */
  document.addEventListener('click', function (event) {
    var link = event.target.closest('a[href^="#"]');
    if (!link) return;

    var id = link.getAttribute('href').slice(1);
    if (!id) return;

    var target = document.getElementById(id);
    if (!target) return;

    event.preventDefault();
    target.scrollIntoView({
      behavior: reducedMotion.matches ? 'auto' : 'smooth',
      block: 'start'
    });

    // Mantiene la URL sincronizada sin provocar un salto adicional
    history.pushState(null, '', '#' + id);
  });

  /* --------------------------------------------------------
     Parallax sutil del hero — sólo desktop y sin movimiento reducido
     -------------------------------------------------------- */
  var backdrop = document.getElementById('hero-backdrop');
  var wideScreen = window.matchMedia('(min-width: 768px)');

  if (backdrop) {
    var ticking = false;

    var applyParallax = function () {
      ticking = false;

      if (reducedMotion.matches || !wideScreen.matches) {
        backdrop.style.transform = '';
        return;
      }

      // El fondo avanza a la mitad de la velocidad del scroll
      backdrop.style.transform = 'translate3d(0, ' + (window.scrollY * 0.5) + 'px, 0)';
    };

    window.addEventListener('scroll', function () {
      if (!ticking) {
        ticking = true;
        window.requestAnimationFrame(applyParallax);
      }
    }, { passive: true });

    applyParallax();
  }
})();
