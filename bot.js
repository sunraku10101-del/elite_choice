alert("BOT LOADED");
const products = [
  {
    name: "Olay Total Effects Day Cream 20g",
    price: "₹347",
    image: "https://m.media-amazon.com/images/I/71xyzABC.jpg",
    link: "https://amzn.to/4ol78oY"
  },
  {
    name: "Cetaphil Bright Healthy Radiance Serum 30ml",
    price: "₹1609",
    image: "https://m.media-amazon.com/images/I/81abcXYZ.jpg",
    link: "https://amzn.to/YOUR_LINK"
  }
];

const grid = document.getElementById("productGrid");

products.forEach(p => {
  grid.innerHTML += `
    <div class="card">
      <img src="${p.image}" alt="${p.name}" loading="lazy">
      <h3>${p.name}</h3>
      <p class="price">${p.price}</p>
      <a class="buy" href="${p.link}" target="_blank">Buy Now</a>
    </div>
  `;
});
