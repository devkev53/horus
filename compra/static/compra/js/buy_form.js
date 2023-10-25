var buys = {
  items: {
    date: "",
    serie: "",
    reference: "",
    provider: "",
    total: "",
    products: [],
  },
  add: () => {},
};

// Busqueda de productos
const searchProdInput = document.querySelector("#search_prod");
const containerListProducts = document.querySelector("#my-items-list");

// searchProdInput.addEventListener("keyup", async (e, select) => {
//   let terms = e.target.value;
//   let list_products = await getProds(terms);
//   if (list_products.length > 0) {
//     // containerListProducts.classList.add("show");
//     // let html = "<ul>";
//     // list_products.forEach((item) => {
//     //   html += "<li><button class='flex w-full'>";
//     //   html += drawItem(item);
//     //   html += `</button class="item-for-data" data="${item}"></li>`;
//     // });
//     // html += "</ul>";
//     // containerListProducts.innerHTML = html;
//   } else {
//     containerListProducts.classList.remove("show");
//     containerListProducts.innerHTML = "";
//   }
//   console.log(terms);
//   console.log(list_products);
// });

const getProds = async (terms) => {
  url = window.location.pathname;
  data = new FormData();
  data.append("action", "search_products");
  data.append("term", terms);
  let response = await axios.post(url, data);
  return response.data;
};

class myAutoComplete {
  constructor(filterData, terms) {
    this.terms = terms;
    this.filterData = filterData;
  }
  autocomplete({ source, minLengt = 0, select }) {
    let searchInput = document.querySelector("#my-Custom-Autocomplete");
    searchInput.addEventListener("keyup", (e) => {
      this.terms = e.target.value;
      if (terms.length >= minLengt) {
        this.filterData = source.filter((items) =>
          JSON.stringify(items).includes(terms)
        );
        this.draw();
      }
    });
  }
  draw() {
    console.log(this.filterData);
    let html = "<ul>";
    this.filterData.forEach((item) => {
      html += "<li><button class='flex w-full'>";
      html += drawItem(item);
      html += `</button class="item-for-data" data="${item}"></li>`;
    });
    html += "</ul>";
    containerListProducts.innerHTML = html;
  }
}
var availableTags = [
  "ActionScript",
  "AppleScript",
  "Asp",
  "BASIC",
  "C",
  "C++",
  "Clojure",
  "COBOL",
  "ColdFusion",
  "Erlang",
  "Fortran",
  "Groovy",
  "Haskell",
  "Java",
  "JavaScript",
  "Lisp",
  "Perl",
  "PHP",
  "Python",
  "Ruby",
  "Scala",
  "Scheme",
];
const productsAutocomplete = new myAutoComplete();
productsAutocomplete.autocomplete({
  source: getProds(this.terms),
  minLengt: 2,
});

const drawItem = (item) => {
  // let name = "";
  // if (item.name.length >= 50) {
  //   name = item.name.slice(0, 50) + "...";
  // } else {
  //   name = item.name;
  // }
  return `
    <div class="item-conainer flex w-full p-2 gap-4 items-center" id="${item.id}">
      <picture class="flex w-16 h-16" ><img class="object-fit rounded-xl" src="${item.image}" /></picture>
      <span>${item.name}</span>
      <span>Q. ${item.price_sale}</span>
    </div>
  `;
};
