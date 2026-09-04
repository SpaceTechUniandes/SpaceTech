/**
 * nav.js — Chrome del sitio: header fijo, menú móvil y año del footer.
 */
(function () {
  'use strict';

  var body = document.body;
  var header = document.getElementById('header');
  var toggle = document.getElementById('nav-toggle');
  var menu = document.getElementById('nav-menu');

  /* --------------------------------------------------------
     Menú hamburguesa
     -------------------------------------------------------- */
  function setMenu(open) {
    body.classList.toggle('nav-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Cerrar menú de navegación' : 'Abrir menú de navegación');
  }

  function closeMenu() {
    if (body.classList.contains('nav-open')) {
      setMenu(false);
    }
  }

  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      setMenu(!body.classList.contains('nav-open'));
    });

    // Cierra el menú al elegir un destino
    menu.addEventListener('click', function (event) {
      if (event.target.closest('.nav__link') || event.target.closest('.mega__link')) {
        closeMenu();
      }
    });

    // Escape cierra el menú y devuelve el foco al botón
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && body.classList.contains('nav-open')) {
        closeMenu();
        toggle.focus();
      }
    });

    // Al pasar a desktop el panel deja de tener sentido
    window.matchMedia('(min-width: 768px)').addEventListener('change', closeMenu);
  }

  /* --------------------------------------------------------
     Mega menús: se abren al pasar el cursor en desktop y con
     click/teclado en cualquier tamaño.
     -------------------------------------------------------- */
  var menuItems = Array.prototype.slice.call(document.querySelectorAll('[data-menu]'));
  var hoverCapable = window.matchMedia('(hover: hover) and (pointer: fine) and (min-width: 768px)');

  function openMenu(item, open) {
    item.classList.toggle('is-open', open);
    item.querySelector('.nav__trigger').setAttribute('aria-expanded', String(open));
  }

  function closeAllMenus(except) {
    menuItems.forEach(function (item) {
      if (item !== except) openMenu(item, false);
    });
  }

  menuItems.forEach(function (item) {
    var trigger = item.querySelector('.nav__trigger');

    trigger.addEventListener('click', function () {
      var open = !item.classList.contains('is-open');
      closeAllMenus(item);
      openMenu(item, open);
    });

    // El panel es descendiente del <li>, así que el cursor puede bajar
    // hasta él sin que se dispare mouseleave.
    item.addEventListener('mouseenter', function () {
      if (hoverCapable.matches) {
        closeAllMenus(item);
        openMenu(item, true);
      }
    });

    item.addEventListener('mouseleave', function () {
      if (hoverCapable.matches) openMenu(item, false);
    });

    // Con teclado el menú se abre al activar el botón, no al recibir foco:
    // abrirlo en 'focus' haría que Escape lo cerrara y lo reabriera al
    // devolver el foco al disparador. Salir del item con Tab sí cierra.
    item.addEventListener('focusout', function (event) {
      if (!item.contains(event.relatedTarget)) openMenu(item, false);
    });
  });

  if (menuItems.length) {
    // Escape cierra el menú abierto y devuelve el foco a su disparador
    document.addEventListener('keydown', function (event) {
      if (event.key !== 'Escape') return;
      menuItems.forEach(function (item) {
        if (item.classList.contains('is-open')) {
          openMenu(item, false);
          item.querySelector('.nav__trigger').focus();
        }
      });
    });

    // Un click fuera de la navegación cierra todo
    document.addEventListener('click', function (event) {
      if (!event.target.closest('[data-menu]')) closeAllMenus(null);
    });

    // En desktop el panel dejaría de estar bajo el cursor al hacer scroll
    window.addEventListener('scroll', function () {
      if (hoverCapable.matches) closeAllMenus(null);
    }, { passive: true });
  }

  /* --------------------------------------------------------
     Header: fondo translúcido + blur tras 60px de scroll
     -------------------------------------------------------- */
  if (header) {
    var scrolled = false;

    var updateHeader = function () {
      var next = window.scrollY > 60;
      if (next !== scrolled) {
        scrolled = next;
        header.classList.toggle('header--scrolled', scrolled);
      }
    };

    window.addEventListener('scroll', updateHeader, { passive: true });
    updateHeader();
  }

  /* --------------------------------------------------------
     Año dinámico del footer
     -------------------------------------------------------- */
  var year = document.getElementById('footer-year');
  if (year) {
    year.textContent = String(new Date().getFullYear());
  }
})();
