/*
* groups.js
* This is just a general file for anything JS related to the groups page (excluding the Monaco editor, that gets it's own file)
*/

document.querySelectorAll('.tab-box').forEach(box => {
    const tabs = box.querySelectorAll('[role="tab"]');
    const contents = box.querySelectorAll('[role="tab-content"]');

    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => {
        tabs.forEach(t => {
          t.classList.remove('tab-active');
          t.setAttribute('aria-selected', 'false');
        });
        contents.forEach(c => c.classList.add('hidden'));

        tab.classList.add('tab-active');
        tab.setAttribute('aria-selected', 'true');
        contents[index].classList.remove('hidden');
      });
    });
});