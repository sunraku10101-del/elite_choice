alert("BOT LOADED");

const products = [
  {
    title: "Olay Total Effects Day Cream",
    price: "₹347",
    image: "images/PRODUCT1.JPG",
    link: "https://amzn.to/4ol78oY"
  }
];

const grid = document.getElementById("productGrid");

products.forEach(product => {
  const card = document.createElement("div");
  card.className = "product-card";

  card.innerHTML = `
    <img src="${product.image}" alt="${product.title}">
    <div class="product-title">${product.title}</div>
    <div class="product-price">${product.price}</div>
    <a href="${product.link}" target="_blank" class="buy-btn" style="background:#ff9900;">
      Buy Now
    </a>
  `;

  grid.appendChild(card);
});
