document.addEventListener("DOMContentLoaded", function () {
  let installPrompt;
  const installAppBtn = document.getElementById("installAppBtn");
  const pwaInstallBanner = document.getElementById("pwaInstallBanner");
  const closeInstallBanner = document.getElementById("closeInstallBanner");

  window.addEventListener("beforeinstallprompt", function (event) {
    event.preventDefault();
    installPrompt = event;
    if (installAppBtn) installAppBtn.hidden = false;
    if (pwaInstallBanner) pwaInstallBanner.hidden = false;
  });

  if (installAppBtn) {
    installAppBtn.addEventListener("click", async function () {
      if (!installPrompt) return;
      installPrompt.prompt();
      await installPrompt.userChoice;
      installPrompt = null;
      installAppBtn.hidden = true;
      if (pwaInstallBanner) pwaInstallBanner.hidden = true;
    });
  }

  if (closeInstallBanner) {
    closeInstallBanner.addEventListener("click", function () {
      pwaInstallBanner.hidden = true;
    });
  }

  window.addEventListener("appinstalled", function () {
    if (pwaInstallBanner) pwaInstallBanner.hidden = true;
    if (installAppBtn) installAppBtn.hidden = true;
  });

  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("/sw.js").catch(function () {});
  }

  const toggleBtn = document.getElementById("sidebarToggle");
  const sidebar = document.getElementById("sidebar");

  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener("click", function () {
      sidebar.classList.toggle("show");
    });

    document.addEventListener("click", function (e) {
      if (
        window.innerWidth < 992 &&
        sidebar.classList.contains("show") &&
        !sidebar.contains(e.target) &&
        e.target !== toggleBtn &&
        !toggleBtn.contains(e.target)
      ) {
        sidebar.classList.remove("show");
      }
    });
  }

  const verseCarousel = document.getElementById("verseCarousel");
  if (verseCarousel) {
    const slides = Array.from(verseCarousel.querySelectorAll(".verse-slide"));
    let currentIndex = Number(verseCarousel.dataset.startIndex || 0);

    setInterval(function () {
      currentIndex = (currentIndex + 1) % slides.length;
      slides.forEach(function (slide, index) {
        slide.classList.toggle("active", index === currentIndex);
      });
    }, 14000);
  }

  // Auto-dismiss alerts after 5 seconds
  document.querySelectorAll(".alert").forEach(function (alertEl) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alertEl);
      if (bsAlert) bsAlert.close();
    }, 6000);
  });
});
