const modalInstruction = document.querySelector(".instruction-modal");
const getModalInstruction = document.querySelector(".modal-instruction");
const closeModalInstruction = document.querySelector(".close-instruction");
const modalBasket = document.querySelector(".basket-button");
const getModalBasket = document.querySelector(".modal-basket");
const closeModalBasket = document.querySelector(".close-basket");

modalInstruction.addEventListener("click", toggleModalInstruction);
closeModalInstruction.addEventListener("click", toggleModalInstruction);

modalBasket.addEventListener("click", toggleModalBasket);
closeModalBasket.addEventListener("click", toggleModalBasket);

function toggleModalInstruction() {
  getModalInstruction.classList.toggle("is-open-instruction");
}
function toggleModalBasket() {
  getModalBasket.classList.toggle("is-open-basket");
}

/*const modalInstruction = document.getElementById("instruction-link");
const getModalInstruction = document.querySelector(".modal-instruction");
const closeModalInstruction = document.querySelector(".close-instruction");
const modalBasket = document.getElementById("basket-button");
const getModalBasket = document.querySelector(".modal-basket");
const closeModalBasket = document.querySelector(".close-basket");

const setListener = (element, type, handler) => {
  if (element) {
    return;
  }
  element.addEventListener(type, handler);
};

setListener(modalBasket, "click", toggleModalBasket);
setListener(closeModalBasket, "click", toggleModalBasket);

setListener(modalInstruction, "click", toggleModalInstruction);
setListener(closeModalInstruction, "click", toggleModalInstruction);

function toggleModalInstruction() {
  getModalInstruction.classList.toggle("is-open-instruction");
}
function toggleModalBasket() {
  getModalBasket.classList.toggle("is-open-basket");
}
 */
