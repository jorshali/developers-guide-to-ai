from sentence_transformers import SentenceTransformer

models_to_compare = ["all-MiniLM-L6-v2", "paraphrase-MiniLM-L6-v2"]

products_with_category = [
  ("Sony Wireless Noise-Cancelling Headphones", "Electronics"),
  ("Canon Professional DSLR Camera Kit", "Electronics"),
  ("Jenson Wireless Earbuds Pro", "Electronics"),
  ("Heavy Ski Jacket", "Apparel"),
  ("Lightweight Ski Jacket", "Apparel"),
  ("Down Jacket", "Apparel"),
  ("Gortex Mittens", "Apparel"),
]

products_to_categorize = [
  "Panasonic Wireless Noise-Reduction Headphones",
  "Leather Gloves"
]

sentences_to_encode = [product[0] for product in products_with_category]

for model_name in models_to_compare:
  print("Creating model: " + model_name)

  model = SentenceTransformer(model_name)

  embeddings = model.encode(sentences_to_encode)
  new_product_embeddings = model.encode(products_to_categorize)

  idx_to_compare = 0

  similarities = model.similarity(new_product_embeddings, embeddings)

  for new_product_idx, new_product_embedding in enumerate(new_product_embeddings):
    print(products_to_categorize[new_product_idx])

    for idx, embedding in enumerate(embeddings):
      print(
        f"- {products_with_category[idx][0]}, Category: {products_with_category[idx][1]}, Score: {similarities[new_product_idx][idx]:.4f}")
