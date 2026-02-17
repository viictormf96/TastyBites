
//Paginación
function changePage(pageNumber) {
  const url = new URL(window.location.href);
  url.searchParams.set("page", pageNumber);
  window.location.href = url.toString();
}


/**
 * Función genérica para actualizar parámetros en la URL.
 * Mantiene la lógica de resetear a página 1 al filtrar.
 */
const updateCategoryParam = (key, value) => {
  const url = new URL(window.location.href);

  if (value) {
    url.searchParams.set(key, value);
  } else {
    url.searchParams.delete(key);
  }

  // Si estamos filtrando o cambiando vista, volvemos a la página 1
  if (url.searchParams.has("page")) {
    url.searchParams.set("page", "1");

    if(value == "grid"){
       url.searchParams.delete("page");
    }
  }

  window.location.href = url.toString();
};

const initCategoryFilters = () => {
  const urlParams = new URLSearchParams(window.location.search);
  const ViewList = document.getElementById("view-list");
  const ViewGrid = document.getElementById("view-grid");

  if (ViewGrid) {
    ViewGrid.addEventListener("click", (e) => {
      e.preventDefault();
      updateCategoryParam("view", "grid");
      if (url.searchParams.has("page")) {
        url.searchParams.delete("page");
      }
    });
  }

  if (ViewList) {
    ViewList.addEventListener("click", (e) => {
      e.preventDefault();
      updateCategoryParam("view", "list");
    });
  }
};

// Ejecución segura del inicializador
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initCategoryFilters);
} else {
  initCategoryFilters();
}