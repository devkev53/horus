const dropBtns = document.querySelectorAll(".dropdownBtn");
const dropdowns = document.querySelectorAll(".table-dropdownMenu");

dropBtns.forEach((button) => {
  button.addEventListener("click", (e) => {
    let dropdownId = e.target.getAttribute("data-dropdown-toggle");
    let dropdown = document.querySelector(`#${dropdownId}`);
    dropdowns.forEach((drop) => {
      if (drop.getAttribute("id") === dropdownId) {
        drop.classList.toggle("show");
      } else {
        drop.classList.remove("show");
      }
    });
  });
});
