function changePage(pageNumber) {
  const url = new URL(window.location.href);

  url.searchParams.set("page", pageNumber);

  window.location.href = url.toString();
}

document.addEventListener("DOMContentLoaded", () => {
  const select = document.getElementById("sort-recipes");

  // 1. Detectar el cambio en el select
  select.addEventListener("change", function () {
    const value = this.value;

    // 2. Obtener la URL actual y manipular los parámetros
    const url = new URL(window.location.href);

    // Seteamos el parámetro 'sort' con el valor del select
    url.searchParams.set("sort", value);

    // 3. Redirigir a la nueva URL (Esto dispara la vista en Django)
    window.location.href = url.toString();
  });

  const ViewList = document.getElementById("view-list");
  const ViewGrid = document.getElementById("view-grid");

  const updateViewParam = (viewMode, param) => {
    const url = new URL(window.location.href);

    url.searchParams.set(param, viewMode);
    url.searchParams.delete("page");

    // Redirigir para que Django procese la nueva vista
    window.location.href = url.toString();
  };

  if (ViewGrid) {
    ViewGrid.addEventListener("click", (e) => {
      e.preventDefault();
      updateViewParam("grid", "view");
    });
  }

  if (ViewList) {
    ViewList.addEventListener("click", (e) => {
      e.preventDefault();
      updateViewParam("list", "view");
    });
  }

  // 4. Mantener la opción seleccionada después de que la página recargue
  const currentParams = new URLSearchParams(window.location.search);

  const activeSort = currentParams.get("sort");

  if (activeSort) {
    select.value = activeSort;
  }
});
