<script setup>
import { 
  SearchstaxWrapper, 
  SearchstaxInputWidget, 
  SearchstaxResultWidget,
  SearchstaxFacetsWidget,
  SearchstaxPaginationWidget 
} from '@searchstax-inc/searchstudio-ux-vue';

// 1. CONFIGURATION: Fill these in from your SearchStax Dashboard
const sampleConfig = {
  language: "en",
  searchURL: "https://searchcloud-19-us-east-1.searchstax.com/29847/kevindemo-7321/emselect", // Select Endpoint
  suggesterURL: "https://searchcloud-19-us-east-1.searchstax.com/29847/kevindemo-7321_suggester/emsuggest", // Suggest Endpoint
  trackApiKey: "EfuKnHZMlwlnkn5zZfq37swqvrdz6W8jf8NA7DUDLNc",
  searchAuth: "b3d6f83114a137bff6667c4f55826ccecc421077",
  authType: "token", // Usually "token" or "basic"
  router: { enabled: true } // Keeps the search query in the URL for sharing
};
</script>

<template>
  <div class="search-page-container">
    <header class="demo-header">
      <h1>2Ks Financial Demo</h1>
    </header>

    <SearchstaxWrapper v-bind="sampleConfig">
      
      <div class="main-layout">
        <aside class="facets-sidebar">
          <h3>Filters</h3>
          <SearchstaxFacetsWidget />
        </aside>

        <main class="results-area">
          <div class="search-input-section">
            <SearchstaxInputWidget placeholder="Search advisors or advice..." />
          </div>

          <SearchstaxResultWidget />
          
          <div class="pagination-footer">
            <SearchstaxPaginationWidget />
          </div>
        </main>
      </div>

    </SearchstaxWrapper>
  </div>
</template>

<style>
/* Basic styling to make it look clean for your demo */

.search-page-container { max-width: 1200px; margin: 0 auto; padding: 20px; font-family: sans-serif; }
.demo-header { text-align: center; border-bottom: 2px solid #eee; margin-bottom: 30px; }
.main-layout { display: flex; gap: 40px; }
.facets-sidebar { width: 250px; }
.results-area { flex-grow: 1; }
.search-input-section { margin-bottom: 30px; }
.pagination-footer { margin-top: 40px; display: flex; justify-content: center; }
</style>