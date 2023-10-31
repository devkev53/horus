var tblProdList;

// ------------------------ FUNCION QUE CIERRA EL MODAL DEL CLIENTE ------------------------
function closeModal(addClientModal) {
  addClientModal.classList.remove("show");
  document.querySelector("#addClientForm").reset();
}

const addClientModal = document.querySelector("#addClientModal");
const btnCloseModal = document.querySelector(".btnClose-modal");
document.querySelector("#id_date").valueAsDate = new Date();

const listClient = () => {};

// ------------------------ MANEJO DE LOS DATOS DEL CLIENTE ------------------------
let clientInput = $("#id_client_id").select2();
let clienteView = $("#id_cliente");
let nitInput = document.querySelector("#id_search_nit");
let formSearchNit = new FormData();
let responseData = {};
var clientData = {};

// ------------------------ FUNCION OBTENER CLIENTE CON AXIOS SEGUN NIT ------------------------
async function get_client_for_nit(value) {
  formSearchNit.append("action", "search_client");
  formSearchNit.append("nit", value);
  let response = await axios.post(window.location.pathname, formSearchNit);
  if (!response.data.hasOwnProperty("error")) {
    clienteView.val(response.data.get_full_name);
    clientData = response.data;
  } else {
    clienteView.val("Consumidor Final");
    clientData = {};
  }
}

// ------------------------ EVENTO DE KEY UP SOBRE EL INPUT NIT ------------------------
nitInput.addEventListener("keyup", async (e) => {
  if (e.target.value.length > 5) {
    get_client_for_nit(e.target.value);
  }
});
// ------------------------ EVENTO DE FOCUS SOBRE EL INPUT NIT ------------------------
nitInput.addEventListener("focus", (e) => {
  if (e.target.value === "C/F") {
    e.target.value = "";
  }
});
// ------------------------ EVENTO LOST FOCUS SOBRE EL INPUT NIT ------------------------
nitInput.addEventListener("focusout", (e) => {
  if (e.target.value === "") {
    e.target.value = "C/F";
    clienteView.val("Consumidor Final");
  } else if (e.target.value.length > 5) {
    if (Object.keys(clientData).length <= 0) {
      Swal.fire({
        title: "Notificacion",
        icon: "info",
        text: "Desea registrar un nuevo cliente..?",
        confirmButtonColor: "#759AA5",
        cancleButtonColor: "#52525b",
        showCancelButton: true,
        confirmButtonText: "Si, Registrar!",
        cancleButtonText: "No, Cancelar",
      }).then(async (result) => {
        if (result.isConfirmed) {
          $("#id_nit").val(e.target.value);
          addClientModal.classList.add("show");
        }
      });
    }
  } else {
    e.target.value = "C/F";
  }
});

// -*-*-*-*-*-*-*-*-*-*-*-*-*-*- CREACION DEL DICCIONARIO SALES -*-*-*-*-*-*-*-*-*-*-*-*-*-*-
var sales = {
  items: {
    date: "",
    serie: "",
    dte: "",
    authorization_date: "",
    client_id: "",
    subtotal: "",
    discount: "",
    total: "",
    products: [],
  },
  calculate: function () {
    rowSub = 0;
    let subtotal = 0;
    let discount = $("#id_discount").val();
    $.each(this.items.products, function (pos, dic) {
      subtotal += dic.quantity * parseFloat(dic.price_sale);
    });

    this.subtotal = subtotal;
    this.discount = discount;
    let total = (subtotal - discount).toFixed(2);
    this.total = (subtotal - parseFloat(discount)).toFixed(2);
    $("#id_subtotal").val(this.subtotal.toFixed(2));
    $("#id_total").val(this.total);
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
    tblProdList = $("#sale-prods-table").DataTable({
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

// ------------------------ EVENTO ONCHANGE SOBRE EL INPUT DE DESCUENTO ------------------------
$("#id_discount").on("change", function (e) {
  let discount = this.value;
  sales.calculate();
});

// ------------------------ EVENTO ONCHANGE SOBRE EL INPUT DE LA CANTIDAD ------------------------
$("#sale-prods-table tbody")
  // Elimnar un elemento de la tabla de productos
  .on("click", 'button[rel="remove"]', function () {
    let tr = tblProdList.cell($(this).closest("td, li")).index();
    alert_action(
      "Notificación",
      "Estas seguro de eliminar el producto del detalle",
      () => {
        sales.items.products.splice(tr.row, 1);
        sales.list();
      }
    );
  })
  // ------------------------ EVENTO ONCHANGE SOBRE EL INPUT DE CANTINDAD ------------------------

  // Cambiar a cantidad de articulos del producto en la tabala de productos
  .on("change", 'input[name="quantity"]', function () {
    let cant = $(this).val();
    if (parseInt(cant) <= 0) {
      $(this).val(1);
      myError("Error Cantidad", "No se permiten valores negativos");
      return;
    }
    let tr = tblProdList.cell($(this).closest("td, li")).index();
    let stock_aviable = sales.items.products[tr.row].stock;
    if (parseInt(cant) > stock_aviable) {
      $(this).val(stock_aviable);
      myError(
        "Error Cantidad",
        `Unicamente se cuentan con: ${stock_aviable} unidades del producto: ${
          sales.items.products[tr.row].name
        }`
      );
      return;
    }

    sales.items.products[tr.row].quantity = cant;
    let rowId = sales.items.products[tr.row].id;
    let rowSubtotal = (
      sales.items.products[tr.row].subtotal *
      sales.items.products[tr.row].quantity
    ).toFixed(2);
    $("td:eq(4)", tblProdList.row(tr.row).node()).html(`Q. ${rowSubtotal}`);
    sales.calculate();
  });

// ------------------------ GUARDAMOS EN VARIABLES LOS ELEMENTOS NECESARIOS
// ------------------------ PARA EL AUTCOMPLETADO DEL BUSCAR PRODUCTOS ------------------------
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
  sales.add(item);
};

// ------------------------ EVENTO KEY UP DE BUSCAR PRODUCTOS ------------------------
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

// ------------------------ FUNCION QUE REALIZA LA CONSULTA DE PRODUCTOS ------------------------
const getProds = async (terms) => {
  url = window.location.pathname;
  data = new FormData();
  data.append("action", "search_products");
  data.append("term", terms);
  let response = await axios.post(url, data);
  return response.data;
};

// ------------------------ FUNCION QUE DIBUJA AL OBJECTO DEL AUTOCOMPLETADO ------------------------
const drawItem = (item) => {
  let name = "";
  if (item.name.length >= 50) {
    name = item.name.slice(0, 50) + "...";
  } else {
    name = item.name;
  }
  return `
    <div class="item-conainer" id="${item.id}">
      <picture class="flex min-w-20 w-20 h-20" >
        <img class="object-fill min-w-20 h-20 rounded-xl" src="${item.image}" />
      </picture>
      <div class="w-full flex flex-col items-start">
        <p class="text-ellipsis overflow-hidden break-normal">${item.name}</p>
        <p class='${
          item.stock < 3
            ? "text-red-700"
            : item.stock < 6
            ? "text-orange-700"
            : "text-green-700"
        } font-bold'> - Stock: ${item.stock} - </p>
        <p><b>Q. ${item.price_sale}</b></p>
      </div>
    </div>
  `;
};

// *-*-*-*-*-*-*-*-*-*-*- Crear un Cliente con Modal *-*-*-*-*-*-*-*-*-*-*-
$("#addClientForm").on("submit", async function (e) {
  e.preventDefault();
  let params = new FormData(this);
  let clientCreated = await submit_with_axios(
    window.location.pathname,
    "Notificacion",
    "Estas seguro de crear este cliente..?",
    params,
    () => closeModal(addClientModal)
  );
  get_client_for_nit(clientCreated.nit);
});

// *-*-*-*-*-*-*-*-*-*-*- Agregar una Venta *-*-*-*-*-*-*-*-*-*-*-
$("#addSaleForm").on("submit", function (e) {
  e.preventDefault();
  if (sales.items.products.length <= 0) {
    return myAlert(
      "Notificación",
      "No se han registrado productos a la compra..!"
    );
  }
  sales.items.date = $("#id_date").val();
  sales.items.serie = $("#id_serie").val();
  sales.items.dte = $("#id_dte").val();
  sales.items.authorization_date = $("#id_authorization_date");
  sales.items.subtotal = $("#id_subtotal").val();
  sales.items.discount = $("#id_discount").val();
  sales.items.total = $("#id_total").val();
  sales.items.client_id = clientData.id;
  let params = new FormData();
  params.append("action", "add");
  params.append("sale", JSON.stringify(sales.items));
  // console.log(params);
  submit_with_axios(
    window.location.pathname,
    "Notificación",
    "¿Esta seguro de realizar la siguiente acción..?",
    params,
    () => {
      location.href = url_redirect;
    }
  );
});

sales.list();
