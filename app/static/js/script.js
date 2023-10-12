// // Replace Text In Header

// const checkReplace = document.querySelector(".replace-me");

// if (checkReplace !== null) {
//   const replace = new ReplaceMe(checkReplace, {
//     animation: "animated fadeIn",
//     speed: 2000,
//     separator: ",",
//     loopCount: "infinite",
//     autorun: true,
//   });
// }

// User scroll for navbar
function userScroll() {
  const navbar = document.querySelector(".navbar");

  window.addEventListener("scroll", () => {
    if (window.scrollY > 50) {
      navbar.classList.add("bg-dark");

      navbar.classList.add("navbar-sticky");
    } else {
      navbar.classList.remove("bg-dark");

      navbar.classList.remove("navbar-sticky");
    }
  });
}

document.addEventListener("DOMContentLoaded", userScroll);

// // Video Modal
// const videoBtn = document.querySelector(".video-btn");
// const videoModal = document.querySelector("#videoModal");
// const video = document.querySelector("#video");
// let videoSrc;

// if (videoBtn !== null) {
//   videoBtn.addEventListener("click", () => {
//     videoSrc = videoBtn.getAttribute("data-bs-src");
//   });
// }

// if (videoModal !== null) {
//   videoModal.addEventListener("shown.bs.modal", () => {
//     video.setAttribute(
//       "src",
//       videoSrc + "?autoplay=1;modestbranding=1;showinfo=0"
//     );
//   });

//   videoModal.addEventListener("hide.bs.modal", () => {
//     video.setAttribute("src", videoSrc);
//   });
// }

// Tooltips
const tooltipTriggerList = document.querySelectorAll(
  '[data-bs-toggle="tooltip"]'
);
const tooltipList = [...tooltipTriggerList].map(
  (tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl)
);

// Sorting
function sortTable(n, tableId) {
  var table,
    rows,
    switching,
    i,
    x,
    y,
    shouldSwitch,
    dir,
    switchcount = 0;
  table = document.getElementById(tableId);
  switching = true;
  //Set the sorting direction to ascending:
  dir = "asc";
  /*Make a loop that will continue until
  no switching has been done:*/
  while (switching) {
    //start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /*Loop through all table rows (except the
    first, which contains table headers):*/
    for (i = 1; i < rows.length - 1; i++) {
      //start by saying there should be no switching:
      shouldSwitch = false;
      /*Get the two elements you want to compare,
      one from current row and one from the next:*/
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];
      /*check if the two rows should switch place,
      based on the direction, asc or desc:*/
      if (dir == "asc") {
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          //if so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      } else if (dir == "desc") {
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          //if so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      /*If a switch has been marked, make the switch
      and mark that a switch has been done:*/
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      //Each time a switch is done, increase this count by 1:
      switchcount++;
    } else {
      /*If no switching has been done AND the direction is "asc",
      set the direction to "desc" and run the while loop again.*/
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}

// search teammates
document
  .querySelector("#search-teammates")
  .addEventListener("input", filterList);

function filterList() {
  const searchInput = document.querySelector("#search-teammates");
  const filter = searchInput.value.toLowerCase();
  const listItems = document.querySelectorAll(".group-item");

  listItems.forEach((item) => {
    let text = item.textContent;
    if (text.toLowerCase().includes(filter.toLowerCase())) {
      item.classList.remove("d-none");
    } else {
      item.classList.add("d-none");
    }
  });
}
