/**
 * static/js/lab.js - KartShelf Interactive DSA Laboratory & Workbench
 * Provides live DOM/SVG visualizations, operation controls, benchmarks,
 * and academic syllabus mappings for instructor viva examination.
 */

// Tab Switching
function initTabNavigation() {
  const tabBtns = document.querySelectorAll('.unit-tab-btn');
  const panels = document.querySelectorAll('.lab-panel');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetUnit = btn.getAttribute('data-unit');

      tabBtns.forEach(b => b.classList.remove('active'));
      panels.forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      const targetPanel = document.getElementById(targetUnit);
      if (targetPanel) targetPanel.classList.add('active');

      // Refresh relevant tab visualizers
      loadTabContent(targetUnit);
    });
  });

  // Check URL hash for direct tab link (e.g. /lab#unit-3)
  const hash = window.location.hash.replace('#', '');
  if (hash) {
    const matchingBtn = document.querySelector(`.unit-tab-btn[data-unit="${hash}"]`);
    if (matchingBtn) matchingBtn.click();
  } else {
    loadTabContent('unit-1');
  }
}

function loadTabContent(unit) {
  if (unit === 'unit-1') {
    fetchStackLab();
    fetchQueueLab();
    fetchPQLab();
    fetchPolyMatrixLab();
  } else if (unit === 'unit-2') {
    fetchTreesLab();
    fetchBTreeLab();
  } else if (unit === 'unit-3') {
    fetchGraphLab();
  } else if (unit === 'unit-4') {
    fetchSortingLab();
    fetchSearchingLab();
    fetchHashingLab();
  } else if (unit === 'unit-5') {
    fetchTrieLab();
    fetchDisjointSetLab();
  } else if (unit === 'syllabus') {
    fetchSyllabusTable();
  }
}

// =========================================================================
// UNIT I: STACKS, QUEUES, PRIORITY QUEUES, LINKED LISTS
// =========================================================================
async function fetchStackLab(postData = null) {
  try {
    const opts = postData ? {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(postData)
    } : {};

    const res = await fetch('/api/lab/stack', opts);
    const data = await res.json();

    const box = document.getElementById('stackVizBox');
    if (!box) return;

    const stack = data.stack || {};
    const dynStack = data.dynamic_stack || {};
    const multi = data.multistack || {};

    box.innerHTML = `
      <div style="width: 100%; margin-bottom: 1rem;">
        <div style="font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700; color: var(--mustard); margin-bottom: 0.35rem;">
          1. Standard Array Stack (Size: ${stack.size} / ${stack.capacity}, Top: ${stack.top_index})
        </div>
        <div style="display: flex; gap: 4px; overflow-x: auto; padding: 4px 0;">
          ${(stack.items || []).map((it, idx) => `
            <div style="background: ${idx === stack.top_index ? 'var(--terracotta)' : 'var(--paper-card)'}; color: var(--ink); border: 1.5px solid var(--ink); padding: 0.35rem 0.65rem; border-radius: 4px; font-family: var(--font-mono); font-size: 0.75rem; text-align: center;">
              <div>[${idx}]</div>
              <strong>${it}</strong>
              ${idx === stack.top_index ? '<div style="font-size: 0.65rem; color: #FFF;">TOP &uarr;</div>' : ''}
            </div>
          `).join('') || '<div style="font-size: 0.8rem; color: var(--ink-muted);">Stack is empty</div>'}
        </div>
      </div>

      <div style="width: 100%; margin-bottom: 1rem; border-top: 1px dashed var(--soft-sand); padding-top: 0.75rem;">
        <div style="font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700; color: var(--sage); margin-bottom: 0.35rem;">
          2. Geometric DynamicStack (Capacity: ${dynStack.capacity}, Size: ${dynStack.size})
        </div>
        <div style="display: flex; gap: 4px; overflow-x: auto; padding: 4px 0;">
          ${(dynStack.raw_slots || []).map((slot, idx) => `
            <div style="background: ${slot !== 'None' ? 'var(--deep-teal)' : '#2A2724'}; color: #FFF; border: 1px solid var(--ink); padding: 0.3rem 0.5rem; border-radius: 4px; font-family: var(--font-mono); font-size: 0.72rem; min-width: 48px; text-align: center;">
              <div>Slot ${idx}</div>
              <div>${slot !== 'None' ? slot : '<em>empty</em>'}</div>
            </div>
          `).join('')}
        </div>
        ${(dynStack.resize_events && dynStack.resize_events.length > 0) ? `
          <div style="font-family: var(--font-mono); font-size: 0.7rem; color: var(--ink-muted); margin-top: 0.35rem;">
            Last resize event: ${dynStack.resize_events[dynStack.resize_events.length - 1].reason} (${dynStack.resize_events[dynStack.resize_events.length - 1].old_capacity} &rarr; ${dynStack.resize_events[dynStack.resize_events.length - 1].new_capacity})
          </div>
        ` : ''}
      </div>

      <div style="width: 100%; border-top: 1px dashed var(--soft-sand); padding-top: 0.75rem;">
        <div style="font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700; color: var(--mustard); margin-bottom: 0.35rem;">
          3. MultiStack (3 Stacks Partitioned in 1 Array Buffer of Size ${multi.total_capacity})
        </div>
        <div style="display: flex; gap: 4px; overflow-x: auto; padding: 4px 0;">
          ${(multi.array || []).map((val, idx) => {
            const partitionIdx = Math.floor(idx / (multi.total_capacity / multi.num_stacks));
            const colors = ['#E4572E', '#14565F', '#F2B134'];
            return `
              <div style="border: 2px solid ${colors[partitionIdx]}; background: var(--paper-card); color: var(--ink); padding: 0.3rem 0.45rem; border-radius: 4px; font-family: var(--font-mono); font-size: 0.72rem; text-align: center;">
                <div style="color: ${colors[partitionIdx]}; font-weight: 700;">S${partitionIdx}</div>
                <div>${val}</div>
              </div>
            `;
          }).join('')}
        </div>
      </div>
    `;
  } catch (e) {
    console.error('Stack lab error:', e);
  }
}

async function fetchQueueLab(postData = null) {
  try {
    const opts = postData ? {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(postData)
    } : {};

    const res = await fetch('/api/lab/queue', opts);
    const data = await res.json();

    const box = document.getElementById('queueVizBox');
    if (!box) return;

    const cq = data.circular_queue || {};
    const dq = data.deque || {};

    box.innerHTML = `
      <div style="width: 100%; margin-bottom: 1rem;">
        <div style="font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700; color: var(--mustard); margin-bottom: 0.35rem;">
          1. CircularQueue Ring Buffer (Capacity: ${cq.capacity}, Count: ${cq.size}, Front: ${cq.front}, Rear: ${cq.rear})
        </div>
        <div style="display: flex; gap: 6px; overflow-x: auto;">
          ${(cq.raw_buffer || []).map((val, idx) => {
            const isFront = idx === cq.front && cq.size > 0;
            const isRear = idx === cq.rear && cq.size > 0;
            return `
              <div style="background: var(--paper-card); color: var(--ink); border: 2px solid ${isFront ? 'var(--terracotta)' : isRear ? 'var(--mustard)' : 'var(--ink)'}; padding: 0.4rem 0.6rem; border-radius: 6px; font-family: var(--font-mono); font-size: 0.75rem; text-align: center; min-width: 60px;">
                <div style="font-size: 0.65rem; color: var(--ink-muted);">[Idx ${idx}]</div>
                <strong>${val !== '_' ? val : '<em>empty</em>'}</strong>
                <div style="font-size: 0.65rem; font-weight: 700;">
                  ${isFront ? '<span style="color: var(--terracotta);">FRONT</span>' : ''}
                  ${isRear ? '<span style="color: var(--mustard);">REAR</span>' : ''}
                </div>
              </div>
            `;
          }).join('')}
        </div>
      </div>

      <div style="width: 100%; border-top: 1px dashed var(--soft-sand); padding-top: 0.75rem;">
        <div style="font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700; color: var(--sage); margin-bottom: 0.35rem;">
          2. Double-Ended Queue (Deque) (Count: ${dq.size} / ${dq.capacity}, Front: ${dq.front}, Rear: ${dq.rear})
        </div>
        <div style="display: flex; gap: 6px; overflow-x: auto;">
          ${(dq.raw_slots || []).map((val, idx) => `
            <div style="background: var(--paper-card); color: var(--ink); border: 1.5px solid var(--ink); padding: 0.35rem 0.55rem; border-radius: 6px; font-family: var(--font-mono); font-size: 0.75rem; text-align: center; min-width: 55px;">
              <div style="font-size: 0.65rem; color: var(--ink-muted);">[${idx}]</div>
              <div>${val !== '_' ? val : '<em>empty</em>'}</div>
            </div>
          `).join('')}
        </div>
        <div style="font-family: var(--font-mono); font-size: 0.72rem; color: var(--ink-muted); margin-top: 0.4rem;">
          Input-Restricted Deque: Insert rear only; Delete both ends. &bull; Output-Restricted Deque: Delete front only; Insert both ends.
        </div>
      </div>
    `;
  } catch (e) {}
}

async function fetchPQLab(postData = null) {
  try {
    const opts = postData ? {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(postData)
    } : {};

    const res = await fetch('/api/lab/priority-queue', opts);
    const data = await res.json();

    const box = document.getElementById('heapVizBox');
    if (!box) return;

    const heap = data.binary_heap || {};
    const arr = heap.array || [];

    box.innerHTML = `
      <div style="width: 100%;">
        <div style="font-family: var(--font-mono); font-size: 0.8rem; color: var(--mustard); font-weight: 700; margin-bottom: 0.4rem;">
          Binary Max-Heap (${heap.size} nodes, ${heap.comparisons} comparisons logged)
        </div>
        <div style="display: flex; gap: 4px; overflow-x: auto; margin-bottom: 0.75rem;">
          ${arr.map(node => `
            <div style="background: var(--deep-teal); color: #FFF; border: 1.5px solid var(--ink); padding: 0.35rem 0.55rem; border-radius: 4px; font-family: var(--font-mono); font-size: 0.75rem; text-align: center;">
              <div style="font-size: 0.65rem; color: var(--mustard);">p = ${node.priority}</div>
              <div style="font-weight: 700;">${node.item.slice ? node.item.slice(0, 10) : node.item}</div>
              <div style="font-size: 0.65rem; color: #FFF; opacity: 0.7;">idx ${node.index}</div>
            </div>
          `).join('') || '<div style="font-size: 0.8rem; color: var(--ink-muted);">Heap is empty</div>'}
        </div>
        <div style="font-family: var(--font-mono); font-size: 0.75rem; background: var(--paper-card); color: var(--ink); padding: 0.5rem; border-radius: 4px; border: 1px solid var(--ink);">
          <strong>Complexity Comparison:</strong><br>
          Binary Heap: Insert <strong>O(log N)</strong>, Extract Max <strong>O(log N)</strong>, Contiguous array<br>
          Linked List PQ: Insert <strong>O(N)</strong>, Extract Max <strong>O(1)</strong>, Pointer overhead
        </div>
      </div>
    `;
  } catch (e) {}
}

async function fetchPolyMatrixLab() {
  try {
    const res = await fetch('/api/lab/linked-list');
    const data = await res.json();

    const box = document.getElementById('polyMatrixVizBox');
    if (!box) return;

    const poly = data.polynomial || {};
    const matrix = data.sparse_matrix || {};

    box.innerHTML = `
      <div style="width: 100%; margin-bottom: 1rem;">
        <div style="font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700; color: var(--mustard); margin-bottom: 0.25rem;">
          Polynomial Linked List Arithmetic
        </div>
        <div style="font-family: var(--font-mono); font-size: 0.82rem; background: var(--paper-card); color: var(--ink); padding: 0.5rem; border-radius: 4px; border: 1px solid var(--ink);">
          <div>P1(x) = ${poly.p1 ? poly.p1.string : ''}</div>
          <div>P2(x) = ${poly.p2 ? poly.p2.string : ''}</div>
          <div style="color: var(--terracotta); font-weight: 700; margin-top: 0.2rem;">P1 + P2 = ${poly.sum ? poly.sum.string : ''} (O(N+M))</div>
          <div style="color: var(--deep-teal); font-weight: 700;">P1 &times; P2 = ${poly.product ? poly.product.string : ''} (O(N&times;M))</div>
          <div>P1 evaluated at x = 2: <strong>${poly.p1_eval_at_2}</strong></div>
        </div>
      </div>

      <div style="width: 100%; border-top: 1px dashed var(--soft-sand); padding-top: 0.75rem;">
        <div style="font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700; color: var(--sage); margin-bottom: 0.25rem;">
          Sparse User &times; Product Ratings Matrix (Triplet Linked List)
        </div>
        <div style="font-family: var(--font-mono); font-size: 0.78rem; color: var(--ink-muted); margin-bottom: 0.4rem;">
          Dimensions: ${matrix.rows} Users &times; ${matrix.cols} Products (${matrix.non_zero_count} non-zero ratings, <strong>${matrix.sparsity_pct}% Sparsity</strong>)
        </div>
        <div style="display: flex; gap: 4px; flex-wrap: wrap; max-height: 90px; overflow-y: auto;">
          ${(matrix.triplets || []).slice(0, 12).map(t => `
            <div style="background: var(--paper-card); color: var(--ink); border: 1px solid var(--ink); padding: 0.2rem 0.45rem; border-radius: 4px; font-family: var(--font-mono); font-size: 0.72rem;">
              (User ${t.row}, Prod #${t.col + 1}): ★ ${t.val}
            </div>
          `).join('')}
        </div>
      </div>
    `;
  } catch (e) {}
}

// =========================================================================
// UNIT II: TREES (AVL, BST, THREADED BST, B-TREE, B+)
// =========================================================================
async function fetchTreesLab(postData = null) {
  try {
    const opts = postData ? {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(postData)
    } : {};

    const res = await fetch('/api/lab/trees', opts);
    const data = await res.json();

    // Render AVL
    const avl = data.avl || {};
    const avlTelem = document.getElementById('avlTelemetryBar');
    if (avlTelem) {
      avlTelem.innerHTML = `
        Nodes: <strong>${avl.node_count}</strong> | Height: <strong>${avl.height}</strong> | 
        Rotations &bull; LL: <strong>${avl.rotations ? avl.rotations.LL : 0}</strong>, 
        RR: <strong>${avl.rotations ? avl.rotations.RR : 0}</strong>, 
        LR: <strong>${avl.rotations ? avl.rotations.LR : 0}</strong>, 
        RL: <strong>${avl.rotations ? avl.rotations.RL : 0}</strong> (Total: <strong>${avl.rotations ? avl.rotations.total : 0}</strong>)
      `;
    }

    const avlBox = document.getElementById('avlVizBox');
    if (avlBox) {
      avlBox.innerHTML = renderTreeVisual(avl.tree, 'AVL');
    }

    // Render BST & Threaded BST
    const bst = data.bst || {};
    const tbst = data.threaded_bst || {};
    const bstTraversals = document.getElementById('bstTraversalsBox');
    if (bstTraversals) {
      bstTraversals.innerHTML = `
        <div><strong>Inorder (Recursive &amp; Stack Iterative):</strong> ${(bst.inorder || []).slice(0, 8).join(', ')}...</div>
        <div><strong>Preorder:</strong> ${(bst.preorder || []).slice(0, 8).join(', ')}...</div>
        <div><strong>ThreadedBST (Stackless O(1) space):</strong> ${(tbst.inorder || []).slice(0, 8).join(', ')}...</div>
      `;
    }

    const bstBox = document.getElementById('bstVizBox');
    if (bstBox) {
      bstBox.innerHTML = renderTreeVisual(bst.tree, 'BST');
    }
  } catch (e) {}
}

function renderTreeVisual(node, label) {
  if (!node) return '<div style="color: var(--ink-muted); font-size: 0.8rem;">Tree is empty</div>';

  function buildHtml(curr) {
    if (!curr) return '';
    const hasChildren = curr.children && curr.children.length > 0;
    return `
      <div style="display: flex; flex-direction: column; align-items: center; margin: 4px;">
        <div style="background: var(--paper-card); color: var(--ink); border: 1.5px solid var(--ink); border-radius: 6px; padding: 0.25rem 0.5rem; font-family: var(--font-mono); font-size: 0.72rem; text-align: center; box-shadow: 2px 2px 0 var(--ink);">
          <strong>${curr.name}</strong>
          ${curr.height ? `<div style="font-size: 0.65rem; color: var(--ink-muted);">h=${curr.height}, bal=${curr.balance}</div>` : ''}
        </div>
        ${hasChildren ? `
          <div style="width: 2px; height: 10px; background: var(--ink);"></div>
          <div style="display: flex; gap: 8px; border-top: 1px solid var(--ink); padding-top: 4px;">
            ${curr.children.map(c => buildHtml(c)).join('')}
          </div>
        ` : ''}
      </div>
    `;
  }

  return `<div style="overflow-x: auto; padding: 0.5rem; width: 100%; display: flex; justify-content: center;">${buildHtml(node)}</div>`;
}

async function fetchBTreeLab() {
  try {
    const res = await fetch('/api/lab/btree');
    const data = await res.json();

    const box = document.getElementById('btreeVizBox');
    if (!box) return;

    const bt = data.b_tree || {};
    const bplus = data.b_plus_tree || {};

    box.innerHTML = `
      <div style="width: 100%; margin-bottom: 1rem;">
        <div style="font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700; color: var(--mustard); margin-bottom: 0.35rem;">
          1. B-Tree of Minimum Degree t=${bt.t} (${bt.size} entries)
        </div>
        <div style="font-family: var(--font-mono); font-size: 0.78rem; background: var(--paper-card); color: var(--ink); padding: 0.6rem; border-radius: 6px; border: 1.5px solid var(--ink);">
          Root Keys: <strong>${JSON.stringify(bt.tree ? bt.tree.keys : [])}</strong> &bull; Children Count: ${bt.tree && bt.tree.children ? bt.tree.children.length : 0}
        </div>
      </div>

      <div style="width: 100%;">
        <div style="font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700; color: var(--sage); margin-bottom: 0.35rem;">
          2. B+ Tree Linked Leaf Chain (Order ${bplus.order}, ${bplus.size} items) &bull; Range Scans in O(log N + K)
        </div>
        <div style="display: flex; gap: 8px; overflow-x: auto; align-items: center; padding: 4px 0;">
          ${(bplus.leaf_chain || []).map((leaf, idx) => `
            <div style="background: var(--deep-teal); color: #FFF; border: 1.5px solid var(--ink); border-radius: 6px; padding: 0.4rem 0.65rem; font-family: var(--font-mono); font-size: 0.75rem; text-align: center; white-space: nowrap;">
              <div style="font-size: 0.65rem; color: var(--mustard);">Leaf ${idx + 1} (${leaf.values_count} items)</div>
              <div>Keys: [${leaf.keys.slice(0, 3).join(', ')}]</div>
            </div>
            ${idx < bplus.leaf_chain.length - 1 ? '<span style="font-size: 1.1rem; color: var(--mustard); font-weight: 800;">&rarr;</span>' : ''}
          `).join('')}
        </div>
      </div>
    `;
  } catch (e) {}
}

// =========================================================================
// UNIT III: GRAPHS & NETWORKS
// =========================================================================
async function fetchGraphLab() {
  try {
    const res = await fetch('/api/lab/graph');
    const data = await res.json();

    const mstBox = document.getElementById('mstResultBox');
    const adjBox = document.getElementById('graphAdjBox');

    const net = data.delivery_network || {};
    const prim = net.prim_mst || {};
    const kruskal = net.kruskal_mst || {};
    const prodGraph = data.product_graph_sample || {};

    if (mstBox) {
      mstBox.innerHTML = `
        <div style="width: 100%;">
          <div style="font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700; color: var(--mustard); margin-bottom: 0.4rem;">
            Warehouse Delivery Network: Prim vs Kruskal Minimum Spanning Tree
          </div>
          <div style="background: var(--paper-card); color: var(--ink); border: 1.5px solid var(--ink); border-radius: 6px; padding: 0.75rem; font-family: var(--font-mono); font-size: 0.78rem; margin-bottom: 0.75rem;">
            <div>Prim's Algorithm MST Total Cost: <strong style="color: var(--terracotta);">${prim.total_cost} km</strong> (${(prim.edges || []).length} distribution links)</div>
            <div>Kruskal's Algorithm MST Total Cost: <strong style="color: var(--deep-teal);">${kruskal.total_cost} km</strong> (verified cycle-free via DisjointSet)</div>
          </div>
          <div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--ink-muted); margin-bottom: 0.35rem;">MST Distribution Route Edges:</div>
          <div style="display: flex; gap: 6px; flex-wrap: wrap;">
            ${(prim.edges || []).map(e => `
              <div style="background: var(--sand-tint); border: 1px solid var(--ink); border-radius: 4px; padding: 0.25rem 0.5rem; font-family: var(--font-mono); font-size: 0.72rem;">
                ${e.from} &harr; ${e.to} (<strong>${e.cost}km</strong>)
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }

    if (adjBox) {
      adjBox.innerHTML = `
        <div style="width: 100%;">
          <div style="font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700; color: var(--sage); margin-bottom: 0.4rem;">
            Product Relation Graph (${prodGraph.vertex_count} vertices, ${prodGraph.edge_count} edges, ${prodGraph.connected_components_count} components)
          </div>
          <div style="font-family: var(--font-mono); font-size: 0.75rem; background: var(--paper-card); color: var(--ink); border: 1.5px solid var(--ink); border-radius: 6px; padding: 0.6rem; max-height: 160px; overflow-y: auto;">
            <div style="font-weight: 700; color: var(--deep-teal); margin-bottom: 0.2rem;">Adjacency List Sample:</div>
            ${Object.entries(prodGraph.adjacency_list || {}).slice(0, 6).map(([u, nbrs]) => `
              <div>Prod #${u} &rarr; [${nbrs.map(n => `#${n.to}`).join(', ')}]</div>
            `).join('')}
          </div>
        </div>
      `;
    }
  } catch (e) {}
}

// =========================================================================
// UNIT IV: SORTING, SEARCHING, HASHING
// =========================================================================
async function fetchSortingLab() {
  try {
    const res = await fetch('/api/lab/sorting');
    const data = await res.json();

    const benchTable = document.getElementById('sortingBenchmarkTable');
    if (benchTable) {
      benchTable.innerHTML = `
        <table class="complexity-table">
          <thead>
            <tr>
              <th>Algorithm</th>
              <th>Comparisons</th>
              <th>Data Movements</th>
              <th>Execution Time</th>
              <th>Stability</th>
              <th>Theoretical Time Complexity</th>
            </tr>
          </thead>
          <tbody>
            ${(data.benchmarks || []).map(b => `
              <tr>
                <td><strong>${b.algorithm}</strong></td>
                <td><strong style="color: var(--terracotta);">${b.comparisons}</strong></td>
                <td>${b.moves}</td>
                <td><strong>${b.time_ms} ms</strong></td>
                <td><span class="dsa-pill" style="background: ${b.is_stable ? 'var(--sage)' : 'var(--sand-tint)'}; color: var(--ink);">${b.is_stable ? 'Stable' : 'Unstable'}</span></td>
                <td style="font-family: var(--font-mono);">${b.algorithm.includes('Counting') ? 'O(N + K)' : b.algorithm.includes('Shell') ? 'O(N^1.5)' : 'O(N log N)'}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      `;
    }

    const stabBox = document.getElementById('stabilityVizBox');
    if (stabBox) {
      const stab = data.stability_demo || {};
      const mItems = stab.merge_sort_stable ? stab.merge_sort_stable.items : [];
      const qItems = stab.quick_sort_unstable ? stab.quick_sort_unstable.items : [];

      stabBox.innerHTML = `
        <div style="width: 100%;">
          <div style="font-family: var(--font-mono); font-size: 0.78rem; margin-bottom: 0.4rem; color: var(--sage);">
            <strong>Merge Sort (STABLE):</strong> Preserves original price order on equal rating ties:
          </div>
          <div style="font-family: var(--font-mono); font-size: 0.72rem; background: var(--paper-card); color: var(--ink); border: 1px solid var(--ink); border-radius: 4px; padding: 0.4rem; margin-bottom: 0.6rem;">
            ${mItems.slice(0, 4).map(it => `[${it.name}: ★${it.rating}, ₹${it.price}]`).join(' &bull; ')}
          </div>

          <div style="font-family: var(--font-mono); font-size: 0.78rem; margin-bottom: 0.4rem; color: var(--terracotta);">
            <strong>Quick Sort (UNSTABLE):</strong> Scrambles price order during pivot partitioning:
          </div>
          <div style="font-family: var(--font-mono); font-size: 0.72rem; background: var(--paper-card); color: var(--ink); border: 1px solid var(--ink); border-radius: 4px; padding: 0.4rem;">
            ${qItems.slice(0, 4).map(it => `[${it.name}: ★${it.rating}, ₹${it.price}]`).join(' &bull; ')}
          </div>
        </div>
      `;
    }
  } catch (e) {}
}

async function fetchSearchingLab() {
  const targetSku = (document.getElementById('searchTargetSkuInput') || {}).value || 'KS-ELEC-012';
  try {
    const res = await fetch(`/api/lab/searching?sku=${encodeURIComponent(targetSku)}`);
    const data = await res.json();

    const box = document.getElementById('searchingVizBox');
    if (!box) return;

    const lin = data.linear_search || {};
    const bin = data.binary_search || {};

    box.innerHTML = `
      <div style="width: 100%;">
        <div style="font-family: var(--font-mono); font-size: 0.82rem; font-weight: 700; color: var(--mustard); margin-bottom: 0.4rem;">
          Searching SKU "${data.target}" across ${data.array_size} catalog records:
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; margin-bottom: 0.6rem;">
          <div style="background: var(--paper-card); border: 1.5px solid var(--ink); border-radius: 6px; padding: 0.6rem; font-family: var(--font-mono); font-size: 0.75rem;">
            <div style="font-weight: 700; color: var(--terracotta);">Linear Search (O(N))</div>
            <div>Comparisons: <strong style="font-size: 1.1rem;">${lin.comparisons}</strong></div>
            <div>Time: ${lin.time_ms} ms</div>
          </div>
          <div style="background: var(--paper-card); border: 1.5px solid var(--ink); border-radius: 6px; padding: 0.6rem; font-family: var(--font-mono); font-size: 0.75rem;">
            <div style="font-weight: 700; color: var(--sage);">Binary Search (O(log N))</div>
            <div>Comparisons: <strong style="font-size: 1.1rem;">${bin.comparisons}</strong></div>
            <div>Time: ${bin.time_ms} ms</div>
          </div>
        </div>
        <div style="font-family: var(--font-mono); font-size: 0.78rem; color: var(--deep-teal); font-weight: 700;">
          ${data.comparison_ratio}
        </div>
      </div>
    `;
  } catch (e) {}
}

async function fetchHashingLab(postData = null) {
  const hashFn = (document.getElementById('hashFnSelect') || {}).value || 'division';
  const strat = (document.getElementById('collisionStrategySelect') || {}).value || 'chaining';

  try {
    const url = `/api/lab/hashing?fn=${hashFn}&strategy=${strat}`;
    const opts = postData ? {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(postData)
    } : {};

    const res = await fetch(url, opts);
    const data = await res.json();

    const telem = document.getElementById('hashingTelemetryBar');
    if (telem) {
      telem.innerHTML = `
        Capacity: <strong>${data.capacity}</strong> | Items: <strong>${data.count}</strong> | 
        Load Factor &alpha;: <strong>${data.load_factor}</strong> | 
        Total Collisions: <strong style="color: var(--terracotta);">${data.total_collisions}</strong> | 
        Probes: <strong>${data.total_probes}</strong>
      `;
    }

    const box = document.getElementById('hashingBucketsViz');
    if (box) {
      box.innerHTML = `
        <div style="display: flex; gap: 6px; overflow-x: auto; width: 100%; padding: 4px 0;">
          ${(data.buckets || []).map(b => `
            <div style="background: var(--paper-card); color: var(--ink); border: 1.5px solid var(--ink); border-radius: 6px; padding: 0.4rem 0.55rem; font-family: var(--font-mono); font-size: 0.72rem; min-width: 75px; text-align: center;">
              <div style="font-weight: 700; color: var(--mustard);">Bucket ${b.index}</div>
              <div style="font-size: 0.65rem; color: var(--ink-muted);">${b.status}</div>
              ${(b.entries || []).map(e => `
                <div style="background: var(--sand-tint); border: 1px solid var(--ink); border-radius: 3px; padding: 2px 4px; margin-top: 3px; font-size: 0.65rem; white-space: nowrap;">
                  ${e.key.slice ? e.key.slice(0, 10) : e.key}
                </div>
              `).join('')}
            </div>
          `).join('')}
        </div>
      `;
    }
  } catch (e) {}
}

// =========================================================================
// UNIT V: TRIE & DISJOINT SET
// =========================================================================
async function fetchTrieLab() {
  const prefix = (document.getElementById('trieTestPrefix') || {}).value || 'air';
  try {
    const res = await fetch(`/api/lab/trie?prefix=${encodeURIComponent(prefix)}`);
    const data = await res.json();

    const box = document.getElementById('trieVizBox');
    if (!box) return;

    box.innerHTML = `
      <div style="width: 100%;">
        <div style="font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700; color: var(--mustard); margin-bottom: 0.4rem;">
          Trie Dictionary (${data.total_words} unique indexed search terms)
        </div>
        <div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--ink-muted); margin-bottom: 0.5rem;">
          Query Prefix: "<strong>${data.query_prefix}</strong>" &bull; Autocomplete Matches:
        </div>
        <div style="display: flex; flex-direction: column; gap: 4px; margin-bottom: 0.75rem;">
          ${(data.completions || []).map(c => `
            <div style="background: var(--paper-card); color: var(--ink); border: 1px solid var(--ink); border-radius: 4px; padding: 0.35rem 0.6rem; font-family: var(--font-mono); font-size: 0.75rem;">
              <span style="font-weight: 800; color: var(--terracotta);">${c.prefix}</span><span>${c.suffix}</span>
            </div>
          `).join('') || '<div style="font-size: 0.75rem; color: var(--ink-muted);">No completions found for this prefix.</div>'}
        </div>
      </div>
    `;
  } catch (e) {}
}

async function fetchDisjointSetLab(postData = null) {
  try {
    const opts = postData ? {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(postData)
    } : {};

    const res = await fetch('/api/lab/disjoint-set', opts);
    const data = await res.json();

    const box = document.getElementById('disjointSetVizBox');
    if (!box) return;

    box.innerHTML = `
      <div style="width: 100%;">
        <div style="font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700; color: var(--sage); margin-bottom: 0.4rem;">
          Disjoint Set Partitions (${data.num_components} variant clusters across ${data.total_elements} products)
        </div>
        <div style="display: flex; gap: 6px; flex-wrap: wrap;">
          ${(data.components || []).slice(0, 10).map(c => `
            <div style="background: var(--paper-card); color: var(--ink); border: 1.5px solid var(--ink); border-radius: 6px; padding: 0.4rem 0.6rem; font-family: var(--font-mono); font-size: 0.72rem;">
              <div style="font-weight: 700; color: var(--deep-teal);">Rep: #${c.representative}</div>
              <div>Members: [${c.members.join(', ')}]</div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  } catch (e) {}
}

// =========================================================================
// SYLLABUS TABLE
// =========================================================================
async function fetchSyllabusTable() {
  try {
    const res = await fetch('/api/lab/syllabus');
    const data = await res.json();
    const tbody = document.getElementById('syllabusTableBody');
    if (!tbody) return;

    tbody.innerHTML = (data.syllabus || []).map(row => `
      <tr>
        <td><strong>${row.unit}</strong></td>
        <td><strong>${row.topic}</strong></td>
        <td><code>${row.impl}</code></td>
        <td>${row.feature}</td>
        <td><span class="dsa-pill">${row.complexity}</span></td>
      </tr>
    `).join('');
  } catch (e) {}
}

// =========================================================================
// EVENT HANDLERS
// =========================================================================
document.addEventListener('DOMContentLoaded', () => {
  initTabNavigation();

  // Stack controls
  const sPush = document.getElementById('labStackPush');
  const sPop = document.getElementById('labStackPop');
  const sVal = document.getElementById('stackInputVal');
  if (sPush) sPush.addEventListener('click', () => fetchStackLab({ target: 'stack', op: 'push', value: sVal.value }));
  if (sPop) sPop.addEventListener('click', () => fetchStackLab({ target: 'stack', op: 'pop' }));

  const dPush = document.getElementById('labDynPush');
  const dPop = document.getElementById('labDynPop');
  if (dPush) dPush.addEventListener('click', () => fetchStackLab({ target: 'dynamic_stack', op: 'push', value: sVal.value }));
  if (dPop) dPop.addEventListener('click', () => fetchStackLab({ target: 'dynamic_stack', op: 'pop' }));

  // Queue controls
  const cqEnq = document.getElementById('labCqEnqueue');
  const cqDeq = document.getElementById('labCqDequeue');
  const qVal = document.getElementById('queueInputVal');
  if (cqEnq) cqEnq.addEventListener('click', () => fetchQueueLab({ target: 'circular_queue', op: 'enqueue', value: qVal.value }));
  if (cqDeq) cqDeq.addEventListener('click', () => fetchQueueLab({ target: 'circular_queue', op: 'dequeue' }));

  const dqFront = document.getElementById('labDqAddFront');
  const dqRear = document.getElementById('labDqAddRear');
  if (dqFront) dqFront.addEventListener('click', () => fetchQueueLab({ target: 'deque', op: 'add_front', value: qVal.value }));
  if (dqRear) dqRear.addEventListener('click', () => fetchQueueLab({ target: 'deque', op: 'add_rear', value: qVal.value }));

  // Heap controls
  const hIns = document.getElementById('labHeapInsert');
  const hExt = document.getElementById('labHeapExtract');
  const hItem = document.getElementById('heapItemVal');
  const hPri = document.getElementById('heapPriorityVal');
  if (hIns) hIns.addEventListener('click', () => fetchPQLab({ op: 'insert', item: hItem.value, priority: parseFloat(hPri.value) || 5.0 }));
  if (hExt) hExt.addEventListener('click', () => fetchPQLab({ op: 'extract' }));

  // Trees controls
  const avlIns = document.getElementById('labAvlInsert');
  const avlDel = document.getElementById('labAvlDelete');
  const avlKey = document.getElementById('avlKeyInput');
  const avlVal = document.getElementById('avlValInput');
  if (avlIns) avlIns.addEventListener('click', () => fetchTreesLab({ tree: 'avl', op: 'insert', key: parseFloat(avlKey.value), value: avlVal.value }));
  if (avlDel) avlDel.addEventListener('click', () => fetchTreesLab({ tree: 'avl', op: 'delete', key: parseFloat(avlKey.value) }));

  const bstIns = document.getElementById('labBstInsert');
  const bstDel = document.getElementById('labBstDelete');
  const bstKey = document.getElementById('bstKeyInput');
  if (bstIns) bstIns.addEventListener('click', () => fetchTreesLab({ tree: 'bst', op: 'insert', key: parseFloat(bstKey.value), value: `Item_${bstKey.value}` }));
  if (bstDel) bstDel.addEventListener('click', () => fetchTreesLab({ tree: 'bst', op: 'delete', key: parseFloat(bstKey.value) }));

  // Hashing controls
  const hashFnSel = document.getElementById('hashFnSelect');
  const hashStratSel = document.getElementById('collisionStrategySelect');
  const hashIns = document.getElementById('insertHashKeyBtn');
  const hashKey = document.getElementById('newHashKeyInput');
  if (hashFnSel) hashFnSel.addEventListener('change', () => fetchHashingLab());
  if (hashStratSel) hashStratSel.addEventListener('change', () => fetchHashingLab());
  if (hashIns) hashIns.addEventListener('click', () => fetchHashingLab({ key: hashKey.value, value: `Prod_${hashKey.value}` }));

  // Searching controls
  const searchCompBtn = document.getElementById('runSearchCompareBtn');
  if (searchCompBtn) searchCompBtn.addEventListener('click', () => fetchSearchingLab());

  // Trie controls
  const trieBtn = document.getElementById('testTrieBtn');
  if (trieBtn) trieBtn.addEventListener('click', () => fetchTrieLab());

  // Disjoint set controls
  const dsUnion = document.getElementById('dsUnionBtn');
  const dsId1 = document.getElementById('dsId1');
  const dsId2 = document.getElementById('dsId2');
  if (dsUnion) dsUnion.addEventListener('click', () => fetchDisjointSetLab({ id1: parseInt(dsId1.value), id2: parseInt(dsId2.value) }));
});
