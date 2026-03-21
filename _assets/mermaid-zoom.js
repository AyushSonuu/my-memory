// Mermaid zoom/pan controls
document.addEventListener('DOMContentLoaded', () => {
    initMermaidControls();
});

// Re-init on navigation (MkDocs instant loading)
if (typeof document$ !== 'undefined') {
    document$.subscribe(() => {
        setTimeout(initMermaidControls, 500);
    });
}

function initMermaidControls() {
    document.querySelectorAll('.mermaid').forEach((el) => {
        if (el.closest('.mermaid-wrapper')) return; // Already wrapped

        // Wrap mermaid in a container
        const wrapper = document.createElement('div');
        wrapper.className = 'mermaid-wrapper';

        // Create controls
        const controls = document.createElement('div');
        controls.className = 'mermaid-controls';
        controls.innerHTML = `
            <button class="zoom-in" title="Zoom In">+</button>
            <button class="zoom-out" title="Zoom Out">−</button>
            <button class="zoom-reset" title="Reset">⟲</button>
            <button class="zoom-fit" title="Fullscreen">⛶</button>
        `;

        el.parentNode.insertBefore(wrapper, el);
        wrapper.appendChild(controls);
        wrapper.appendChild(el);

        // State
        let scale = 1;
        let translateX = 0;
        let translateY = 0;
        let isDragging = false;
        let startX, startY;

        function applyTransform() {
            el.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
        }

        // Zoom buttons
        controls.querySelector('.zoom-in').addEventListener('click', (e) => {
            e.stopPropagation();
            scale = Math.min(scale * 1.25, 5);
            applyTransform();
        });

        controls.querySelector('.zoom-out').addEventListener('click', (e) => {
            e.stopPropagation();
            scale = Math.max(scale / 1.25, 0.3);
            applyTransform();
        });

        controls.querySelector('.zoom-reset').addEventListener('click', (e) => {
            e.stopPropagation();
            scale = 1;
            translateX = 0;
            translateY = 0;
            applyTransform();
        });

        controls.querySelector('.zoom-fit').addEventListener('click', (e) => {
            e.stopPropagation();
            // Toggle expanded view
            wrapper.classList.toggle('mermaid-expanded');
            if (!wrapper.classList.contains('mermaid-expanded')) {
                scale = 1;
                translateX = 0;
                translateY = 0;
                applyTransform();
            }
        });

        // Mouse wheel zoom
        wrapper.addEventListener('wheel', (e) => {
            e.preventDefault();
            const delta = e.deltaY > 0 ? 0.9 : 1.1;
            scale = Math.min(Math.max(scale * delta, 0.3), 5);
            applyTransform();
        }, { passive: false });

        // Pan with mouse drag
        el.addEventListener('mousedown', (e) => {
            isDragging = true;
            startX = e.clientX - translateX;
            startY = e.clientY - translateY;
            el.style.cursor = 'grabbing';
        });

        document.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            translateX = e.clientX - startX;
            translateY = e.clientY - startY;
            applyTransform();
        });

        document.addEventListener('mouseup', () => {
            isDragging = false;
            el.style.cursor = 'grab';
        });

        // Touch support
        let lastTouchDist = 0;
        el.addEventListener('touchstart', (e) => {
            if (e.touches.length === 1) {
                isDragging = true;
                startX = e.touches[0].clientX - translateX;
                startY = e.touches[0].clientY - translateY;
            } else if (e.touches.length === 2) {
                lastTouchDist = Math.hypot(
                    e.touches[0].clientX - e.touches[1].clientX,
                    e.touches[0].clientY - e.touches[1].clientY
                );
            }
        }, { passive: true });

        el.addEventListener('touchmove', (e) => {
            if (e.touches.length === 1 && isDragging) {
                translateX = e.touches[0].clientX - startX;
                translateY = e.touches[0].clientY - startY;
                applyTransform();
            } else if (e.touches.length === 2) {
                const dist = Math.hypot(
                    e.touches[0].clientX - e.touches[1].clientX,
                    e.touches[0].clientY - e.touches[1].clientY
                );
                if (lastTouchDist) {
                    scale = Math.min(Math.max(scale * (dist / lastTouchDist), 0.3), 5);
                    applyTransform();
                }
                lastTouchDist = dist;
            }
        }, { passive: true });

        el.addEventListener('touchend', () => {
            isDragging = false;
            lastTouchDist = 0;
        });
    });
}
