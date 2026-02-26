document.addEventListener('DOMContentLoaded', () => {
    const refreshBtn = document.getElementById('refreshBtn');
    const tabs = document.querySelectorAll('.tab');
    const sections = document.querySelectorAll('.content-section');

    // Tab switching logic
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const target = tab.getAttribute('data-target');

            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            sections.forEach(s => {
                if (s.id === target + 'Section') {
                    s.style.display = 'block';
                    // Fetch KB content if memory tab is clicked
                    if (target === 'memory') {
                        loadKB();
                    }
                } else {
                    s.style.display = 'none';
                }
            });
        });
    });

    async function loadKB() {
        const kbContainer = document.getElementById('kbContent');
        try {
            const response = await fetch('/api/kb');
            if (response.ok) {
                const data = await response.json();
                kbContainer.innerHTML = data.html;
            }
        } catch (error) {
            console.error('KB Load failed:', error);
            kbContainer.innerHTML = '<p>Error loading memory.</p>';
        }
    }

    // Refresh button logic
    refreshBtn.addEventListener('click', async () => {
        refreshBtn.classList.add('loading');
        refreshBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Refreshing...';

        try {
            const response = await fetch('/api/refresh');
            if (response.ok) {
                // To keep it simple for the MVP, we just reload the page for now
                window.location.reload();
            }
        } catch (error) {
            console.error('Refresh failed:', error);
            refreshBtn.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Error';
        } finally {
            refreshBtn.classList.remove('loading');
        }
    });
});
