// ADC 3K — Import river scout results into site-intel.html
// Open site-intel.html → DevTools Console → paste this:

(async function() {
  const resp = await fetch('data/river_sites.json');
  const newSites = await resp.json();
  const existing = JSON.parse(localStorage.getItem('adc3k_sites') || '[]');
  const existingIds = new Set(existing.map(s => s.id));
  const toAdd = newSites.filter(s => !existingIds.has(s.id));
  localStorage.setItem('adc3k_sites', JSON.stringify([...existing, ...toAdd]));
  console.log('Imported ' + toAdd.length + ' new river sites. Reload the page.');
  location.reload();
})();
