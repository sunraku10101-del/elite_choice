alert("BOT LOADED ✅");

const products = [
  {
    title: "Cetaphil Bright Healthy Radiance Serum",
    price: "₹1609",
    image: "https://m.media-amazon.com/images/I/61dG5+NQ9xL._SL1500_.jpg",
    link: "https://amzn.to/4ol78oY"
  },
  {
    title: "Olay Total Effects Day Cream",
    price: "₹347",
    image: "https://m.media-amazon.com/images/I/71+6JzL5KLL._SL1500_.jpg",
    link: "https://amzn.to/4ol78oY"
  }
];

const grid = document.getElementById("productGrid");

products.forEach(p => {
  const card = document.createElement("div");
  card.className = "card";
  card.innerHTML = `
    <img src="${p.image}">
    <h3>${p.title}</h3>
    <p class="price">${p.price}</p>
    <a href="${p.link}" target="_blank">
      <button>Check Price on Amazon</button>
    </a>
  `;
  grid.appendChild(card);
});
