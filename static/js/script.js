// Message flash
document.addEventListener("DOMContentLoaded", () => {
  const flashMessage = document.querySelector(".flash");

  if (flashMessage) {
    setTimeout(() => {
      flashMessage.style.display = "none";
    }, 5000);
  }
});

// =========================
// Confirmation suppressions
// =========================
function confirmDeleteAccount() {
  return confirm("Voulez-vous vraiment supprimer votre compte ?");
}

function confirmDeleteProject() {
  return confirm("Voulez-vous supprimer ce projet ?");
}

function confirmDeleteTask() {
  return confirm("Voulez-vous supprimer cette tâche ?");
}

function confirmDeleteClient() {
  return confirm("Voulez-vous supprimer ce client ?");
}
