const products = [
    {
  "img": "https://via.placeholder.com/300x300?text=TEST+PRODUCT",
  "title": "TEST PRODUCT – JS RENDER CHECK",
  "price": "₹123",
  "link": "https://www.amazon.in/?tag=elitechoic002-21"
},

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

