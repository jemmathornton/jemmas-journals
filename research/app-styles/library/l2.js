(() => {
  // give each shelf link its shelf's colour (the dot already carries it), so the link can be drawn as a spine
  document.querySelectorAll('.nav a').forEach(a => { const d = a.querySelector('.dot'); if (d) { a.style.setProperty('--c', d.style.getPropertyValue('--c')); a.classList.add('spine-link'); } });
  // the banner's covers stand on boards: measure one cover so the boards fall between the rows
  const hs = document.querySelector('.hero-shelf');
  if (hs) {
    const img = hs.querySelector('img');
    const h = img.getBoundingClientRect().height, g = parseFloat(getComputedStyle(hs).rowGap) || 0;
    hs.style.setProperty('--h', h + 'px'); hs.style.setProperty('--g', g + 'px');
  }
})();
