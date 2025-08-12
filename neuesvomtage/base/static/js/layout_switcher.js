(() => {
  'use strict'

  const STORAGE_KEY = 'layout'; // values: 'multi' | 'single'
  const DEFAULT_LAYOUT = 'multi';

  const getStoredLayout = () => localStorage.getItem(STORAGE_KEY) || DEFAULT_LAYOUT;
  const setStoredLayout = (layout) => localStorage.setItem(STORAGE_KEY, layout);

  const applyLayout = (layout) => {
    const body = document.body;
    body.classList.remove('layout-multi', 'layout-single');
    body.classList.add(layout === 'single' ? 'layout-single' : 'layout-multi');

    // Update toggle button icon/title if present
    const btn = document.getElementById('layout-toggle');
    if (btn) {
      const icon = btn.querySelector('i');
      if (icon) {
        // columns icon for multi, bars icon for single
        icon.className = layout === 'single' ? 'fas fa-bars fa-fw' : 'fas fa-columns fa-fw';
      }
      btn.setAttribute('aria-pressed', layout === 'single' ? 'true' : 'false');
      btn.title = layout === 'single' ? 'Single column' : 'Multi column';
    }
  };

  // Apply immediately so CSS layout is correct ASAP
  document.addEventListener('DOMContentLoaded', () => {
    const current = getStoredLayout();
    applyLayout(current);

    const btn = document.getElementById('layout-toggle');
    if (btn) {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const current = getStoredLayout();
        const next = current === 'single' ? 'multi' : 'single';
        setStoredLayout(next);
        applyLayout(next);
      });
    }
  });
})();
