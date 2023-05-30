const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto('https://en.wikipedia.org/wiki/List_of_NBA_champions');

  const data = await page.evaluate(() => {
    const table = document.querySelector('.wikitable .sortable');
    const headers = Array.from(table.querySelectorAll('th')).map(th => th.textContent.trim());
    const rows = Array.from(table.querySelectorAll('tr')).slice(1);
    const data = rows.map(row => {
      const cells = Array.from(row.querySelectorAll('td'));
      const year = cells[0].textContent.trim().split('[')[0];
      const date = cells[1].textContent.trim().split('[')[0];
      const eastWinner = cells[2].textContent.trim().split('[')[0];
      const westWinner = cells[3].textContent.trim().split('[')[0];
      return { year, date, eastWinner, westWinner };
    });
    return data;
  });

  console.log(data);

  await browser.close();
})();
