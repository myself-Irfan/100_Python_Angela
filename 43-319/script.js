document.addEventListener("DOMContentLoaded", () => {
  function addHr() {
    const headings = document.querySelectorAll('h1, h2');
    headings.forEach(heading => {
      const hr = document.createElement('hr');
      heading.after(hr);
    });
  }
  addHr();
});
