/* =====================================================================
   TABLICE UE — script.js
   Vanilla JS. Dwie części:
   1. Przełączanie motywu Dark/Light (wzorzec z base-template projektu)
   2. Logika narzędzia: rozpoznawanie lokalizacji po numerze rejestracyjnym
      (zakładka "Sprawdź numer") oraz wyszukiwanie w drugą stronę
      (zakładka "Szukaj po lokalizacji")

   Dane (DATA) są wczytywane z osadzonego <script id="plate-data">,
   żeby cała aplikacja działała offline z jednego pliku index.html.
===================================================================== */

(function () {
  'use strict';

  /* -------------------------------------------------------------------
     1. PRZEŁĄCZANIE MOTYWU (DARK / LIGHT)
  ------------------------------------------------------------------- */
  const STORAGE_KEY = 'tablice-ue-theme';
  const root = document.documentElement;
  const toggleBtn = document.getElementById('theme-toggle');

  function getPreferredTheme() {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved === 'light' || saved === 'dark') return saved;
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    return prefersDark ? 'dark' : 'light';
  }

  function applyTheme(theme) {
    root.setAttribute('data-theme', theme);
    if (toggleBtn) toggleBtn.setAttribute('aria-pressed', String(theme === 'dark'));
  }

  function toggleTheme() {
    const current = root.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    applyTheme(next);
    localStorage.setItem(STORAGE_KEY, next);
  }

  applyTheme(getPreferredTheme());
  if (toggleBtn) toggleBtn.addEventListener('click', toggleTheme);

  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (!localStorage.getItem(STORAGE_KEY)) applyTheme(e.matches ? 'dark' : 'light');
  });

  /* -------------------------------------------------------------------
     2. DANE
  ------------------------------------------------------------------- */
  const DATA = JSON.parse(document.getElementById('plate-data').textContent);
  const countryOrder = Object.keys(DATA);

  function countryLabel(code) {
    const c = DATA[code];
    return `${c.flag} ${c.name}`;
  }

  function populateCountrySelect(sel) {
    sel.innerHTML = '';
    const geo = countryOrder.filter((c) => DATA[c].type === 'geographic');
    const nongeo = countryOrder.filter((c) => DATA[c].type !== 'geographic');

    const g1 = document.createElement('optgroup');
    g1.label = 'Systemy geograficzne (można rozpoznać region)';
    geo.forEach((code) => {
      const o = document.createElement('option');
      o.value = code;
      o.textContent = countryLabel(code);
      g1.appendChild(o);
    });

    const g2 = document.createElement('optgroup');
    g2.label = 'Systemy niegeograficzne';
    nongeo.forEach((code) => {
      const o = document.createElement('option');
      o.value = code;
      o.textContent = countryLabel(code);
      g2.appendChild(o);
    });

    sel.appendChild(g1);
    sel.appendChild(g2);
  }

  const selFwd = document.getElementById('country-fwd');
  const selRev = document.getElementById('country-rev');
  populateCountrySelect(selFwd);
  populateCountrySelect(selRev);
  selFwd.value = 'PL';
  selRev.value = 'PL';

  /* -------------------------------------------------------------------
     3. ZAKŁADKI (Sprawdź numer / Szukaj po lokalizacji)
  ------------------------------------------------------------------- */
  const tabButtons = document.querySelectorAll('.tab');
  const tabForward = document.getElementById('tab-forward');
  const tabReverse = document.getElementById('tab-reverse');

  tabButtons.forEach((btn) => {
    btn.addEventListener('click', () => {
      tabButtons.forEach((b) => {
        b.classList.remove('active');
        b.setAttribute('aria-selected', 'false');
      });
      btn.classList.add('active');
      btn.setAttribute('aria-selected', 'true');
      const tab = btn.dataset.tab;
      tabForward.hidden = tab !== 'forward';
      tabReverse.hidden = tab !== 'reverse';
    });
  });

  /* -------------------------------------------------------------------
     4. WYSZUKIWANIE W PRZÓD (numer → lokalizacja)
  ------------------------------------------------------------------- */
  function updateFwdMeta() {
    const code = selFwd.value;
    const c = DATA[code];
    const el = document.getElementById('country-meta-fwd');
    if (c.type === 'geographic') {
      el.innerHTML = `<b>Format:</b> ${c.plateFormat}<br><b>Poziom lokalizacji:</b> ${c.level}<br>${c.parseNote}`;
    } else {
      el.innerHTML = `⚠️ ${c.parseNote}`;
    }
  }
  selFwd.addEventListener('change', updateFwdMeta);
  updateFwdMeta();

  function extractLeadingLetters(raw) {
    const upper = raw.toUpperCase().trim();
    // Jeśli w numerze jest wyraźny separator (spacja/myślnik/kropka), prefiks regionu
    // to zwykle dokładnie to, co przed pierwszym separatorem (np. "M-AB 1234" -> "M").
    const sepMatch = upper.match(/^([A-ZΑ-ΩА-Я]+)[\s\-.]/);
    if (sepMatch) return { letters: sepMatch[1] };

    // Brak separatora — weź wiodący ciąg liter aż do pierwszej cyfry.
    const s = upper.replace(/[\s\-.]/g, '');
    let letters = '';
    for (const ch of s) {
      if (/[A-ZΑ-ΩА-Я]/.test(ch)) letters += ch;
      else break;
    }
    return { letters };
  }

  function findMatch(countryCode, rawInput) {
    const c = DATA[countryCode];
    if (c.type !== 'geographic') return { status: 'nogeo', country: c };

    // Specjalny przypadek: Białoruś — kod regionu to cyfra po myślniku na końcu.
    if (countryCode === 'BY') {
      const m = rawInput.trim().match(/-(\d)\s*$/) || rawInput.trim().match(/(\d)\s*$/);
      if (m) {
        const digit = m[1];
        const hit = c.entries.find((e) => e.codes.includes(digit));
        if (hit) return { status: 'hit', entry: hit, country: c, matchedCode: digit };
      }
      return { status: 'miss', country: c };
    }

    const { letters } = extractLeadingLetters(rawInput);
    if (!letters) return { status: 'miss', country: c };

    // zbuduj mapę code -> entry raz (cache)
    if (!c._codeMap) {
      c._codeMap = {};
      c.entries.forEach((e) => {
        e.codes.forEach((code) => {
          c._codeMap[code] = e;
        });
      });
      (c.historicalEntries || []).forEach((e) => {
        e.codes.forEach((code) => {
          if (!c._codeMap[code]) {
            c._codeMapHist = c._codeMapHist || {};
            c._codeMapHist[code] = e;
          }
        });
      });
    }

    // próbuj od najdłuższego prefiksu (max 3) w dół do 1 znaku
    const maxLen = Math.min(letters.length, 3);
    for (let len = maxLen; len >= 1; len--) {
      const candidate = letters.slice(0, len);
      if (c._codeMap[candidate]) {
        return { status: 'hit', entry: c._codeMap[candidate], country: c, matchedCode: candidate };
      }
    }
    // spróbuj też historycznych (np. Czechy)
    if (c._codeMapHist) {
      for (let len = maxLen; len >= 1; len--) {
        const candidate = letters.slice(0, len);
        if (c._codeMapHist[candidate]) {
          return { status: 'hit-historical', entry: c._codeMapHist[candidate], country: c, matchedCode: candidate };
        }
      }
    }
    return { status: 'miss', country: c };
  }

  function renderFwdResult(res) {
    const el = document.getElementById('fwd-result');
    if (res.status === 'nogeo') {
      el.innerHTML = `<div class="result-nogeo"><b>${res.country.flag} ${res.country.name}</b> nie koduje lokalizacji na tablicy rejestracyjnej.<br><br>${res.country.parseNote}</div>`;
      return;
    }
    if (res.status === 'miss') {
      el.innerHTML = `<div class="result-miss">Nie rozpoznano prefiksu dla <b>${res.country.name}</b>. Sprawdź czy numer jest wpisany poprawnie (format: ${res.country.plateFormat || '—'}).</div>`;
      return;
    }
    const e = res.entry;
    const histNote =
      res.status === 'hit-historical'
        ? '<div class="sub">⏱️ Kod z historycznego systemu (sprzed reformy) — może dotyczyć starszego pojazdu.</div>'
        : '';
    el.innerHTML = `
      <div class="result-hit">
        <div class="loc">${e.location}</div>
        <div class="sub">${res.country.flag} ${res.country.name}${e.region ? ' • ' + e.region : ''}${e.unit ? ' • ' + e.unit : ''}</div>
        <div class="sub">Rozpoznany kod: <span class="badge">${res.matchedCode}</span></div>
        ${histNote}
      </div>
    `;
  }

  const btnCheck = document.getElementById('btn-check');
  const plateInput = document.getElementById('plate-input');

  btnCheck.addEventListener('click', () => {
    const val = plateInput.value.trim();
    if (!val) {
      document.getElementById('fwd-result').innerHTML = '';
      return;
    }
    renderFwdResult(findMatch(selFwd.value, val));
  });

  plateInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') btnCheck.click();
  });

  /* -------------------------------------------------------------------
     5. WYSZUKIWANIE W DRUGĄ STRONĘ (lokalizacja → kody)
  ------------------------------------------------------------------- */
  let czMode = 'modern';
  const czToggle = document.getElementById('cz-toggle');

  function currentRevEntries() {
    const c = DATA[selRev.value];
    if (selRev.value === 'CZ') {
      return czMode === 'modern' ? c.entries : c.historicalEntries || [];
    }
    if (selRev.value === 'PL' && c.citiesIndex) {
      return c.entries.concat(c.citiesIndex);
    }
    return c.entries;
  }

  function updateRevMeta() {
    const c = DATA[selRev.value];
    const metaEl = document.getElementById('rev-meta');
    czToggle.hidden = selRev.value !== 'CZ';
    metaEl.hidden = false;
    if (c.type !== 'geographic') {
      metaEl.innerHTML = `⚠️ ${c.parseNote}`;
    } else {
      metaEl.innerHTML = `<b>Format:</b> ${c.plateFormat}<br><b>Poziom lokalizacji:</b> ${c.level}`;
    }
    renderRevList('');
  }

  function normalizeText(s) {
    return s
      .toLowerCase()
      .replace(/ł/g, 'l')
      .normalize('NFD')
      .replace(/[̀-ͯ]/g, ''); // usuń akcenty/diakrytyki (ą,ć,ę,ń,ó,ś,ź,ż)
  }

  function fuzzyMatch(query, text) {
    if (!query) return true;
    const nq = normalizeText(query);
    const nt = normalizeText(text);
    if (nt.includes(nq) || nq.includes(nt)) return true;
    // dopasowanie po wspólnym rdzeniu słowa (np. "brzeziny" vs "brzezinski")
    const minLen = Math.min(nq.length, nt.length);
    if (minLen < 4) return false;
    let common = 0;
    while (common < minLen && nq[common] === nt[common]) common++;
    return common >= 5 || (common >= 4 && common >= minLen - 2);
  }

  function renderRevList(query) {
    const listEl = document.getElementById('rev-list');
    const c = DATA[selRev.value];
    if (c.type !== 'geographic') {
      listEl.innerHTML = `<div class="empty-hint">Brak danych geograficznych dla tego kraju.</div>`;
      return;
    }
    const entries = currentRevEntries();
    const q = query.trim();
    let filtered = entries;
    if (q) {
      filtered = entries.filter((e) => fuzzyMatch(q, e.location) || fuzzyMatch(q, e.region || ''));
    }
    filtered = filtered.slice().sort((a, b) => a.location.localeCompare(b.location, 'pl'));
    if (filtered.length === 0) {
      listEl.innerHTML = `<div class="empty-hint">Brak wyników. Spróbuj innej nazwy.</div>`;
      return;
    }
    const cap = 200;
    const shown = filtered.slice(0, cap);
    listEl.innerHTML =
      shown
        .map(
          (e) => `
        <div class="list-item">
          <div>
            <div class="name">${e.location}</div>
            ${(e.region || e.unit) ? `<div class="region">${[e.region, e.unit].filter(Boolean).join(' • ')}</div>` : ''}
          </div>
          <div class="codes">${e.codes.map((code) => `<span class="badge">${code}</span>`).join('')}</div>
        </div>
      `
        )
        .join('') +
      (filtered.length > cap ? `<div class="empty-hint">…i ${filtered.length - cap} więcej. Doprecyzuj wyszukiwanie.</div>` : '');
  }

  selRev.addEventListener('change', updateRevMeta);
  document.getElementById('loc-search').addEventListener('input', (e) => {
    renderRevList(e.target.value);
  });
  czToggle.querySelectorAll('button').forEach((btn) => {
    btn.addEventListener('click', () => {
      czToggle.querySelectorAll('button').forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      czMode = btn.dataset.mode;
      renderRevList(document.getElementById('loc-search').value);
    });
  });

  updateRevMeta();

  /* -------------------------------------------------------------------
     6. ROK W STOPCE
  ------------------------------------------------------------------- */
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();
})();
