// Footer year
document.querySelectorAll('#year').forEach(el => { el.textContent = new Date().getFullYear(); });

// Mobile nav toggle
const navToggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');

if (navToggle && navLinks) {
  navToggle.addEventListener('click', () => {
    const isOpen = navLinks.classList.toggle('open');
    navToggle.classList.toggle('open', isOpen);
    navToggle.setAttribute('aria-expanded', String(isOpen));
  });

  navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      navLinks.classList.remove('open');
      navToggle.classList.remove('open');
      navToggle.setAttribute('aria-expanded', 'false');
    });
  });
}

// Contact form (front-end only — no backend wired up yet)
const contactForm = document.getElementById('contactForm');
if (contactForm) {
  contactForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const note = document.getElementById('formNote');
    note.textContent = 'Bedankt voor je bericht! Ik neem zo snel mogelijk contact met je op.';
    contactForm.reset();
  });
}



/* ============================================================
   TOEGANKELIJKE LIGHTBOX VOOR PROCES-BEELDEN
   ============================================================ */
const zoomableImages = document.querySelectorAll('.proj-zoomable, [data-lightbox]');

if (zoomableImages.length > 0) {
  // Bouw of selecteer lightbox overlay
  let lightbox = document.getElementById('projLightbox');
  if (!lightbox) {
    lightbox = document.createElement('div');
    lightbox.id = 'projLightbox';
    lightbox.className = 'proj-lightbox';
    lightbox.setAttribute('role', 'dialog');
    lightbox.setAttribute('aria-modal', 'true');
    lightbox.setAttribute('aria-label', 'Afbeelding uitvergroot bekijken');
    lightbox.innerHTML = `
      <button class="proj-lightbox-close" id="projLightboxClose" aria-label="Sluit afbeelding">&times;</button>
      <button class="proj-lightbox-nav proj-lightbox-prev" id="projLightboxPrev" aria-label="Vorige afbeelding">&#8592;</button>
      <div class="proj-lightbox-content">
        <img class="proj-lightbox-img" id="projLightboxImg" src="" alt="">
        <p class="proj-lightbox-caption" id="projLightboxCaption"></p>
      </div>
      <button class="proj-lightbox-nav proj-lightbox-next" id="projLightboxNext" aria-label="Volgende afbeelding">&#8594;</button>
    `;
    document.body.appendChild(lightbox);
  }

  const lbImg = document.getElementById('projLightboxImg');
  const lbCaption = document.getElementById('projLightboxCaption');
  const lbClose = document.getElementById('projLightboxClose');
  const lbPrev = document.getElementById('projLightboxPrev');
  const lbNext = document.getElementById('projLightboxNext');

  const galleryItems = Array.from(zoomableImages);
  let currentIndex = -1;
  let lastFocusedElement = null;

  function openLightbox(index) {
    if (index < 0 || index >= galleryItems.length) return;
    currentIndex = index;
    lastFocusedElement = document.activeElement;

    const el = galleryItems[currentIndex];
    const targetImg = el.tagName === 'IMG' ? el : (el.querySelector('img') || el);
    const src = el.getAttribute('data-full') || targetImg.getAttribute('data-full') || targetImg.currentSrc || targetImg.src || el.src;
    const alt = targetImg.getAttribute('alt') || el.getAttribute('alt') || '';
    const captionText = el.getAttribute('data-caption') || targetImg.getAttribute('data-caption') || alt;

    lbImg.src = src;
    lbImg.alt = alt;
    lbCaption.textContent = captionText;

    // Toon/verberg prev/next als er maar 1 item is
    if (galleryItems.length <= 1) {
      lbPrev.style.display = 'none';
      lbNext.style.display = 'none';
    } else {
      lbPrev.style.display = 'flex';
      lbNext.style.display = 'flex';
    }

    lightbox.classList.add('active');
    document.body.style.overflow = 'hidden';
    lbClose.focus();
  }

  function closeLightbox() {
    lightbox.classList.remove('active');
    document.body.style.overflow = '';
    lbImg.src = '';
    if (lastFocusedElement) {
      lastFocusedElement.focus();
    }
  }

  function showPrev() {
    if (galleryItems.length <= 1) return;
    const newIndex = (currentIndex - 1 + galleryItems.length) % galleryItems.length;
    openLightbox(newIndex);
  }

  function showNext() {
    if (galleryItems.length <= 1) return;
    const newIndex = (currentIndex + 1) % galleryItems.length;
    openLightbox(newIndex);
  }

  // Klik event handlers
  galleryItems.forEach((img, idx) => {
    img.addEventListener('click', () => {
      openLightbox(idx);
    });

    // Toegankelijk via toetsenbord (Enter of Spatie)
    if (!img.hasAttribute('tabindex')) {
      img.setAttribute('tabindex', '0');
      img.setAttribute('role', 'button');
      img.setAttribute('aria-haspopup', 'dialog');
      img.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          openLightbox(idx);
        }
      });
    }
  });

  lbClose.addEventListener('click', closeLightbox);
  lbPrev.addEventListener('click', (e) => { e.stopPropagation(); showPrev(); });
  lbNext.addEventListener('click', (e) => { e.stopPropagation(); showNext(); });

  lightbox.addEventListener('click', (e) => {
    if (e.target === lightbox) {
      closeLightbox();
    }
  });

  // Toetsenbordbediening (Esc, Pijltjes, Focus trap)
  document.addEventListener('keydown', (e) => {
    if (!lightbox.classList.contains('active')) return;

    if (e.key === 'Escape') {
      e.preventDefault();
      closeLightbox();
    } else if (e.key === 'ArrowLeft') {
      e.preventDefault();
      showPrev();
    } else if (e.key === 'ArrowRight') {
      e.preventDefault();
      showNext();
    } else if (e.key === 'Tab') {
      // Eenvoudige focus trap
      const focusables = [lbClose, lbPrev, lbNext].filter(el => el.style.display !== 'none');
      const first = focusables[0];
      const last = focusables[focusables.length - 1];

      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }
  });
}

/* ============================================================
   STICKY PROCES TOC SCROLLSPY (DETAILPAGINA'S)
   ============================================================ */
const tocLinks = document.querySelectorAll('.proj-toc-list a');
const stepSections = document.querySelectorAll('.proj-step-item, .project-text section');

if (tocLinks.length > 0 && stepSections.length > 0) {
  const observerOptions = {
    root: null,
    rootMargin: '-20% 0px -70% 0px',
    threshold: 0
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute('id');
        tocLinks.forEach(link => {
          if (link.getAttribute('href') === `#${id}`) {
            link.classList.add('is-active');
            link.setAttribute('aria-current', 'true');
          } else {
            link.classList.remove('is-active');
            link.removeAttribute('aria-current');
          }
        });
      }
    });
  }, observerOptions);

  stepSections.forEach(section => {
    observer.observe(section);
  });
}
