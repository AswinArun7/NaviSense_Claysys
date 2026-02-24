/* ═══════════════════════════════════════════════════════════════════
   NAVISENSE — app.js
   Multi-step Wizard, Interactivity, and Mock Itinerary Generation
═══════════════════════════════════════════════════════════════════ */

'use strict';

/* ── State ── */
const state = {
  currentStep: 1,
  totalSteps: 4,
  selectedBudget: null,
  selectedPurposes: [],
  selectedPace: null,
  checkpoints: [],
};

/* ── Destination suggestions ── */
const DESTINATIONS = [
  { emoji: '🗼', name: 'Paris, France' },
  { emoji: '🏯', name: 'Kyoto, Japan' },
  { emoji: '🏝️', name: 'Maldives' },
  { emoji: '🏔️', name: 'Swiss Alps, Switzerland' },
  { emoji: '🌆', name: 'New York City, USA' },
  { emoji: '🗽', name: 'New York, USA' },
  { emoji: '🎭', name: 'Rome, Italy' },
  { emoji: '🌉', name: 'San Francisco, USA' },
  { emoji: '🏖️', name: 'Bali, Indonesia' },
  { emoji: '🎪', name: 'Barcelona, Spain' },
  { emoji: '🌸', name: 'Tokyo, Japan' },
  { emoji: '🏛️', name: 'Athens, Greece' },
  { emoji: '🌴', name: 'Dubai, UAE' },
  { emoji: '🗺️', name: 'Cairo, Egypt' },
  { emoji: '🌿', name: 'Costa Rica' },
  { emoji: '🏟️', name: 'London, UK' },
  { emoji: '🌊', name: 'Sydney, Australia' },
  { emoji: '🏕️', name: 'Patagonia, Argentina' },
  { emoji: '🌺', name: 'Honolulu, Hawaii' },
  { emoji: '🦁', name: 'Nairobi, Kenya' },
  { emoji: '🌮', name: 'Mexico City, Mexico' },
  { emoji: '🎸', name: 'Nashville, USA' },
  { emoji: '🍕', name: 'Naples, Italy' },
  { emoji: '🏰', name: 'Prague, Czech Republic' },
  { emoji: '🌷', name: 'Amsterdam, Netherlands' },
  { emoji: '🦅', name: 'Reykjavik, Iceland' },
  { emoji: '🌄', name: 'Queenstown, New Zealand' },
  { emoji: '🎋', name: 'Osaka, Japan' },
  { emoji: '🌁', name: 'Vancouver, Canada' },
  { emoji: '🕌', name: 'Istanbul, Turkey' },
  { emoji: '🏙️', name: 'Singapore' },
  { emoji: '🏗️', name: 'Mumbai, India' },
  { emoji: '🌅', name: 'Santorini, Greece' },
  { emoji: '🏂', name: 'Zermatt, Switzerland' },
  { emoji: '🎨', name: 'Florence, Italy' },
];

/* ── Season utility ── */
function getSeason(dateStr) {
  if (!dateStr) return null;
  const m = new Date(dateStr).getMonth() + 1;
  if (m >= 3 && m <= 5) return { label: '🌸 Spring', color: '#f59e0b' };
  if (m >= 6 && m <= 8) return { label: '☀️ Summer', color: '#ef4444' };
  if (m >= 9 && m <= 11) return { label: '🍂 Autumn', color: '#f97316' };
  return { label: '❄️ Winter', color: '#06b6d4' };
}

/* ═══════════════════ NAVBAR ═══════════════════ */
window.addEventListener('scroll', () => {
  const nav = document.getElementById('navbar');
  nav.classList.toggle('scrolled', window.scrollY > 30);
});

document.getElementById('navHamburger').addEventListener('click', () => {
  document.getElementById('mobileNav').classList.toggle('open');
});

window.closeMobileNav = () => {
  document.getElementById('mobileNav').classList.remove('open');
};

/* ═══════════════════ SCROLL HELPERS ═══════════════════ */
window.scrollToPlanner = () => {
  document.getElementById('planner').scrollIntoView({ behavior: 'smooth', block: 'start' });
};
window.scrollToHowItWorks = () => {
  document.getElementById('how-it-works').scrollIntoView({ behavior: 'smooth', block: 'start' });
};

/* ═══════════════════ INTERSECTION OBSERVER — Animations ═══════════════════ */
const observerCallback = (entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const el = entry.target;
      const delay = el.dataset.delay || 0;
      setTimeout(() => el.classList.add('visible'), Number(delay));
      observer.unobserve(el);
    }
  });
};
const observer = new IntersectionObserver(observerCallback, { threshold: 0.12 });
document.querySelectorAll('.feature-card, .hiw-step').forEach(el => observer.observe(el));

/* ═══════════════════ STEP NAVIGATION ═══════════════════ */
window.nextStep = () => {
  if (!validateStep(state.currentStep)) return;
  if (state.currentStep < state.totalSteps) {
    goToStep(state.currentStep + 1);
  }
};

window.prevStep = () => {
  if (state.currentStep > 1) {
    goToStep(state.currentStep - 1);
  }
};

function goToStep(next) {
  const currentEl = document.getElementById(`step-${state.currentStep}`);
  currentEl.classList.remove('active');

  state.currentStep = next;

  const nextEl = document.getElementById(`step-${state.currentStep}`);
  nextEl.style.display = 'none';
  setTimeout(() => {
    nextEl.style.display = '';
    nextEl.classList.add('active');
  }, 10);

  updateProgress();
  window.scrollTo({ top: document.getElementById('planner').offsetTop - 80, behavior: 'smooth' });
}

function updateProgress() {
  const steps = document.querySelectorAll('.prog-step');
  steps.forEach((step, i) => {
    const stepNum = i + 1;
    step.classList.remove('active', 'done');
    if (stepNum < state.currentStep) step.classList.add('done');
    if (stepNum === state.currentStep) step.classList.add('active');
  });

  // Fill connector lines
  for (let i = 1; i < 4; i++) {
    const line = document.getElementById(`line-${i}-${i + 1}`);
    line.classList.toggle('filled', state.currentStep > i);
  }

  // Update aria
  document.getElementById('wizardProgress').setAttribute('aria-valuenow', state.currentStep);
}

/* ── Step Validation ── */
function validateStep(step) {
  if (step === 1) {
    const from = document.getElementById('fromCity').value.trim();
    const to = document.getElementById('toCity').value.trim();
    if (!from) return shakeField('fromCity', 'Please enter your starting location');
    if (!to) return shakeField('toCity', 'Please enter your destination');
    return true;
  }
  if (step === 2) {
    const start = document.getElementById('startDate').value;
    const nights = parseInt(document.getElementById('nightsSlider').value);
    if (!start) return shakeField('startDate', 'Please pick a departure date');
    if (!nights) return false;
    return true;
  }
  if (step === 3) {
    if (!state.selectedBudget) {
      return shakeGroup('budgetCards', 'Please select a budget tier');
    }
    return true;
  }
  if (step === 4) {
    if (state.selectedPurposes.length === 0) {
      return shakeGroup('purposeGrid', 'Please select at least one travel purpose');
    }
    if (!state.selectedPace) {
      return shakeGroup('paceOptions', 'Please select your travel pace');
    }
    return true;
  }
  return true;
}

function shakeField(id, msg) {
  const el = document.getElementById(id);
  el.classList.add('input-error');
  el.title = msg;
  el.style.borderColor = 'var(--c-danger)';
  el.addEventListener('input', function clear() {
    el.classList.remove('input-error');
    el.style.borderColor = '';
    el.removeEventListener('input', clear);
  }, { once: true });
  setTimeout(() => { el.style.borderColor = ''; }, 2000);
  el.focus();
  return false;
}

function shakeGroup(id, msg) {
  const el = document.getElementById(id);
  el.style.setProperty('animation', 'none');
  el.offsetHeight; // reflow
  el.style.animation = 'shakeX .4s ease';
  el.addEventListener('animationend', () => el.style.animation = '', { once: true });
  return false;
}

// Add shakeX keyframe dynamically
const shakeStyle = document.createElement('style');
shakeStyle.textContent = `
  @keyframes shakeX {
    0%,100%{transform:translateX(0)}
    20%{transform:translateX(-8px)}
    40%{transform:translateX(8px)}
    60%{transform:translateX(-5px)}
    80%{transform:translateX(5px)}
  }
`;
document.head.appendChild(shakeStyle);

/* ═══════════════════ DESTINATION AUTOCOMPLETE ═══════════════════ */
function setupAutocomplete(inputId, suggestionsId) {
  const input = document.getElementById(inputId);
  const sugBox = document.getElementById(suggestionsId);

  input.addEventListener('input', () => {
    const q = input.value.toLowerCase().trim();
    if (!q) { sugBox.classList.remove('open'); return; }

    const matches = DESTINATIONS.filter(d => d.name.toLowerCase().includes(q)).slice(0, 6);
    if (!matches.length) { sugBox.classList.remove('open'); return; }

    sugBox.innerHTML = matches.map(d =>
      `<div class="sug-item" data-name="${d.name}">
         <span class="sug-emoji">${d.emoji}</span>
         ${d.name}
       </div>`
    ).join('');
    sugBox.classList.add('open');

    sugBox.querySelectorAll('.sug-item').forEach(item => {
      item.addEventListener('click', () => {
        input.value = item.dataset.name;
        sugBox.classList.remove('open');
      });
    });
  });

  document.addEventListener('click', e => {
    if (!input.contains(e.target)) sugBox.classList.remove('open');
  });
}

setupAutocomplete('fromCity', 'fromSuggestions');
setupAutocomplete('toCity', 'toSuggestions');

/* ═══════════════════ CHECKPOINTS ═══════════════════ */
document.getElementById('addCheckpointBtn').addEventListener('click', addCheckpoint);
document.getElementById('checkpointInput').addEventListener('keydown', e => {
  if (e.key === 'Enter') { e.preventDefault(); addCheckpoint(); }
});

function addCheckpoint() {
  const input = document.getElementById('checkpointInput');
  const val = input.value.trim();
  if (!val || state.checkpoints.includes(val)) { input.value = ''; return; }
  state.checkpoints.push(val);
  renderCheckpoints();
  input.value = '';
}

function removeCheckpoint(val) {
  state.checkpoints = state.checkpoints.filter(c => c !== val);
  renderCheckpoints();
}

function renderCheckpoints() {
  const container = document.getElementById('checkpointTags');
  container.innerHTML = state.checkpoints.map(c =>
    `<span class="checkpoint-tag">
       📍 ${c}
       <span class="tag-remove" onclick="removeCheckpoint('${c.replace(/'/g, "\\'")}')">✕</span>
     </span>`
  ).join('');
}
window.removeCheckpoint = removeCheckpoint;

/* ═══════════════════ DATES & DURATION ═══════════════════ */
const startDateInput = document.getElementById('startDate');
const endDateInput = document.getElementById('endDate');
const nightsSlider = document.getElementById('nightsSlider');
const nightsVal = document.getElementById('nightsVal');

// Set min date to today
const today = new Date().toISOString().split('T')[0];
startDateInput.min = today;

startDateInput.addEventListener('change', () => {
  endDateInput.min = startDateInput.value;
  syncDuration();
});
endDateInput.addEventListener('change', syncDuration);
nightsSlider.addEventListener('input', () => {
  state.nights = parseInt(nightsSlider.value);
  nightsVal.textContent = state.nights;
  updateSliderFill();
  syncDurationFromNights();
});

function syncDuration() {
  const s = startDateInput.value;
  const e = endDateInput.value;
  if (!s || !e) return;
  const diff = Math.round((new Date(e) - new Date(s)) / 86400000);
  if (diff > 0) {
    nightsSlider.value = Math.min(diff, 30);
    state.nights = diff;
    nightsVal.textContent = diff;
    updateSliderFill();
    updateDurationDisplay(diff, s);
  }
}

function syncDurationFromNights() {
  const s = startDateInput.value;
  if (!s) return;
  const endDate = new Date(s);
  endDate.setDate(endDate.getDate() + state.nights);
  endDateInput.value = endDate.toISOString().split('T')[0];
  updateDurationDisplay(state.nights, s);
}

function updateDurationDisplay(nights, dateStr) {
  const days = nights + 1;
  const display = document.getElementById('durationDisplay');
  document.getElementById('durNum').textContent = `${days} Days / ${nights} Nights`;

  const season = getSeason(dateStr);
  const seasonEl = document.getElementById('durSeason');
  if (season) {
    seasonEl.textContent = season.label;
    seasonEl.style.color = season.color;
    seasonEl.style.borderColor = season.color + '40';
    seasonEl.style.background = season.color + '15';
  }

  display.style.borderColor = 'rgba(108,99,255,.3)';
  display.style.background = 'rgba(108,99,255,.06)';
}

function updateSliderFill() {
  const val = nightsSlider.value;
  const pct = ((val - nightsSlider.min) / (nightsSlider.max - nightsSlider.min)) * 100;
  nightsSlider.style.setProperty('--_pct', `${pct}%`);
}
// Init
nightsSlider.value = 5; state.nights = 5; updateSliderFill();

/* ═══════════════════ BUDGET CARDS ═══════════════════ */
document.querySelectorAll('.budget-card').forEach(card => {
  card.addEventListener('click', () => {
    document.querySelectorAll('.budget-card').forEach(c => { c.classList.remove('selected'); c.setAttribute('aria-checked', 'false'); });
    card.classList.add('selected');
    card.setAttribute('aria-checked', 'true');
    state.selectedBudget = card.dataset.value;
  });
});

/* ═══════════════════ PURPOSE BUTTONS ═══════════════════ */
document.querySelectorAll('.purpose-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    btn.classList.toggle('selected');
    const val = btn.dataset.value;
    if (state.selectedPurposes.includes(val)) {
      state.selectedPurposes = state.selectedPurposes.filter(p => p !== val);
    } else {
      state.selectedPurposes.push(val);
    }
  });
});

/* ═══════════════════ PACE BUTTONS ═══════════════════ */
document.querySelectorAll('.pace-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.pace-btn').forEach(b => b.classList.remove('selected'));
    btn.classList.add('selected');
    state.selectedPace = btn.dataset.value;
  });
});

/* ═══════════════════ ITINERARY GENERATION ═══════════════════ */
const MOCK_ACTIVITIES = {
  morning: [
    { title: 'Sunrise Viewpoint', desc: 'Catch the golden hour at the most iconic vantage point. Arrive early for the best light and fewer crowds.', tags: ['Sightseeing', '🌅 Scenic'] },
    { title: 'Local Traditional Breakfast', desc: 'Start the day at a beloved neighborhood café. Try the regional specialty paired with freshly brewed coffee.', tags: ['Food', '☕ Breakfast'] },
    { title: 'Historic Temple Walk', desc: 'Explore century-old temples and shrines in the early morning quiet. A guide joins for context-rich stories.', tags: ['Culture', '🏛️ Heritage'] },
    { title: 'Morning Street Market Tour', desc: 'Weave through vibrant stalls of fresh produce, spices, and handcrafts. Sample seasonal fruits and local snacks.', tags: ['Food', '🛍️ Market'] },
    { title: 'Guided Walking Tour — Old Town', desc: 'Discover the medieval quarter with a knowledgeable local guide. Pass through cobblestone lanes and hidden courtyards.', tags: ['Culture', 'Sightseeing'] },
  ],
  midday: [
    { title: 'Signature Local Cuisine Lunch', desc: 'Sit down at an award-winning restaurant for the definitive local dining experience — a curated tasting menu.', tags: ['Food', '🍽️ Lunch'] },
    { title: 'Museum of National History', desc: 'Spend two hours immersed in world-class exhibits spanning thousands of years of civilisation.', tags: ['Culture', '🏛️ Museum'] },
    { title: 'Scenic Boat or Cable Car Ride', desc: 'Glide over the landscape on this iconic journey — cameras ready for panoramic views that define the destination.', tags: ['Sightseeing', '🚠 Transport'] },
    { title: 'Artisan Workshop Experience', desc: 'Learn a traditional craft from local artisans in a hands-on 90-minute session. Take home your creation.', tags: ['Culture', '🎨 Activity'] },
    { title: 'Nature Walk in National Park', desc: 'A guided 3km trail through lush landscapes. Spot endemic flora, birdlife, and seasonal wildflowers.', tags: ['Adventure', '🌿 Nature'] },
  ],
  afternoon: [
    { title: 'Rooftop Café & City Panorama', desc: 'Unwind with a cold brew or local tea on a stunning rooftop terrace overlooking the city skyline.', tags: ['Relaxation', '☕ Café'] },
    { title: 'Adventure Activity', desc: 'Adrenaline-pumping activity handpicked for your pace — zipline, rock climb, or kayak through scenic waterways.', tags: ['Adventure', '⚡ Activity'] },
    { title: 'Local Cooking Class', desc: 'Under a local chef\'s guidance, prepare 3 regional dishes from scratch. Enjoy what you cook for dinner.', tags: ['Food', '🍳 Hands-on'] },
    { title: 'Flea Market & Street Art Quarter', desc: 'Browse curated vintage stalls and murals in the creative district. Perfect for unique souvenirs.', tags: ['Leisure', '🎨 Culture'] },
    { title: 'Spa & Wellness Retreat', desc: 'Recharge with a traditional therapeutic massage or local wellness ritual. Book the 90-minute signature treatment.', tags: ['Relaxation', '💆 Wellness'] },
  ],
  evening: [
    { title: 'Golden Hour Photography Walk', desc: 'Join a sunset stroll to the best photography spots — waterfront, hilltop, or courtyard — as warm light floods the scene.', tags: ['Sightseeing', '📸 Photo'] },
    { title: 'Fine Dining Experience', desc: 'Reserve a window table at the top-rated restaurant in the area. Multi-course meal with local wine pairing.', tags: ['Food', '🍷 Dinner'] },
    { title: 'Night Market & Street Food Crawl', desc: 'Wander through the electric night market sampling skewers, dumplings, fresh juices, and artisan desserts.', tags: ['Food', '🌃 Nightlife'] },
    { title: 'Traditional Cultural Performance', desc: 'Watch an authentic folk dance, traditional theatre, or musical performance — a living window into local heritage.', tags: ['Culture', '🎭 Show'] },
    { title: 'Rooftop Bar — Sundowner Cocktails', desc: 'End the day with crafted cocktails at the city\'s most celebrated rooftop bar as the skyline glitters below.', tags: ['Nightlife', '🍸 Bar'] },
  ],
};

const TIMES = {
  morning: '07:00',
  midday: '12:00',
  afternoon: '15:30',
  evening: '19:30',
};

const TAG_TYPES = {
  'Food': 'type-food',
  'Sightseeing': 'type-sight',
  'Culture': 'type-sight',
  'Adventure': 'type-activity',
  'Relaxation': 'type-activity',
  'Leisure': 'type-activity',
  'Nightlife': 'type-travel',
  'Transport': 'type-travel',
};

function randomFrom(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function buildDayActivities() {
  return [
    { period: 'morning', ...randomFrom(MOCK_ACTIVITIES.morning) },
    { period: 'midday', ...randomFrom(MOCK_ACTIVITIES.midday) },
    { period: 'afternoon', ...randomFrom(MOCK_ACTIVITIES.afternoon) },
    { period: 'evening', ...randomFrom(MOCK_ACTIVITIES.evening) },
  ];
}

function renderTimeslotTags(tags) {
  return tags.map(tag => {
    const typeClass = Object.keys(TAG_TYPES).find(k => tag.includes(k));
    const cls = typeClass ? TAG_TYPES[typeClass] : '';
    return `<span class="ts-tag ${cls}">${tag}</span>`;
  }).join('');
}

/** Stored itinerary data (raw API days array) — used for modify flow. */
let itineraryState = [];

function renderTimeline(days) {
  itineraryState = days;   // persist for modify flow
  const container = document.getElementById('timelineContent');
  container.innerHTML = '';
  let totalActivities = 0;

  days.forEach((day, di) => {
    totalActivities += day.activities.length;
    const card = document.createElement('div');
    card.className = 'day-card' + (di === 0 ? ' open' : '');
    card.innerHTML = `
      <div class="day-header" onclick="toggleDay(this)">
        <div class="day-num">D${di + 1}</div>
        <div class="day-info">
          <div class="day-title">${day.title}</div>
          <div class="day-sub">${day.subtitle}</div>
        </div>
        <span class="day-toggle">▼</span>
      </div>
      <div class="day-body">
        ${day.activities.map((act, ai) => `
          <div class="time-slot" id="slot-${di}-${ai}">
            <div class="ts-time">${TIMES[act.period]}</div>
            <div class="ts-dot-col">
              <div class="ts-dot"></div>
              ${ai < day.activities.length - 1 ? '<div class="ts-line"></div>' : ''}
            </div>
            <div class="ts-content">
              <div class="ts-title-row">
                <span class="ts-title">${act.title}</span>
                ${(act.alternatives && act.alternatives.length)
        ? `<button class="ts-modify-btn" onclick="openModifyModal(${di},${ai})" title="Swap this activity">✏️ Modify</button>`
        : ''}
              </div>
              <div class="ts-desc">${act.desc}</div>
              <div class="ts-tags">${renderTimeslotTags(act.tags)}</div>
            </div>
          </div>
        `).join('')}
      </div>
    `;
    container.appendChild(card);
  });

  return totalActivities;
}

window.toggleDay = function (header) {
  const card = header.parentElement;
  card.classList.toggle('open');
};

/* ─────────────────────────────────────────
   MODIFY FLOW — swap activities locally
───────────────────────────────────────── */

let _modifyCtx = null;  // { dayIdx, actIdx }

/** Open the alternatives modal for a specific activity slot. */
window.openModifyModal = function (dayIdx, actIdx) {
  const act = itineraryState[dayIdx]?.activities[actIdx];
  if (!act) return;

  _modifyCtx = { dayIdx, actIdx };

  document.getElementById('modalCurrentActivity').textContent = act.title;

  const alts = act.alternatives || [];
  document.getElementById('modalOptions').innerHTML = alts.length
    ? alts.map((alt, i) => `
        <button class="modal-option" onclick="selectAlternative(${i})">
          <div class="mo-top">
            <span class="mo-title">${alt.title}</span>
            <span class="mo-cost">${alt.cost_inr > 0 ? '₹' + alt.cost_inr.toLocaleString('en-IN') : 'Free'}</span>
          </div>
          <p class="mo-desc">${alt.description || ''}</p>
          <span class="ts-tag type-${alt.category}">${alt.category}</span>
        </button>`).join('')
    : '<p style="color:var(--c-text-3)">No alternatives available for this slot.</p>';

  const modal = document.getElementById('modifyModal');
  modal.style.display = 'flex';
  document.body.style.overflow = 'hidden';
};

/** Swap current activity with the chosen alternative and re-render that slot. */
window.selectAlternative = function (altIdx) {
  if (!_modifyCtx) return;
  const { dayIdx, actIdx } = _modifyCtx;
  const act = itineraryState[dayIdx]?.activities[actIdx];
  if (!act) return;

  const chosen = act.alternatives[altIdx];
  if (!chosen) return;

  // Swap: put current into alternatives pool, put chosen as the main
  const oldAlts = [...(act.alternatives || [])];
  oldAlts.splice(altIdx, 1);
  oldAlts.push({ title: act.title, description: act.desc, category: act.tags?.[0]?.toLowerCase() || 'sightseeing', cost_inr: 0 });

  // Update state
  itineraryState[dayIdx].activities[actIdx] = {
    ...act,
    title: chosen.title,
    desc: chosen.description,
    tags: [
      chosen.category.charAt(0).toUpperCase() + chosen.category.slice(1),
      chosen.cost_inr > 0 ? `₹${chosen.cost_inr.toLocaleString('en-IN')}` : 'Free',
    ],
    alternatives: oldAlts,
  };

  closeModifyModal();

  // Re-render only the affected slot
  const slotEl = document.getElementById(`slot-${dayIdx}-${actIdx}`);
  if (slotEl) {
    const updated = itineraryState[dayIdx].activities[actIdx];
    slotEl.querySelector('.ts-title').textContent = updated.title;
    slotEl.querySelector('.ts-desc').textContent = updated.desc;
    slotEl.querySelector('.ts-tags').innerHTML = renderTimeslotTags(updated.tags);
    // flash highlight
    slotEl.classList.add('slot-updated');
    setTimeout(() => slotEl.classList.remove('slot-updated'), 1200);
  }
};

/** Close the alternatives modal. */
window.closeModifyModal = function () {
  document.getElementById('modifyModal').style.display = 'none';
  document.body.style.overflow = '';
  _modifyCtx = null;
};

// Close on backdrop click
document.addEventListener('click', (e) => {
  if (e.target.id === 'modifyModal') closeModifyModal();
});

/* ── Budget estimation ── */
const BUDGET_RATES = {
  budget: { hotel: 2500, food: 1500, transport: 1200, activities: 1000 },
  moderate: { hotel: 7500, food: 4000, transport: 2000, activities: 2500 },
  premium: { hotel: 16000, food: 8000, transport: 4000, activities: 6000 },
  luxury: { hotel: 37000, food: 16000, transport: 8000, activities: 12000 },
};

function renderBudgetBreakdown(nights) {
  const rates = BUDGET_RATES[state.selectedBudget] || BUDGET_RATES.moderate;
  const items = [
    { label: '🏨 Accommodation', daily: rates.hotel },
    { label: '🍽️ Food & Dining', daily: rates.food },
    { label: '🚘 Transport', daily: rates.transport },
    { label: '🎟️ Activities', daily: rates.activities },
  ];
  const total = items.reduce((sum, it) => sum + it.daily * nights, 0);
  const maxVal = Math.max(...items.map(it => it.daily));

  document.getElementById('budgetBreakdown').innerHTML = items.map(it => {
    const subtotal = it.daily * nights;
    const pct = Math.round((it.daily / maxVal) * 100);
    return `
      <div class="bb-row">
        <span class="bb-label">${it.label}</span>
        <div class="bb-bar-wrap"><div class="bb-bar" style="width:${pct}%"></div></div>
        <span class="bb-val">₹${subtotal.toLocaleString('en-IN')}</span>
      </div>
    `;
  }).join('');

  document.getElementById('budgetTotalVal').textContent = `₹${total.toLocaleString('en-IN')}`;

  // Update summary counts
  const currency = document.getElementById('currencySelect').value;
  const custom = document.getElementById('totalBudget').value;
  document.getElementById('sumDays').textContent = nights + 1;
  document.getElementById('sumNights').textContent = nights;
}

/* ── Season insight ── */
const SEASON_INSIGHTS = {
  '🌸 Spring': {
    badge: { text: '🌸 Spring — Great Time to Visit', color: '#f59e0b' },
    body: 'Mild temperatures and blooming landscapes make spring ideal for sightseeing and outdoor activities. Expect moderate crowds and pleasant weather. Pack a light jacket for evenings.',
    tips: [
      'Book accommodations 6–8 weeks in advance — spring demand peaks early.',
      'Festival season begins in many destinations; check local events.',
      'Rain showers possible — lightweight waterproof jacket recommended.',
    ]
  },
  '☀️ Summer': {
    badge: { text: '☀️ Summer — Peak Season', color: '#ef4444' },
    body: 'Long days, warm weather, and vibrant energy define summer travel. Popular sites will be busy — plan early morning visits to skip crowds. Sunscreen and hydration are essential.',
    tips: [
      'Book flights and stays 3–4 months ahead — prices surge in summer.',
      'Visit iconic sites before 9:00 AM or after 5:00 PM to avoid peak crowds.',
      'Air conditioning varies widely — confirm with accommodations.',
    ]
  },
  '🍂 Autumn': {
    badge: { text: '🍂 Autumn — Hidden Gem Season', color: '#f97316' },
    body: 'Autumn offers the sweet spot: fewer crowds, cooler temperatures, and dramatic foliage. Many locals consider it the best time to travel. Shoulder-season pricing saves 20–30%.',
    tips: [
      'Autumn is the best season for photography — golden light and vivid colors.',
      'Shoulder season = fewer tourists; enjoy attractions with more breathing room.',
      'Temperatures can drop sharply — layer clothing for flexibility.',
    ]
  },
  '❄️ Winter': {
    badge: { text: '❄️ Winter — Off-Season Value', color: '#06b6d4' },
    body: 'Winter travel rewards the adventurous with lowest prices, minimal crowds, and magical atmospheres. Some attractions may have reduced hours — check schedules in advance.',
    tips: [
      'Off-season pricing: save up to 40% on flights and hotels.',
      'Verify opening hours — some outdoor sites close or reduce access in winter.',
      'Pack thermal layers, waterproof boots, and a warm overcoat.',
    ]
  },
};

function renderSeasonInsight(dateStr) {
  const season = getSeason(dateStr);
  if (!season) return;
  const data = SEASON_INSIGHTS[season.label];
  if (!data) return;

  document.getElementById('seasonBody').innerHTML = `
    <div class="season-badge" style="background:${data.badge.color}22;color:${data.badge.color}">${data.badge.text}</div>
    <p>${data.body}</p>
  `;
}

/* ── Tips pool ── */
const TIPS_POOL = [
  'Download offline maps before departing — roaming can be expensive.',
  'Carry local currency for small vendors; card acceptance varies.',
  'Travel insurance is essential — cover medical, trip cancellation, and baggage.',
  'Learn 5 key phrases in the local language — locals deeply appreciate the effort.',
  'Stay in neighborhoods away from tourist centers for authentic experiences.',
  'Book top attractions online in advance to skip physical queues.',
  'Visit museums on their free or discounted admission days.',
  'Keep backup copies of all travel documents in cloud storage.',
  'Try the local breakfast instead of hotel buffets — better food, lower cost.',
  'Use public transit like locals — it\'s faster and far more affordable.',
  'Pack a portable charger and universal power adapter.',
  'Respecting local customs and dress codes opens more doors.',
];

function renderTips(tipsArr) {
  // Use real tips from API if provided, otherwise fall back to local pool
  const arr = (tipsArr && tipsArr.length)
    ? tipsArr
    : TIPS_POOL.sort(() => Math.random() - .5).slice(0, 4);
  document.getElementById('tipsList').innerHTML = arr.map(t => `<li>${t}</li>`).join('');
}

/* ── Context chips ── */
function renderContextChips(data) {
  const budgetLabels = { budget: '🎒 Budget Tier', moderate: '🏨 Moderate Tier', premium: '✨ Premium Tier', luxury: '👑 Luxury Tier' };
  const season = getSeason(data.startDate);
  const chips = [
    season && `<span class="ctx-chip">${season.label}</span>`,
    state.selectedBudget && `<span class="ctx-chip">${budgetLabels[state.selectedBudget]}</span>`,
    state.selectedPurposes.map(p => `<span class="ctx-chip">🎯 ${p.charAt(0).toUpperCase() + p.slice(1)}</span>`).join(''),
    state.selectedPace && `<span class="ctx-chip">⏩ ${state.selectedPace.charAt(0).toUpperCase() + state.selectedPace.slice(1)} Pace</span>`,
    data.nights && `<span class="ctx-chip">🌙 ${data.nights} Nights</span>`,
  ].filter(Boolean);
  document.getElementById('contextChips').innerHTML = chips.join('');
}

/* ── Generate Itinerary ── */
const API_BASE = 'http://localhost:8000';

window.generateItinerary = async function () {
  if (!validateStep(4)) return;

  const loaderOverlay = document.getElementById('loaderOverlay');
  loaderOverlay.classList.add('active');

  const body = buildRequestBody();

  try {
    // Run loader animation + real API call in parallel for smooth UX
    const [, apiData] = await Promise.all([
      simulateLoader(),
      fetchItinerary(body),
    ]);

    loaderOverlay.classList.remove('active');

    if (!apiData || apiData.error) {
      showError(apiData?.error || 'Failed to generate itinerary. Please try again.');
      return;
    }

    renderResult(apiData, body);

  } catch (err) {
    loaderOverlay.classList.remove('active');
    showError('Network error — is the backend running on port 8000?');
    console.error(err);
  }
};

/** Collect all wizard form values into the API request body. */
function buildRequestBody() {
  const rawBudget = parseFloat(document.getElementById('totalBudget')?.value) || null;
  const currency = document.getElementById('currencySelect')?.value || 'INR';
  const groupSize = document.getElementById('groupSize')?.value || 'couple';

  return {
    from: document.getElementById('fromCity').value.trim(),
    to: document.getElementById('toCity').value.trim(),
    start_date: document.getElementById('startDate').value,
    nights: state.nights || parseInt(document.getElementById('nightsSlider').value),
    budget: state.selectedBudget || 'moderate',
    purposes: state.selectedPurposes,
    pace: state.selectedPace || 'moderate',
    checkpoints: state.checkpoints,
    accommodation: document.getElementById('accommodation')?.value || null,
    group_size: groupSize,
    special_needs: document.getElementById('specialNeeds')?.value || null,
    total_budget: rawBudget,
    currency: currency,
  };
}

/** Call the backend /generate-plan endpoint. Returns parsed JSON or null. */
async function fetchItinerary(body) {
  const res = await fetch(`${API_BASE}/generate-plan`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`Server error: ${res.status}`);
  return res.json();
}

/** Show an error toast and log to console. */
function showError(msg) {
  showToast('⚠️ ' + msg);
  console.error('[Navisense]', msg);
}

async function simulateLoader() {
  const steps = document.querySelectorAll('.ls-item');
  const bar = document.getElementById('loaderBar');
  const totalSteps = steps.length;

  for (let i = 0; i < totalSteps; i++) {
    if (i > 0) steps[i - 1].classList.remove('active');
    steps[i].classList.add('active');
    bar.style.width = `${((i + 1) / totalSteps) * 92}%`;
    await sleep(900 + Math.random() * 400);
    steps[i].classList.remove('active');
    steps[i].classList.add('done');
  }
  bar.style.width = '100%';
  await sleep(400);
}

function sleep(ms) { return new Promise(res => setTimeout(res, ms)); }

/* ── Render Result (real API response) ── */
function renderResult(apiData, requestBody) {
  const destination = apiData.destination || requestBody.to;
  const nights = requestBody.nights || state.nights || 5;

  // Adapt real API days → timeline format
  const days = (apiData.days || []).map((d, i) => ({
    title: `Day ${d.day}: ${d.theme || 'Exploration'}`,
    subtitle: i === 0
      ? `Arrive & begin exploring ${destination}`
      : i === (apiData.days.length - 1)
        ? `Final day in ${destination}`
        : 'Full day exploration',
    activities: (d.activities || []).map(act => ({
      period: act.period || 'morning',
      title: act.title,
      desc: act.description,
      tags: [
        act.category ? act.category.charAt(0).toUpperCase() + act.category.slice(1) : 'Activity',
        act.cost_inr > 0 ? `₹${act.cost_inr.toLocaleString('en-IN')}` : 'Free',
      ],
      alternatives: act.alternatives || [],   // ← carry through for Modify button
    })),
  }));

  // Header
  document.getElementById('irTitle').textContent = `Your ${destination} Itinerary`;
  const startFmt = requestBody.start_date
    ? new Date(requestBody.start_date).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })
    : '';
  document.getElementById('irMeta').textContent =
    `${requestBody.from} → ${destination}${startFmt ? ` · Departing ${startFmt}` : ''} · ${nights + 1} Days`;

  // Context chips
  renderContextChips({ startDate: requestBody.start_date, nights });

  // Timeline
  const totalActivities = renderTimeline(days);

  // Budget — use real data from API if available, else estimate
  const bs = apiData.budget_summary;
  if (bs && bs.total_inr) {
    renderRealBudget(bs, requestBody);
  } else {
    renderBudgetBreakdown(nights);
  }

  // Summary counts
  document.getElementById('sumDays').textContent = nights + 1;
  document.getElementById('sumNights').textContent = nights;
  document.getElementById('sumActivities').textContent = totalActivities;

  // Season insight
  renderSeasonInsight(requestBody.start_date);

  // Weather — show if returned by API
  renderWeather(apiData.weather);

  // Tips — prefer real API tips, fall back to local pool
  renderTips(apiData.tips);

  // Show result section
  const resultSection = document.getElementById('itineraryResult');
  resultSection.classList.add('visible');
  setTimeout(() => resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' }), 100);
}

/** Render budget breakdown from real Gemini budget_summary object. */
function renderRealBudget(bs, requestBody) {
  const groupCount = { solo: 1, couple: 2, small: 4, medium: 8, large: 12 }[requestBody?.group_size] || 2;
  const nights = requestBody?.nights || 1;

  const items = [
    { label: '🏨 Accommodation', val: bs.accommodation_inr || 0 },
    { label: '🍽️ Food & Dining', val: bs.food_inr || 0 },
    { label: '🚘 Transport', val: bs.transport_inr || 0 },
    { label: '🎟️ Activities', val: bs.activities_inr || 0 },
  ];
  const maxVal = Math.max(...items.map(i => i.val), 1);
  const total = bs.total_inr || items.reduce((s, i) => s + i.val, 0);

  document.getElementById('budgetBreakdown').innerHTML = items.map(it => {
    const pct = Math.round((it.val / maxVal) * 100);
    const perPersonDay = groupCount > 1
      ? ` <span class="bb-sub">(₹${Math.round(it.val / groupCount).toLocaleString('en-IN')}/person)</span>`
      : '';
    return `
      <div class="bb-row">
        <span class="bb-label">${it.label}</span>
        <div class="bb-bar-wrap"><div class="bb-bar" style="width:${pct}%"></div></div>
        <span class="bb-val">₹${it.val.toLocaleString('en-IN')}${perPersonDay}</span>
      </div>`;
  }).join('');

  // Total + per-person breakdown
  const perPerson = groupCount > 1
    ? ` <span class="bb-perperson">≈ ₹${Math.round(total / groupCount).toLocaleString('en-IN')}/person</span>`
    : '';
  document.getElementById('budgetTotalVal').innerHTML =
    `₹${total.toLocaleString('en-IN')}${perPerson}`;
}

/* ── Reset ── */
window.resetPlanner = function () {
  // Hide result
  document.getElementById('itineraryResult').classList.remove('visible');

  // Reset form
  document.getElementById('fromCity').value = '';
  document.getElementById('toCity').value = '';
  document.getElementById('startDate').value = '';
  document.getElementById('endDate').value = '';
  nightsSlider.value = 5; state.nights = 5;
  nightsVal.textContent = '5';
  updateSliderFill();
  document.getElementById('durNum').textContent = '—';
  document.getElementById('durSeason').textContent = '';
  document.getElementById('durationDisplay').style.borderColor = '';
  document.getElementById('durationDisplay').style.background = '';

  // Reset budget
  document.querySelectorAll('.budget-card').forEach(c => { c.classList.remove('selected'); c.setAttribute('aria-checked', 'false'); });
  state.selectedBudget = null;

  // Reset purposes
  document.querySelectorAll('.purpose-btn').forEach(b => b.classList.remove('selected'));
  state.selectedPurposes = [];

  // Reset pace
  document.querySelectorAll('.pace-btn').forEach(b => b.classList.remove('selected'));
  state.selectedPace = null;

  // Reset checkpoints
  state.checkpoints = [];
  renderCheckpoints();

  // Reset loader
  document.querySelectorAll('.ls-item').forEach(el => el.classList.remove('active', 'done'));
  document.getElementById('loaderBar').style.width = '0%';

  // Go to step 1
  state.currentStep = 1;
  document.querySelectorAll('.wizard-step').forEach(s => s.classList.remove('active'));
  document.getElementById('step-1').classList.add('active');
  updateProgress();

  scrollToPlanner();
};

/* ── Regenerate Plan ── */
window.regeneratePlan = async function () {
  const btn = document.getElementById('regenerateBtn');
  if (btn) { btn.disabled = true; btn.textContent = '\u23f3 Regenerating\u2026'; }

  const loaderOverlay = document.getElementById('loaderOverlay');
  loaderOverlay.classList.add('active');

  document.querySelectorAll('.ls-item').forEach(el => el.classList.remove('active', 'done'));
  document.getElementById('loaderBar').style.width = '0%';

  const body = buildRequestBody();

  try {
    const [, apiData] = await Promise.all([
      simulateLoader(),
      fetchItinerary(body),
    ]);
    loaderOverlay.classList.remove('active');
    if (!apiData || apiData.error) {
      showError(apiData?.error || 'Regeneration failed. Please try again.');
    } else {
      renderResult(apiData, body);
    }
  } catch (err) {
    loaderOverlay.classList.remove('active');
    showError('Network error \u2014 is the backend running?');
    console.error(err);
  } finally {
    if (btn) { btn.disabled = false; btn.textContent = '\ud83d\udd04 Regenerate'; }
  }
};

/** Render weather data into the sidebar weather card. */
function renderWeather(weather) {
  const card = document.getElementById('weatherCard');
  const body = document.getElementById('weatherBody');
  if (!card || !body || !weather || !weather.condition) {
    if (card) card.style.display = 'none';
    return;
  }
  card.style.display = '';
  body.innerHTML = `
    <div class="weather-row">
      <span class="weather-condition">${weather.condition}</span>
      <span class="weather-temp">\u2191${weather.temp_max_c ?? '?'}\u00b0C \u00b7 \u2193${weather.temp_min_c ?? '?'}\u00b0C</span>
    </div>
    ${weather.rain_mm > 0 ? `<p class="weather-rain">\ud83c\udf27\ufe0f ${weather.rain_mm} mm expected</p>` : ''}
    <p class="weather-tip">\ud83d\udca1 ${weather.tip || ''}</p>
  `;
}

/* ── View Toggle ── */
window.setView = function (mode) {
  const result = document.getElementById('itineraryResult');
  result.classList.toggle('compact-view', mode === 'compact');
  document.getElementById('viewTimeline').classList.toggle('active', mode === 'timeline');
  document.getElementById('viewCompact').classList.toggle('active', mode === 'compact');
};

/* ── Print & Share ── */
window.printItinerary = function () { window.print(); };

window.shareItinerary = function () {
  const to = document.getElementById('toCity').value || 'your destination';
  const msg = `🌍 Check out my AI-crafted ${to} itinerary on Navisense!`;
  if (navigator.share) {
    navigator.share({ title: 'Navisense Itinerary', text: msg, url: window.location.href }).catch(() => { });
  } else {
    navigator.clipboard.writeText(window.location.href + ' — ' + msg)
      .then(() => showToast('Link copied to clipboard!'))
      .catch(() => showToast('Share link: ' + window.location.href));
  }
};

/* ── Toast notification ── */
function showToast(msg) {
  let toast = document.getElementById('nsToast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'nsToast';
    toast.style.cssText = `
      position:fixed;bottom:32px;left:50%;transform:translateX(-50%) translateY(20px);
      background:var(--c-surface-3);border:1px solid var(--c-border-hi);
      color:var(--c-text);font-size:.9rem;font-weight:600;padding:12px 24px;
      border-radius:var(--radius-full);box-shadow:var(--shadow-md);z-index:9999;
      opacity:0;transition:all .3s ease;
    `;
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.style.opacity = '1';
  toast.style.transform = 'translateX(-50%) translateY(0)';
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(-50%) translateY(20px)';
  }, 3000);
}

/* ══════════════════════════════════
   INIT
══════════════════════════════════ */
// Set initial progress
updateProgress();

// Ensure step 1 is visible
document.getElementById('step-1').classList.add('active');

// Ensure itinerary is hidden
document.getElementById('itineraryResult').classList.remove('visible');

/* ── Cursor trail (subtle enhancement) ── */
const trail = [];
const TRAIL_COUNT = 8;
for (let i = 0; i < TRAIL_COUNT; i++) {
  const dot = document.createElement('div');
  dot.style.cssText = `
    position:fixed;pointer-events:none;z-index:99999;
    width:${4 + i * 0.5}px;height:${4 + i * 0.5}px;
    border-radius:50%;background:rgba(108,99,255,${0.08 - i * 0.008});
    transition:transform ${0.05 + i * 0.04}s ease;
    transform:translate(-50%,-50%);
  `;
  document.body.appendChild(dot);
  trail.push({ el: dot, x: 0, y: 0 });
}

let mouseX = 0, mouseY = 0;
document.addEventListener('mousemove', e => { mouseX = e.clientX; mouseY = e.clientY; });

function animateTrail() {
  let ox = mouseX, oy = mouseY;
  trail.forEach((t, i) => {
    t.x += (ox - t.x) * 0.3;
    t.y += (oy - t.y) * 0.3;
    t.el.style.left = t.x + 'px';
    t.el.style.top = t.y + 'px';
    ox = t.x; oy = t.y;
  });
  requestAnimationFrame(animateTrail);
}
animateTrail();

console.log('%cNavisense ✦ AI Travel Planner', 'color:#6c63ff;font-size:18px;font-weight:800;');
console.log('%cUI Demo — No backend required', 'color:#9ba3c4;');
