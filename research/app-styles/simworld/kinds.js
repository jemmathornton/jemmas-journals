// tags each lot card with a lot-type family (mock-up only), read from the card's own type label
document.querySelectorAll('a.listing').forEach(a => {
  const t = (a.querySelector('.type')?.textContent || '').toLowerCase();
  let k = 'other';
  if (/rental/.test(t)) k = 'rental';
  else if (/residential|starter|home/.test(t)) k = 'home';
  else if (/restaurant|bar|lounge|caf|diner|bakery|boba|nightclub|pub/.test(t)) k = 'food';
  else if (/retail|shop|store|thrift|market/.test(t)) k = 'shop';
  else if (/park|library|gym|museum|pool|community|spa|club|centre|center|cemetery|arts|marketplace|karaoke|festival|school|hall/.test(t)) k = 'community';
  a.dataset.kind = k;
});
