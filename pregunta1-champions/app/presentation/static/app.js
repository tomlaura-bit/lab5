document.querySelectorAll("[data-match]").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelector("#match_id").value = button.dataset.match
    document.querySelector("#prediction-form").scrollIntoView({ behavior: "smooth" })
  })
})

