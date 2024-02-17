const headerTexts = [
  "languages",
  "lines",
  "blanks",
  "code",
  "files",
  "comments",
];

const escapeHTML = (unsafeText) =>
  unsafeText.replace(/[&<"']/g, (m) => {
    switch (m) {
      case "&":
        return "&amp;";
      case "<":
        return "&lt;";
      case '"':
        return "&quot;";
      default:
        return "&#039;";
    }
  });

const getLocData = async (url, branch) => {
  const endpoint = new URL(`${window.origin}`);
  endpoint.pathname += "res";
  endpoint.searchParams.append("url", decodeURIComponent(url));
  endpoint.searchParams.append("is_svg", true);
  if (branch) {
    endpoint.searchParams.append("branch", branch);
  }
  const response = await fetch(endpoint.toString(), {
    method: "GET",
    mode: "same-origin",
    cache: "no-cache",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
    },
    redirect: "follow",
    referrerPolicy: "no-referrer",
  });
  return { res: response, body: await response.json() };
};

const addThead = (tableElm, _body) => {
  const theadElm = document.createElement("thead");
  const theadTrElm = document.createElement("tr");
  headerTexts.forEach((headerText) => {
    const theadThElm = document.createElement("th");
    theadThElm.innerText = headerText;
    theadTrElm.appendChild(theadThElm);
  });
  theadElm.appendChild(theadTrElm);
  tableElm.appendChild(theadElm);
};

const addTbody = (tableElm, body) => {
  const tbodyElm = document.createElement("tbody");
  Object.keys(body.result).forEach((languageText) => {
    const total = body.result[languageText];
    const tbodyTrElm = document.createElement("tr");
    const tbodyThElm = document.createElement("th");
    tbodyThElm.innerText = languageText;
    tbodyTrElm.appendChild(tbodyThElm);

    headerTexts.slice(1).forEach((headerText) => {
      const tbodyTdElm = document.createElement("td");
      tbodyTdElm.innerText = total[headerText];
      tbodyTrElm.appendChild(tbodyTdElm);
    });
    tbodyElm.appendChild(tbodyTrElm);
  });
  tableElm.appendChild(tbodyElm);
};

const addTfoot = (tableElm, body) => {
  const tfootElm = document.createElement("tfoot");
  const tfootTrElm = document.createElement("tr");
  const tfootThElm = document.createElement("th");
  tfootThElm.innerText = "Total";
  tfootTrElm.appendChild(tfootThElm);

  headerTexts.slice(1).forEach((headerText) => {
    const tfootTdElm = document.createElement("td");
    tfootTdElm.innerText = body.total[headerText];
    tfootTrElm.appendChild(tfootTdElm);
  });
  tfootElm.appendChild(tfootTrElm);
  tableElm.appendChild(tfootElm);
};

const updateResult = () => {
  const url = encodeURIComponent(document.getElementById("url").value);
  const branch = encodeURIComponent(document.getElementById("branch").value);
  if (!url) return;

  const resultElm = document.getElementById("result");
  const errorElm = document.getElementById("error");
  const formElm = document.getElementById("form_fieldset");

  errorElm.innerText = "Loading...";
  formElm.disabled = true;

  getLocData(url, branch).then(({ res, body }) => {
    formElm.disabled = false;
    if (res.status !== 200) {
      errorElm.innerText = `${res.status} ${res.statusText}`;
      return;
    }
    errorElm.innerText = "";

    // table
    const tableElm = document.createElement("table");
    addThead(tableElm, body);
    addTbody(tableElm, body);
    addTfoot(tableElm, body);
    const tableCaptionElm = document.createElement("caption");
    const repoUrl = decodeURIComponent(url);
    tableCaptionElm.innerHTML = [
      `Repo: <a href="${repoUrl}">${repoUrl}</a>`,
      `, Branch: ${escapeHTML(branch || "(empty)")}</div>`,
    ].join("");
    tableElm.appendChild(tableCaptionElm);

    // badge
    const badgeElm = document.createElement("div");
    badgeElm.classList.add("badge");
    const badgeLinkElm = document.createElement("a");
    badgeLinkElm.href = `${window.origin}/svg?url=${url}&branch=${branch}`;
    badgeLinkElm.target = "_blank";
    badgeLinkElm.innerHTML = body.svg;
    badgeElm.appendChild(badgeLinkElm);

    // add table + badge
    if (document.getElementsByTagName("table").length > 0) {
      resultElm.prepend(document.createElement("hr"));
    }
    resultElm.prepend(badgeElm);
    resultElm.prepend(tableElm);
  });
};
