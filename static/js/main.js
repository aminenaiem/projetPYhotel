/**
 * HôtelLuxe – JavaScript principal
 */

document.addEventListener('DOMContentLoaded', () => {

  // ── Fermeture automatique des alertes après 5s ────────────────────────
  document.querySelectorAll('.alert.fade.show').forEach(alert => {
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      bsAlert?.close();
    }, 5000);
  });

  // ── Calcul dynamique du prix total dans le formulaire réservation ─────
  const checkinInput  = document.getElementById('id_date_checkin');
  const checkoutInput = document.getElementById('id_date_checkout');
  const chambreSelect = document.getElementById('id_chambre');
  const prixDisplay   = document.getElementById('prix-total-display');

  function updatePrixTotal() {
    if (!checkinInput || !checkoutInput || !chambreSelect || !prixDisplay) return;
    const checkin  = new Date(checkinInput.value);
    const checkout = new Date(checkoutInput.value);
    const option   = chambreSelect.options[chambreSelect.selectedIndex];
    const prixNuit = parseFloat(option?.dataset?.prix || 0);

    if (checkin && checkout && checkout > checkin && prixNuit > 0) {
      const nuits = Math.ceil((checkout - checkin) / (1000 * 60 * 60 * 24));
      const total = nuits * prixNuit;
      prixDisplay.innerHTML = `
        <div class="alert alert-info border-0 mt-3">
          <i class="bi bi-calculator me-2"></i>
          <strong>${nuits} nuit(s)</strong> × <strong>${prixNuit.toFixed(2)} MAD</strong>
          = <strong class="text-success fs-5">${total.toFixed(2)} MAD</strong>
        </div>`;
    } else {
      prixDisplay.innerHTML = '';
    }
  }

  if (checkinInput)  checkinInput.addEventListener('change', updatePrixTotal);
  if (checkoutInput) checkoutInput.addEventListener('change', updatePrixTotal);
  if (chambreSelect) chambreSelect.addEventListener('change', updatePrixTotal);

  // ── Confirmation de suppression ───────────────────────────────────────
  document.querySelectorAll('[data-confirm]').forEach(el => {
    el.addEventListener('click', e => {
      if (!confirm(el.dataset.confirm || 'Confirmer cette action ?')) {
        e.preventDefault();
      }
    });
  });

  // ── Tooltip Bootstrap ─────────────────────────────────────────────────
  document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
    new bootstrap.Tooltip(el, { trigger: 'hover' });
  });

  // ── Filtre date checkout (min = checkin) ──────────────────────────────
  if (checkinInput && checkoutInput) {
    checkinInput.addEventListener('change', () => {
      checkoutInput.min = checkinInput.value;
      if (checkoutInput.value && checkoutInput.value <= checkinInput.value) {
        checkoutInput.value = '';
      }
    });
    // Initialiser le min de today
    const today = new Date().toISOString().split('T')[0];
    if (checkinInput && !checkinInput.value) checkinInput.min = today;
  }

});
