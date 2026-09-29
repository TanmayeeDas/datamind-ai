const API_BASE_URL = "http://127.0.0.1:8000";


const connectButton =
    document.getElementById("connectButton");

const askButton =
    document.getElementById("askButton");

const uploadButton =
    document.getElementById("uploadButton");


const databaseSourceButton =
    document.getElementById("databaseSourceButton");

const fileSourceButton =
    document.getElementById("fileSourceButton");


const databaseSection =
    document.getElementById("databaseSection");

const fileSection =
    document.getElementById("fileSection");


const connectionStatus =
    document.getElementById("connectionStatus");

const connectionMessage =
    document.getElementById("connectionMessage");

const uploadMessage =
    document.getElementById("uploadMessage");


const resultSection =
    document.getElementById("resultSection");


const chartSection =
    document.getElementById("chartSection");

const chartType =
    document.getElementById("chartType");

const xColumn =
    document.getElementById("xColumn");

const yColumn =
    document.getElementById("yColumn");

const generateChartButton =
    document.getElementById("generateChartButton");

const chartContainer =
    document.getElementById("chartContainer");


const dashboardSection =
    document.getElementById("dashboardSection");

const revenueValue =
    document.getElementById("revenueValue");

const ordersValue =
    document.getElementById("ordersValue");

const customersValue =
    document.getElementById("customersValue");

const profitValue =
    document.getElementById("profitValue");



let currentDatabaseResult = null;
let currentChartSource = null;

let databaseConnected = false;
let fileUploaded = false;


// ------------------------------------
// Data Source Selection
// ------------------------------------

databaseSourceButton.addEventListener(
    "click",
    () => {

        databaseSourceButton.classList.add("active");
        fileSourceButton.classList.remove("active");

        databaseSection.classList.remove("hidden");
        fileSection.classList.add("hidden");

    }
);


fileSourceButton.addEventListener(
    "click",
    () => {

        fileSourceButton.classList.add("active");
        databaseSourceButton.classList.remove("active");

        fileSection.classList.remove("hidden");
        databaseSection.classList.add("hidden");

    }
);


// ------------------------------------
// Connect Database
// ------------------------------------

connectButton.addEventListener(
    "click",
    async () => {

        const host =
            document.getElementById("host").value;

        const port =
            Number(
                document.getElementById("port").value
            );

        const database =
            document.getElementById("database").value;

        const username =
            document.getElementById("username").value;

        const password =
            document.getElementById("password").value;


        connectionMessage.textContent =
            "Connecting...";


        try {

            const response = await fetch(
                `${API_BASE_URL}/database/connect`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        host,
                        port,
                        database,
                        username,
                        password
                    })
                }
            );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Connection failed."
                );

            }


            databaseConnected = true;
            fileUploaded = false;


            connectionStatus.textContent =
                "Connected";

            connectionMessage.textContent =
                "Database connected successfully.";

        }

        catch (error) {

            databaseConnected = false;

            connectionStatus.textContent =
                "Not Connected";

            connectionMessage.textContent =
                error.message;

        }

    }
);


// ------------------------------------
// Upload File
// ------------------------------------

uploadButton.addEventListener(
    "click",
    async () => {

        const fileInput =
            document.getElementById("fileInput");

        const file =
            fileInput.files[0];


        if (!file) {

            uploadMessage.textContent =
                "Please select a CSV or Excel file.";

            return;
        }


        const formData =
            new FormData();

        formData.append(
            "file",
            file
        );


        uploadMessage.textContent =
            "Uploading...";


        try {

            const response = await fetch(
                `${API_BASE_URL}/upload/file`,
                {
                    method: "POST",
                    body: formData
                }
            );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "File upload failed."
                );

            }


            fileUploaded = true;
            databaseConnected = false;


            chartSection.classList.remove("hidden");

            xColumn.innerHTML = "";
            yColumn.innerHTML = "";

            data.columns.forEach(column => {

                const xOption =
                    document.createElement("option");

                xOption.value = column;
                xOption.textContent = column;

                xColumn.appendChild(xOption);


                const yOption =
                    document.createElement("option");

                yOption.value = column;
                yOption.textContent = column;

                yColumn.appendChild(yOption);

            });


            connectionStatus.textContent =
                "File Connected";


            uploadMessage.textContent =
                `${data.filename} uploaded successfully. ` +
                `${data.rows} rows and ` +
                `${data.columns.length} columns found.`;

        }

        catch (error) {

            fileUploaded = false;

            uploadMessage.textContent =
                error.message;

        }

    }
);


// ------------------------------------
// Ask Question
// ------------------------------------

askButton.addEventListener(
    "click",
    async () => {

        const question =
            document.getElementById("question").value.trim();


        if (!question) {

            alert(
                "Please enter a question."
            );

            return;
        }


        // --------------------------------
        // CSV / Excel
        // --------------------------------

        if (fileUploaded) {

            askButton.textContent =
                "Analyzing...";


            try {

                const response = await fetch(
                    `${API_BASE_URL}/upload/ask`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type": "application/json"
                        },

                        body: JSON.stringify({
                            question
                        })
                    }
                );


                const data =
                    await response.json();


                if (!response.ok) {

                    throw new Error(
                        data.detail ||
                        "File analysis failed."
                    );

                }


                displayFileResults(data);

            }

            catch (error) {

                alert(error.message);

            }

            finally {

                askButton.textContent =
                    "Ask DataMind";

            }

            return;
        }


        // --------------------------------
        // PostgreSQL
        // --------------------------------

        if (!databaseConnected) {

            alert(
                "Please connect a database or upload a file first."
            );

            return;
        }


        const host =
            document.getElementById("host").value;

        const port =
            Number(
                document.getElementById("port").value
            );

        const database =
            document.getElementById("database").value;

        const username =
            document.getElementById("username").value;

        const password =
            document.getElementById("password").value;


        askButton.textContent =
            "Analyzing...";


        try {

            const response = await fetch(
                `${API_BASE_URL}/query/generate`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        question,
                        host,
                        port,
                        database,
                        username,
                        password
                    })
                }
            );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Query failed."
                );

            }


            displayResults(data);

        }

        catch (error) {

            alert(error.message);

        }

        finally {

            askButton.textContent =
                "Ask DataMind";

        }

    }
);


// ------------------------------------
// Display PostgreSQL Results
// ------------------------------------

function displayResults(data) {

    currentDatabaseResult = data;
    currentChartSource = "database";

    resultSection.classList.remove(
        "hidden"
    );


    document.getElementById(
        "sqlResult"
    ).textContent = data.sql;


    const tableHead =
        document.getElementById(
            "resultTableHead"
        );

    tableHead.innerHTML = "";


    const headerRow =
        document.createElement("tr");


    data.columns.forEach(
        column => {

            const th =
                document.createElement("th");

            th.textContent =
                column;

            headerRow.appendChild(th);

        }
    );


    tableHead.appendChild(
        headerRow
    );


    const tableBody =
        document.getElementById(
            "resultTableBody"
        );

    tableBody.innerHTML = "";


    data.rows.forEach(
        row => {

            const tr =
                document.createElement("tr");


            row.forEach(
                value => {

                    const td =
                        document.createElement("td");

                    td.textContent =
                        value === null
                            ? "NULL"
                            : value;

                    tr.appendChild(td);

                }
            );


            tableBody.appendChild(tr);

        }
    );

    // Show chart section for database results

    chartSection.classList.remove("hidden");

    xColumn.innerHTML = "";
    yColumn.innerHTML = "";

    data.columns.forEach(column => {

        const xOption =
            document.createElement("option");

        xOption.value = column;
        xOption.textContent = column;

        xColumn.appendChild(xOption);


        const yOption =
            document.createElement("option");

        yOption.value = column;
        yOption.textContent = column;

        yColumn.appendChild(yOption);

    });
    updateDashboard(data);

}

function renderRecommendedChart(data) {

    console.log("1. Recommended chart function called");
    console.log("2. Received data:", data);
    console.log("3. Chart recommendation:", data.chart);
    console.log("4. Plotly:", typeof Plotly);
    console.log(
        "5. Chart container:",
        document.getElementById("chartContainer")
    );

    const chart = data.chart;

    // Keep the rest of your existing code below

    if (!chart || !data.columns || !data.rows) {
        return;
    }

    // Populate dropdowns using the analysis result columns
    xColumn.innerHTML = "";
    yColumn.innerHTML = "";

    data.columns.forEach(column => {
        xColumn.add(new Option(column, column));
        yColumn.add(new Option(column, column));
    });

    chartType.value = chart.type;
    xColumn.value = chart.x;
    yColumn.value = chart.y;

    chartSection.classList.remove("hidden");

    const xIndex = data.columns.indexOf(chart.x);
    const yIndex = data.columns.indexOf(chart.y);

    if (xIndex === -1 || yIndex === -1) {
        console.error("Chart columns missing", chart);
        return;
    }

    Plotly.newPlot(
        chartContainer,
        [{
            type: chart.type,
            x: data.rows.map(row => row[xIndex]),
            y: data.rows.map(row => Number(row[yIndex])),
            marker: { opacity: 0.85 }
        }],
        {
            title: chart.title,
            xaxis: { title: chart.x },
            yaxis: { title: chart.y },
            autosize: true
        },
        { responsive: true }
    );
}

// ------------------------------------
// Display CSV / Excel Results
// ------------------------------------

function displayFileResults(data) {

    currentChartSource = "file";

    resultSection.classList.remove(
        "hidden"
    );


    const sqlResult =
        document.getElementById(
            "sqlResult"
        );


    const tableHead =
        document.getElementById(
            "resultTableHead"
        );

    const tableBody =
        document.getElementById(
            "resultTableBody"
        );


    // Text answer

    if (data.type === "text") {

        sqlResult.textContent =
            "File Analysis";

        tableHead.innerHTML = "";

        tableBody.innerHTML = "";


        const row =
            document.createElement("tr");

        const cell =
            document.createElement("td");

        cell.textContent =
            data.answer;

        row.appendChild(cell);

        tableBody.appendChild(row);

        return;
    }


    // Table answer

    if (data.type === "table") {

        sqlResult.textContent =
            "File Analysis";

        tableHead.innerHTML = "";

        tableBody.innerHTML = "";


        const headerRow =
            document.createElement("tr");


        data.columns.forEach(
            column => {

                const th =
                    document.createElement("th");

                th.textContent =
                    column;

                headerRow.appendChild(th);

            }
        );


        tableHead.appendChild(
            headerRow
        );


        data.rows.forEach(
            row => {

                const tr =
                    document.createElement("tr");


                row.forEach(
                    value => {

                        const td =
                            document.createElement("td");

                        td.textContent =
                            value === null
                                ? "NULL"
                                : value;

                        tr.appendChild(td);

                    }
                );


                tableBody.appendChild(tr);

            }
        );
        console.log("1. File result received:", data);
        console.log("2. Chart recommendation:", data.chart);

        updateDashboard(data);

        console.log("3. Calling chart renderer");
        renderRecommendedChart(data);

        console.log("4. Renderer returned");
    
    }

}

generateChartButton.addEventListener(
    "click",
    async () => {

        if (
            currentChartSource !== "database" &&
            !fileUploaded
        ) {

            alert(
                "Please connect a database or upload a file first."
            );

            return;
        }


        const selectedChartType =
            chartType.value;

        const selectedXColumn =
            xColumn.value;

        const selectedYColumn =
            yColumn.value;


        generateChartButton.textContent =
            "Generating...";


        try {

            let endpoint;
            let requestBody;


            // -----------------------------
            // Database Result
            // -----------------------------

            if (currentChartSource === "database") {

                endpoint =
                    `${API_BASE_URL}/chart/generate-result`;

                requestBody = {
                    chart_type: selectedChartType,
                    x_column: selectedXColumn,
                    y_column: selectedYColumn,
                    columns: currentDatabaseResult.columns,
                    rows: currentDatabaseResult.rows
                };

            }


            // -----------------------------
            // CSV / Excel
            // -----------------------------

            else {

                endpoint =
                    `${API_BASE_URL}/chart/generate`;

                requestBody = {
                    chart_type: selectedChartType,
                    x_column: selectedXColumn,
                    y_column: selectedYColumn
                };

            }


            const response = await fetch(
                endpoint,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify(requestBody)
                }
            );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Chart generation failed."
                );

            }


            const figure =
                JSON.parse(data.chart);


            Plotly.newPlot(
                chartContainer,
                figure.data,
                figure.layout,
                {
                    responsive: true
                }
            );

        }

        catch (error) {

            alert(error.message);

        }

        finally {

            generateChartButton.textContent =
                "Generate Chart";

        }

    }
);



function updateDashboard(data) {

    if (!data || !data.columns || !data.rows) {
        return;
    }


    dashboardSection.classList.remove(
        "hidden"
    );


    const columns =
        data.columns.map(
            column => column.toLowerCase()
        );


    const rows =
        data.rows;


    // -----------------------------
    // Revenue
    // -----------------------------

    const revenueIndex =
        columns.findIndex(
            column =>
                column.includes("revenue") ||
                column.includes("sales")
        );


    if (revenueIndex !== -1) {

        const totalRevenue =
            rows.reduce(
                (total, row) =>
                    total +
                    (Number(row[revenueIndex]) || 0),
                0
            );

        revenueValue.textContent =
            formatNumber(totalRevenue);

    }


    // -----------------------------
    // Orders
    // -----------------------------

    const orderIndex =
        columns.findIndex(
            column =>
                column.includes("order_id") ||
                column.includes("orderid") ||
                column === "order"
        );


    if (orderIndex !== -1) {

        const uniqueOrders =
            new Set(
                rows.map(
                    row => row[orderIndex]
                )
            ).size;

        ordersValue.textContent =
            formatNumber(uniqueOrders);

    } else {

        ordersValue.textContent =
            formatNumber(rows.length);

    }


    // -----------------------------
    // Customers
    // -----------------------------

    const customerIndex =
        columns.findIndex(
            column =>
                column.includes("customer_id") ||
                column.includes("customerid") ||
                column === "customer"
        );


    if (customerIndex !== -1) {

        const uniqueCustomers =
            new Set(
                rows.map(
                    row => row[customerIndex]
                )
            ).size;

        customersValue.textContent =
            formatNumber(uniqueCustomers);

    }


    // -----------------------------
    // Profit
    // -----------------------------

    const profitIndex =
        columns.findIndex(
            column =>
                column.includes("profit")
        );


    if (profitIndex !== -1) {

        const totalProfit =
            rows.reduce(
                (total, row) =>
                    total +
                    (Number(row[profitIndex]) || 0),
                0
            );

        profitValue.textContent =
            formatNumber(totalProfit);

    }

}


function formatNumber(value) {

    return new Intl.NumberFormat(
        "en-IN",
        {
            maximumFractionDigits: 2
        }
    ).format(value);

}