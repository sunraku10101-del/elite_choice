<script>
alert("BOT CONNECTED");

const products = [
  {
    title: "Cetaphil Bright Healthy Radiance Serum",
    price: "₹347",
    image: "https://images.unsplash.com/photo-1585238342028-4bbcaa6f8a8b",
    link: "#"
  },
  {
    title: "L'Oreal Paris Revitalift Cream",
    price: "₹499",
    image: "https://images.unsplash.com/photo-1594759951986-d6d80b3d47ff",
    link: "#"
  },
  {
    title: "Nivea Face Wash",
    price: "₹199",
    image: "https://images.unsplash.com/photo-1600185362472-67d73e2f4d44",
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
    <a href="${p.link}" class="buy" target="_blank">Buy Now</a>
  `;
  grid.appendChild(card);
});
</script>
