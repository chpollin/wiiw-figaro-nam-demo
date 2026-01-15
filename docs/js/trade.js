/**
 * FIGARO-NAM Explorer - Handelspartner-Visualisierung
 * Horizontales Balkendiagramm fuer Export/Import/Bilanz
 */

let tradeTooltip = null;
let tradeMode = 'exporte';
let tradeTopN = 15;

/**
 * Handelspartner-Chart initialisieren
 */
function initTradeChart() {
    if (!DATA.trade) return;

    // Tooltip erstellen
    tradeTooltip = createTooltip();

    // Mode-Dropdown
    const modeSelect = document.getElementById('trade-mode');
    if (modeSelect) {
        modeSelect.addEventListener('change', () => {
            tradeMode = modeSelect.value;
            updateTradeChart();
        });
    }

    // TopN-Slider
    const topnSlider = document.getElementById('trade-topn');
    const topnValue = document.getElementById('trade-topn-value');
    if (topnSlider) {
        topnSlider.addEventListener('input', () => {
            tradeTopN = parseInt(topnSlider.value);
            if (topnValue) topnValue.textContent = tradeTopN;
            updateTradeChart();
        });
    }

    // Chart zeichnen
    updateTradeChart();
}

/**
 * Handelspartner-Chart aktualisieren
 */
function updateTradeChart() {
    if (!DATA.trade) return;

    const svg = d3.select('#chart-handel');
    svg.selectAll('*').remove();

    const container = document.querySelector('#chart-handel').parentElement;
    const margin = { top: 30, right: 40, bottom: 50, left: 120 };
    const width = container.clientWidth - margin.left - margin.right;
    const height = container.clientHeight - margin.top - margin.bottom;

    // Abbrechen wenn Container nicht sichtbar (Tab inaktiv)
    if (width <= 0 || height <= 0) return;

    const g = svg.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Daten je nach Modus
    let data = [];
    let title = '';

    if (tradeMode === 'exporte') {
        data = DATA.trade.exporte.slice(0, tradeTopN);
        title = 'Exporte nach Handelspartner (Deutschland 2019)';
    } else if (tradeMode === 'importe') {
        data = DATA.trade.importe.slice(0, tradeTopN);
        title = 'Importe nach Handelspartner (Deutschland 2019)';
    } else if (tradeMode === 'bilanz') {
        data = DATA.trade.bilanz.slice(0, tradeTopN);
        title = 'Handelsbilanz nach Partner (Deutschland 2019)';
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
        .attr('y', -10)
        .attr('text-anchor', 'middle')
        .style('font-size', '14px')
        .style('font-weight', '600')
        .text(title);

    if (tradeMode === 'bilanz') {
        drawBalanceChart(g, data, width, height);
    } else {
        drawBarChart(g, data, width, height, tradeMode);
    }
}

/**
 * Einfaches Balkendiagramm (Export oder Import)
 */
function drawBarChart(g, data, width, height, mode) {
    const valueKey = 'wert';
    const barClass = mode === 'exporte' ? 'bar-export' : 'bar-import';

    // Skalen
    const yScale = d3.scaleBand()
        .domain(data.map(d => d.partner_name))
        .range([0, height])
        .padding(0.2);

    const xScale = d3.scaleLinear()
        .domain([0, d3.max(data, d => d[valueKey]) * 1.1])
        .range([0, width]);

    // Achsen
    g.append('g')
        .attr('class', 'axis y-axis')
        .call(d3.axisLeft(yScale));

    g.append('g')
        .attr('class', 'axis x-axis')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(xScale).tickFormat(d => formatNumber(d, 0)));

    // X-Achsen-Label
    g.append('text')
        .attr('x', width / 2)
        .attr('y', height + 40)
        .attr('text-anchor', 'middle')
        .style('font-size', '12px')
        .style('fill', '#7f8c8d')
        .text('Mio. EUR');

    // Balken
    g.selectAll('.bar')
        .data(data)
        .enter()
        .append('rect')
        .attr('class', barClass)
        .attr('y', d => yScale(d.partner_name))
        .attr('x', 0)
        .attr('height', yScale.bandwidth())
        .attr('width', d => xScale(d[valueKey]))
        .on('mouseover', function(event, d) {
            d3.select(this).style('opacity', 0.8);
            showTooltip(tradeTooltip,
                `<strong>${d.partner_name}</strong><br/>
                 Wert: ${formatNumber(d[valueKey])} EUR<br/>
                 Anteil: ${d.anteil.toFixed(1)}%`,
                event);
        })
        .on('mouseout', function() {
            d3.select(this).style('opacity', 1);
            hideTooltip(tradeTooltip);
        });

    // Werte an Balken
    g.selectAll('.bar-label')
        .data(data)
        .enter()
        .append('text')
        .attr('class', 'bar-label')
        .attr('y', d => yScale(d.partner_name) + yScale.bandwidth() / 2 + 4)
        .attr('x', d => xScale(d[valueKey]) + 5)
        .style('font-size', '10px')
        .style('fill', '#7f8c8d')
        .text(d => d.anteil.toFixed(1) + '%');
}

/**
 * Handelsbilanz-Chart (Export vs Import mit Saldo)
 */
function drawBalanceChart(g, data, width, height) {
    // Skalen
    const yScale = d3.scaleBand()
        .domain(data.map(d => d.partner_name))
        .range([0, height])
        .padding(0.2);

    const maxVal = d3.max(data, d => Math.max(d.exporte, d.importe));
    const xScale = d3.scaleLinear()
        .domain([0, maxVal * 1.1])
        .range([0, width / 2 - 20]);

    // Mittellinie
    const center = width / 2;

    g.append('line')
        .attr('x1', center)
        .attr('x2', center)
        .attr('y1', 0)
        .attr('y2', height)
        .style('stroke', '#bdc3c7')
        .style('stroke-width', 1);

    // Y-Achse (Partner-Namen)
    g.append('g')
        .attr('class', 'axis y-axis')
        .attr('transform', `translate(${center},0)`)
        .call(d3.axisLeft(yScale).tickSize(0))
        .selectAll('text')
        .style('text-anchor', 'middle');

    // Export-Balken (rechts)
    g.selectAll('.bar-export')
        .data(data)
        .enter()
        .append('rect')
        .attr('class', 'bar-export')
        .attr('y', d => yScale(d.partner_name))
        .attr('x', center + 5)
        .attr('height', yScale.bandwidth() / 2)
        .attr('width', d => xScale(d.exporte))
        .on('mouseover', function(event, d) {
            showTooltip(tradeTooltip,
                `<strong>${d.partner_name}</strong><br/>
                 Export: ${formatNumber(d.exporte)} EUR<br/>
                 Import: ${formatNumber(d.importe)} EUR<br/>
                 Saldo: ${formatNumber(d.saldo)} EUR`,
                event);
        })
        .on('mouseout', function() {
            hideTooltip(tradeTooltip);
        });

    // Import-Balken (links, gespiegelt)
    g.selectAll('.bar-import')
        .data(data)
        .enter()
        .append('rect')
        .attr('class', 'bar-import')
        .attr('y', d => yScale(d.partner_name) + yScale.bandwidth() / 2)
        .attr('x', d => center - 5 - xScale(d.importe))
        .attr('height', yScale.bandwidth() / 2)
        .attr('width', d => xScale(d.importe))
        .on('mouseover', function(event, d) {
            showTooltip(tradeTooltip,
                `<strong>${d.partner_name}</strong><br/>
                 Export: ${formatNumber(d.exporte)} EUR<br/>
                 Import: ${formatNumber(d.importe)} EUR<br/>
                 Saldo: ${formatNumber(d.saldo)} EUR`,
                event);
        })
        .on('mouseout', function() {
            hideTooltip(tradeTooltip);
        });

    // Legende
    const legend = g.append('g')
        .attr('transform', `translate(${width - 100}, -20)`);

    legend.append('rect')
        .attr('width', 12)
        .attr('height', 12)
        .attr('fill', '#27ae60');
    legend.append('text')
        .attr('x', 16)
        .attr('y', 10)
        .style('font-size', '11px')
        .text('Exporte');

    legend.append('rect')
        .attr('x', 70)
        .attr('width', 12)
        .attr('height', 12)
        .attr('fill', '#e74c3c');
    legend.append('text')
        .attr('x', 86)
        .attr('y', 10)
        .style('font-size', '11px')
        .text('Importe');
}

// Fenster-Resize
window.addEventListener('resize', () => {
    if (document.getElementById('handel').classList.contains('active')) {
        updateTradeChart();
    }
});
