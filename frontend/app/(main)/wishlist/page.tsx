const wishlist = [
  { name: "오버핏 스트라이프 셔츠", source: "zigzag", price: "39,000원" },
  { name: "레더 스니커즈", source: "29cm", price: "99,000원" },
];

export default function WishlistPage() {
  return (
    <section className="card">
      <p className="eyebrow">Saved Items</p>
      <h1>Wishlist</h1>
      <ul className="wishlist-list">
        {wishlist.map((item) => (
          <li key={item.name}>
            <div>
              <strong>{item.name}</strong>
              <p>{item.source}</p>
            </div>
            <div className="wishlist-right">
              <span>{item.price}</span>
              <button type="button">Remove</button>
            </div>
          </li>
        ))}
      </ul>
    </section>
  );
}
