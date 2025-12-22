const fashionProducts = [
  {
    img: "https://m.media-amazon.com/images/I/71g2ednj0JL._SY550_.jpg",
    title: "Men's Casual Slim Fit T-Shirt",
    price: "₹499",
    link: "https://www.amazon.in/?tag=elitechoic002-21"
  }
];

const fashionContainer = document.getElementById("fashion-list");

fashionProducts.forEach(p => {
  fashionContainer.innerHTML += `
    <div class="card">
      <img src="${p.img}" alt="${p.title}">
      <h3>${p.title}</h3>
      <div class="price">${p.price}</div>
      <a class="btn" href="${p.link}" target="_blank">Buy Now</a>
    </div>
  `;
});
