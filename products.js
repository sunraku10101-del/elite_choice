const products = [
  {
    img: "https://m.media-amazon.com/images/I/617LQkadkXL._SY450_.jpg",
    title: "URBANMAC Liquid Matte Lipstick 12Pcs Set",
    price: "₹279",
    link: "https://www.amazon.in/dp/B0BTP1L9DD?tag=elitechoic002-21"
  }
];

const container = document.getElementById("product-list");

products.forEach(p => {
  container.innerHTML += `
    <div class="card">
      <img src="${p.img}" alt="${p.title}">
      <h3>${p.title}</h3>
      <div class="price">${p.price}</div>
      <a class="btn" href="${p.link}" target="_blank">Buy Now</a>
    </div>
  `;
});

