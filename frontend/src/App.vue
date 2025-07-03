<template>
  <div id="app">
    <div class="header">
      <span>CROMA</span>
    </div>
    
    <div class="container">
      <h1>Televisions & Accessories</h1>
      
      <div class="controls">
        <button @click="refreshProducts" :disabled="loading" class="refresh-btn">
          {{ loading ? 'Loading...' : 'Refresh Products' }}
        </button>
        <button @click="triggerScrape" :disabled="loading" class="scrape-btn">
          {{ loading ? 'Scraping...' : 'Scrape Products' }}
        </button>
        <div class="data-source" v-if="dataSource">
          Data source: <span class="source-badge" :class="dataSource">{{ getSourceLabel(dataSource) }}</span>
        </div>
      </div>

      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>{{ loadingMessage }}</p>
      </div>

      <div v-else-if="error" class="error">
        <p>{{ error }}</p>
        <button @click="triggerScrape" class="retry-btn">Scrape Data</button>
      </div>

      <div v-else-if="products.length > 0" class="product-grid">
        <Product 
          v-for="product in products" 
          :key="product.product_id" 
          :product="product" 
        />
      </div>

      <div v-else class="no-products">
        <p>No products available</p>
        <p>Click "Scrape Products" to fetch real data from Croma website</p>
        <button @click="triggerScrape" class="scrape-btn" style="margin-top: 20px;">
          Scrape Products
        </button>
      </div>
    </div>
  </div>  
</template>

<script>
import Product from './Product.vue'

export default {  
  name: 'App',
  components: {
    Product
  },
  data() {
    return {
      products: [],
      loading: true,
      error: null,
      dataSource: null,
      loadingMessage: 'Loading products...'
    }
  },
  mounted() {
    this.fetchProducts()
  },
  methods: {
    async fetchProducts() {
      this.loading = true
      this.error = null
      this.loadingMessage = 'Loading products...'
      
      try {
        const response = await fetch('http://127.0.0.1:5001/products')
        const data = await response.json()
        
        if (data.success) {
          this.products = data.data || []
          this.dataSource = data.source || 'unknown'
        } else {
          // Handle specific error messages from backend
          this.error = data.message || 'Failed to fetch products'
          this.products = []
        }
      } catch (error) {
        console.error('Error fetching products:', error)
        this.error = `Failed to connect to server: ${error.message}`
        this.products = []
      } finally {
        this.loading = false
      }
    },
    
    refreshProducts() {
      this.fetchProducts()
    },

    async triggerScrape() {
      this.loading = true
      this.loadingMessage = 'Scraping real data from Croma website...'
      this.error = null
      
      try {
        const response = await fetch('http://127.0.0.1:5001/scrape', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            url: 'https://www.croma.com/televisions-accessories/c/997'
          })
        })
        
        const result = await response.json()
        
        if (result.success) {
          // Refresh products after successful scraping
          await this.fetchProducts()
          console.log('Real scraping completed:', result)
        } else {
          console.error('Scraping failed:', result.message)
          this.error = result.message || 'Scraping failed'
          
          // Add specific handling for blocked requests
          if (response.status === 403) {
            this.error = `${result.message}\n\n${result.suggestion || ''}`
          }
        }
      } catch (error) {
        console.error('Error during scraping:', error)
        this.error = `Scraping failed: ${error.message}`
      } finally {
        this.loading = false
      }
    },

    getSourceLabel(source) {
      const labels = {
        'scraped': 'Live Scraped',
        'cached': 'Cached Data'
      }
      return labels[source] || source
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f5f5f5;
}

#app {
  min-height: 100vh;
}

.header {
  background: linear-gradient(135deg, #e31e24 0%, #b71c1c 100%);
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header span {
  color: white;
  font-size: 28px;
  font-weight: bold;
  letter-spacing: 2px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
  font-size: 2rem;
  font-weight: 300;
}

.controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  flex-wrap: wrap;
  gap: 10px;
}

.refresh-btn {
  background: #e31e24;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s ease;
}

.refresh-btn:hover:not(:disabled) {
  background: #c71e24;
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.scrape-btn {
  background: #28a745;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s ease;
}

.scrape-btn:hover:not(:disabled) {
  background: #218838;
}

.scrape-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.data-source {
  font-size: 14px;
  color: #666;
}

.source-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: 600;
  font-size: 12px;
  text-transform: uppercase;
}

.source-badge.scraped {
  background: #4caf50;
  color: white;
}

.source-badge.fallback {
  background: #ff9800;
  color: white;
}

.loading {
  text-align: center;
  padding: 60px 20px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #e31e24;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error {
  text-align: center;
  padding: 60px 20px;
  color: #e31e24;
}

.retry-btn {
  background: #e31e24;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  cursor: pointer;
  margin-top: 20px;
}

.no-products {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  padding: 20px 0;
}

@media (max-width: 768px) {
  .container {
    padding: 15px;
  }
  
  .product-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 16px;
  }
  
  .controls {
    flex-direction: column;
    align-items: stretch;
  }
}

@media (max-width: 480px) {
  .product-grid {
    grid-template-columns: 1fr;
  }
  
  .header span {
    font-size: 24px;
  }
  
  h1 {
    font-size: 1.5rem;
  }
}
</style>



