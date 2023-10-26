var tblProdList;
var buys = {
  items: {
    date: "",
    serie: "",
    reference: "",
    provider: "",
    total: "",
    products: [],
  },
  calculate: function () {
    var subtotal = 0;
    $.each(this.items.products, function (pos, dic) {
      subtotal += dic.quantity * parseFloat(dic.price_sale);
    });
    this.total = subtotal;
    $("#id_total").val(this.total.toFixed(2));
  },
  add: function (item) {
    this.items.products.push(item);
    this.list();
  },
  list: function () {
    this.calculate();
    tblProdList = $("#buy-prods-table").DataTable({
      responsive: true,
      autoWidth: false,
      destroy: true,
      deferRender: true,
      rowCallback: function (row, data) {
        $(row).find('input[name="cantidad"]');
      },
      data: this.items.products,
      columns: [
        { data: "id" },
        { data: "name" },
        { data: "price_sale" },
        { data: "quantity" },
        { data: "subtotal" },
      ],
      columnDefs: [
        {
          targets: [0],
          class: "",
          ordenable: false,
          render: function (data, type, row) {
            return `<button rel="remove" class="btn-delete" type="button"><i class="fas fa-trash-alt"></i> </button>`;
          },
        },
        {
          targets: [1],
          class: "product",
          render: function (data, type, row) {
            return `<p class="truncate text-ellipsis">${row.name}</p>`;
          },
        },
        {
          targets: [3],
          class: "quantity",
          render: function (data, type, row) {
            return `<input onchange="${() =>
              changeQuantity(event)}" name="quantity" id="cant-${
              row.id
            }" class="bg-gray-50 border border-zinc-300 text-zinc-600" type="number" value="${
              row.quantity
            }"/>`;
          },
        },
        {
          targets: [2, 4],
          render: function (data, type, row) {
            return `Q. ${parseFloat(data).toFixed(2)}`;
          },
        },
      ],
    });
  },
};

function changeQuantity(event) {
  console.log(event);
}

// Busqueda de productos
const searchProdInput = document.querySelector("#search_prod");
const containerListProducts = document.querySelector("#my-items-list");
const dltBtn = document.querySelector("#delete_list");

dltBtn.addEventListener("click", () => {
  searchProdInput.value = "";
  containerListProducts.classList.remove("show");
  containerListProducts.innerHTML = "";
});

var listFilterProds = [];
const hadleClickItemList = function (event, item) {
  event.stopPropagation();
  listFilterProds = [];
  searchProdInput.value = "";
  containerListProducts.classList.remove("show");
  containerListProducts.innerHTML = "";
  buys.add(item);
};

searchProdInput.addEventListener("keyup", async (e, select) => {
  let terms = e.target.value;
  listFilterProds = await getProds(terms);
  if (listFilterProds.length > 0) {
    containerListProducts.classList.add("show");
    let html = "<ul>";
    listFilterProds.forEach((item) => {
      data = JSON.stringify(item);
      html += `<li><button onclick='hadleClickItemList(event, ${data})' class='flex w-full'>`;
      html += drawItem(item);
      html += `</button class="item-for-data" data="${item}"></li>`;
    });
    html += "</ul>";
    containerListProducts.innerHTML = html;
  } else {
    containerListProducts.classList.remove("show");
    containerListProducts.innerHTML = "";
  }
});

const getProds = async (terms) => {
  url = window.location.pathname;
  data = new FormData();
  data.append("action", "search_products");
  data.append("term", terms);
  let response = await axios.post(url, data);
  return response.data;
};

const drawItem = (item) => {
  let name = "";
  if (item.name.length >= 50) {
    name = item.name.slice(0, 50) + "...";
  } else {
    name = item.name;
  }
  return `
    <div class="item-conainer w-full p-2 gap-4 items-center" id="${item.id}">
      <picture class="flex w-20 h-20" ><img class="object-fit rounded-xl" src="${item.image}" /></picture>
      <span>${item.name}</span>
      <span><b>Q. ${item.price_sale}</b></span>
    </div>
  `;
};
