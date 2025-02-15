document.addEventListener("DOMContentLoaded", function () {
  const sections = document.querySelectorAll(".sections section");
  const tabs = document.querySelectorAll(".ways li");
  const uploadSection = sections[0];
  const downloadSection = sections[1];
  const sendButton = document.getElementById("send");

  // Initialize with the upload section active
  sections.forEach(section => section.classList.remove("active"));
  uploadSection.classList.add("active");

  tabs.forEach((tab, index) => {
    tab.addEventListener("click", function () {
      tabs.forEach(t => t.classList.remove("active"));
      tab.classList.add("active");

      sections.forEach(section => section.classList.remove("active"));
      sections[index].classList.add("active");
    });
  });

  sendButton.addEventListener("click", function () {
    const activeSection = document.querySelector(".sections section.active");

    if (activeSection === uploadSection) {
      alert("Upload section action triggered.");
    } else if (activeSection === downloadSection) {
      alert("Download section action triggered.");
    }
  });
});
