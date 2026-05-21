db = db.getSiblingDB('spider');

db.createCollection('raw_items');

db.raw_items.updateOne(
  { sku_id: 'SKU-MONGO-RAW-001' },
  {
    $setOnInsert: {
      sku_id: 'SKU-MONGO-RAW-001',
      site_id: 'JD',
      source_url: 'https://example.com/products/SKU-MONGO-RAW-001',
      raw_title: 'Demo crawler raw document 001',
      raw_price: '1299',
      scraped_at: new Date()
    }
  },
  { upsert: true }
);

db.raw_items.updateOne(
  { sku_id: 'SKU-MONGO-RAW-002' },
  {
    $setOnInsert: {
      sku_id: 'SKU-MONGO-RAW-002',
      site_id: 'JD',
      source_url: 'https://example.com/products/SKU-MONGO-RAW-002',
      raw_title: 'Demo crawler raw document 002',
      raw_price: '2399',
      scraped_at: new Date()
    }
  },
  { upsert: true }
);

db.raw_items.createIndex({ sku_id: 1 }, { unique: true });
