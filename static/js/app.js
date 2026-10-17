/**
 * static/js/app.js - KartShelf Frontend Application Logic
 * Modern, responsive e-commerce web application with scratch-built Python DSA backend.
 * Powers Trie autocomplete, custom sorting engines, recent searches (CircularQueue),
 * recently viewed (Deque), infinite carousel (CircularLinkedList), HeaderLinkedList cart,
 * and a full interactive checkout payment simulation.
 */

// Offline image fallback generator
function handleImageError(img, productName) {
  img.onerror = null;
  const initials = (productName || 'KS')
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map(w => w[0].toUpperCase())
    .join('');

  const parent = img.parentElement;
  if (parent) {
    img.style.display = 'none';
    const avatar = document.createElement('div');
    avatar.className = 'img-fallback-avatar';
    avatar.innerHTML = `
      <div style="font-size: 2.2rem; font-family: var(--font-heading);">${initials}</div>
      <div style="font-size: 0.8rem; margin-top: 0.35rem; color: var(--ink-muted); font-family: var(--font-body);">${productName}</div>
    `;
    parent.appendChild(avatar);
  }
}

// Toast notification helper
function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = 'toast';
  if (type === 'success') {
    toast.style.background = 'var(--sage)';
    toast.style.color = 'var(--ink)';
  } else if (type === 'error') {
    toast.style.background = 'var(--terracotta)';
    toast.style.color = '#FFF';
  }
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    setTimeout(() => toast.remove(), 250);
  }, 2600);
}

// Global Cart State Cache
let currentCartState = {
  items: [],
  total_items: 0,
  grand_total: 0
};

// State management & Filter Undo Stack
const filterState = {
  q: '',
  category: '',
  min: 0,
  max: 50000,
  rating: 0,
  sort: 'price_asc',
  algo: 'merge'
};

const filterUndoStack = [];

function pushFilterUndoState() {
  filterUndoStack.push({ ...filterState });
  updateUndoButtonState();
}

function updateUndoButtonState() {
  const undoBtn = document.getElementById('undoFilterBtn');
  if (undoBtn) {
    undoBtn.style.opacity = filterUndoStack.length > 0 ? '1' : '0.5';
    undoBtn.textContent = `↶ Undo (${filterUndoStack.length})`;
  }
}

// =========================================================================
// CATALOG DATA FETCHING & RENDERING
// =========================================================================
async function fetchProducts() {
  const grid = document.getElementById('productGrid');
  if (!grid) return;

  grid.innerHTML = '<div style="grid-column: 1/-1; padding: 3rem; text-align: center; font-family: var(--font-body); font-size: 1.1rem; color: var(--ink-muted);">Curating marketplace catalog...</div>';

  try {
    const params = new URLSearchParams({
      q: filterState.q,
      category: filterState.category,
      min: filterState.min,
      max: filterState.max,
      rating: filterState.rating,
      sort: filterState.sort,
      algo: filterState.algo
    });

    const res = await fetch(`/api/products?${params.toString()}`);
    const data = await res.json();

    // Update count & live telemetry badge
    const countSpan = document.getElementById('productCountSpan');
    if (countSpan) countSpan.textContent = data.count;

    const telemBadge = document.getElementById('dsaTelemetryBadge');
    if (telemBadge && data.dsa_telemetry) {
      const dt = data.dsa_telemetry;
      telemBadge.textContent = `${dt.algorithm} | ${dt.comparisons} comps | ${dt.time_ms}ms | ${dt.is_stable ? 'Stable' : 'Unstable'}`;
      telemBadge.title = `Sorting Engine: ${dt.algorithm}\nComparisons: ${dt.comparisons}\nData Moves: ${dt.moves}\nExecution: ${dt.time_ms}ms`;
    }

    renderProductCards(data.products || []);
  } catch (err) {
    console.error('Failed to fetch products:', err);
    grid.innerHTML = '<div style="grid-column: 1/-1; color: var(--terracotta); text-align: center;">Error loading products. Please try again.</div>';
  }
}

function renderProductCards(products) {
  const grid = document.getElementById('productGrid');
  if (!grid) return;

  if (products.length === 0) {
    grid.innerHTML = `
      <div style="grid-column: 1/-1; text-align: center; padding: 3.5rem 1.5rem; background: var(--paper-card); border: var(--border-ink); border-radius: var(--radius-card); box-shadow: var(--shadow-editorial);">
        <h3 style="font-size: 1.4rem; margin-bottom: 0.5rem; font-family: var(--font-heading);">No products match your filter criteria</h3>
        <p style="color: var(--ink-muted); margin-bottom: 1.25rem;">Try broadening your price range or clearing search keywords.</p>
        <button id="resetAllFiltersBtn" class="nav-link-btn primary">Reset All Filters</button>
      </div>
    `;
    const resetBtn = document.getElementById('resetAllFiltersBtn');
    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        filterState.q = '';
        filterState.category = '';
        filterState.min = 0;
        filterState.max = 50000;
        filterState.rating = 0;
        fetchProducts();
      });
    }
    return;
  }

  grid.innerHTML = products.map(p => {
    const imgSrc = p.image_url || `https://picsum.photos/seed/${p.image_seed}/600/450`;
    return `
    <article class="product-card">
      <div class="product-card-img-wrapper">
        <a href="/product/${p.id}" style="display: block; width: 100%; height: 100%;">
          <img class="product-card-img" 
               src="${imgSrc}" 
               alt="${p.name}" 
               loading="lazy"
               onerror="handleImageError(this, '${p.name.replace(/'/g, "\\'")}')">
        </a>
        ${p.discount_pct > 0 ? `<span class="discount-ribbon">${p.discount_pct}% OFF</span>` : ''}
        <span class="stock-pill">${p.stock} in stock</span>
      </div>
      <div class="product-card-body">
        <div class="product-card-meta">
          <span class="product-brand">${p.brand}</span>
          <div class="product-rating">
            <svg class="star-icon" viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            <span>${p.rating}</span>
          </div>
        </div>
        <h3 class="product-card-title">
          <a href="/product/${p.id}">${p.name}</a>
        </h3>
        <div style="margin: 0.25rem 0;">
          <span style="font-size: 0.72rem; color: var(--ink-muted); text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">
            ${p.subcategory || p.category}
          </span>
        </div>
        <div class="product-card-pricing">
          <span class="current-price">&#8377;${p.price.toLocaleString('en-IN')}</span>
          ${p.original_price > p.price ? `<span class="original-price">&#8377;${p.original_price.toLocaleString('en-IN')}</span>` : ''}
        </div>
        <div class="product-card-actions">
          <button class="add-cart-btn" onclick="addToCart(${p.id})">
            Add to Cart
          </button>
        </div>
      </div>
    </article>
    `;
  }).join('');
}

// =========================================================================
// TRIE AUTOCOMPLETE
// =========================================================================
function initTrieAutocomplete() {
  const searchInput = document.getElementById('searchInput');
  const dropdown = document.getElementById('autocompleteDropdown');
  const list = document.getElementById('autocompleteList');
  if (!searchInput || !dropdown || !list) return;

  let debounceTimer = null;

  searchInput.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    const prefix = searchInput.value.trim();

    if (prefix.length < 1) {
      dropdown.classList.remove('open');
      list.innerHTML = '';
      return;
    }

    debounceTimer = setTimeout(async () => {
      try {
        const res = await fetch(`/api/autocomplete?prefix=${encodeURIComponent(prefix)}`);
        const data = await res.json();
        const completions = data.completions || [];

        if (completions.length === 0) {
          dropdown.classList.remove('open');
          return;
        }

        list.innerHTML = completions.map(item => `
          <div class="autocomplete-item" data-word="${item.full_word}">
            <div class="autocomplete-match-text">
              <span class="autocomplete-prefix-bold">${item.prefix}</span><span>${item.suffix}</span>
            </div>
            <span class="autocomplete-badge">Search</span>
          </div>
        `).join('');

        dropdown.classList.add('open');

        // Add click events to autocomplete items
        list.querySelectorAll('.autocomplete-item').forEach(el => {
          el.addEventListener('click', () => {
            const word = el.getAttribute('data-word');
            searchInput.value = word;
            dropdown.classList.remove('open');
            submitSearch(word);
          });
        });
      } catch (e) {
        console.error('Autocomplete error:', e);
      }
    }, 120);
  });

  searchInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      dropdown.classList.remove('open');
      submitSearch(searchInput.value.trim());
    }
  });

  // Close dropdown when clicking outside
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.nav-search-container')) {
      dropdown.classList.remove('open');
    }
  });
}

async function submitSearch(query) {
  pushFilterUndoState();
  filterState.q = query;

  if (query) {
    try {
      await fetch('/api/recent-searches', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });
      fetchRecentSearches();
    } catch (e) {}
  }

  fetchProducts();
}

// =========================================================================
// ACTIVITY STRIP (Recent Searches & Recently Viewed)
// =========================================================================
async function fetchRecentSearches() {
  const container = document.getElementById('recentSearchesList');
  if (!container) return;

  try {
    const res = await fetch('/api/recent-searches');
    const data = await res.json();
    const searches = data.searches || [];

    if (searches.length === 0) {
      container.innerHTML = '<span style="font-size: 0.8rem; color: var(--ink-muted);">None yet</span>';
      return;
    }

    container.innerHTML = searches.map(s => `
      <button class="recent-chip" onclick="applyRecentSearch('${s.replace(/'/g, "\\'")}')">${s}</button>
    `).join('');
  } catch (e) {}
}

function applyRecentSearch(term) {
  const input = document.getElementById('searchInput');
  if (input) input.value = term;
  submitSearch(term);
}

async function fetchRecentlyViewed() {
  const container = document.getElementById('recentlyViewedList');
  if (!container) return;

  try {
    const res = await fetch('/api/recently-viewed');
    const data = await res.json();
    const items = data.items || [];

    if (items.length === 0) {
      container.innerHTML = '<span style="font-size: 0.8rem; color: var(--ink-muted);">None yet</span>';
      return;
    }

    container.innerHTML = items.slice(0, 4).map(p => `
      <a href="/product/${p.id}" class="recent-chip" title="${p.name}">
        ${p.name.length > 18 ? p.name.slice(0, 16) + '...' : p.name}
      </a>
    `).join('');
  } catch (e) {}
}

// =========================================================================
// FEATURED CAROUSEL (Circular Linked List)
// =========================================================================
let carouselItems = [];
let carouselCurrentIndex = 0;

async function initCarousel() {
  const track = document.getElementById('carouselTrack');
  if (!track) return;

  try {
    const res = await fetch('/api/carousel');
    const data = await res.json();
    carouselItems = data.items || [];

    if (carouselItems.length === 0) return;

    track.innerHTML = carouselItems.map(p => {
      const imgSrc = p.image_url || `https://picsum.photos/seed/${p.image_seed}/600/450`;
      return `
      <div class="carousel-item-card">
        <div style="position: relative; aspect-ratio: 4/3; overflow: hidden; border-radius: 8px; border: 1px solid var(--ink); margin-bottom: 0.5rem;">
          <a href="/product/${p.id}" style="display: block; width: 100%; height: 100%;">
            <img src="${imgSrc}" 
                 alt="${p.name}" 
                 style="width: 100%; height: 100%; object-fit: cover;"
                 onerror="handleImageError(this, '${p.name.replace(/'/g, "\\'")}')">
          </a>
          <span class="discount-ribbon">${p.discount_pct}% OFF</span>
        </div>
        <div style="font-family: var(--font-heading); font-size: 0.95rem; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
          <a href="/product/${p.id}">${p.name}</a>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-top: 0.35rem;">
          <span style="font-family: var(--font-heading); font-size: 1.15rem; font-weight: 800;">&#8377;${p.price.toLocaleString('en-IN')}</span>
          <button class="nav-link-btn" onclick="addToCart(${p.id})" style="padding: 0.2rem 0.6rem; font-size: 0.8rem; font-weight: 700;">+ Add</button>
        </div>
      </div>
      `;
    }).join('');

    // Controls
    const prevBtn = document.getElementById('carouselPrevBtn');
    const nextBtn = document.getElementById('carouselNextBtn');

    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        carouselCurrentIndex = (carouselCurrentIndex + 1) % carouselItems.length;
        updateCarouselTransform();
      });
    }

    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        carouselCurrentIndex = (carouselCurrentIndex - 1 + carouselItems.length) % carouselItems.length;
        updateCarouselTransform();
      });
    }
  } catch (e) {
    console.error('Carousel init error:', e);
  }
}

function updateCarouselTransform() {
  const track = document.getElementById('carouselTrack');
  if (track) {
    const cardWidth = 280 + 20; // width + gap
    track.style.transform = `translateX(-${carouselCurrentIndex * cardWidth}px)`;
  }
}

// =========================================================================
// CATEGORY TREE
// =========================================================================
async function initCategories() {
  const container = document.getElementById('categoryChips');
  if (!container) return;

  try {
    const res = await fetch('/api/categories');
    const data = await res.json();
    const categories = data.categories || {};

    const catButtons = Object.keys(categories).map(catName => `
      <button class="category-chip-btn" data-cat="${catName}">${catName}</button>
    `).join('');

    container.innerHTML = `
      <button class="category-chip-btn active" data-cat="">All Collections</button>
      ${catButtons}
    `;

    container.querySelectorAll('.category-chip-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        container.querySelectorAll('.category-chip-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        pushFilterUndoState();
        filterState.category = btn.getAttribute('data-cat') || '';
        fetchProducts();
      });
    });
  } catch (e) {}
}

// =========================================================================
// SHOPPING CART
// =========================================================================
async function fetchCart() {
  try {
    const res = await fetch('/api/cart');
    const data = await res.json();
    currentCartState = data;
    updateCartUI(data);
  } catch (e) {
    console.error('Fetch cart error:', e);
  }
}

function updateCartUI(cartData) {
  currentCartState = cartData;

  const countBadges = document.querySelectorAll('#cartCountBadge, #headerNodeCount');
  countBadges.forEach(b => { if (b) b.textContent = cartData.total_items || 0; });

  const totalSpans = document.querySelectorAll('#cartGrandTotal, #headerNodeTotal');
  totalSpans.forEach(s => { if (s) s.textContent = `₹${(cartData.grand_total || 0).toLocaleString('en-IN')}`; });

  // Update Pay Now modal summary values if open or present
  const modalSubtotal = document.getElementById('modalSummarySubtotal');
  const modalTotal = document.getElementById('modalSummaryTotal');
  const payBtnAmt = document.getElementById('confirmPayBtnAmt');
  const formattedTotal = `₹${(cartData.grand_total || 0).toLocaleString('en-IN')}`;
  if (modalSubtotal) modalSubtotal.textContent = formattedTotal;
  if (modalTotal) modalTotal.textContent = formattedTotal;
  if (payBtnAmt) payBtnAmt.textContent = formattedTotal;

  // Render items in slide drawer
  const drawerItems = document.getElementById('cartDrawerItems');
  if (drawerItems) {
    if (!cartData.items || cartData.items.length === 0) {
      drawerItems.innerHTML = '<div style="text-align: center; color: var(--ink-muted); margin-top: 3.5rem; font-size: 0.95rem;">Your cart is currently empty.</div>';
    } else {
      drawerItems.innerHTML = cartData.items.map(item => {
        const imgSrc = item.image_url || `https://picsum.photos/seed/${item.image_seed}/600/450`;
        return `
        <div class="cart-item-row">
          <img class="cart-item-thumb" 
               src="${imgSrc}" 
               alt="${item.name}" 
               onerror="handleImageError(this, '${item.name.replace(/'/g, "\\'")}')">
          <div class="cart-item-details">
            <div class="cart-item-title">${item.name}</div>
            <div class="cart-item-price">&#8377;${item.price.toLocaleString('en-IN')} &times; ${item.quantity} = &#8377;${item.subtotal.toLocaleString('en-IN')}</div>
            <div class="cart-qty-control">
              <button class="qty-btn" onclick="updateCartQty(${item.product_id}, ${item.quantity - 1})">-</button>
              <input type="number" min="1" max="99" class="qty-input-direct" value="${item.quantity}" onchange="updateCartQty(${item.product_id}, parseInt(this.value) || 1)" title="Type quantity directly">
              <button class="qty-btn" onclick="updateCartQty(${item.product_id}, ${item.quantity + 1})">+</button>
              <button onclick="removeCartItem(${item.product_id})" style="margin-left: auto; color: var(--terracotta); background: none; border: none; cursor: pointer; text-decoration: underline; font-size: 0.8rem; font-weight: 600;">Remove</button>
            </div>
          </div>
        </div>
        `;
      }).join('');
    }
  }

  // Render items on full cart.html page if present
  const fullCartContainer = document.getElementById('cartFullItemsContainer');
  const emptyState = document.getElementById('cartEmptyState');
  if (fullCartContainer && emptyState) {
    if (!cartData.items || cartData.items.length === 0) {
      fullCartContainer.style.display = 'none';
      emptyState.style.display = 'block';
    } else {
      emptyState.style.display = 'none';
      fullCartContainer.style.display = 'flex';
      fullCartContainer.innerHTML = cartData.items.map(item => {
        const imgSrc = item.image_url || `https://picsum.photos/seed/${item.image_seed}/600/450`;
        return `
        <div class="cart-item-row" style="padding: 1.25rem;">
          <img class="cart-item-thumb" 
               src="${imgSrc}" 
               alt="${item.name}" 
               style="width: 85px; height: 85px;"
               onerror="handleImageError(this, '${item.name.replace(/'/g, "\\'")}')">
          <div class="cart-item-details" style="justify-content: center;">
            <div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--deep-teal);">${item.sku}</div>
            <div class="cart-item-title" style="font-size: 1.15rem;">${item.name}</div>
            <div class="cart-item-price" style="font-size: 1.1rem;">&#8377;${item.price.toLocaleString('en-IN')}</div>
          </div>
          <div style="display: flex; flex-direction: column; align-items: flex-end; justify-content: space-between;">
            <button onclick="removeCartItem(${item.product_id})" style="color: var(--terracotta); background: none; border: none; cursor: pointer; text-decoration: underline; font-size: 0.85rem; font-weight: 600;">Delete</button>
            <div class="cart-qty-control">
              <button class="qty-btn" onclick="updateCartQty(${item.product_id}, ${item.quantity - 1})">-</button>
              <input type="number" min="1" max="99" class="qty-input-direct" value="${item.quantity}" onchange="updateCartQty(${item.product_id}, parseInt(this.value) || 1)" title="Type quantity directly">
              <button class="qty-btn" onclick="updateCartQty(${item.product_id}, ${item.quantity + 1})">+</button>
            </div>
            <div style="font-family: var(--font-heading); font-size: 1.15rem; font-weight: 800;">
              &#8377;${item.subtotal.toLocaleString('en-IN')}
            </div>
          </div>
        </div>
        `;
      }).join('');
    }
  }
}

async function addToCart(productId, quantity = 1) {
  try {
    const res = await fetch('/api/cart', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ product_id: productId, quantity })
    });
    const data = await res.json();
    updateCartUI(data);
    showToast('Added item to cart!', 'success');
  } catch (e) {
    showToast('Failed to add to cart', 'error');
  }
}

async function updateCartQty(productId, quantity) {
  if (quantity < 1) {
    return removeCartItem(productId);
  }
  try {
    const res = await fetch('/api/cart', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ product_id: productId, quantity })
    });
    const data = await res.json();
    updateCartUI(data);
  } catch (e) {}
}

async function removeCartItem(productId) {
  try {
    const res = await fetch('/api/cart', {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ product_id: productId })
    });
    const data = await res.json();
    updateCartUI(data);
    showToast('Removed item from cart', 'info');
  } catch (e) {}
}

async function clearEntireCart() {
  try {
    const res = await fetch('/api/cart', {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({})
    });
    const data = await res.json();
    updateCartUI(data);
    showToast('Cart cleared', 'info');
  } catch (e) {}
}

// Cart Drawer open/close controls
function initCartDrawer() {
  const openBtn = document.getElementById('openCartBtn');
  const closeBtn = document.getElementById('closeCartBtn');
  const drawer = document.getElementById('cartDrawer');
  const overlay = document.getElementById('cartOverlay');
  const clearBtn = document.getElementById('clearCartBtn');
  const pageClearBtn = document.getElementById('cartPageClearBtn');

  if (openBtn && drawer && overlay) {
    openBtn.addEventListener('click', () => {
      drawer.classList.add('open');
      overlay.classList.add('open');
    });
  }

  function closeDrawer() {
    if (drawer) drawer.classList.remove('open');
    if (overlay) overlay.classList.remove('open');
  }

  if (closeBtn) closeBtn.addEventListener('click', closeDrawer);
  if (overlay) overlay.addEventListener('click', closeDrawer);
  if (clearBtn) clearBtn.addEventListener('click', clearEntireCart);
  if (pageClearBtn) pageClearBtn.addEventListener('click', clearEntireCart);
}

// =========================================================================
// FAKE PAY NOW CHECKOUT MODAL SYSTEM
// =========================================================================
function initPaymentModal() {
  const modalOverlay = document.getElementById('paymentModalOverlay');
  if (!modalOverlay) return;

  const closeBtn = document.getElementById('closePayModalBtn');
  const formBody = document.getElementById('payModalFormBody');
  const processingState = document.getElementById('payProcessingState');
  const successState = document.getElementById('paySuccessState');
  const confirmBtn = document.getElementById('confirmPayBtn');
  const continueBtn = document.getElementById('successContinueShoppingBtn');

  // Trigger buttons
  const drawerPayBtn = document.getElementById('drawerPayNowBtn');
  const pagePayBtn = document.getElementById('pagePayNowBtn');
  const directPayBtn = document.getElementById('detailDirectPayBtn');

  function openModal() {
    if (!currentCartState.items || currentCartState.items.length === 0) {
      showToast('Your cart is empty! Add products first.', 'error');
      return;
    }

    // Reset view states
    if (formBody) formBody.style.display = 'flex';
    if (processingState) processingState.classList.remove('active');
    if (successState) successState.classList.remove('active');

    // Update amounts
    const formatted = `₹${(currentCartState.grand_total || 0).toLocaleString('en-IN')}`;
    const modalSubtotal = document.getElementById('modalSummarySubtotal');
    const modalTotal = document.getElementById('modalSummaryTotal');
    const payBtnAmt = document.getElementById('confirmPayBtnAmt');
    if (modalSubtotal) modalSubtotal.textContent = formatted;
    if (modalTotal) modalTotal.textContent = formatted;
    if (payBtnAmt) payBtnAmt.textContent = formatted;

    // Close cart drawer if open
    const drawer = document.getElementById('cartDrawer');
    const overlay = document.getElementById('cartOverlay');
    if (drawer) drawer.classList.remove('open');
    if (overlay) overlay.classList.remove('open');

    modalOverlay.classList.add('open');
  }

  function closeModal() {
    modalOverlay.classList.remove('open');
  }

  if (drawerPayBtn) drawerPayBtn.addEventListener('click', openModal);
  if (pagePayBtn) pagePayBtn.addEventListener('click', openModal);
  if (closeBtn) closeBtn.addEventListener('click', closeModal);

  if (directPayBtn) {
    directPayBtn.addEventListener('click', async () => {
      const qtyInput = document.getElementById('detailQtyInput');
      const qty = qtyInput ? (parseInt(qtyInput.value) || 1) : 1;
      if (typeof CURRENT_PRODUCT_ID !== 'undefined') {
        await addToCart(CURRENT_PRODUCT_ID, qty);
        openModal();
      }
    });
  }

  // Close when clicking outside modal
  modalOverlay.addEventListener('click', (e) => {
    if (e.target === modalOverlay) closeModal();
  });

  // Tab switching (UPI, Card, Net Banking, COD)
  const tabBtns = modalOverlay.querySelectorAll('.pay-tab-btn');
  const tabContents = modalOverlay.querySelectorAll('.pay-tab-content');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      tabContents.forEach(c => c.classList.remove('active'));
      btn.classList.add('active');
      const targetId = btn.getAttribute('data-tab');
      const targetEl = document.getElementById(targetId);
      if (targetEl) targetEl.classList.add('active');
    });
  });

  // Confirm Payment execution
  if (confirmBtn) {
    confirmBtn.addEventListener('click', () => {
      if (formBody) formBody.style.display = 'none';
      if (processingState) processingState.classList.add('active');

      setTimeout(async () => {
        if (processingState) processingState.classList.remove('active');
        if (successState) successState.classList.add('active');

        // Populate order details
        const orderIdSpan = document.getElementById('successOrderId');
        if (orderIdSpan) {
          orderIdSpan.textContent = `#KS-${Math.floor(100000 + Math.random() * 900000)}`;
        }

        const deliverySpan = document.getElementById('successDeliveryDate');
        if (deliverySpan) {
          const date = new Date();
          date.setDate(date.getDate() + 3);
          const options = { weekday: 'short', month: 'short', day: 'numeric' };
          deliverySpan.textContent = date.toLocaleDateString('en-IN', options);
        }

        // Clear cart on backend and reset UI
        try {
          await fetch('/api/cart', {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({})
          });
          currentCartState = { items: [], total_items: 0, grand_total: 0 };
          updateCartUI(currentCartState);
        } catch (e) {}

        showToast('Payment Authorized & Confirmed!', 'success');
      }, 1600);
    });
  }

  // Continue shopping button
  if (continueBtn) {
    continueBtn.addEventListener('click', () => {
      closeModal();
      if (window.location.pathname.includes('/cart')) {
        window.location.href = '/';
      }
    });
  }
}

// =========================================================================
// PRODUCT DETAILS PAGE SPECIFICS
// =========================================================================
async function initProductDetailsPage() {
  if (typeof CURRENT_PRODUCT_ID === 'undefined') return;

  // Quantity controls on product page
  let qty = 1;
  const minus = document.getElementById('detailQtyMinus');
  const plus = document.getElementById('detailQtyPlus');
  const qtyInput = document.getElementById('detailQtyInput');
  const btnPrice = document.getElementById('detailBtnPrice');
  const addBtn = document.getElementById('detailAddToCartBtn');

  function syncQtyDisplay(newQty) {
    qty = Math.max(1, Math.min(50, newQty));
    if (qtyInput) qtyInput.value = qty;
    if (btnPrice && typeof CURRENT_PRODUCT_PRICE !== 'undefined') {
      btnPrice.textContent = (CURRENT_PRODUCT_PRICE * qty).toLocaleString('en-IN');
    }
  }

  if (minus) minus.addEventListener('click', () => syncQtyDisplay(qty - 1));
  if (plus) plus.addEventListener('click', () => syncQtyDisplay(qty + 1));
  if (qtyInput) {
    qtyInput.addEventListener('change', () => {
      syncQtyDisplay(parseInt(qtyInput.value) || 1);
    });
  }

  if (addBtn) {
    addBtn.addEventListener('click', () => {
      addToCart(CURRENT_PRODUCT_ID, qty);
    });
  }

  // Record in recently viewed
  try {
    await fetch('/api/recently-viewed', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ product_id: CURRENT_PRODUCT_ID })
    });
  } catch (e) {}

  // Load Product Family (Disjoint Set)
  try {
    const res = await fetch(`/api/family/${CURRENT_PRODUCT_ID}`);
    const data = await res.json();
    const familyGrid = document.getElementById('familyGrid');
    if (familyGrid) {
      const variants = data.variants || [];
      if (variants.length <= 1) {
        familyGrid.innerHTML = '<div style="color: var(--ink-muted); font-size: 0.9rem;">This product is a unique standalone design with no other color variants.</div>';
      } else {
        familyGrid.innerHTML = variants.map(v => {
          const imgSrc = v.image_url || `https://picsum.photos/seed/${v.image_seed}/600/450`;
          return `
          <div class="product-card" style="border: ${v.id === CURRENT_PRODUCT_ID ? '2px solid var(--terracotta)' : 'var(--border-ink)'};">
            <div class="product-card-img-wrapper" style="aspect-ratio: 16/10;">
              <a href="/product/${v.id}" style="display: block; width: 100%; height: 100%;">
                <img src="${imgSrc}" 
                     alt="${v.name}" 
                     style="width: 100%; height: 100%; object-fit: cover;"
                     onerror="handleImageError(this, '${v.name.replace(/'/g, "\\'")}')">
              </a>
              ${v.id === CURRENT_PRODUCT_ID ? '<span class="discount-ribbon" style="background: var(--ink);">Current View</span>' : ''}
            </div>
            <div class="product-card-body" style="padding: 0.75rem;">
              <div style="font-family: var(--font-heading); font-size: 0.9rem; font-weight: 700;">
                <a href="/product/${v.id}">${v.name}</a>
              </div>
              <div style="font-family: var(--font-heading); font-weight: 800; margin-top: 0.4rem;">&#8377;${v.price.toLocaleString('en-IN')}</div>
            </div>
          </div>
          `;
        }).join('');
      }
    }
  } catch (e) {}

  // Load Related Products
  try {
    const res = await fetch(`/api/related/${CURRENT_PRODUCT_ID}`);
    const data = await res.json();
    const relatedGrid = document.getElementById('relatedGrid');
    if (relatedGrid) {
      const related = data.related || [];
      if (related.length === 0) {
        relatedGrid.innerHTML = '<div style="color: var(--ink-muted); font-size: 0.9rem;">No related items found.</div>';
      } else {
        relatedGrid.innerHTML = related.map(r => {
          const imgSrc = r.image_url || `https://picsum.photos/seed/${r.image_seed}/600/450`;
          return `
          <div class="product-card">
            <div class="product-card-img-wrapper" style="aspect-ratio: 16/10;">
              <a href="/product/${r.id}" style="display: block; width: 100%; height: 100%;">
                <img src="${imgSrc}" 
                     alt="${r.name}" 
                     style="width: 100%; height: 100%; object-fit: cover;"
                     onerror="handleImageError(this, '${r.name.replace(/'/g, "\\'")}')">
              </a>
              <span class="stock-pill" style="left: 8px; right: auto; background: var(--deep-teal); color: #FFF;">Recommended</span>
            </div>
            <div class="product-card-body" style="padding: 0.75rem;">
              <div style="font-family: var(--font-heading); font-size: 0.9rem; font-weight: 700;">
                <a href="/product/${r.id}">${r.name}</a>
              </div>
              <div style="display: flex; justify-content: space-between; align-items: baseline; margin-top: 0.4rem;">
                <span style="font-family: var(--font-heading); font-weight: 800;">&#8377;${r.price.toLocaleString('en-IN')}</span>
                <button class="nav-link-btn" onclick="addToCart(${r.id})" style="padding: 0.15rem 0.5rem; font-size: 0.8rem; font-weight: 700;">+ Add</button>
              </div>
            </div>
          </div>
          `;
        }).join('');
      }
    }
  } catch (e) {}
}

// =========================================================================
// BUDGET BUNDLE BUILDER ON CART PAGE (Typeable min/max count)
// =========================================================================
function initBudgetBundleBuilder() {
  const runBtn = document.getElementById('runBundleBtn');
  const budgetInput = document.getElementById('bundleBudgetInput');
  const minItemsInput = document.getElementById('bundleMinItems');
  const maxItemsInput = document.getElementById('bundleMaxItems');
  const resultBox = document.getElementById('bundleResultBox');

  if (!runBtn || !budgetInput) return;

  // Quick budget helper buttons
  const b3k = document.getElementById('quickBudget3k');
  const b5k = document.getElementById('quickBudget5k');
  const b10k = document.getElementById('quickBudget10k');
  if (b3k) b3k.addEventListener('click', () => { budgetInput.value = 3000; });
  if (b5k) b5k.addEventListener('click', () => { budgetInput.value = 5000; });
  if (b10k) b10k.addEventListener('click', () => { budgetInput.value = 10000; });

  let currentBundleItems = [];

  runBtn.addEventListener('click', async () => {
    const budget = parseFloat(budgetInput.value) || 5000;
    const minItems = parseInt(minItemsInput ? minItemsInput.value : 2) || 2;
    const maxItems = parseInt(maxItemsInput ? maxItemsInput.value : 5) || 5;

    if (minItems > maxItems) {
      showToast('Min products cannot exceed max products', 'error');
      return;
    }

    runBtn.textContent = 'Optimizing Best Value Combo...';

    try {
      const res = await fetch(`/api/bundle?budget=${budget}&min_items=${minItems}&max_items=${maxItems}`);
      const data = await res.json();

      runBtn.textContent = 'Generate Optimal Combo';
      resultBox.style.display = 'block';

      if (!data.found || !data.bundle || data.bundle.length === 0) {
        resultBox.innerHTML = `<div style="color: var(--terracotta); padding: 1rem; font-weight: 600;">No combination of ${minItems}-${maxItems} products found under ₹${budget.toLocaleString('en-IN')}. Try increasing budget or adjusting item counts.</div>`;
        return;
      }

      currentBundleItems = data.bundle;

      const costEl = document.getElementById('bundleTotalCost');
      const ratingEl = document.getElementById('bundleAvgRating');
      const savingsEl = document.getElementById('bundleSavings');

      if (costEl) costEl.textContent = `₹${data.total_price.toLocaleString('en-IN')}`;
      if (ratingEl) ratingEl.textContent = `★ ${data.average_rating}`;
      if (savingsEl) savingsEl.textContent = `₹${data.savings.toLocaleString('en-IN')}`;

      const itemsList = document.getElementById('bundleItemsList');
      if (itemsList) {
        itemsList.innerHTML = data.bundle.map(p => {
          const imgSrc = p.image_url || `https://picsum.photos/seed/${p.image_seed}/600/450`;
          return `
          <div style="background: var(--paper-card); border: 1.5px solid var(--ink); border-radius: var(--radius-sm); padding: 0.6rem 0.85rem; display: flex; justify-content: space-between; align-items: center; gap: 0.75rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
              <img src="${imgSrc}" alt="${p.name}" style="width: 44px; height: 44px; object-fit: cover; border-radius: 4px; border: 1px solid var(--ink);" onerror="handleImageError(this, '${p.name.replace(/'/g, "\\'")}')">
              <div>
                <a href="/product/${p.id}" style="font-weight: 700; font-size: 0.88rem; color: var(--ink);">${p.name}</a>
                <div style="font-size: 0.75rem; color: var(--ink-muted);">${p.brand} &bull; Rating: ★ ${p.rating}</div>
              </div>
            </div>
            <div style="font-family: var(--font-heading); font-weight: 800; font-size: 0.95rem; white-space: nowrap;">&#8377;${p.price.toLocaleString('en-IN')}</div>
          </div>
          `;
        }).join('');
      }

      const addAllBtn = document.getElementById('addBundleToCartBtn');
      if (addAllBtn) {
        addAllBtn.onclick = async () => {
          addAllBtn.textContent = 'Adding All Items...';
          for (const item of currentBundleItems) {
            await addToCart(item.id, 1);
          }
          addAllBtn.textContent = '✓ All Added to Cart!';
          fetchCart();
        };
      }
    } catch (e) {
      runBtn.textContent = 'Generate Optimal Combo';
      showToast('Error computing bundle', 'error');
    }
  });
}

// =========================================================================
// FILTERS & CONTROLS BINDING
// =========================================================================
function initFilterControls() {
  const sortSelect = document.getElementById('sortSelect');
  const engineSelect = document.getElementById('engineSelect');
  const minPrice = document.getElementById('minPriceInput');
  const maxPrice = document.getElementById('maxPriceInput');
  const applyPriceBtn = document.getElementById('applyPriceFilterBtn');
  const resetPriceBtn = document.getElementById('resetPriceFilterBtn');
  const ratingSelect = document.getElementById('ratingFilterSelect');
  const undoBtn = document.getElementById('undoFilterBtn');

  if (sortSelect) {
    sortSelect.addEventListener('change', () => {
      pushFilterUndoState();
      filterState.sort = sortSelect.value;
      fetchProducts();
    });
  }

  if (engineSelect) {
    engineSelect.addEventListener('change', () => {
      filterState.algo = engineSelect.value;
      fetchProducts();
    });
  }

  if (applyPriceBtn && minPrice && maxPrice) {
    applyPriceBtn.addEventListener('click', () => {
      pushFilterUndoState();
      filterState.min = parseFloat(minPrice.value) || 0;
      filterState.max = parseFloat(maxPrice.value) || 50000;
      fetchProducts();
    });
  }

  if (resetPriceBtn && minPrice && maxPrice) {
    resetPriceBtn.addEventListener('click', () => {
      pushFilterUndoState();
      minPrice.value = 0;
      maxPrice.value = 50000;
      filterState.min = 0;
      filterState.max = 50000;
      fetchProducts();
    });
  }

  if (ratingSelect) {
    ratingSelect.addEventListener('change', () => {
      pushFilterUndoState();
      filterState.rating = parseFloat(ratingSelect.value) || 0;
      fetchProducts();
    });
  }

  if (undoBtn) {
    undoBtn.addEventListener('click', () => {
      if (filterUndoStack.length === 0) {
        showToast('Undo history is empty', 'info');
        return;
      }
      const previousState = filterUndoStack.pop();
      Object.assign(filterState, previousState);

      // Restore form control inputs
      if (sortSelect) sortSelect.value = filterState.sort;
      if (engineSelect) engineSelect.value = filterState.algo;
      if (minPrice) minPrice.value = filterState.min;
      if (maxPrice) maxPrice.value = filterState.max;
      if (ratingSelect) ratingSelect.value = filterState.rating;
      const searchInput = document.getElementById('searchInput');
      if (searchInput) searchInput.value = filterState.q;

      updateUndoButtonState();
      fetchProducts();
      showToast('Filters restored', 'info');
    });
  }
}

// =========================================================================
// INITIALIZATION ON DOM CONTENT LOADED
// =========================================================================
document.addEventListener('DOMContentLoaded', () => {
  initTrieAutocomplete();
  initCartDrawer();
  initPaymentModal();
  fetchCart();

  // Shop homepage specific
  if (document.getElementById('productGrid')) {
    initCategories();
    fetchRecentSearches();
    fetchRecentlyViewed();
    initCarousel();
    initFilterControls();
    fetchProducts();
  }

  // Product detail page specific
  if (typeof CURRENT_PRODUCT_ID !== 'undefined') {
    initProductDetailsPage();
  }

  // Cart page specific
  if (document.getElementById('cartFullItemsContainer')) {
    initBudgetBundleBuilder();
  }
});
