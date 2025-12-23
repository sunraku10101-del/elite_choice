alert("BOT CONNECTED");

const products = [
  {
    title: "Cetaphil Bright Healthy Radiance Serum",
    price: "₹347",
    image: "https://images.unsplash.com/photo-1585238342028-4bbcaa6f8a8b",
    link: "#"
  }
];

const grid = document.getElementById("productGrid");

products.forEach(p => {
  const card = document.createElement("div");
  card.className = "card";
  card.innerHTML = `
    <img src="${p.image}">
    <h3>${p.title}</h3>
    <p>${p.price}</p>
    <a href="${p.link}" class="buy">Buy Now</a>
  `;
  grid.appendChild(card);
});
