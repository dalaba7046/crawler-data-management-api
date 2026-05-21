<script setup>
import { computed, onMounted, ref } from 'vue'

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const items = ref([])
const rawItems = ref([])
const selectedSkuId = ref('')
const selectedItem = ref(null)
const form = ref({ SKU_ID: '', SITE_ID: 'JD' })
const loading = ref(false)
const saving = ref(false)
const errorMessage = ref('')
const notice = ref('')
const rawErrorMessage = ref('')

const activeItems = computed(() => items.value.filter((item) => item.IF_COLLECT === 'Y'))
const deletedItems = computed(() => items.value.filter((item) => item.IF_COLLECT !== 'Y'))
const rawItemCount = computed(() => rawItems.value.length)
const statusCounts = computed(() => {
  return items.value.reduce((counts, item) => {
    counts[item.COLLECT_STATUS] = (counts[item.COLLECT_STATUS] || 0) + 1
    return counts
  }, {})
})

function setMessage(message, isError = false) {
  notice.value = isError ? '' : message
  errorMessage.value = isError ? message : ''
}

async function apiRequest(path, options = {}) {
  const response = await fetch(`${apiBaseUrl}${path}`, options)
  const data = await response.json().catch(() => null)

  if (!response.ok) {
    throw new Error(data?.detail || `API request failed (${response.status})`)
  }

  return data
}

async function loadItems() {
  loading.value = true
  try {
    items.value = await apiRequest('/v1/item/items')
    if (!selectedSkuId.value && items.value.length > 0) {
      await selectItem(items.value[0].SKU_ID)
    } else if (selectedSkuId.value) {
      const existing = items.value.find((item) => item.SKU_ID === selectedSkuId.value)
      selectedItem.value = existing || null
    }
    await loadRawItems()
    setMessage('資料已更新')
  } catch (error) {
    setMessage(error.message, true)
  } finally {
    loading.value = false
  }
}

async function loadRawItems() {
  try {
    rawItems.value = await apiRequest('/v1/mongo/raw-items')
    rawErrorMessage.value = ''
  } catch (error) {
    rawItems.value = []
    rawErrorMessage.value = error.message
  }
}

async function selectItem(skuId) {
  selectedSkuId.value = skuId
  try {
    selectedItem.value = await apiRequest(`/v1/item/item/${encodeURIComponent(skuId)}`)
  } catch (error) {
    selectedItem.value = null
    setMessage(error.message, true)
  }
}

async function createItem() {
  if (!form.value.SKU_ID.trim() || !form.value.SITE_ID.trim()) {
    setMessage('SKU ID 與 Site ID 都必填', true)
    return
  }

  saving.value = true
  try {
    const payload = {
      SKU_ID: form.value.SKU_ID.trim(),
      SITE_ID: form.value.SITE_ID.trim(),
    }
    await apiRequest('/v1/item/item', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
    form.value.SKU_ID = ''
    selectedSkuId.value = payload.SKU_ID
    await loadItems()
    await selectItem(payload.SKU_ID)
    setMessage(`${payload.SKU_ID} 已新增`)
  } catch (error) {
    setMessage(error.message, true)
  } finally {
    saving.value = false
  }
}

async function deleteItem(skuId) {
  saving.value = true
  try {
    await apiRequest(`/v1/item/item/${encodeURIComponent(skuId)}`, {
      method: 'PUT',
    })
    await loadItems()
    await selectItem(skuId)
    setMessage(`${skuId} 已標記為不收集`)
  } catch (error) {
    setMessage(error.message, true)
  } finally {
    saving.value = false
  }
}

onMounted(loadItems)
</script>

<template>
  <main class="app-shell">
    <section class="topbar">
      <div>
        <p class="eyebrow">Crawler Data Management</p>
        <h1>SKU 儀表板</h1>
      </div>
      <button class="icon-button" type="button" :disabled="loading" title="重新整理" @click="loadItems">
        ↻
      </button>
    </section>

    <section class="metrics">
      <article>
        <span>全部 SKU</span>
        <strong>{{ items.length }}</strong>
      </article>
      <article>
        <span>收集中</span>
        <strong>{{ activeItems.length }}</strong>
      </article>
      <article>
        <span>已軟刪除</span>
        <strong>{{ deletedItems.length }}</strong>
      </article>
      <article>
        <span>NEW</span>
        <strong>{{ statusCounts.NEW || 0 }}</strong>
      </article>
      <article>
        <span>Mongo Raw</span>
        <strong>{{ rawItemCount }}</strong>
      </article>
    </section>

    <p v-if="errorMessage" class="message error">{{ errorMessage }}</p>
    <p v-else-if="notice" class="message">{{ notice }}</p>

    <section class="workspace">
      <div class="panel list-panel">
        <div class="panel-header">
          <h2>SKU 清單</h2>
          <span>{{ loading ? '載入中' : `${items.length} 筆` }}</span>
        </div>

        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>SKU ID</th>
                <th>站點</th>
                <th>狀態</th>
                <th>收集</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="item in items"
                :key="item.SKU_ID"
                :class="{ selected: item.SKU_ID === selectedSkuId }"
                @click="selectItem(item.SKU_ID)"
              >
                <td>{{ item.SKU_ID }}</td>
                <td>{{ item.SITE_ID }}</td>
                <td>
                  <span class="status">{{ item.COLLECT_STATUS }}</span>
                </td>
                <td>{{ item.IF_COLLECT }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <aside class="side-stack">
        <form class="panel form-panel" @submit.prevent="createItem">
          <div class="panel-header">
            <h2>新增 SKU</h2>
          </div>
          <label>
            <span>SKU ID</span>
            <input v-model="form.SKU_ID" placeholder="SKU-POSTGRES-006" />
          </label>
          <label>
            <span>Site ID</span>
            <input v-model="form.SITE_ID" placeholder="JD" />
          </label>
          <button class="primary-button" type="submit" :disabled="saving">新增</button>
        </form>

        <section class="panel detail-panel">
          <div class="panel-header">
            <h2>詳細資料</h2>
          </div>

          <div v-if="selectedItem" class="detail-grid">
            <span>SKU ID</span>
            <strong>{{ selectedItem.SKU_ID }}</strong>
            <span>Site ID</span>
            <strong>{{ selectedItem.SITE_ID }}</strong>
            <span>Collect Status</span>
            <strong>{{ selectedItem.COLLECT_STATUS }}</strong>
            <span>If Collect</span>
            <strong>{{ selectedItem.IF_COLLECT }}</strong>
          </div>

          <p v-else class="empty-state">選擇一筆 SKU 查看內容</p>

          <button
            v-if="selectedItem && selectedItem.IF_COLLECT === 'Y'"
            class="danger-button"
            type="button"
            :disabled="saving"
            @click="deleteItem(selectedItem.SKU_ID)"
          >
            標記不收集
          </button>
        </section>

        <section class="panel raw-panel">
          <div class="panel-header">
            <h2>MongoDB Raw Documents</h2>
            <span>{{ rawItems.length }} 筆</span>
          </div>

          <p v-if="rawErrorMessage" class="inline-error">{{ rawErrorMessage }}</p>

          <div v-if="rawItems.length" class="raw-list">
            <article v-for="rawItem in rawItems" :key="rawItem.id">
              <strong>{{ rawItem.sku_id }}</strong>
              <span>{{ rawItem.raw_title }}</span>
              <small>{{ rawItem.source_url }}</small>
            </article>
          </div>

          <p v-else class="empty-state">尚無 MongoDB raw data</p>
        </section>
      </aside>
    </section>
  </main>
</template>
