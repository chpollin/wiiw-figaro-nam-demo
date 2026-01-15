/**
 * FIGARO-NAM Explorer - IO-Verflechtungs-Visualisierung
 * Balkendiagramm fuer Rueckwaerts-/Vorwaertsverflechtung
 */

let linkagesTooltip = null;
let linkageMode = 'rueckwaerts';

/**
 * Verflechtungs-Chart initialisieren
 */
function initLinkagesChart() {
    if (!DATA.linkages) return;

    // Tooltip erstellen
    linkagesTooltip = createTooltip();

    // Mode-Dropdown
    const modeSelect = document.getElementById('linkage-mode');
    if (modeSelect) {
        modeSelect.addEventListener('change', () => {
            linkageMode = modeSelect.value;
            updateLinkagesChart();
        });
    }

    // Chart zeichnen
    updateLinkagesChart();
}

/**
 * Verflechtungs-Chart aktualisieren
 */
function updateLinkagesChart() {
    if (!DATA.linkages) return;

    const svg = d3.select('#chart-verflechtung');
    svg.selectAll('*').remove();

    const container = document.querySelector('#chart-verflechtung').parentElement;
    const margin = { top: 40, right: 60, bottom: 50, left: 220 };
    const width = container.clientWidth - margin.left - margin.right;
    const height = container.clientHeight - margin.top - margin.bottom;

    // Abbrechen wenn Container nicht sichtbar (Tab inaktiv)
    if (width <= 0 || height <= 0) return;

    const g = svg.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Daten je nach Modus
    let data = [];
    let title = '';
    let xLabel = '';

    if (linkageMode === 'rueckwaerts') {
        data = DATA.linkages.rueckwaerts || [];
        title = 'Rueckwaertsverflechtung: Welche Branchen kaufen am meisten Vorleistungen?';
        xLabel = 'Intermediate Inputs (Mio. EUR)';
    } else if (linkageMode === 'vorwaerts') {
        data = DATA.linkages.vorwaerts || [];
        title = 'Vorwaertsverflechtung: Welche Produkte beliefern am meisten andere Sektoren?';
        xLabel = 'Total Supply (Mio. EUR)';
    } else if (linkageMode === 'fluesse') {
        data = DATA.linkages.top_fluesse || [];
        title = 'Top Intersektorale Fluesse (Produkt -> Branche)';
        xLabel = 'Fluss (Mio. EUR)';
    }

    if (data.length === 0) {
        g.append('text')
            .attr('x', width / 2)
            .attr('y', height / 2)
            .attr('text-anchor', 'middle')
            .text('Keine Daten verfuegbar');
        return;
    }

    // Titel
    g.append('text')
        .attr('x', width / 2)
        .attr('y', -20)
        .attr('text-anchor', 'middle')
        .style('font-size', '13px')
        .style('font-weight', '600')
        .text(title);

    if (linkageMode === 'fluesse') {
        drawFlowsChart(g, data, width, height, xLabel);
    } else {
        drawLinkageBarChart(g, data, width, height, xLabel);
    }
}

/**
 * Balkendiagramm fuer Verflechtung
 */
function drawLinkageBarChart(g, data, width, height, xLabel) {
    // Skalen
    const yScale = d3.scaleBand()
        .domain(data.map(d => d.bezeichnung))
        .range([0, height])
        .padding(0.15);

    const xScale = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.wert) * 1.1])
        .range([0, width]);

    // Achsen
    g.append('g')
        .attr('class', 'axis y-axis')
        .call(d3.axisLeft(yScale))
        .selectAll('text')
        .style('font-size', '10px');

    g.append('g')
        .attr('class', 'axis x-axis')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(xScale).tickFormat(d => formatNumber(d, 0)));

    // X-Achsen-Label
    g.append('text')
        .attr('x', width / 2)
        .attr('y', height + 40)
        .attr('text-anchor', 'middle')
        .style('font-size', '11px')
        .style('fill', '#7f8c8d')
        .text(xLabel);

    // Balken
    g.selectAll('.bar')
        .data(data)
        .enter()
        .append('rect')
        .attr('class', 'bar-neutral')
        .attr('y', d => yScale(d.bezeichnung))
        .attr('x', 0)
        .attr('height', yScale.bandwidth())
        .attr('width', d => xScale(d.wert))
        .on('mouseover', function(event, d) {
            d3.select(this).style('opacity', 0.8);
            showTooltip(linkagesTooltip,
                `<strong>${d.bezeichnung}</strong><br/>
                 Code: ${d.code}<br/>
                 Wert: ${formatNumber(d.wert)} EUR`,
                event);
        })
        .on('mouseout', function() {
            d3.select(this).style('opacity', 1);
            hideTooltip(linkagesTooltip);
        });

    // Werte an Balken
    g.selectAll('.bar-label')
        .data(data)
        .enter()
        .append('text')
        .attr('class', 'bar-label')
        .attr('y', d => yScale(d.bezeichnung) + yScale.bandwidth() / 2 + 3)
        .attr('x', d => xScale(d.wert) + 5)
        .style('font-size', '9px')
        .style('fill', '#7f8c8d')
        .text(d => formatNumber(d.wert, 0));
}

/**
 * Chart fuer intersektorale Fluesse
 */
function drawFlowsChart(g, data, width, height, xLabel) {
    // Labels erstellen: "Von -> Nach"
    const labeledData = data.map(d => ({
        ...d,
        label: `${d.von_bezeichnung} -> ${d.nach_bezeichnung}`
    }));

    // Skalen
    const yScale = d3.scaleBand()
        .domain(labeledData.map(d => d.label))
        .range([0, height])
        .padding(0.15);

    const xScale = d3.scaleLinear()
        .domain([0, d3.max(labeledData, d => d.wert) * 1.1])
        .range([0, width]);

    // Achsen
    g.append('g')
        .attr('class', 'axis y-axis')
        .call(d3.axisLeft(yScale))
        .selectAll('text')
        .style('font-size', '9px');

    g.append('g')
        .attr('class', 'axis x-axis')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(xScale).tickFormat(d => formatNumber(d, 0)));

    // X-Achsen-Label
    g.append('text')
        .attr('x', width / 2)
        .attr('y', height + 40)
        .attr('text-anchor', 'middle')
        .style('font-size', '11px')
        .style('fill', '#7f8c8d')
        .text(xLabel);

    // Farb-Skala fuer Fluesse
    const colorScale = d3.scaleSequential(d3.interpolateBlues)
        .domain([0, d3.max(labeledData, d => d.wert)]);

    // Balken
    g.selectAll('.bar')
        .data(labeledData)
        .enter()
        .append('rect')
        .attr('y', d => yScale(d.label))
        .attr('x', 0)
        .attr('height', yScale.bandwidth())
        .attr('width', d => xScale(d.wert))
        .attr('fill', d => colorScale(d.wert))
        .on('mouseover', function(event, d) {
            d3.select(this).style('opacity', 0.8);
            showTooltip(linkagesTooltip,
                `<strong>Intersektoraler Fluss</strong><br/>
                 Von: ${d.von_bezeichnung} (${d.von_code})<br/>
                 Nach: ${d.nach_bezeichnung} (${d.nach_code})<br/>
                 Wert: ${formatNumber(d.wert)} EUR`,
                event);
        })
        .on('mouseout', function() {
            d3.select(this).style('opacity', 1);
            hideTooltip(linkagesTooltip);
        });

    // Werte an Balken
    g.selectAll('.bar-label')
        .data(labeledData)
        .enter()
        .append('text')
        .attr('class', 'bar-label')
        .attr('y', d => yScale(d.label) + yScale.bandwidth() / 2 + 3)
        .attr('x', d => xScale(d.wert) + 5)
        .style('font-size', '9px')
        .style('fill', '#7f8c8d')
        .text(d => formatNumber(d.wert, 1));
}

// Fenster-Resize
window.addEventListener('resize', () => {
    if (document.getElementById('verflechtung').classList.contains('active')) {
        updateLinkagesChart();
    }
});
