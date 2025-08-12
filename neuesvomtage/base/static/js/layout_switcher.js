$(function () {
    const STORAGE_KEY = 'layout'; // values: 'multi' | 'single'
    const DEFAULT_LAYOUT = 'multi';

    const getStoredLayout = () => localStorage.getItem(STORAGE_KEY) || DEFAULT_LAYOUT;
    const setStoredLayout = (layout) => localStorage.setItem(STORAGE_KEY, layout);

    const applyLayout = (layout) => {
        const root = document.documentElement;
        root.classList.remove('layout-multi', 'layout-single');
        root.classList.add(layout === 'single' ? 'layout-single' : 'layout-multi');

        const btn = document.getElementById('layout-toggle');
        if (btn) {
            const icon = btn.querySelector('i');
            if (icon) {
                icon.className = layout === 'single' ? 'fas fa-bars fa-fw' : 'fas fa-columns fa-fw';
            }
            btn.setAttribute('aria-pressed', layout === 'single' ? 'true' : 'false');
            btn.title = layout === 'single' ? 'Single column' : 'Multi column';
        }
    };

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
})
