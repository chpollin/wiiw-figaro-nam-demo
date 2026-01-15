/**
 * FIGARO-NAM Explorer - Zeitreihen-Visualisierung
 * Multi-Line Chart mit Krisen-Markern
 */

let tsChart = null;
let tsTooltip = null;
let selectedCountries = ['DE'];
let selectedAggregate = 'hh_konsum';

/**
 * Laender-Checkboxen initialisieren
 */
function initCountryCheckboxes() {
    const container = document.getElementById('ts-laender');
    if (!container || !DATA.timeSeries) return;

    container.innerHTML = '';

    // Nur Laender mit Daten anzeigen
    const aggregateData = DATA.timeSeries.aggregate['hh_konsum'] || {};
    const countriesWithData = DATA.timeSeries.laender.filter(code =>
        aggregateData[code] && aggregateData[code].length > 0
    );

    countriesWithData.forEach(code => {
        const label = document.createElement('label');
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.value = code;
        checkbox.checked = code === 'DE';
        checkbox.addEventListener('change', () => {
            if (checkbox.checked) {
                if (!selectedCountries.includes(code)) {
                    selectedCountries.push(code);
                }
            } else {
                selectedCountries = selectedCountries.filter(c => c !== code);
            }
            updateTimeSeriesChart();
        });

        const name = DATA.timeSeries.laender_namen[code] || code;
        label.appendChild(checkbox);
        label.appendChild(document.createTextNode(name));
        container.appendChild(label);
    });

    // Hinweis wenn nur ein Land verfuegbar
    if (countriesWithData.length === 1) {
        const hint = document.createElement('span');
        hint.className = 'data-hint';
        hint.textContent = ' (nur DE-Daten verfuegbar)';
        hint.style.fontSize = '0.8em';
        hint.style.color = '#7f8c8d';
        container.appendChild(hint);
    }
}

/**
 * Zeitreihen-Chart initialisieren
 */
function initTimeSeriesChart() {
    if (!DATA.timeSeries) return;

    // Tooltip erstellen
    tsTooltip = createTooltip();

    // Laender-Checkboxen
    initCountryCheckboxes();

    // Aggregat-Dropdown
    const aggregatSelect = document.getElementById('ts-aggregat');
    if (aggregatSelect) {
        aggregatSelect.addEventListener('change', () => {
            selectedAggregate = aggregatSelect.value;
            updateTimeSeriesChart();
        });
    }

    // Chart zeichnen
    updateTimeSeriesChart();
}

/**
 * Zeitreihen-Chart aktualisieren
 */
function updateTimeSeriesChart() {
    if (!DATA.timeSeries) return;

    const svg = d3.select('#chart-zeitreihen');
    svg.selectAll('*').remove();

    const container = document.querySelector('#chart-zeitreihen').parentElement;
    const margin = { top: 30, right: 100, bottom: 50, left: 80 };
    const width = container.clientWidth - margin.left - margin.right;
    const height = container.clientHeight - margin.top - margin.bottom;

    // Abbrechen wenn Container nicht sichtbar
    if (width <= 0 || height <= 0) return;

    const g = svg.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Daten vorbereiten
    const jahre = DATA.timeSeries.jahre;
    const aggregateData = DATA.timeSeries.aggregate[selectedAggregate];

    if (!aggregateData) {
        g.append('text')
            .attr('x', width / 2)
            .attr('y', height / 2)
            .attr('text-anchor', 'middle')
            .text('Keine Daten verfuegbar');
        return;
    }

    // Nur Laender mit Daten und ausgewaehlte
    const validCountries = selectedCountries.filter(c => aggregateData[c] && aggregateData[c].length > 0);

    if (validCountries.length === 0) {
        g.append('text')
            .attr('x', width / 2)
            .attr('y', height / 2)
            .attr('text-anchor', 'middle')
            .text('Bitte mindestens ein Land auswaehlen');
        return;
    }

    // Skalen
    const xScale = d3.scaleLinear()
        .domain([d3.min(jahre), d3.max(jahre)])
        .range([0, width]);

    let allValues = [];
    validCountries.forEach(c => {
        if (aggregateData[c]) {
            allValues = allValues.concat(aggregateData[c]);
        }
    });

    const yScale = d3.scaleLinear()
        .domain([0, d3.max(allValues) * 1.1])
        .range([height, 0]);

    // Achsen
    const xAxis = d3.axisBottom(xScale)
        .tickFormat(d3.format('d'))
        .ticks(jahre.length);

    const yAxis = d3.axisLeft(yScale)
        .tickFormat(d => formatNumber(d, 0));

    g.append('g')
        .attr('class', 'axis x-axis')
        .attr('transform', `translate(0,${height})`)
        .call(xAxis);

    g.append('g')
        .attr('class', 'axis y-axis')
        .call(yAxis);

    // Y-Achsen-Label
    g.append('text')
        .attr('transform', 'rotate(-90)')
        .attr('y', -60)
        .attr('x', -height / 2)
        .attr('text-anchor', 'middle')
        .style('font-size', '12px')
        .style('fill', '#7f8c8d')
        .text('Mio. EUR');

    // Krisen-Marker
    if (DATA.timeSeries.krisen_marker) {
        DATA.timeSeries.krisen_marker.forEach(krise => {
            const x = xScale(krise.jahr);

            g.append('line')
                .attr('class', 'crisis-marker')
                .attr('x1', x)
                .attr('x2', x)
                .attr('y1', 0)
                .attr('y2', height);

            g.append('text')
                .attr('class', 'crisis-label')
                .attr('x', x + 5)
                .attr('y', 15)
                .text(krise.bezeichnung);
        });
    }

    // Linien zeichnen
    const line = d3.line()
        .x((d, i) => xScale(jahre[i]))
        .y(d => yScale(d))
        .curve(d3.curveMonotoneX);

    validCountries.forEach(country => {
        const values = aggregateData[country];
        if (!values || values.length === 0) return;

        g.append('path')
            .datum(values)
            .attr('class', `line line-${country}`)
            .attr('d', line)
            .style('stroke', COUNTRY_COLORS[country] || '#333');

        // Punkte fuer Interaktion
        g.selectAll(`.dot-${country}`)
            .data(values)
            .enter()
            .append('circle')
            .attr('class', `dot-${country}`)
            .attr('cx', (d, i) => xScale(jahre[i]))
            .attr('cy', d => yScale(d))
            .attr('r', 4)
            .style('fill', COUNTRY_COLORS[country] || '#333')
            .style('opacity', 0)
            .on('mouseover', function(event, d) {
                const i = values.indexOf(d);
                d3.select(this).style('opacity', 1);
                showTooltip(tsTooltip,
                    `<strong>${DATA.timeSeries.laender_namen[country]}</strong><br/>
                     ${jahre[i]}: ${formatNumber(d)} EUR`,
                    event);
            })
            .on('mouseout', function() {
                d3.select(this).style('opacity', 0);
                hideTooltip(tsTooltip);
            });
    });

    // Legende
    const legend = g.append('g')
        .attr('class', 'legend')
        .attr('transform', `translate(${width + 10}, 0)`);

    validCountries.forEach((country, i) => {
        const legendItem = legend.append('g')
            .attr('transform', `translate(0, ${i * 20})`);

        legendItem.append('line')
            .attr('x1', 0)
            .attr('x2', 20)
            .attr('y1', 0)
            .attr('y2', 0)
            .style('stroke', COUNTRY_COLORS[country] || '#333')
            .style('stroke-width', 2);

        legendItem.append('text')
            .attr('x', 25)
            .attr('y', 4)
            .style('font-size', '11px')
            .text(DATA.timeSeries.laender_namen[country] || country);
    });
}

// Fenster-Resize
window.addEventListener('resize', () => {
    if (document.getElementById('zeitreihen').classList.contains('active')) {
        updateTimeSeriesChart();
    }
});
