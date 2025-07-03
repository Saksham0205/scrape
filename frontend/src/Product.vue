<template>
  <div class="product-card">
    <div class="product-image" v-if="product.image_url">
      <img :src="product.image_url" :alt="product.title" />
    </div>
    <div class="product-image placeholder" v-else>
      <div class="placeholder-icon">📺</div>
    </div>
    
    <div class="product-info">
      <h3 class="product-title">{{ product.title }}</h3>
      
      <div class="price-section">
        <div class="current-price">{{ product.sale_price || product.price }}</div>
        <div class="original-price" v-if="product.price && product.sale_price && product.price !== product.sale_price">
          {{ product.price }}
        </div>
      </div>
      
      <div class="discount-badge" v-if="product.discount_message">
        {{ product.discount_message }}
      </div>
      
      <button class="add-to-cart-btn">Add to Cart</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Product',
  props: {
    product: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
.product-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.product-image {
  height: 200px;
  overflow: hidden;
  background: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.placeholder {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.placeholder-icon {
  font-size: 3rem;
  opacity: 0.7;
}

.product-info {
  padding: 16px;
}

.product-title {
  font-size: 14px;
  font-weight: 600;
  margin: 0 0 12px 0;
  color: #333;
  line-height: 1.4;
  height: 40px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.price-section {
  margin-bottom: 8px;
}

.current-price {
  font-size: 18px;
  font-weight: 700;
  color: #e31e24;
  margin-bottom: 4px;
}

.original-price {
  font-size: 14px;
  color: #999;
  text-decoration: line-through;
}

.discount-badge {
  background: #ff6b35;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 12px;
  display: inline-block;
}

.add-to-cart-btn {
  width: 100%;
  background: #e31e24;
  color: white;
  border: none;
  padding: 12px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.add-to-cart-btn:hover {
  background: #c71e24;
}
</style> 