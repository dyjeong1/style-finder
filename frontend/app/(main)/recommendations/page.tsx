const mockItems = [
  { name: "오버핏 스트라이프 셔츠", category: "TOP", price: "39,000원", score: "0.95" },
  { name: "와이드 데님 팬츠", category: "BOTTOM", price: "59,000원", score: "0.89" },
  { name: "미니 숄더백", category: "BAG", price: "45,000원", score: "0.84" },
];

export default function RecommendationPage() {
  return (
    <section className="card">
      <p className="eyebrow">Step 2</p>
      <h1>Recommendations</h1>
      <div className="filter-row">
        <select>
          <option>All Category</option>
          <option>Top</option>
          <option>Bottom</option>
          <option>Outer</option>
          <option>Shoes</option>
          <option>Bag</option>
        </select>
        <select>
          <option>Similarity Desc</option>
          <option>Price Asc</option>
          <option>Price Desc</option>
        </select>
      </div>
      <div className="card-grid">
        {mockItems.map((item) => (
          <article className="product-card" key={item.name}>
            <div className="badge">{item.category}</div>
            <h3>{item.name}</h3>
            <p>{item.price}</p>
            <small>similarity {item.score}</small>
            <button type="button">Add to Wishlist</button>
          </article>
        ))}
      </div>
    </section>
  );
}
