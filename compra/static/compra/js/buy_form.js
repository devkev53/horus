var tblProdList;
document.querySelector("#id_date").valueAsDate = new Date();

// Creacion del datatbale con el dicionario
var buys = {
  items: {
    date: "",
    serie: "",
    reference: "",
    provider_id: "",
    total: "",
    products: [],
  },
  calculate: function () {
    rowSub = 0;
    var subtotal = 0;
    $.each(this.items.products, function (pos, dic) {
      subtotal += dic.quantity * parseFloat(dic.price_sale);
    });

    this.total = subtotal;
    $("#id_total").val(this.total.toFixed(2));
  },
  add: function (item) {
    // Se realiza verificacion que el listado este vacio
    if (this.items.products.length === 0) {
      this.items.products.push(item);
    } else {
      // Si no esta vacio creamos un array con los ids de los items
      listTemp = [];
      $.each(this.items.products, function (index, value) {
        // Iteramos y agreamos en el array temporal
        listTemp.push(value.id);
      });
      // Validamos si existe el id en el array temporal
      if (listTemp.includes(item.id)) {
        alert("Opps..! El elemento ya existe en el listado");
      } else {
        this.items.products.push(item);
      }
    }
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
        $(row).find('input[name="quantity"]');
      },
      data: this.items.products,
      language: changeLanguageDataTable,
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
            return `<input name="quantity" min="1" id="cant-${row.id}" class="bg-gray-50 border border-zinc-300 text-zinc-600" type="number" value="${row.quantity}"/>`;
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

$("#buy-prods-table tbody")
  // Elimnar un elemento de la tabla de productos
  .on("click", 'button[rel="remove"]', function () {
    let tr = tblProdList.cell($(this).closest("td, li")).index();
    alert_action(
      "Notificación",
      "Estas seguro de eliminar el producto del detalle",
      () => {
        buys.items.products.splice(tr.row, 1);
        buys.list();
      }
    );
  })
  // Cambiar a cantidad de articulos del producto en la tabala de productos
  .on("change", 'input[name="quantity"]', function () {
    let cant = $(this).val();
    if (parseInt(cant) <= 0) {
      $(this).val(1);
      alert("No se permiten valores negativos");
      return;
    }
    let tr = tblProdList.cell($(this).closest("td, li")).index();

    buys.items.products[tr.row].quantity = cant;
    // console.log(buys.items.products[tr.row].subtotal);
    let rowId = buys.items.products[tr.row].id;
    let rowSubtotal = (
      buys.items.products[tr.row].subtotal *
      buys.items.products[tr.row].quantity
    ).toFixed(2);
    $("td:eq(4)", tblProdList.row(tr.row).node()).html(`Q. ${rowSubtotal}`);
    buys.calculate();
  });

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

$("form").on("submit", function (e) {
  e.preventDefault();
  if (buys.items.products.length <= 0) {
    return myAlert(
      "Notificación",
      "No se han registrado productos a la compra..!"
    );
  }
  buys.items.date = $("#id_date").val();
  buys.items.serie = $("#id_serie").val();
  buys.items.reference = $("#id_reference").val();
  buys.items.provider_id = $("#id_provider_id").val();
  buys.items.total = $("#id_total").val();
  let params = new FormData();
  params.append("action", $('input[name="action"]').val());
  params.append("buys", JSON.stringify(buys.items));
  console.log(buys.items);
  console.log(params);
  submit_with_axios(
    window.location.pathname,
    "Notificación",
    "¿Esta seguro de realizar la siguiente acción?",
    params,
    () => {
      location.href = url_redirect;
    }
  );
});

buys.list();
